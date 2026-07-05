# Data formats

## Raw IV sweep `.txt`

Tab- or space-separated columns with header row:

```
Voltage Current Time
0.000E+00    -3.261E-11    0.000E+00
...
```

Read by `read_data_file()` in `analysis/core/sweep_analyzer.py`.

---

## Device tracking JSON

**Path (canonical):**

```
{sample}/sample_analysis/analysis/device_tracking/{device_id}_history.json
```

**Device ID:** `{sample_name}_{section}_{number}` — e.g. `D94_G_12`

**Schema:**

```json
{
  "device_id": "D94_G_12",
  "created": "2026-01-15T10:30:00",
  "last_updated": "2026-01-20T14:22:00",
  "total_measurements": 3,
  "measurements": [
    {
      "timestamp": "2026-01-20T14:22:00",
      "cycle_number": 3,
      "classification": {
        "device_type": "memristive",
        "confidence": 0.85,
        "memristivity_score": 72.5,
        "forming_stage": "formed_memristive",
        "yield_bucket": "...",
        "conduction_mechanism": "..."
      },
      "resistance": {
        "ron_mean": 1.2e3,
        "roff_mean": 5.0e4,
        "switching_ratio": 41.7,
        "on_off_ratio": 41.7
      },
      "voltage": { "von_mean": 0.5, "voff_mean": -0.5, "max_voltage": 1.0 },
      "hysteresis": { "has_hysteresis": true, "pinched": true, "normalized_area": 0.12 },
      "quality": { "memory_window_quality": 0.8, "stability": 0.9 },
      "warnings": []
    }
  ]
}
```

**Notes:**

- Writer uses `"measurements"`; some readers also accept `"all_measurements"`.
- Appended on each classified sweep when `device_id` and `save_directory` are passed to `quick_analyze`.

---

## classification_log.txt

**Path:** `{sample}/{section}/{device_num}/classification_log.txt`

Human-readable append-only log written by **Measurement GUI** (not the analysis package). Includes device type, confidence, memristivity score, score breakdown, warnings.

Companion file: `classification_summary.txt` — one line per sweep for quick scanning.

---

## Extended analysis report

When Extended mode is on in Measurement GUI:

```
{sample}/sample_analysis/analysis/sweeps/{device_id}/{filename}_analysis.txt
```

Also per-device:

```
{sample}/{section}/{device_num}/sweep_analysis/{filename}_research.json
```

---

## Yield manifest

**Path:** `{sample}/sample_analysis/yield_analysis/yield_manifest.json`

Built from tracking history or manual Excel `{sample_name}.xlsx`. See Switchbox_GUI `yield_source.py`.

---

## Batch consolidation outputs

Produced by `tools/data_consolidation/batch_classify.py`:

| File | Content |
|------|---------|
| `classification_results.json` | Full records + nested `analysis.classification` |
| `classification_results.csv` | Flattened rows; sort by `review_priority`, `confidence` |
| `classification_summary.txt` | Type distribution statistics |
| `device_yield_summary.json` | Per-device yield tiers |
| `review_corrections.json` | Manual label overrides (survives re-runs) |

Consolidated input naming (from `consolidate.py`):

```
D94-A-1-1-FS-0.5v-0.05sv-0.05sd-Py-St_v2_led-3.txt
│   │ │  └── original filename
│   │ └───── device number
│   └─────── section letter
└─────────── sample id (Dxx)
```

---

## quick_analyze return dict (top-level keys)

| Key | Description |
|-----|-------------|
| `device_info` | Metadata, device name |
| `classification` | `device_type`, `memristivity_score`, `confidence`, `forming_stage`, ... |
| `resistance_metrics` | Ron, Roff, ratios |
| `voltage_metrics` | Von, Voff, max voltage |
| `hysteresis_metrics` | Area, pinched flag |
| `performance_metrics` | Quality scores |
| `summary_stats` | Aggregated stats |
| `research_diagnostics` | Present when `analysis_level='research'` |
