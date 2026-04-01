# my-personal-pagespeed-maximizer

`my-personal-pagespeed-maximizer` est un skill personnel d'execution pour l'optimisation PageSpeed.

Il existe pour eviter le faux workflow suivant:

- faire un audit
- commenter les resultats
- s'arreter la

Ce n'est pas le comportement voulu.

Le comportement voulu est:

1. mesurer la vraie page avec Google PageSpeed Insights
2. comprendre quel type de page on a entre les mains
3. decider si on doit faire une vraie boucle complete, un re-check cible, ou seulement un guard check
4. identifier les changements a plus fort levier
5. appliquer les changements autorises
6. re-tester apres chaque batch utile
7. si un run contredit fortement l'etat attendu, relancer PSI pour confirmer avant de conclure
8. continuer jusqu'au plafond pratique ou jusqu'a une contrainte reelle

Autrement dit:

> ce skill n'est pas un audit de performance
>
> c'est un moteur d'optimisation PageSpeed de bout en bout

## Ce qu'il cherche a imposer

Ce skill impose une logique operationnelle stricte:

- mesurer d'abord, supposer ensuite
- utiliser Google PageSpeed Insights comme moteur principal de diagnostic
- raisonner mobile-first
- viser le maximum pratique, pas juste le vert
- ne jamais faire de changement visuel sans approbation explicite
- garder uniquement les optimisations qui ameliorent vraiment la mesure
- ne jamais conclure a une regression ou a une victoire sur un seul run aberrant
- arreter la boucle seulement quand il n'y a plus de gain materiel defendable

## La these centrale

La these la plus importante de ce skill est:

> on n'optimise pas chaque URL individuellement, on optimise des archetypes de performance

Donc:

- une nouvelle page from scratch merite souvent une vraie boucle complete
- une page qui reutilise un template deja valide ne merite pas forcement une boucle complete
- mais une page sur un template connu peut quand meme necessiter une re-ouverture du loop si elle change le hero, le LCP probable, les scripts tiers, les embeds, ou la charge runtime du premier viewport

La vraie question n'est pas:

> "est-ce une nouvelle page ?"

La vraie question est:

> "est-ce que cette page introduit un nouveau profil de performance ?"

## Ce que le skill doit faire en usage reel

En usage reel, ce skill doit produire un cycle complet:

### 1. Baseline

- mesurer la page reelle
- extraire les metriques de base
- identifier le LCP probable
- identifier la famille de goulots la plus forte

### 2. Classification

- full archetype optimization
- targeted variant re-check
- inherited validation

et si la page est critique, imposer au minimum un guard check direct

### 3. Traduction diagnostic -> action

Le skill ne doit pas juste dire "voici les problemes".

Il doit dire:

- ce qui semble etre la vraie cause
- quel changement technique tester
- pourquoi ce changement est prioritaire
- si ce changement est visible ou invisible pour l'utilisateur

### 4. Execution

Si le changement est autorise, le skill doit l'appliquer.

Le comportement attendu n'est pas:

- audit
- recommandations
- stop

Le comportement attendu est:

- audit
- decisions
- changements
- re-mesure

### 5. Re-test

Apres chaque batch utile:

- rerun PSI
- comparer les vraies metriques
- garder la modification si elle ameliore reellement le resultat
- rejeter ou revert si elle degrade

Si un run est fortement contradictoire, le skill ne doit pas conclure immediatement.
Il doit rerun PSI pour confirmer, puis decider sur le signal stable plutot que sur l'anomalie isolee.

### 6. Stop rule

Le loop ne s'arrete pas quand la page devient "verte".

Il s'arrete quand:

- les principaux goulots ont ete traites
- les gains restants sont marginaux
- les gains restants exigent un changement visuel non approuve
- ou la page a atteint son plafond pratique sous les contraintes actuelles

## Pourquoi ce skill est strategique

Sans cette discipline, on tombe presque toujours dans l'un de ces deux travers:

### 1. Sous-execution

On fait un audit, on raconte ce qu'on voit, puis on laisse le travail reel a plus tard.

### 2. Sur-execution aveugle

On applique des recettes de perf a la mode sans verifier si elles aident vraiment cette page precise.

Ce skill existe pour eviter ces deux erreurs.

## Pourquoi il doit rester universel

Ce skill ne doit pas dependre d'un framework particulier.

Il doit raisonner en langage de performance observable:

- LCP
- premier viewport
- CSS et JS critiques
- scripts tiers
- charge runtime
- stabilite du layout
- chemin reseau et reponse serveur

Ensuite seulement, l'agent traduit cela dans la stack locale.

## Ce qu'il ne doit pas devenir

Ce skill ne doit pas devenir:

- un audit SEO generaliste
- une checklist de best practices recopies sans verification
- une machine a forcer du 100/100 a l'aveugle
- un pretexte pour modifier le visuel sans approbation
- une fiche de recettes propre a une seule stack

Sa valeur n'est pas de citer des astuces.

Sa valeur est de porter une discipline:

- evidence first
- execution complete
- maximisation reelle
- respect des contraintes produit
- optimisation par archetype de performance
