# Project instructions

## Scope

This workspace supports a first research paper on pixel-space diffusion, with a candidate application to approximately five-second video. Do not assume a finalized contribution, model, GPU budget, dataset, publication venue, or training environment.

## Evidence and records

- Use Chinese for learning notes and meeting preparation; keep identifiers and commands in English.
- Prefer primary sources. Record paper version, section/table/figure, source URL and retrieval date for technical claims.
- Distinguish paper-reported results, inspected code, actual local runs, hypotheses and meeting decisions.
- Never treat image results as verified video results. Check pixel-space versus latent-space modeling explicitly.
- Keep original PDFs immutable; record changes of version as separate files and update the index and manifest.
- Every experiment needs an ID, hypothesis, baseline, configuration, code/data versions, seed, resource budget and evaluation protocol. Record failures too.
- Do not overwrite existing experiment outputs. Put new runs in a new ID or run folder.
- Keep external repositories traceable to source, commit and license; put original code under `external/` and own changes under `code/` or a documented patch.

## Boundaries

- Do not start training, download model weights or large datasets, provision paid resources, stage, commit, push or publish without explicit user authorization.
- Public paper downloads and requested research notes are within the authorized documentation task.
- Do not invent novelty, citations, measurements or advisor decisions. Writing remains a draft for the user's review and authorship.
- Save dataset and checkpoint paths in `data/README.md`; keep credentials out of all records.
- Before a completion claim, verify files, local links and archive integrity. A scaffold is not a reproduced model.
