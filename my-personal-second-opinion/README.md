# my-personal-second-opinion

Obtenir un second avis independant de deux autres moteurs IA avant de valider un plan ou une decision technique importante.

## La these derriere ce skill

Un seul modele IA, aussi bon soit-il, a des biais systematiques. Il va privilegier certains patterns, ignorer certains risques, et confirmer ses propres hypotheses.

Deux modeles independants qui arrivent a la meme conclusion, c'est un signal fort. Deux modeles qui divergent, c'est un signal encore plus precieux : ca veut dire qu'il y a un angle qu'on n'a pas vu.

Ce skill institutionnalise cette pratique. Il ne demande pas "est-ce que ca va ?". Il demande a deux moteurs differents de faire leur propre analyse, independamment, puis synthetise les resultats.

## Comment ca fonctionne

Le skill est **context-aware** : il detecte dans quel outil il tourne et consulte les deux *autres*.

| Je suis dans... | Je consulte... |
|---|---|
| **Claude Code** | Codex (OpenAI) + Gemini (Google) |
| **Codex** | Claude Code (Anthropic) + Gemini (Google) |
| **Gemini** | Claude Code (Anthropic) + Codex (OpenAI) |

La regle cle : **ne jamais se consulter soi-meme**. Si on est dans Codex, inutile de demander l'avis de Codex — il le donne deja dans la session en cours.

Chaque moteur recoit le meme prompt structure (contexte, question, contraintes) et produit son analyse independamment. Le moteur dans lequel on se trouve synthetise ensuite les deux reponses : consensus, divergences, risques, et recommandation finale.

## Quand ce skill s'active

### Automatiquement (via hook)

Un hook (`plan-review.sh`) detecte quand un plan est redige. Si un plan est detecte (headers de plan + etapes structurees), le hook bloque et force l'invocation du skill.

Ce hook existe dans :
- **Claude Code** : hook Stop dans `~/.claude/hooks/plan-review.sh`
- **Gemini CLI** : hook AfterAgent dans `~/.gemini/hooks/plan-review.sh`
- **Codex** : pas de hook natif, enforcement par regle dans AGENTS.md

### Manuellement

L'utilisateur peut aussi l'invoquer explicitement avec "ask Codex", "ask Gemini", "second opinion", ou en mentionnant directement le skill.

## Pourquoi c'est obligatoire sur les plans

Les plans sont le point ou les erreurs coutent le plus cher. Un mauvais plan, c'est des heures de travail dans la mauvaise direction. Un bon plan avec un angle mort, c'est un incident en production.

Le cout d'un second avis est de 1-2 minutes (deux appels paralleles en arriere-plan). Le cout d'un plan incorrect est de plusieurs heures de rework.

Le ratio est tellement desequilibre qu'il n'y a aucune raison de ne pas le faire systematiquement.

## Les moteurs et leurs forces

| Moteur | Commande | Forces |
|--------|----------|--------|
| **Codex** (OpenAI) | `codex exec --dangerously-bypass-approvals-and-sandbox` | Code, architecture, infrastructure |
| **Gemini** (Google) | `gemini -p` | Raisonnement profond, contexte long (1M tokens), audio/video natif |
| **Claude Code** (Anthropic) | `claude -p` | Frontend, integration codebase, multi-fichiers |

## L'evolution de ce skill

Ce skill a commence comme un outil unidirectionnel : depuis Claude Code, on consultait Codex et Gemini. C'etait utile, mais incomplet.

Le probleme est apparu quand Codex a commence a utiliser le skill aussi — sauf qu'il suivait les memes instructions ecrites pour Claude Code. Resultat : Codex consultait... Codex. Un appel recursif inutile. Le meme modele, les memes biais, zero perspective independante.

La version actuelle est bidirectionnelle et context-aware. Chaque outil detecte automatiquement qui il est (via des variables d'environnement : `CLAUDECODE`, `CODEX_CI`, `GEMINI_CLI`) et consulte les deux autres. Plus jamais de consultation de soi-meme.

## Architecture

- **Skill** : `~/.agents/skills/my-personal-second-opinion/SKILL.md` — source de verite, lu par les 3 outils via symlinks
- **Hook Claude Code** : `~/.claude/hooks/plan-review.sh` — detection de plan, force l'invocation
- **Hook Gemini** : `~/.gemini/hooks/plan-review.sh` — meme logique, adaptee au format Gemini
- **Regle Codex** : dans CLAUDE.md / AGENTS.md — enforcement "soft" par instruction
- **Output** : les reponses des moteurs sont ecrites dans `/tmp/` (jamais dans le contexte), lues apres completion
