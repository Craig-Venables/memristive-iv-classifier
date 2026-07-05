<#
.SYNOPSIS
    Patch analysis/__init__.py so core/API import without the plotting package.

    Run automatically after sync from Switchbox_GUI, or manually after copying analysis/.
#>
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path $PSScriptRoot -Parent
$InitFile = Join-Path $RepoRoot "analysis\__init__.py"

if (-not (Test-Path $InitFile)) {
    Write-Warning "analysis/__init__.py not found — skip patch"
    exit 0
}

$content = Get-Content $InitFile -Raw

$oldBlock = @'
# Aggregators (combine multiple units)
from .aggregators import DeviceAnalyzer, SectionAnalyzer, SampleAnalysisOrchestrator, ComprehensiveAnalyzer

# API (most commonly used)
from .api import IVSweepAnalyzer, IVSweepLLMAnalyzer, quick_analyze, analyze_sweep
'@

$newBlock = @'
# API (most commonly used)
from .api import IVSweepAnalyzer, IVSweepLLMAnalyzer, quick_analyze, analyze_sweep

# Aggregators require the plotting package (Switchbox_GUI only)
try:
    from .aggregators import (
        DeviceAnalyzer,
        SectionAnalyzer,
        SampleAnalysisOrchestrator,
        ComprehensiveAnalyzer,
    )
except ImportError:
    DeviceAnalyzer = None  # type: ignore[misc, assignment]
    SectionAnalyzer = None  # type: ignore[misc, assignment]
    SampleAnalysisOrchestrator = None  # type: ignore[misc, assignment]
    ComprehensiveAnalyzer = None  # type: ignore[misc, assignment]
'@

if ($content -match [regex]::Escape("# Aggregators require the plotting package")) {
    Write-Host "Standalone patch already applied."
    exit 0
}

if ($content -notmatch [regex]::Escape($oldBlock.Trim())) {
    Write-Warning "analysis/__init__.py layout changed — patch not applied. Edit manually."
    exit 1
}

$content = $content.Replace($oldBlock, $newBlock)

# Ensure API import order: core, then api, then aggregators try block
$coreBlock = "# Core analyzer (fundamental, no aggregation)`r`nfrom .core import SweepAnalyzer`r`n`r`n"
if ($content -notmatch "from \.core import SweepAnalyzer") {
    Write-Warning "Unexpected __init__.py structure"
    exit 1
}

Set-Content -Path $InitFile -Value $content -NoNewline
Write-Host "Applied standalone patch to analysis/__init__.py"
