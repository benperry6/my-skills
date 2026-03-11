# My Personal Context Distillation

`my-personal-context-distillation` est un skill personnel conçu pour transformer du contexte brut en contexte exploitable.

Son rôle n'est pas d'écrire directement des landing pages, des pubs, des emails ou des articles. Son rôle est plus fondamental : construire la mémoire métier d'un projet pour que les autres skills marketing puissent ensuite travailler avec un niveau de contexte suffisant.

## Pourquoi ce skill existe

Les agents IA savent aujourd'hui exécuter, naviguer, lire, écrire, coder, rechercher et produire.

Le vrai problème n'est plus seulement l'exécution.

Le vrai problème, c'est le manque de contexte propriétaire.

Sans contexte métier, même un très bon agent finit par produire :

- du contenu générique
- des hypothèses non vérifiées
- une compréhension approximative du business
- une mauvaise lecture de l'audience réelle

Ce skill a été créé pour résoudre précisément ce problème.

## Le problème qu'il adresse

Dans un repo, les informations utiles au marketing sont souvent dispersées :

- founder dumps
- transcripts speech-to-text
- exports ChatGPT
- docs produit
- notes de décision
- intuition fondateur
- débuts de recherche marché
- learnings de campagnes

En l'état, tout cela n'est pas une mémoire exploitable.

Il faut une couche de distillation.

## Ce que le skill produit

Le skill maintient quatre fichiers canoniques dans `.agents/` :

- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`

Et, lorsque la recherche client est en jeu, il maintient aussi :

- `docs/context-sources/voc-bank.csv`

Cette banque VoC sert de couche de preuves persistante derrière le KYC.

## La logique centrale

Le skill repose sur une séparation volontaire entre plusieurs couches :

### 1. Les sources brutes

Elles vivent dans `docs/context-sources/`.

Exemples :

- transcripts fondateur
- exports de conversations
- notes d'exploration
- matériaux de recherche

### 2. Les fichiers canoniques

Ils vivent dans `.agents/`.

Ce sont les fichiers source-of-truth qu'un autre agent ou qu'un autre skill doit pouvoir relire plus tard sans repartir de zéro.

### 3. La compilation marketing

Ce skill ne compile pas lui-même le contexte marketing final utilisé par les autres skills.

Cette responsabilité appartient à un autre skill :

- `product-marketing-context`

Autrement dit :

- `my-personal-context-distillation` édite la vérité
- `product-marketing-context` compile cette vérité pour l'exécution downstream

## Pourquoi cette séparation est importante

Un repo a besoin de deux choses différentes :

- une mémoire durable, nuancée, maintenable
- un résumé opérationnel compact pour les skills marketing

Si on mélange les deux, on obtient soit :

- une doc trop pauvre
- soit une doc trop lourde
- soit une doc qui n'est plus vraiment source de vérité

La séparation entre distillation et compilation permet de garder le système propre.

## Le cas particulier de Know Your Customer

`know-your-customer.md` ne doit pas être fondé principalement sur l'intuition fondateur.

Le skill applique donc une règle plus stricte sur cette partie :

- les croyances fondateur servent seulement de direction de recherche
- les vérités client doivent venir de vraie VoC publique ou de vraie recherche utilisateur
- rien ne doit être guessé
- si une information n'est pas suffisamment prouvée, elle reste partielle ou va dans `Open Questions`

La VoC Bank existe pour ça.

Elle permet :

- de ne pas refaire les mêmes recherches plus tard
- de garder les citations et sources
- de synthétiser le KYC sur une base traçable

## Ce que le skill ne fait pas

Ce skill ne sert pas à :

- écrire la landing page finale
- produire les ads
- faire le messaging final
- construire le plan d'expériences CRO
- choisir la meilleure stratégie paid media

Tout cela vient ensuite, avec les skills d'exécution.

## Workflow type

1. On dépose les sources dans `docs/context-sources/`
2. Le skill distille vers les fichiers canoniques
3. Il maintient aussi `voc-bank.csv` si le KYC est concerné
4. Une fois les fichiers canoniques assez solides, on lance `product-marketing-context`
5. Ensuite seulement, on lance les autres skills marketing

## Pourquoi ce skill est important

Ce skill est important parce qu'il ferme une boucle.

Avant :

- les équipes humaines portaient implicitement le contexte business
- les agents IA exécutaient sans ce contexte

Après :

- le contexte devient explicite
- durable
- versionné
- réutilisable
- transmissible d'un repo à l'autre

Ce n'est pas juste un skill de nettoyage documentaire.

C'est une brique d'infrastructure pour la production marketing assistée par IA.

## Story derrière le skill

Ce skill est né d'un constat simple :

les agents deviennent très bons pour produire, mais restent faibles dès qu'ils doivent produire quelque chose de vraiment spécifique à un business sans mémoire fiable.

L'objectif n'était donc pas de créer "encore un skill marketing".

L'objectif était de créer la couche qui permet aux autres skills marketing de ne plus travailler dans le vide.

## Statut

Le skill a été :

- conçu pour un usage multi-repo
- testé sur un cas réel de produit email-forwarding
- durci itérativement à partir de vrais runs
- renforcé sur :
  - la séparation vérité / compilation
  - la discipline KYC
  - la VoC Bank persistante
  - le reporting final
  - le niveau de prudence sur les claims partiellement soutenus

## Fichiers principaux

- [SKILL.md](./SKILL.md)
- [references/file-contracts.md](./references/file-contracts.md)
- [references/kyc-research.md](./references/kyc-research.md)
- [references/voc-bank-schema.md](./references/voc-bank-schema.md)

## En une phrase

`my-personal-context-distillation` transforme du contexte brut en mémoire métier durable, afin que les autres agents puissent produire du marketing réellement spécifique, traçable et exploitable.
