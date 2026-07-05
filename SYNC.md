# Sync this repo from Switchbox_GUI

See [docs/SYNC_WITH_SWITCHBOX.md](docs/SYNC_WITH_SWITCHBOX.md) for full instructions.

## Quick sync (from Switchbox_GUI root)

```powershell
.\tools\sync_to_classifier_repo.ps1
cd ..\memristive-iv-classifier
git add -A
git commit -m "Sync from Switchbox_GUI"
git push
```

## What is copied

- `analysis/`
- `tools/data_consolidation/`
- `tools/classification_validation/`

Docs and examples in this repo are **not** overwritten by sync — update them manually when rules change.

## Source of truth

**Switchbox_GUI** until you explicitly choose to develop here instead.
