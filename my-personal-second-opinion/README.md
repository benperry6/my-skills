# my-personal-second-opinion

Obtenir un second avis independant de deux autres moteurs IA, tout en gardant le skill a jour quand les CLIs evoluent.

## Ce que ce skill fait maintenant

Ce skill n'est plus un simple routeur "appelle les deux autres outils". Il est maintenant **self-healing**:

- si un appel a un moteur externe casse, ce n'est plus un bug silencieux
- l'agent orchestrateur doit d'abord reparer ce chemin d'appel
- il doit verifier le correctif en comportement reel
- il ne doit enregistrer le learning que si le chemin repare fonctionne vraiment
- puis il reprend automatiquement la mission initiale sans demander a l'utilisateur de relancer le travail

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

est la base de connaissance reutilisable du skill.

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
- `gemini -m gemini-3-flash-preview -p ... --output-format json` a ete reverifie comme fonctionnel
- `gemini -m gemini-3.1-pro-preview -p ... --output-format json` a echoue ici en `429 MODEL_CAPACITY_EXHAUSTED`
- `gemini -m gemini-3.1-flash-lite-preview -p ... --output-format json` a echoue ici en `404 ModelNotFoundError`
- le chemin implicite sans modele explicite n'est pas assez deterministe pour ce skill: il peut rerouter via un utility router interne et produire du bruit de tools

Donc, dans l'etat actuel verifie, le skill doit:

- preferer un modele Gemini explicite plutot que compter sur la route implicite
- utiliser `gemini-3-flash-preview` comme chemin stable actuellement verifie sur cette machine
- garder `gemini-2.5-flash` puis `gemini-2.5-pro` comme fallbacks reels
- ne promouvoir `gemini-3.1-*` en chemin canonique qu'apres succes reel dans l'environnement courant

## Pourquoi c'est important

Ce skill sert justement dans les moments ou on a besoin d'un regard externe supplementaire: plan important, architecture, debug complexe, revue securite, decision a enjeu.

Si ce skill casse au moment ou on en a besoin, ce n'est pas un detail. C'est une panne d'infrastructure de raisonnement. La bonne reaction n'est donc pas de l'ignorer, mais de le reparer proprement, de memoriser la solution verifiee, puis de reprendre le travail.
