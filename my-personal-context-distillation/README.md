# My Personal Context Distillation

`my-personal-context-distillation` n'est pas un skill de documentation.

C'est une brique d'infrastructure conçue pour résoudre ce qui reste, à mes yeux, le principal problème de la production de contenu par agents IA : le manque de contexte propriétaire sur le business.

## La thèse derrière ce skill

J'opère plusieurs types de business :

- des SaaS
- des sites d'affiliation
- quelques activités physiques

Leur point commun est simple : chacun dépend d'un site web.

Et un site web sans trafic ne produit pas de business.

Dans la pratique, ce trafic vient surtout de deux grandes mécaniques :

- les gens nous trouvent via la recherche, y compris Google et les moteurs de réponse IA
- nous amenons les gens à nous via les ads et le media buying

Dans les deux cas, la matière première reste la même :

- du contenu

Du contenu pour être trouvé.
Du contenu pour être cliqué.
Du contenu pour convertir.

## Le problème historique

Pendant longtemps, ce contenu était produit par des équipes humaines.

Ces équipes ne se contentaient pas d'écrire.

Elles apportaient trois choses en même temps :

- une capacité d'exécution
- une expertise sur le format ou le canal
- une connaissance intime du business, de l'offre, de l'audience et du langage du marché

C'est ce troisième point qui faisait la différence.

Les équipes savaient :

- quoi raconter
- comment le raconter
- à qui parler
- quoi mettre en avant
- quoi éviter

Autrement dit, elles savaient produire du contenu qui ne sonnait pas générique.

## Ce qui a changé avec les agents IA

Les outils de type ChatGPT ont d'abord été très utiles pour répondre à des questions.

Puis des agents comme Codex ou Claude Code ont fait sauter une autre barrière : ils peuvent maintenant agir, chercher, lire, écrire, coder, naviguer et exécuter.

Ensuite, les skills ont ajouté une autre couche :

- une spécialisation réutilisable
- des workflows dédiés
- de la méthode
- des garde-fous

Donc aujourd'hui, les agents savent déjà beaucoup mieux produire qu'avant.

Mais il restait un manque.

## Le manque qui restait

Même avec de bons agents et de bons skills, le contenu produit reste souvent :

- propre
- rapide
- techniquement acceptable
- mais trop générique

Pourquoi ?

Parce qu'un agent ne peut pas inventer le contexte réel d'un business.

S'il ne connaît pas :

- l'offre
- le business model
- la logique de monétisation
- l'histoire de la marque
- le langage réel du marché
- les attentes et objections du client

alors il guess.

Et dès qu'il guess, la qualité chute.

## L'idée fondatrice

L'idée de départ est née autour d'un fichier `business-model.md` créé manuellement dans un projet.

Au début, ce fichier paraissait simplement utile.

Puis il est devenu évident qu'il ne s'agissait pas d'un besoin local à un seul projet, mais d'une brique générique qui manque à presque tous les repos où l'on demande ensuite aux agents de produire du contenu.

Le constat a donc évolué :

- un seul fichier n'est pas suffisant
- ce besoin existe dans tous les business
- si on veut que des agents remplacent une partie du travail des équipes humaines de contenu, il faut leur donner explicitement ce que ces équipes avaient implicitement

D'où le framework de base :

- `business-model.md`
- `storytelling.md`
- `know-your-customer.md`

Puis une quatrième couche s'est imposée :

- `performance-memory.md`

## Ce que ce skill fait exactement

Ce skill prend du matériau brut :

- founder dumps
- transcripts speech-to-text
- exports de conversations
- notes produit
- docs de repo
- learnings marketing
- signaux marché

et le transforme en mémoire métier exploitable.

Il maintient les fichiers canoniques suivants dans `.agents/` :

- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`

Et quand le sujet client est concerné, il maintient aussi :

- `docs/context-sources/voc-bank.csv`

## Ce dont ce skill a besoin en input

Pour bien fonctionner, ce skill a besoin d'un vrai matériau fondateur en entrée.

Le meilleur input pour `business-model.md` et `storytelling.md` n'est pas un brief sec en 5 lignes.

C'est un founder dump suffisamment riche pour expliquer :

- ce que fait vraiment le business
- comment il gagne de l'argent
- ce qu'il vend
- à qui
- pourquoi il existe
- comment il est né
- ce qui compte vraiment dans l'offre
- ce qu'il faut absolument éviter de déformer

Le format recommandé est simple :

- un ou plusieurs audios du fondateur
- transformés en speech-to-text
- déposés dans `docs/context-sources/`

Si 30 minutes, 1 heure, ou davantage sont nécessaires pour raconter correctement le business, ce n'est pas un problème.

Un input long mais réel vaut mieux qu'un contexte trop court, trop propre, ou trop abstrait.

Pour `know-your-customer.md`, le fondateur peut aussi fournir un point de départ utile :

- les segments visés
- l'intuition du marché
- les clients supposés
- les problèmes supposés
- les concurrents ou alternatives déjà connus

Mais cet input n'est qu'un seed de recherche.

La vérité client doit ensuite être soutenue par de la vraie VoC et de la vraie recherche publique.

## Pourquoi ces fichiers existent

### `business-model.md`

Pour expliquer comment l'activité crée de la valeur et gagne de l'argent.

### `storytelling.md`

Pour expliquer d'où vient le business, ce qu'il défend, et comment il doit sonner.

### `know-your-customer.md`

Pour expliquer qui est le client, ce qu'il vit, ce qu'il veut, ce qu'il craint, et avec quels mots il l'exprime.

### `performance-memory.md`

Pour éviter que les learnings réels disparaissent après une campagne, un test ou un run.

## Le cas spécial de Know Your Customer

C'est la partie la plus sensible du système.

Sur le business model ou le storytelling, le fondateur reste souvent la meilleure source.

Sur le client, ce n'est pas vrai.

Le fondateur a souvent :

- des intuitions utiles
- des hypothèses plausibles
- une direction de recherche

mais pas nécessairement la vérité du marché.

C'est pourquoi ce skill impose une discipline particulière sur le KYC :

- le fondateur sert de point de départ, pas de vérité finale
- les affirmations client doivent être soutenues par de la vraie VoC ou de la vraie recherche
- rien ne doit être guessé
- les zones non prouvées doivent rester partielles ou aller dans `Open Questions`

La `VoC Bank` sert justement à garder la preuve derrière la synthèse.

## Ce qu'il ne faut pas faire

Il ne faut pas lancer ce skill avec un contexte business trop léger puis espérer un bon résultat par magie.

Si les matériaux fondateurs sont trop faibles, trop vagues, trop courts, ou trop incomplets, le bon comportement n'est pas de foncer tête baissée.

Le bon comportement est :

- de distiller uniquement ce qui est réellement soutenu
- de pousser le reste dans `Open Questions`
- de dire clairement que le repo n'est pas encore prêt pour une compilation marketing de qualité
- et de demander au fondateur plus de contexte avant d'aller plus loin

Autrement dit :

- pas assez de contexte business fiable = pas de bon `business-model.md`
- pas assez de contexte fondateur réel = pas de bon `storytelling.md`
- pas assez de vraie VoC = pas de bon `know-your-customer.md`

## Pourquoi la VoC Bank existe

Refaire sans cesse la même recherche marché serait absurde.

Cela coûte :

- du temps
- des ressources
- de l'argent

et cela augmente le risque de perdre des nuances au moment de la synthèse.

La `VoC Bank` existe donc comme couche de persistance :

- pour conserver les citations
- pour garder les sources
- pour éviter de repartir de zéro
- pour appuyer le KYC sur une base traçable

## Ce skill n'écrit pas le marketing final

Ce point est volontaire.

`my-personal-context-distillation` n'écrit pas directement :

- les pages de vente
- les ads
- les emails
- les plans CRO
- les documents de messaging

Son rôle est plus en amont.

Il prépare le terrain.

Il construit la mémoire.

Il transforme un repo sans contexte en repo avec contexte.

## La séparation clé du système

Il y a une séparation volontaire entre :

- la vérité canonique
- la compilation opérationnelle

Ce skill édite la vérité.

Un autre skill, `product-marketing-context`, compile ensuite cette vérité en un contexte plus directement consommable par les skills marketing downstream.

Autrement dit :

- `my-personal-context-distillation` construit la mémoire durable
- `product-marketing-context` prépare cette mémoire pour l'exécution

Cette séparation évite de mélanger :

- source de vérité
- résumé de travail
- exécution marketing

## Ce que ce skill essaie de rendre possible

L'ambition derrière ce skill n'est pas simplement d'avoir de "meilleures notes de projet".

L'ambition est plus grande :

donner à des agents IA une partie de ce que les équipes humaines apportaient naturellement, afin qu'ils puissent produire un contenu réellement spécifique au business, à l'audience et au contexte.

L'objectif n'est pas de produire plus de contenu générique.

L'objectif est de produire un contenu :

- plus spécifique
- plus cohérent
- plus traçable
- plus réutilisable
- plus proche du niveau d'une équipe humaine spécialisée

## Workflow

1. On dépose les sources dans `docs/context-sources/`
2. Le skill distille ces sources vers les fichiers canoniques
3. Il maintient la `VoC Bank` si le KYC est concerné
4. Si le contexte est encore trop faible, le skill doit le dire explicitement et demander davantage de matière avant d'aller plus loin
5. Une fois le contexte suffisamment solide, on lance `product-marketing-context`
6. Ensuite seulement, on lance les skills d'exécution marketing

## Comment l'utiliser concrètement

Le skill ne demande pas une formule magique, mais il fonctionne mieux si la demande est explicite sur trois points :

- le mode attendu : `bootstrap`, `update`, `performance-update`, ou `audit`
- les sources à utiliser
- le niveau d'exigence sur le KYC et la `VoC Bank`

Si tu sais déjà que le contexte fondateur est léger, la bonne demande n'est pas "fais au mieux".

La bonne demande est plutôt :

- distille uniquement ce qui est réellement soutenu
- liste ce qu'il manque
- et dis-moi explicitement si tu as besoin de plus de contexte fondateur avant de continuer

### Prompt simple pour lancer le skill

```text
Use the `my-personal-context-distillation` skill in bootstrap mode.

Source material:
- `docs/context-sources/...`

Goal:
- create or update:
  - `.agents/business-model.md`
  - `.agents/storytelling.md`
  - `.agents/know-your-customer.md`
  - `.agents/performance-memory.md`
  - `docs/context-sources/voc-bank.csv`

Rules:
- do not invent
- use founder material for business-model and storytelling
- use real public voice-of-customer research for know-your-customer
- persist meaningful customer evidence in `voc-bank.csv`
- keep unsupported points in `Open Questions`
- when finished, propose running `product-marketing-context`
```

### Prompt simple pour mettre à jour un repo déjà initialisé

```text
Use the `my-personal-context-distillation` skill in update mode.

New source material:
- `docs/context-sources/...`

Goal:
- update the canonical context files without flattening nuance
- update `docs/context-sources/voc-bank.csv` if KYC is in scope
- keep unsupported claims explicit
- propose running `product-marketing-context` when done
```

### Prompt prêt à l'emploi pour re-générer `product-marketing-context`

Si un `product-marketing-context` existe déjà mais a été généré trop tôt, sans vrai contexte, utilise un prompt explicite comme celui-ci :

```text
Use the `product-marketing-context` skill to re-create the compiled marketing context from the canonical `.agents` context files.

Use these files as the primary source-of-truth inputs:
- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`

Goal:
- create or fully refresh `.agents/product-marketing-context.md`

Rules:
- do not treat README, landing pages, stale marketing copy, or any existing compiled marketing context as the source of truth if the canonical `.agents` files already exist
- limited repo discovery is allowed only as a secondary supporting input to find useful implementation-grounded or spec-grounded details that are missing from the compiled output
- do not let repo-wide discovery override, weaken, or contradict the four canonical context files
- treat any existing `product-marketing-context` file as replaceable derivative context, not as the source of truth
- preserve only what is consistent with the four canonical context files
- if the files conflict, the four canonical `.agents` files win
- when using secondary repo discovery, include only details that are clearly compatible with the canonical context and useful for downstream marketing work
- when done, summarize what was kept, what changed, what was added from secondary repo discovery, and what was removed from the previous compiled context
```

## Pourquoi ce skill compte dans cette stack

Sans lui :

- les agents savent produire, mais sans mémoire fiable
- les skills savent exécuter, mais sur une base trop pauvre
- le contenu retombe vite dans le générique

Avec lui :

- le contexte devient explicite
- versionné
- durable
- transmissible d'un repo à l'autre
- exploitable par d'autres agents

Ce skill ne remplace donc pas les autres skills.

Il les rend beaucoup plus utiles.

## Statut actuel

Le skill a été :

- conçu pour un usage multi-repo
- testé sur un cas réel de produit email-forwarding
- durci itérativement à partir de vrais runs
- renforcé sur :
  - la séparation vérité / compilation
  - la discipline KYC
  - la `VoC Bank` persistante
  - le reporting final
  - la prudence sur les claims partiellement soutenus

## Fichiers principaux

- [SKILL.md](./SKILL.md)
- [references/file-contracts.md](./references/file-contracts.md)
- [references/kyc-research.md](./references/kyc-research.md)
- [references/voc-bank-schema.md](./references/voc-bank-schema.md)

## En une phrase

`my-personal-context-distillation` transforme du contexte brut en mémoire métier durable, pour que les agents puissent produire un marketing moins générique, plus spécifique, et plus proche du niveau d'une équipe humaine qui connaît réellement le business.
