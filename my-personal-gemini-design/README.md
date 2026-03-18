# my-personal-gemini-design

Assistant de design pour le developpement frontend. Verifie shadcn/ui d'abord, consulte Gemini pour l'esthetique, valide la qualite, puis integre dans le codebase.

## Pourquoi ce skill existe

Claude Code est excellent en frontend. Il comprend les types, le routing, le state, le multi-fichiers, les tests. Mais quand il s'agit de produire un composant visuellement ambitieux — une page complete, un dashboard, une refonte UI — il a tendance a produire quelque chose de fonctionnel mais generique.

Gemini, de son cote, a un sens esthetique different. Quand on lui donne les bons prompts orientes design, il produit du JSX visuellement plus soigne : meilleure hierarchie visuelle, meilleurs espacements, meilleure utilisation des transitions et des etats interactifs.

L'idee de ce skill est simple : combiner les deux.

Claude Code garde le controle total du codebase (types, imports, state, routing, tests). Mais quand il doit creer un composant visuel, il consulte Gemini pour obtenir une proposition esthetique, puis l'integre lui-meme dans le projet en verifiant la coherence.

C'est le meme pattern que le skill `second-opinion` : consulter n'est pas deleguer. Gemini propose, Claude Code dispose.

## Le workflow en 4 etapes

### Etape 1 — shadcn/ui d'abord

Avant de generer quoi que ce soit, le skill verifie si des composants shadcn/ui couvrent deja le besoin. Pas la peine de reinventer un `Button`, un `Card` ou un `Dialog` quand ils existent deja, testes, accessibles, et coherents avec le design system.

Le skill impose aussi les Critical Rules de shadcn : couleurs semantiques, `FieldGroup` + `Field` pour les formulaires, `gap-*` au lieu de `space-*`, `data-icon` pour les icones, etc.

### Etape 2 — Consultation Gemini

Le skill appelle `gemini -p` avec un prompt de design structure qui :

- Decrit le composant a creer et le contexte du projet
- Impose l'utilisation des composants shadcn identifies a l'etape 1
- Demande un output qui suit les conventions shadcn (tokens semantiques, composition)
- Se concentre sur le visuel : layout, hierarchie, esthetique, interactivite, responsive
- Exclut explicitement la logique metier, les types, le state, le routing

### Etape 3 — Fallback Antigravity

Gemini CLI a des limites de requetes quotidiennes (Google AI Pro). Si la limite est atteinte :

1. Le skill detecte le rate limit (429, quota, RESOURCE_EXHAUSTED)
2. Il essaie Antigravity Manager (un proxy local sur `localhost:8045`)
3. Si Antigravity est off, il arrete et dit clairement a l'utilisateur quoi faire

Pas de boucle silencieuse, pas de retry aveugle. Un message clair et un arret net.

### Etape 4 — Quality gate

Claude Code evalue le resultat de Gemini :

1. Passe le code dans le skill `web-design-guidelines` (conformite UI/UX, accessibilite)
2. Verifie la conformite shadcn (couleurs semantiques, composition correcte)
3. Verifie la coherence avec le codebase (types, imports, naming)
4. Decide : utiliser tel quel, adapter, ou jeter et refaire lui-meme

C'est cette derniere etape qui fait la difference. Gemini n'est pas un executeur aveugle. Si son output est mediocre, Claude Code le jette et fait mieux lui-meme. Si son output est bon, Claude Code l'integre en corrigeant les details (imports, types, naming).

## Quand ce skill s'active (et quand il ne s'active pas)

**S'active** : nouveau composant visuel, nouvelle page, refonte UI.

**Ne s'active pas** : fix CSS, ajout d'un champ dans un formulaire, ajustement de padding, mise a jour de texte. Pour ces cas, Claude Code fait le travail directement — pas besoin d'un aller-retour avec Gemini.

## Les prompts de design

Les prompts sont ecrits dans le skill. Ils ne sont pas copies d'un produit tiers. Ils couvrent : layout et structure visuelle, esthetique (espacement, typographie, couleurs), interactivite (hover, transitions, animations), responsive, et integration shadcn.

## Pourquoi les prompts sont dans le skill et pas dans un MCP

A l'origine, j'utilisais le Gemini Design MCP pour ca. Il fonctionnait, mais :

- Les MCPs bug regulierement (serveur down, proxy instable, timeout)
- Le MCP est une dependance tierce payante avec des limites de tokens
- Le MCP ne connait pas mon codebase (il ne voit que ce qu'on lui passe en params)

En integrant les prompts directement dans le skill et en appelant `gemini -p`, on elimine toutes ces dependances. Plus simple, plus robuste, gratuit (utilise l'auth Gemini CLI locale).
