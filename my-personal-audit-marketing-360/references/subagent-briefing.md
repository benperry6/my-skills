# Subagent Briefing Template

This text is prepended to every subagent's task prompt, BEFORE the skill invocation.

---

## Template (copy verbatim into each subagent prompt)

```
INSTRUCTIONS OBLIGATOIRES — Lis et applique AVANT de commencer ton rapport.

## Étape 1 — Test d'applicabilité

Avant TOUTE production de contenu, évalue honnêtement :

APPLICABILITÉ : [score 1-10]
JUSTIFICATION : [1 phrase — pourquoi ce skill s'applique concrètement à CE business, avec un élément factuel observable]
CONTRE-ARGUMENT : [1 phrase — la meilleure raison pour laquelle ce skill ne s'appliquerait PAS à ce business]

Ces 3 lignes DOIVENT être les 3 premières lignes de ton fichier output (après le titre).

### Règles de scoring

- 8-10 : Le skill est au cœur de ce business. Produire le rapport complet.
- 5-7 : Partiellement applicable. Produire le rapport mais sois vigilant sur ce qui est extrapolé vs observé.
- 1-4 : Le skill ne s'applique pas naturellement. NE PAS produire de rapport. Écrire uniquement 5-10 lignes expliquant pourquoi et ce qu'il faudrait pour que ça devienne pertinent. STOP.

### Comment scorer honnêtement

Pose-toi ces questions :
- Est-ce que j'ai des données OBSERVABLES sur le site/produit pour alimenter ce rapport ? (pages, prix, contenu, UX réelle)
- Si je remplaçais le nom du business par un autre du même secteur, est-ce que 80% de mon rapport resterait identique ? → Si oui, c'est trop générique, baisse le score.
- Est-ce qu'un consultant humain expert facturerait un livrable de ce type pour ce client ? → Si la réponse est "ça serait tiré par les cheveux", baisse le score.

## Étape 2 — Production du rapport

Si score >= 5, produis ton rapport NATIVEMENT — comme tu le ferais normalement avec ce skill. Ne change pas ton style, ta structure, ou ta profondeur. Le rapport doit être le meilleur que tu puisses produire.

MAIS : à la fin du rapport, ajoute cette séparation :

---

## --- ZONE EXTRAPOLÉE ---

Tout ce qui suit est du contenu que je considère comme extrapolé, spéculatif, ou basé sur des bonnes pratiques générales plutôt que sur des observations spécifiques à ce business.

[Déplace ici tout contenu de ton rapport qui correspond à ces critères :]

- Recommandations qui s'appliqueraient à N'IMPORTE QUEL business du même secteur sans modification
- Estimations chiffrées non basées sur des données observées (ex: "pourrait augmenter de 30%" sans source)
- Analogies avec d'autres marques/industries sans lien direct vérifié
- Propositions qui requièrent des hypothèses majeures sur les ressources, l'équipe, ou le budget du client
- Idées "nice to have" vs recommandations basées sur des problèmes observés

IMPORTANT : ne supprime PAS ce contenu du rapport. Déplace-le dans cette zone. Il reste visible et potentiellement utile, mais il est clairement séparé du contenu solide.

## Étape 3 — Résumé éditeur

Termine le fichier par :

---
RÉSUMÉ ÉDITEUR
Applicabilité : [score]/10
Contenu solide (au-dessus de la zone extrapolée) : [estimation en % du rapport]
Contenu extrapolé (dans la zone) : [estimation en % du rapport]
Top 3 recommandations les plus solides : [liste]
À ignorer si budget limité : [liste]
---

Lis le fichier 00-business-context.md ci-dessous pour le contexte du business à auditer, puis lance ton analyse.
```

---

## Usage

When constructing a subagent Task prompt, structure it as:

```
[Subagent briefing template above]

[Path to business context file]

[Skill invocation — e.g., "Use the seo-audit skill on https://example.com"]
```
