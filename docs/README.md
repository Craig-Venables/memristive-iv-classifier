# Classification system — start here

This documentation describes the IV classification pipeline extracted from Switchbox_GUI. Read these pages in order if you are new to the system.

## 5-minute overview

1. **Input:** Voltage and current arrays from an IV sweep (live measurement or `.txt` file).
2. **Engine:** `SweepAnalyzer` splits loops, computes Ron/Roff/hysteresis, scores memristivity, assigns a device type.
3. **API:** `quick_analyze()` wraps the engine and returns a structured dict.
4. **Persistence:** When `device_id` and `save_directory` are passed, results append to `{sample}/sample_analysis/analysis/device_tracking/{device_id}_history.json`.
5. **Display:** Switchbox_GUI Sample GUI reads that JSON for map colors; batch tools write CSV/JSON for review.

## Document index

| Doc | Question it answers |
|-----|---------------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | How do the modules fit together? |
| [CLASSIFICATION_RULES.md](CLASSIFICATION_RULES.md) | What is memristive vs ohmic? How is the score computed? |
| [OVERLAY_RULES.md](OVERLAY_RULES.md) | How does the device map decide green vs gray vs blue? |
| [DATA_FORMATS.md](DATA_FORMATS.md) | What do the JSON and log files look like? |
| [API.md](API.md) | How do I call `quick_analyze` from Python? |
| [BATCH_WORKFLOW.md](BATCH_WORKFLOW.md) | How do I batch-classify a whole dataset? |
| [SYNC_WITH_SWITCHBOX.md](SYNC_WITH_SWITCHBOX.md) | How do I refresh this repo after editing Switchbox_GUI? |

## Analysis levels

| Level | Classification | Typical use |
|-------|----------------|-------------|
| `basic` | No | Metrics only (Ron, Roff, areas) |
| `classification` | Yes | Live measurement, batch classify, map overlay |
| `full` | Yes | + conduction models, extended metrics |
| `research` | Yes | + deep diagnostics (NDR, loop similarity) |

Live measurement in Switchbox_GUI uses `classification` for speed. Batch tools use `classification`. Retroactive full-sample work may use `full` or `research`.

## What is not in this repo

- Tkinter / PyQt GUIs (Switchbox_GUI)
- Hardware drivers, multiplexer, plotting aggregators
- Nottingham OneDrive save-path defaults

See Switchbox_GUI `gui/measurement_gui/` and `gui/sample_gui/classification_overlay.py` for integration details.
