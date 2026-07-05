# Memristive IV Classifier

Rule-based IV sweep classification for memristive and related device types. This repository is a **documented snapshot** of the classification engine and offline batch/review tools from [Switchbox_GUI](https://github.com/pythonProject/Switchbox_GUI).

**Source of truth for daily development:** Switchbox_GUI (`analysis/` and `tools/` there). Update this repo when you want a Git record or shareable reference — see [SYNC.md](SYNC.md).

## What this repo contains

| Path | Description |
|------|-------------|
| [`analysis/`](analysis/) | Core engine: `SweepAnalyzer`, `quick_analyze`, device tracking JSON |
| [`tools/data_consolidation/`](tools/data_consolidation/) | Flatten datasets, batch classify, review GUIs |
| [`tools/classification_validation/`](tools/classification_validation/) | Weight tuning and validation against labeled sweeps |
| [`docs/`](docs/) | Architecture, rules, data formats, API reference |
| [`examples/`](examples/) | Standalone scripts (no GUI required) |

## Quick start

```powershell
cd memristive-iv-classifier
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Classify one sweep file
python examples/classify_single_sweep.py path\to\sweep.txt
```

## Documentation

Start at **[docs/README.md](docs/README.md)** for a 5-minute overview, then:

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — pipeline from sweep to tracking JSON
- [CLASSIFICATION_RULES.md](docs/CLASSIFICATION_RULES.md) — device types, memristivity score, forming
- [OVERLAY_RULES.md](docs/OVERLAY_RULES.md) — Sample GUI map display rules (in Switchbox_GUI)
- [DATA_FORMATS.md](docs/DATA_FORMATS.md) — JSON, logs, batch CSV schemas
- [API.md](docs/API.md) — `quick_analyze`, kwargs, return dict
- [BATCH_WORKFLOW.md](docs/BATCH_WORKFLOW.md) — consolidate → classify → review
- [SYNC_WITH_SWITCHBOX.md](docs/SYNC_WITH_SWITCHBOX.md) — refresh this repo from Switchbox_GUI

## Relationship to Switchbox_GUI

Switchbox_GUI integrates this classifier into live measurement (Measurement GUI), device map overlays (Sample GUI), and plotting. Those GUI layers stay in Switchbox_GUI; this repo holds the **classifier + offline tools + docs**.

**Live repo:** https://github.com/Craig-Venables/memristive-iv-classifier

## License

Same as parent project (University of Nottingham research use). Add a LICENSE file when publishing to GitHub.

## Create GitHub remote (one-time)

When ready to push:

```powershell
cd memristive-iv-classifier
git init
git add .
git commit -m "Initial classification snapshot and documentation"
gh auth login
gh repo create memristive-iv-classifier --public --source=. --push
```

Or create the repo on GitHub manually and `git remote add origin ...`.
