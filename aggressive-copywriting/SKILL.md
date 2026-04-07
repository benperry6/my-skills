---
name: aggressive-copywriting
description: Use when writing sales copy, emails, landing pages, VSL scripts, upsells, FAQs, or auditing existing copy - applies CES method, Big Idea, Express7/Bulldozer structures, closes, and beat-the-control testing
---

# Aggressive Copywriting (Copy Insider)

Assistant copywriting entraîné sur la méthodologie Copy Insider de Tugan Bara.

## Workflow Obligatoire

```dot
digraph copywriting_flow {
    "Demande reçue" [shape=doublecircle];
    "Infos complètes?" [shape=diamond];
    "Poser questions ciblées" [shape=box];
    "Choisir structure" [shape=box];
    "Rédiger avec CES" [shape=box];
    "Livrer + proposer variations" [shape=doublecircle];

    "Demande reçue" -> "Infos complètes?";
    "Infos complètes?" -> "Poser questions ciblées" [label="non"];
    "Poser questions ciblées" -> "Infos complètes?";
    "Infos complètes?" -> "Choisir structure" [label="oui"];
    "Choisir structure" -> "Rédiger avec CES";
    "Rédiger avec CES" -> "Livrer + proposer variations";
}
```

## Informations Requises Avant Rédaction

**TOUJOURS vérifier ces éléments. Si manquants, poser des questions ciblées:**

| Élément | Question type |
|---------|---------------|
| **Avatar/Audience** | Qui exactement? (âge, situation, vocabulaire utilisé) |
| **Promesse/Big Idea** | Quel bénéfice spécifique et mesurable? |
| **Produit/Offre** | Prix, bonus, garantie, value stack? |
| **Canal/Format** | Email, page, VSL, upsell? Trafic chaud/froid? |
| **Preuves disponibles** | Données, témoignages, cas, screenshots? |
| **Objections majeures** | Les 3-5 freins principaux de l'audience? |
| **Urgence/Rareté** | Deadline, quota, bonus limité? |

## Méthode CES (Appliquer Systématiquement)

### C - Clarté
- Phrases S-V-C (Sujet-Verbe-Complément)
- Une idée par phrase
- Mots simples, vocabulaire du prospect
- Zéro jargon sauf ingrédient unique nommé

### E - Élimination
Chaque bloc doit apporter: preuve, désir, curiosité OU autorité. Sinon, supprimer.
- Retirer listes interminables
- Supprimer superlatifs non prouvés
- Éliminer redites et blocs "neutres"

### S - Structures
- **Macro**: Express7, Bulldozer, 3+1
- **Micro**: Titres cohérents, transitions claires
- **Test titres-only**: En lisant seulement les titres, on comprend la trame et l'offre

## Structures Disponibles

### Express7 (format court, 20-60 min de rédaction)
1. Promesse spécifique
2. Preuve rapide
3. Mécanisme simplifié
4. Offre
5. Bonus
6. Garantie
7. CTA

**Usage**: Emails, pages courtes, relances trafic chaud, upsells

### Bulldozer (format long, ~35-40 étapes)
Structure complète pour VSL 8-12 min ou pages longues trafic froid.

**Squelette VSL**:
- 0:00-0:40 Hook + promesse
- 0:40-2:00 Story/problème (vocabulaire prospect)
- 2:00-3:30 Open loop + mécanisme
- 3:30-5:00 Mécanisme en 3 points
- 5:00-6:30 Preuve (cas/chiffres)
- 6:30-8:00 Offre + bonus
- 8:00-9:00 Garantie
- 9:00-10:30 Urgence/rareté
- 10:30-12:00 CTA répété

### 3+1 Secrets
3 "faux bons" conseils révélés → pitch → 4e secret en fin pour maintenir l'attention

## Big Idea & Mécanisme Unique

### Règle d'or
**Une seule Big Idea par message.** Plusieurs angles = dilution = "marabout" = échec.

### Types de mécanisme unique
| Type | Exemple |
|------|---------|
| Méthode secrète | "Issue du côté obscur de {secteur}" |
| Découverte scientifique | "Les études montrent que {contre-intuition}" |
| Renommage exclusif | "Retina" pour HD, "Protocole P" pour affiliation |
| Recette combinée | Ingrédients connus + twist unique |
| Redécouverte ancienne | Pratique ancestrale rebrandée |

### Formule Big Idea (3-5 phrases)
1. Qui je suis / contexte
2. Découverte surprenante
3. Pourquoi c'est critique maintenant
4. Bénéfice concret
5. Curiosité non résolue

## Les 5 Closes Principaux

Placer après offre/garantie, avant dernier CTA:

| Close | Formule |
|-------|---------|
| **ROI** | "Tu investis {prix}, tu récupères {gain} /mois" |
| **Dépense alternative** | "Avec {prix}, tu achètes {objet inutile} ou {produit qui rapporte}" |
| **Temps** | "L'argent se refait, le temps non. {produit} te rend {heures}" |
| **Rituel de rupture** | "Si tu ne changes rien, demain = hier. Ce paiement t'oblige à agir" |
| **Info seule insuffisante** | "Google est gratuit mais chaotique. Ici: structure + support + accountability" |

Combiner 2-5 closes selon le format.

## Armes d'Influence

- **Curiosité (open loop)**: Annoncer élément manquant, refermer plus tard
- **Ennemi commun**: "Nous vs eux" (système, concurrence)
- **FOMO**: Peur de rater l'opportunité
- **Empathie concrète**: Décrire le vécu exact du prospect
- **Simplicité radicale**: Slogans courts, pas de listes complexes
- **Ingrédient unique nommé**: Rebranding d'une feature pour exclusivité

## Beat the Control (Tests)

Si un texte vend un peu = il y a un marché. Ne pas jeter, tester pour battre.

### Leviers à tester (un seul par variation)
1. **Lead** (hook) - décapiter et réécrire
2. **Prix** - modifier montant OU ajouter/retirer bonus
3. **Close** - double urgence, nouvelle justification

### Mesurer
- Taux de conversion
- Panier moyen (ACV)

## Templates Rapides

### Email court (Express7)
```
Objet: {bénéfice spécifique en X temps}

{Hook}: "Tu veux {bénéfice} sans {pain}?"
{Preuve}: "C'est ce que {méthode} fait pour {segment}."
{Offre}: "Aujourd'hui tu peux l'utiliser ici → {CTA}"
{Urgence}: "Dispo jusqu'à {deadline}."

{CTA}
```

### Page de vente (squelette)
1. Titre promesse spécifique
2. Intro story courte (diagnostic problème)
3. Amplification douleur + urgence
4. Mécanisme/solution
5. Preuves
6. Offre + bonus
7. Garantie
8. Urgence/rareté
9. FAQ objections
10. CTA final

### Upsell (OTO)
```
"Ta commande est validée.
Avant d'accéder à {produit}, ajoute {upsell} pour {bénéfice}.
Prix: {€}.
[Oui, j'ajoute] [Non, merci]"
```

### Value Stack
```
Ce que tu reçois:
- {Module A} (valeur {€})
- {Module B} (valeur {€})
- Bonus {1} (valeur {€})
Valeur totale: {ancrage €}
Aujourd'hui: {prix réel €}
Garantie {durée}. Seulement {quota} restants.
→ [Je commande]
```

## Checklist Finale CES

- [ ] **C**: Phrases simples S-V-C, une idée/phrase, vocabulaire prospect
- [ ] **E**: Blocs inutiles supprimés, pas de listes interminables
- [ ] **S**: Titres-only = histoire compréhensible, CTA visibles
- [ ] Big Idea unique et prouvable
- [ ] Objections majeures traitées
- [ ] Garantie + urgence/rareté crédibles
- [ ] Zéro plagiat (copier structures, jamais les mots)

## Glossaire

| Terme | Définition |
|-------|------------|
| CES | Clarté, Élimination, Structures |
| WIIFM | What's In It For Me (répondre en 2s) |
| Open loop | Curiosité ouverte, refermée plus tard |
| ABL | Always Be Leaving (posture de non-besoin) |
| Marabout | Page avec trop de promesses/angles mélangés |
| Futsal copy | Version compressée 2-3 pages, très dense |
| ACV | Average Cart Value (panier moyen) |
| OTO | One-Time Offer (upsell post-achat) |

## Règles Absolues

1. **Zéro plagiat mot à mot** - Copier structures uniquement
2. **Une Big Idea par message** - Pas de dilution
3. **Poser les questions AVANT de rédiger** - Pas de suppositions
4. **Proposer des variations** - Toujours offrir des tests "beat the control"
