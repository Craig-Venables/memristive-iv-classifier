# Sync with Switchbox_GUI

**Source of truth:** `Switchbox_GUI` — edit classification code there during normal development.

**This repo:** snapshot + documentation. Refresh when you want a Git record, share with collaborators, or tag a milestone.

## What gets synced

| Switchbox_GUI path | This repo path |
|--------------------|----------------|
| `analysis/` | `analysis/` |
| `tools/data_consolidation/` | `tools/data_consolidation/` |
| `tools/classification_validation/` | `tools/classification_validation/` |

**Not synced:** GUI code, plotting, hardware, `Json_Files/`, root `requirements.txt`.

## Option A — Sync script (recommended)

From Switchbox_GUI root:

```powershell
.\tools\sync_to_classifier_repo.ps1
```

Optional custom target:

```powershell
.\tools\sync_to_classifier_repo.ps1 -TargetRepo "C:\path\to\memristive-iv-classifier"
```

Then in the classifier repo:

```powershell
cd ..\memristive-iv-classifier
git add -A
git commit -m "Sync from Switchbox_GUI"
git push
```

## Option B — Manual robocopy

From Switchbox_GUI root:

```powershell
$dest = "..\memristive-iv-classifier"
robocopy analysis\ "$dest\analysis" /MIR /XD __pycache__ /XF *.pyc
robocopy tools\data_consolidation\ "$dest\tools\data_consolidation" /MIR /XD __pycache__ /XF *.pyc *.log
robocopy tools\classification_validation\ "$dest\tools\classification_validation" /MIR /XD __pycache__ /XF *.pyc
```

## After syncing

1. Re-run `examples/classify_single_sweep.py` on a test file if you changed core logic
2. Update docs in `docs/` if behaviour or schemas changed
3. Commit with a note of the Switchbox_GUI commit hash if useful

## Documentation-only updates

You can edit `docs/` and `examples/` in this repo without syncing code. Keep docs aligned when classification rules change in Switchbox_GUI.

## First-time GitHub push

See root [README.md](../README.md) — `git init`, `gh repo create`, push.

If `gh` is not logged in:

```powershell
gh auth login
```
