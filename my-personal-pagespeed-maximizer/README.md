# my-personal-pagespeed-maximizer

`my-personal-pagespeed-maximizer` est un skill personnel de doctrine.

Il existe pour eviter de refaire, page par page et repo par repo, la meme discussion floue sur "est-ce qu'il faut rechecker cette page ?", "est-ce qu'on vise juste le vert ?", ou "est-ce que cette optimisation est vraiment bonne ou juste a la mode ?"

## Ce que ce skill cherche a imposer

Ce skill ne traite pas PageSpeed comme un audit cosmetique.

Il impose une logique operationnelle:

- mesurer d'abord, supposer ensuite
- utiliser Google PageSpeed Insights comme moteur principal de diagnostic
- pousser une page jusqu'a son plafond pratique, pas juste jusqu'au vert
- proteger strictement le visuel et l'UX tant qu'aucun changement visible n'a ete explicitement approuve
- capitaliser les apprentissages verifies plutot que les intuitions
- raisonner en langage de performance observable, pas en langage de framework

## La these centrale

La these la plus importante de ce skill est simple:

> on n'optimise pas chaque URL individuellement, on optimise des archetypes de performance

Autrement dit:

- une nouvelle page "from scratch" merite souvent une vraie boucle complete
- une page qui reutilise un template deja valide ne merite pas forcement une boucle complete
- mais une simple "page sur le meme template" peut quand meme necessiter un rerun si elle change le hero, le LCP probable, les scripts tiers, les embeds, le comportement runtime du premier viewport, ou tout autre levier perf-sensible

La vraie question n'est donc pas "est-ce une nouvelle page ?"

La vraie question est:

> "est-ce que cette page introduit un nouveau profil de performance ?"

Si oui, il faut reouvrir la boucle.
Si non, la page peut heriter d'une validation precedente.

## Pourquoi ce skill est strategique

Sans cette doctrine, on tombe generalement dans l'un de ces deux travers:

### 1. Sur-optimiser chaque page

On gaspille du temps, de l'energie et des tokens a rerun un workflow lourd sur des pages qui ne changent presque rien au chemin de rendu reel.

### 2. Sous-optimiser des pages "presque identiques"

On suppose qu'un template deja optimise couvre automatiquement toutes ses variantes, alors qu'une hero image differente, une video, un embed, ou un script tiers peut suffire a casser le LCP, le TBT, ou le CLS.

Ce skill existe pour eviter ces deux erreurs.

## Pourquoi il doit rester universel

Sa these ne depend pas d'un framework particulier.

Elle reste valable pour:

- un site statique
- un CMS
- une SPA
- un site SSR
- une app hybride
- une stack custom

Le skill ne doit donc pas dire "fais du Next.js" ou "fais du React".

Il doit dire:

- quel element est probablement LCP
- ce qui retarde son rendu
- ce qui surcharge le premier viewport
- ce qui casse la stabilite du layout
- ce qui justifie une boucle complete, un recheck cible, ou un heritage de validation

Ensuite seulement, l'agent qui l'utilise traduit cela dans la stack locale.

## Ce qu'il doit rendre systematique

Le skill doit toujours:

- classer la page dans le bon mode: boucle complete, recheck cible, ou inheritance
- appliquer la politique de decision dans le bon ordre: full rerun, puis recheck cible, puis seulement heritage
- raisonner mobile-first
- traiter les diagnostics PSI comme des hypotheses a tester
- garder uniquement les changements qui ameliorent vraiment la mesure
- rejeter ou revert les pseudo-optimisations qui degradent le resultat
- s'arreter seulement quand il n'y a plus de gain materiel defendable

## Ce qu'il faut maintenant rendre non-negociable

Le skill doit etre explicite sur la politique de skip:

- quand un full rerun est obligatoire
- quand un recheck cible est obligatoire
- quand l'heritage de validation est autorise
- quand un simple garde-fou leger devient obligatoire meme si l'heritage parait legitime
- et ce que ce garde-fou leger doit faire exactement

Sans cela, un skill de performance devient trop facilement soit trop laxiste, soit trop gourmand.

La regle doit etre:

- sur une page critique, l'heritage peut rester autorise
- mais il n'autorise jamais a sauter toute verification directe

Et "page critique" ne doit plus etre laisse a l'interpretation libre:

- homepage
- money page
- launch page
- page a trafic important attendu
- page a cout d'echec eleve

## Ce qu'il ne doit pas devenir

Ce skill ne doit pas devenir:

- un audit SEO generaliste
- une checklist de "best practices" recopiees sans verification
- une machine a forcer du 100/100 aveuglement meme si cela casse l'UX ou le produit
- un pretexte pour faire des changements visuels sans validation
- une fiche de recettes liee a une seule stack

Sa valeur n'est pas de citer des recettes.

Sa valeur est de porter une discipline:

- evidence first
- maximisation reelle
- respect des contraintes produit
- optimisation par archetype de performance
