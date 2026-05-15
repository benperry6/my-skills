---
name: audit-marketing-360
description: >
  Orchestrate a comprehensive marketing audit using all available marketing skills as parallel subagents, with built-in applicability filtering and quality control. Use when the user wants to audit a brand, website, or business's entire marketing strategy. Triggers: "audit marketing," "audit 360," "rapport marketing complet," "analyse marketing globale," or when evaluating everything that could be improved for a client/prospect. Acts as team lead coordinating specialized subagents and compiling a consolidated report with only substantiated recommendations.
---

# Audit Marketing 360

Orchestrate a full marketing audit by deploying specialized marketing skills as subagents, filtering out stretched/speculative content, and delivering a consolidated report of substantiated recommendations.

## Workflow

### Phase 1 — Reconnaissance

1. **Crawl the target site** using firecrawl MCP (`mcp__firecrawl__firecrawl_map` then `mcp__firecrawl__firecrawl_scrape` on key pages)
2. **Scrape 4-6 key pages** in parallel: homepage, products/pricing, blog, about, a landing page, promotions
3. **Write business context** to `{output_dir}/00-business-context.md` — this file is shared with all subagents

Business context must include: product/service, pricing model, target audience, distribution channels, social proof, competitors, site structure, technical stack.

### Phase 2 — Subagent Deployment

1. **Select applicable skills** from the registry: see [references/skills-registry.md](references/skills-registry.md)
2. **Brief each subagent** by prepending the briefing template to its task: see [references/subagent-briefing.md](references/subagent-briefing.md)
3. **Launch in waves** respecting these rules:
   - Max 3-4 agents per wave
   - All agents use `run_in_background: true`
   - Each agent writes output to `{output_dir}/XX-{skill-name}.md`
   - Wait for 2/3 of a wave to complete before launching next wave
   - Between waves, consider running `/compact` if context is heavy

**Wave composition** (recommended order, adapt based on selected skills):
- Wave 1: SEO audit, Copywriting, Page CRO (foundational analysis)
- Wave 2: Pricing strategy, Content strategy, Experiential offer (strategic layer)
- Wave 3: Marketing psychology, Competitor analysis, Programmatic SEO (growth layer)
- Wave 4: Email sequences, Social content, Referral program, Marketing ideas (tactical layer)

Each subagent receives:
- The business context file path
- The subagent briefing instructions (from references/subagent-briefing.md)
- Its native skill invocation

### Phase 3 — Compilation

After all subagents complete:

1. **Read each report's header** (first 5 lines) to get applicability score and justification
2. **For reports with score >= 5**: read the full report, identify the `--- ZONE EXTRAPOLÉE ---` separator
3. **Compile the final report** using ONLY content ABOVE the separator (the solid zone)
4. **Write final report** to `{output_dir}/RAPPORT-FINAL.md` — NO template, NO fixed structure. Each business is different, each audit is different, each report must be too. Let the content dictate the structure.

### Compilation Rules

1. **NE JAMAIS inclure** de contenu provenant de la "Zone extrapolée" d'un subagent dans le rapport final
2. **Toujours vérifier** les claims factuels (noindex, prix, fonctionnalités) en cross-référençant avec les données crawlées
3. **Favoriser la spécificité** : une recommandation qui cite une page/un texte/un chiffre précis du site est toujours préférable à un conseil générique
4. **Résoudre les contradictions** : si deux subagents se contredisent, investiguer et ne garder que la version vérifiable
5. **Scorer honnêtement** : le score global doit refléter la réalité, pas flatter le client
6. **Audits non applicables** : lister les audits qui se sont abstenus (s'il y en a eu), avec leur justification en 1 ligne. Ceci démontre au client que l'analyse est honnête et calibrée — on ne force pas des recommandations là où elles ne s'appliquent pas. Note : on ne parle jamais de "skills" dans le rapport client, mais de "audits".

## Output Structure

```
{output_dir}/
├── 00-business-context.md          (shared context)
├── 01-seo-audit.md                 (subagent report with zone extrapolée)
├── 02-copywriting-audit.md         (subagent report with zone extrapolée)
├── ...                             (one per deployed skill)
├── XX-[last-skill].md              (subagent report with zone extrapolée)
└── RAPPORT-FINAL.md                (consolidated, solid-only report)
```

## Configuration

The user provides:
- **Target URL** (required)
- **Output directory** (default: `./audit/`)
- **Additional skills to force-include** (optional, e.g., "experiential-offer-design")
- **Skills to exclude** (optional)
- **Language** (default: same as user's language)

## References

- [Subagent briefing template](references/subagent-briefing.md) — Exact instructions prepended to each subagent
- [Skills registry](references/skills-registry.md) — Available marketing skills with applicability criteria
