import json, os, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Run from this directory (or anywhere -- paths are relative to this file).
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DESKTOP = OUT_DIR  # write charts alongside the data by default

def load(name):
    return json.load(open(f"{OUT_DIR}/{name}.json"))

def median_t632(obs, key):
    vals = [o[key]["t632"] for o in obs if o.get(key) and o[key].get("t632") is not None]
    return statistics.median(vals) if vals else None

cases = {
    "attack_fast":   dict(attackRaw=0,  releaseRaw=7),
    "attack_slow":   dict(attackRaw=19, releaseRaw=7),
    "release_fast":  dict(attackRaw=9,  releaseRaw=0),
    "release_slow":  dict(attackRaw=9,  releaseRaw=15),
    "heavy_limiting":dict(attackRaw=9,  releaseRaw=7),
    "gentle_glue":   dict(attackRaw=9,  releaseRaw=7),
    "baseline_mid":  dict(attackRaw=9,  releaseRaw=7),
}

attack_points, release_points = [], []
for name, meta in cases.items():
    d = load(name)
    obs = d["observations"]
    a = median_t632(obs, "attack")
    r = median_t632(obs, "release")
    if a is not None: attack_points.append((meta["attackRaw"], a * 1000, name))
    if r is not None: release_points.append((meta["releaseRaw"], r * 1000, name))

# ---------------------------------------------------------------
# Chart 1: Attack/Release calibration -- old guess vs new calibration vs real data
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), facecolor="#1a1a1a")

def style_axis(ax, title, xlabel):
    ax.set_facecolor("#111111")
    ax.set_title(title, color="white", fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel, color="#cccccc")
    ax.set_ylabel("Time (ms)", color="#cccccc")
    ax.tick_params(colors="#cccccc")
    for spine in ax.spines.values(): spine.set_color("#444444")
    ax.grid(True, color="#333333", linewidth=0.6)

ax = axes[0]
style_axis(ax, "Compressor Attack", "Attack raw (0-19)")
xs = list(range(20))
old = [1.0 + x/19*39.0 for x in xs]
new = [13.00 + x/19*53.86 for x in xs]
ax.plot(xs, old, color="#888888", linestyle="--", label="old guessed formula")
ax.plot(xs, new, color="#4dd0ff", linewidth=2.2, label="new calibrated formula")
for raw, ms, name in attack_points:
    endpoint = raw in (0, 19)
    lbl = "measured endpoint (used for calibration)" if endpoint and raw == 0 else \
          ("measured cross-check (raw=9, held fixed elsewhere)" if not endpoint and raw == 9 and name == "release_fast" else None)
    ax.scatter([raw], [ms], color="#ff9f40" if not endpoint else "#4dd0ff",
              s=90 if endpoint else 55, zorder=5,
              edgecolor="white", linewidth=0.8, label=lbl)
    ax.annotate(name, (raw, ms), color="#dddddd", fontsize=7, xytext=(4, 4), textcoords="offset points")
ax.legend(facecolor="#1a1a1a", labelcolor="white", fontsize=8, loc="upper left")

ax = axes[1]
style_axis(ax, "Compressor Release", "Release raw (0-15)")
xs = list(range(16))
old = [10.0 + x/15*670.0 for x in xs]
new = [9.75 + x/15*41.09 for x in xs]
ax.plot(xs, old, color="#888888", linestyle="--", label="old guessed formula (goes to 680ms)")
ax.plot(xs, new, color="#4dd0ff", linewidth=2.2, label="new calibrated formula")
for raw, ms, name in release_points:
    endpoint = raw in (0, 15)
    ax.scatter([raw], [ms], color="#ff9f40" if not endpoint else "#4dd0ff",
              s=90 if endpoint else 55, zorder=5,
              edgecolor="white", linewidth=0.8)
    ax.annotate(name, (raw, ms), color="#dddddd", fontsize=7, xytext=(4, 4), textcoords="offset points")
ax.set_ylim(0, 100)  # old formula's 680ms would dwarf everything else -- zoom to where the real data lives
ax.legend(facecolor="#1a1a1a", labelcolor="white", fontsize=8, loc="upper left")

fig.suptitle("Compressor Attack/Release: guessed formula vs. real Motif ES6 hardware measurement (2026-08-27)",
             color="white", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f"{DESKTOP}/compressor_attack_release_calibration.jpg", dpi=150, facecolor=fig.get_facecolor())
print("wrote compressor_attack_release_calibration.jpg")

# ---------------------------------------------------------------
# Chart 2: Static transfer curves (real measured input vs output level)
# ---------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(8, 8), facecolor="#1a1a1a")
ax2.set_facecolor("#111111")
ax2.set_title("Compressor static transfer -- real hardware measurement", color="white", fontsize=13, fontweight="bold")
ax2.set_xlabel("Dry input level (dBFS, pre-hardware)", color="#cccccc")
ax2.set_ylabel("Captured output level (dBFS, post-hardware)", color="#cccccc")
ax2.tick_params(colors="#cccccc")
for spine in ax2.spines.values(): spine.set_color("#444444")
ax2.grid(True, color="#333333", linewidth=0.6)

colors = {"heavy_limiting": "#ff5050", "gentle_glue": "#4dd0ff", "baseline_mid": "#8bff6b"}
labels = {"heavy_limiting": "heavy_limiting (Threshold=20, Ratio=7 raw)",
          "gentle_glue": "gentle_glue (Threshold=100, Ratio=0 raw)",
          "baseline_mid": "baseline_mid (Threshold=60, Ratio=4 raw)"}
for name, color in colors.items():
    d = load(name)
    pts = sorted((o["outputRMSDBFS"], o["inputRMSDBFS"]) for o in d["observations"]
                if o["testPoint"]["family"] == "staticTransfer" and o["testPoint"]["highLevelDBFS"] > -60)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax2.plot(xs, ys, color=color, marker="o", markersize=4, linewidth=1.8, label=labels[name])

lims = [-65, -5]
ax2.plot(lims, lims, color="#666666", linestyle=":", linewidth=1, label="1:1 (no compression)")
ax2.set_xlim(*lims); ax2.set_ylim(*lims)
ax2.legend(facecolor="#1a1a1a", labelcolor="white", fontsize=8, loc="upper left")
fig2.tight_layout()
fig2.savefig(f"{DESKTOP}/compressor_static_transfer.jpg", dpi=150, facecolor=fig2.get_facecolor())
print("wrote compressor_static_transfer.jpg")
