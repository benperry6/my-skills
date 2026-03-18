# my-personal-frontend-backend-routing

Route automatiquement le frontend vers Claude Code et le backend vers Codex, quel que soit l'outil dans lequel on a lancé la session.

## Le probleme que ce skill resout

J'utilise trois outils IA pour coder : Claude Code, Codex (OpenAI) et Gemini CLI.

L'observation de base est simple :

- Claude Code excelle dans le frontend. Il comprend le design, le JSX, le CSS, les composants, les interactions visuelles, le responsive. Il produit du code UI qui n'a pas besoin d'etre retouche.
- Codex excelle dans le backend. Il comprend les API, les workers, les models, les migrations, l'infra. Il produit du code serveur robuste et bien structure.

Le probleme, c'est que dans la vraie vie, une feature touche presque toujours les deux. Un systeme de notifications, c'est un worker (backend) + un endpoint API (backend) + une page dans le dashboard (frontend). Trois fichiers, deux specialites.

Avant ce skill, mon workflow ressemblait a ca :

1. Lancer Codex, lui donner la feature entiere
2. Codex fait le backend correctement, mais produit un frontend mediocre
3. Switcher vers Claude Code
4. Demander a Claude Code de "retaper tout le frontend que Codex vient de faire"
5. Claude Code refait le frontend correctement

Ce va-et-vient etait manuel, lent, et source d'erreurs. A chaque switch, il fallait re-expliquer le contexte, montrer les fichiers, preciser les conventions.

## Ce que fait ce skill

Il automatise ce va-et-vient.

Quand un outil detecte qu'il est sur le point d'editer un fichier qui releve de la specialite de l'autre outil, il delegue automatiquement :

| Je suis dans... | Fichier frontend | Fichier backend |
|---|---|---|
| **Claude Code** | J'execute | Je delegue a Codex |
| **Codex** | Je delegue a Claude Code | J'execute |
| **Gemini** | Je delegue a Claude Code | Je delegue a Codex |

L'utilisateur ne switche jamais d'outil. Il reste dans celui qu'il a ouvert. C'est l'outil qui appelle l'autre en arriere-plan quand il en a besoin.

## Comment ca fonctionne

### Detection

Le skill ne s'appuie pas sur des patterns de fichiers rigides. Il donne des heuristiques (composants UI = frontend, endpoints API = backend, etc.) et laisse l'IA juger. Chaque stack est differente, et une liste de regles hardcodees ne pourrait pas couvrir tous les cas.

### Delegation

Quand un outil delegue, il prepare un "context package" : l'identite du projet, les conventions, les fichiers pertinents, les types partages, la consigne precise, et les limites (quels fichiers toucher, lesquels ne pas toucher). Ce package est envoye a l'autre outil en mode headless (`codex exec` ou `claude -p`).

### Review post-delegation

Apres la delegation, l'outil orchestrateur relit tout ce que l'autre a produit, verifie la coherence (types, imports, naming), corrige les petits ecarts, et rapporte a l'utilisateur ce qui a ete fait et par qui.

### Integration avec le design

Quand Claude Code fait du frontend et que la tache implique un nouveau composant visuel ou une refonte UI, il invoque le skill `my-personal-gemini-design` pour obtenir une proposition esthetique avant de coder.

## Pourquoi ce skill existe en tant que skill (et pas en tant que regle)

Une regle dans CLAUDE.md peut dire "delegue le backend a Codex". Mais une regle ne peut pas :

- Detecter automatiquement si un fichier est frontend ou backend
- Preparer un context package structure
- Gerer les erreurs de delegation
- Imposer une review post-delegation
- S'integrer avec le skill de design

Un skill donne toute cette logique de maniere structuree, reproductible, et partageable entre les trois outils.

## La regle d'enforcement

En complement du skill, une regle dans CLAUDE.md (lue par les 3 outils via symlinks) dit :

> Avant d'editer un fichier, verifier si ce fichier releve de la specialite d'un autre outil. Si oui, invoquer le skill de routing.

C'est un enforcement "soft" : l'IA suit la regle, pas un hook. Ca fonctionne bien en pratique car les trois outils respectent leurs instructions globales.
