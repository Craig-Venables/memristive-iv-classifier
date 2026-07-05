# Classification rules

Rule-based classification runs inside `SweepAnalyzer._classify_device()` and `_extract_classification_features()`. There is no separate ML model in the default pipeline.

## Device types

| Type | Typical I–V behaviour |
|------|------------------------|
| `memristive` | Pinched hysteresis, switching, memory window |
| `memcapacitive` | Hysteresis with capacitive character (often grouped with memristive for yield) |
| `ohmic` | Approximately linear I–V through origin |
| `rectifying` | Strong polarity dependence, diode-like |
| `forming_rectifying` | Rectifying during forming; may evolve toward memristive |
| `non_conductive` | Very low current / open |
| `capacitive` | Charge storage dominated |
| `conductive` | High conduction without clear switching |
| `uncertain` | Ambiguous or low confidence |

## When classification runs

| Condition | Classification? |
|-----------|-----------------|
| `analysis_level='basic'` | **No** — metrics only |
| `analysis_level='classification'`, `'full'`, `'research'` | **Yes** |
| Pulse measurement with time array | **No** — pulse metrics only |

Live measurement uses `analysis_level='classification'`.

## Memristivity score (0–100)

A weighted score from IV features, including:

- Pinched hysteresis presence and quality
- Switching behaviour (on/off ratio, loop separation)
- Memory window quality
- Hysteresis area and shape
- Polarity dependence

Default memristive threshold: **score ≥ 60** (used by yield and Sample GUI overlay after ≥ 2 sweeps).

Score breakdown is returned in the result dict under `classification` (sub-scores vary by analyzer version).

## Forming stage

Returned as `forming_stage` in classification output, e.g.:

- `unformed`
- `forming`
- `formed_memristive`
- `formed_rectifying`

Used for yield heuristics (`formed_rectifying` may count as promising in overlay logic).

## Confidence

`confidence` (0–1) reflects how clearly the sweep matches the assigned type vs alternatives.

Low confidence sweeps are flagged in batch review (`review_priority` in CSV).

## Yield vs map overlay (important distinction)

These use **different rules** on purpose:

| Context | Memristive rule |
|---------|-----------------|
| **Chip yield** (`yield_source._auto_classify`) | **Ever** memristive or `formed_rectifying` in any sweep |
| **Sample GUI map** (`summarize_device_from_history`) | **Best** memristivity score ≥ 60, only after **≥ 2 sweeps**; 1 sweep = **pending** (gray) |

Do not assume yield count equals map memristive count.

## Tuning weights

Use `tools/classification_validation/` to:

- Label ground-truth sweeps
- Adjust feature weights and thresholds
- Measure accuracy and confusion matrix

Custom weights can be passed to `quick_analyze(..., custom_weights={...})` when supported by the analyzer version in this snapshot.

## Promising devices (overlay summary)

A device is **promising** (not memristive) when:

- Latest type is `rectifying` or `memcapacitive`, **or**
- Best memristivity score is in **40–59** (forming candidate)

Used for the “Promising” count in Sample GUI summary strip.

## References in code

- Classification logic: `analysis/core/sweep_analyzer.py`
- Overlay summarization: Switchbox_GUI `gui/measurement_gui/yield_concentration/yield_source.py` → `summarize_device_from_history()`
- Enhanced classification notes: `analysis/docs/ENHANCED_CLASSIFICATION_README.md` (in snapshot)
