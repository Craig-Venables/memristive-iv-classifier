# API reference

## Import

Run from repo root (or add repo root to `PYTHONPATH`):

```python
from analysis import quick_analyze, analyze_sweep, IVSweepAnalyzer, SweepAnalyzer
from analysis.core.sweep_analyzer import read_data_file
```

**Note:** `ComprehensiveAnalyzer` and other aggregators require the `plotting` package from Switchbox_GUI and are not available in this standalone repo unless you install plotting separately.

## quick_analyze

Primary entry point for one sweep.

```python
result = quick_analyze(
    voltage=v_arr,           # array-like, volts
    current=i_arr,           # array-like, amps
    time=t_arr,              # optional
    metadata={"device_name": "D94_A_1"},
    analysis_level="classification",  # basic | classification | full | research
    device_id="D94_A_1",
    save_directory=r"C:\...\Data_folder\D94",
    cycle_number=2,
)
```

### Common kwargs

| Parameter | Description |
|-----------|-------------|
| `analysis_level` | Depth of analysis (see docs/README.md) |
| `device_id` | Tracking ID `{sample}_{section}_{num}` |
| `save_directory` | Sample root folder for tracking JSON |
| `cycle_number` | Sweep index on device |
| `metadata` | Extra fields stored with measurement |
| `custom_weights` | Override classification weights (if supported) |
| `file_path` | Source file path for metadata |

### Classification block

```python
clf = result["classification"]
clf["device_type"]           # e.g. "memristive"
clf["memristivity_score"]    # 0–100
clf["confidence"]            # 0–1
clf["forming_stage"]         # e.g. "formed_memristive"
```

## analyze_sweep

Same as `quick_analyze` but can load from file:

```python
from analysis import analyze_sweep

result = analyze_sweep(
    file_path="sweep.txt",
    analysis_level="classification",
)
```

## IVSweepAnalyzer

Class-based API for repeated use:

```python
from analysis import IVSweepAnalyzer

analyzer = IVSweepAnalyzer(analysis_level="full")
result = analyzer.analyze_sweep(voltage=v, current=i)
```

## read_data_file

Load `.txt` sweep without classifying:

```python
from analysis.core.sweep_analyzer import read_data_file

data = read_data_file("path/to/sweep.txt")
# returns dict with voltage, current, time arrays
```

## SweepAnalyzer (direct)

Lower-level access:

```python
from analysis import SweepAnalyzer

sa = SweepAnalyzer(
    voltage=v,
    current=i,
    analysis_level="classification",
    device_id="D94_A_1",
    save_directory=r"C:\...\D94",
    cycle_number=1,
)
result = sa.analyze()
```

## Device tracking side effect

Tracking JSON is written inside `SweepAnalyzer` when **both** `device_id` and `save_directory` are set and classification runs. Path:

```
{save_directory}/sample_analysis/analysis/device_tracking/{device_id}_history.json
```

## Batch classify

See [BATCH_WORKFLOW.md](BATCH_WORKFLOW.md). CLI:

```bash
python tools/data_consolidation/batch_classify.py
```

Uses `quick_analyze(..., analysis_level='classification')` internally.

## Errors

- Empty or mismatched V/I arrays: analysis skipped (returns empty or raises depending on caller)
- Missing loops: may classify as `uncertain` or `non_conductive` with warnings in result

## Optional LLM layer

`IVSweepLLMAnalyzer` in `analysis/api/iv_sweep_llm_analyzer.py` adds LLM commentary. Requires separate backends (Ollama, llama-cpp, transformers). Not used in live measurement.
