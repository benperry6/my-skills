# my-personal-second-opinion

Obtenir un second avis independant de deux autres moteurs IA, tout en gardant le skill a jour quand les CLIs evoluent.

## Ce que ce skill fait maintenant

Ce skill n'est plus un simple routeur "appelle les deux autres outils". Il est maintenant **self-healing**:

- si un appel a un moteur externe casse, ce n'est plus un bug silencieux
- l'agent orchestrateur doit d'abord reparer ce chemin d'appel
- il doit verifier le correctif en comportement reel
- il ne doit enregistrer le learning que si le chemin repare fonctionne vraiment
- puis il reprend automatiquement la mission initiale sans demander a l'utilisateur de relancer le travail

## Point d'entree canonique

Le point d'entree a utiliser est maintenant:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --current-engine codex \
  --working-directory "$PWD" \
  --prompt-file /tmp/second-opinion-prompt.txt \
  --output-json /tmp/second-opinion-result.json
```

Pour un audit post-implementation d'une vraie session Claude Code:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --mode post-implementation-audit \
  --current-engine codex \
  --working-directory "$PWD" \
  --session-cwd "$PWD" \
  --audit-path src/app/[locale]/cookies/page.tsx \
  --audit-report-dir .claude/audits \
  --output-json /tmp/second-opinion-post-impl.json
```

Le runner:

- appelle uniquement les autres moteurs par defaut
- applique les retries et fallbacks verifies localement
- capture les logs complets de chaque tentative
- ajoute un learning runtime uniquement apres succes reel
- signale explicitement quand la reparation locale est epuisee et qu'une recherche web orchestrateur est necessaire
- sait aussi auditer une implementation terminee contre une vraie session Claude + le code courant

Pour ce mode post-implementation:

- `--session-cwd` retrouve automatiquement la bonne session Claude locale
- `--session-file` permet de figer explicitement la session source
- `--audit-path` borne l'audit aux fichiers vraiment concernes, ce qui est important dans un repo sale
- `--audit-report-dir` ecrit un artefact durable (`.json` + `.md`) pour transmettre l'audit a une phase de correction ou a une session suivante
- le helper ignore les sessions d'audit generees par ce skill lui-meme et les transcripts sous `subagents/`, pour eviter les boucles
- l'audit utilise maintenant une grille explicite: `Plan coverage`, `Scope drift`, `Correctness risk`, `Runtime confidence`, `Test adequacy`

## Doctrine

Les principes sont les suivants:

1. **Pas de degradation silencieuse**  
   Si le skill a ete invoque, c'est qu'on a besoin de ce second avis. On ne fait pas semblant que "un seul moteur suffit" juste parce qu'un autre a casse.

2. **Repair first**  
   Si un appel casse, l'orchestrateur traite ce probleme en priorite avant de revenir a la tache metier initiale.

3. **Local evidence first**  
   On commence par verifier la realite locale:
   - `--help`
   - version CLI
   - config locale
   - docs package installees
   - comportement reel des commandes

4. **Recherche web si necessaire**  
   Si la surface CLI a change ou si les infos locales ne suffisent pas, on fait de la recherche externe sur les sources officielles / upstream credibles.

5. **Verified learning only**  
   On n'ajoute rien au skill tant qu'on n'a pas un chemin repare qui marche vraiment chez nous.

6. **Resume automatique**  
   Une fois le skill repare, l'orchestrateur relance la phase second-opinion si necessaire puis reprend tout seul la tache initiale.

## Memoire verifiee

Le fichier:

- `references/verified-learning.md`
- `references/runtime-learning.md`

sont la base de connaissance reutilisable du skill.

Repartition:

- `verified-learning.md` = base durable et curatee
- `runtime-learning.md` = incidents reels auto-enregistres par le runner

On y stocke seulement:

- les commandes verifiees
- les signatures d'erreur observees
- les fallbacks qui ont vraiment marche
- les instructions devenues obsolete puis remplacees

## Learnings verifies a ce jour

### Codex

Verifie en comportement reel:

- `codex exec` fonctionne bien en headless
- `--output-last-message` est le signal de succes le plus propre
- `--skip-git-repo-check` est utile quand le cwd n'est pas le vrai git root
- des warnings de startup (`state db`, MCP, etc.) peuvent apparaitre sans invalider l'appel si la vraie reponse a bien ete produite

### Claude

Verifie en comportement reel:

- `claude -p` fonctionne
- `--output-format json` donne une sortie structuree propre

### Gemini

Cas reel observe et requalifie:

- le CLI local est configure en `oauth-personal`, pas en `GEMINI_API_KEY`
- le CLI Gemini a ete mis a jour et reverifie de `0.33.0` vers `0.35.3`
- `gemini -m pro -p ... --output-format json` est bien la bonne premiere tentative sous abonnement
- un smoke test reel via le runner a maintenant reussi avec `gemini-3.1-pro-preview` comme modele principal et `response = "OK"`
- ce succes a quand meme montre des erreurs internes transitoires cote API (`totalRequests = 4`, `totalErrors = 3`), donc il faut conserver des retries bornes / backoff
- `gemini -m auto -p ... --output-format json` a reussi apres cette mise a jour et reste sur le routing d'abonnement
- un run reel reussi de `-m auto` a montre:
  - `utility_router = gemini-2.5-flash-lite`
  - `main = gemini-3-flash-preview`
- `gemini -m gemini-3-pro-preview -p ... --output-format json` n'est pas un bypass verifie ici: il retombe lui aussi sur la capacite `gemini-3.1-pro-preview`
- `gemini -m gemini-3-flash-preview -p ... --output-format json` reste reverifie comme fallback fixe fonctionnel
- `gemini -m gemini-3.1-pro-preview -p ... --output-format json` a echoue ici en `429 MODEL_CAPACITY_EXHAUSTED`
- `gemini -m gemini-3.1-flash-lite-preview -p ... --output-format json` a echoue ici en `404 ModelNotFoundError`
- le chemin implicite sans modele explicite n'est pas assez deterministe pour ce skill: il peut rerouter via un utility router interne et produire du bruit de tools

Donc, dans l'etat actuel verifie, le skill doit:

- tenter `gemini -m pro` d'abord, avec retries bornes et backoff
- si `pro` ne sort toujours pas de resultat exploitable, retomber sur `gemini -m auto` avant de figer un modele plus ancien
- garder `gemini-3-flash-preview`, puis `gemini-2.5-flash`, puis `gemini-2.5-pro` comme fallbacks fixes d'urgence
- conserver le mode headless comme voie canonique pour l'automatisation du skill
- n'utiliser l'interactif (`/model`, `/auth`) qu'en diagnostic, pas comme strategie normale d'execution
- ne promouvoir `gemini-3.1-*` en chemin canonique qu'apres succes reel dans l'environnement courant

## Pourquoi c'est important

Ce skill sert justement dans les moments ou on a besoin d'un regard externe supplementaire: plan important, architecture, debug complexe, revue securite, decision a enjeu.

Il sert maintenant aussi **apres implementation** quand on veut verifier:

- si ce qui a ete code couvre vraiment ce qui etait prevu
- s'il manque des morceaux
- s'il y a des divergences non assumees
- quels tests reels restent necessaires avant de conclure

Le helper `scripts/claude_session_bundle.py` sert a retrouver la bonne session Claude, suivre la chaine de transcripts compactes, et remonter les plans references pour nourrir cet audit post-implementation.

Si ce skill casse au moment ou on en a besoin, ce n'est pas un detail. C'est une panne d'infrastructure de raisonnement. La bonne reaction n'est donc pas de l'ignorer, mais de le reparer proprement, de memoriser la solution verifiee, puis de reprendre le travail.
