# Motif ES Compressor Dynamics

Real hardware measurements of the Song A/D Insertion Compressor on a 2003
Yamaha Motif ES physical synthesizer workstation: attack/release timing,
static transfer (threshold/ratio) behavior, and the actual time-domain
gain-reduction envelope shape, all captured from a live loopback (a
generated test signal driven through the Motif's Compressor and captured
back), not simulated or datasheet-derived.

## 📦 Dataset Specifications
* **Hardware Source:** Yamaha Motif ES6 Physical Unit (Song A/D Insertion effect)
* **Settings Captured:** 7 representative Attack/Release/Threshold/Ratio combinations
* **Points per Setting:** 90 (static transfer sweep + attack/release dynamics + frequency sensitivity + harmonics + program dependency)
* **File Format:** `.json`

## 🖼️ What's here
* `hero_2026-08-27.jpg` -- single-image summary of the session's findings.
* `compressor_attack_release_calibration.jpg` -- measured Attack/Release
  time (ms) vs. raw knob value (0-19 / 0-15), endpoints plus mid-range
  cross-check points.
* `compressor_static_transfer.jpg` -- real input-vs-output level curves
  for three Threshold/Ratio settings, showing the actual compression knee.
* `compressor_attack_release_curves.jpg` -- the real time-domain
  gain-reduction envelope shape itself (not just the summary ms numbers)
  for the fastest and slowest Attack/Release settings. Fast settings show
  a real overshoot spike at the transition before settling to a lower
  steady value; slow settings rise smoothly with no overshoot.
* `*.json` -- one file per hardware setting (`attack_fast`, `attack_slow`,
  `release_fast`, `release_slow`, `heavy_limiting`, `gentle_glue`,
  `baseline_mid`), each holding per-point measurements (input/output
  level, clipping, and where applicable fitted attack/release curve
  parameters -- delay, rise-time percentiles, exponential time constant
  and fit quality, transient peaks, overshoot, settling time). Raw
  per-sample audio traces are not included (100-300MB per setting); these
  files hold the derived measurements.
* `curve_extracts/` -- the actual per-sample gain-reduction envelope
  (time, dB) for the points used in `compressor_attack_release_curves.jpg`,
  pulled from the raw traces via `extract_curves.swift`.
* `compressor_batch_plan.json` / `batch-status.log` -- the plan that was
  run and its full execution log, for reproducibility.
* `make_charts.py` / `make_hero.py` / `make_curves_chart.py` /
  `extract_curves.swift` -- the scripts that generated the images above
  from the JSON data (Python: `pip3 install matplotlib`; the Swift script
  needs `swiftc -O extract_curves.swift -o extract_curves`).

## 🔍 Headline numbers

Measured Attack/Release time (median 63%-rise time across each setting's
observation points):

| raw | Attack (ms) | raw | Release (ms) |
|----:|-------------:|----:|--------------:|
| 0   | 13.00        | 0   | 9.75          |
| 19  | 66.86        | 15  | 50.84         |

These aren't a clean linear relationship end to end -- mid-range points
(raw=9 Attack, raw=7 Release, held fixed while the other parameter was
swept) came in below a straight line on Attack and above it on Release.

## ⚖️ License

Same as the rest of this repository -- CC0 1.0 Universal, public domain.
