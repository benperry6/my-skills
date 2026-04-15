# Verified Learning Checklist

Use this before claiming a skill has learned something durable.

- [ ] the finding came from real behavior, not theory alone
- [ ] an explicit learning trigger fired before the loop was invoked
- [ ] if the target skill defines an overlay, that overlay was applied instead of being ignored
- [ ] the incident and repaired path are stated concretely
- [ ] the evidence is inspectable
- [ ] the confidence tier is explicit (`runtime` or `verified`)
- [ ] runtime incidents are stored in a structured machine-readable format, not only in prose
- [ ] if compatibility matters, the incident shape is checked against `references/runtime-incident.schema.json`
- [ ] if the target skill defines `references/runtime-extensions.schema.json`, the incident `extensions` were validated against it
- [ ] unresolved findings are not promoted
- [ ] the smallest correct write target was chosen
- [ ] `SKILL.md` was touched only if canonical guidance truly changed
- [ ] project-specific memory was not mixed into reusable skill doctrine
- [ ] the write-back is small enough that a later session can audit why it happened
- [ ] if multiple incidents were persisted, they were written in batch rather than one subprocess append per incident
- [ ] if git persistence was required, the resulting artifacts were committed and pushed successfully
