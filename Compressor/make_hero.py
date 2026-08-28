import json, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

DATA = "/Users/richard/Developer/sysex/SonicLens/CalibrationData/Compressor"
DESKTOP = "/Users/richard/Desktop"

def load(name):
    return json.load(open(f"{DATA}/{name}.json"))

BG = "#0d0d0f"
PANEL = "#141417"
GRID = "#2a2a30"
TEXT = "#e8e8ec"
MUTE = "#9a9aa4"
RED = "#ff5c5c"
CYAN = "#4dd0ff"
GREEN = "#8bff6b"
ORANGE = "#ffb347"

fig = plt.figure(figsize=(14, 9), facecolor=BG)
gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[0.55, 3, 1.1], hspace=0.55, wspace=0.35,
                       left=0.06, right=0.96, top=0.93, bottom=0.07)

# ---- Title ----
title_ax = fig.add_subplot(gs[0, :]); title_ax.axis("off")
title_ax.text(0, 0.75, "COMPRESSOR MONTE CARLO", color=TEXT, fontsize=26, fontweight="bold",
              fontfamily="monospace", ha="left", va="center")
title_ax.text(0, 0.15, "Real Motif ES6 hardware measurement  ·  2026-08-27  ·  7 settings, 630 data points",
              color=MUTE, fontsize=13, ha="left", va="center")

# ---- Centerpiece: static transfer curves ----
ax = fig.add_subplot(gs[1, :2])
ax.set_facecolor(PANEL)
colors = {"heavy_limiting": RED, "gentle_glue": CYAN, "baseline_mid": GREEN}
labels = {"heavy_limiting": "Heavy limiting", "gentle_glue": "Gentle glue", "baseline_mid": "Baseline"}
for name, color in colors.items():
    d = load(name)
    pts = sorted((o["outputRMSDBFS"], o["inputRMSDBFS"]) for o in d["observations"]
                if o["testPoint"]["family"] == "staticTransfer" and o["testPoint"]["highLevelDBFS"] > -60)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, marker="o", markersize=4.5, linewidth=2.4, label=labels[name],
           solid_capstyle="round")
lims = [-65, -5]
ax.plot(lims, lims, color="#444", linestyle=":", linewidth=1.2, label="No compression")
ax.set_xlim(*lims); ax.set_ylim(*lims)
ax.set_title("What the compressor actually does to a signal", color=TEXT, fontsize=14, fontweight="bold", loc="left", pad=12)
ax.set_xlabel("Dry input level (dBFS)", color=MUTE, fontsize=10)
ax.set_ylabel("Captured output level (dBFS)", color=MUTE, fontsize=10)
ax.tick_params(colors=MUTE, labelsize=9)
for s in ax.spines.values(): s.set_color(GRID)
ax.grid(True, color=GRID, linewidth=0.6)
leg = ax.legend(facecolor=PANEL, labelcolor=TEXT, fontsize=9.5, loc="upper left", framealpha=0.9)
leg.get_frame().set_edgecolor(GRID)

# ---- Side: attack/release before/after ----
ax2 = fig.add_subplot(gs[1, 2])
ax2.set_facecolor(PANEL)
ax2.axis("off")
ax2.set_title("GUI formulas: guessed vs. measured", color=TEXT, fontsize=13, fontweight="bold", loc="left", pad=12)

rows = [
    ("Attack, fast", "1 ms", "13.0 ms", 13.0/1.0),
    ("Attack, slow", "40 ms", "66.9 ms", 66.9/40.0),
    ("Release, fast", "10 ms", "9.8 ms", 9.8/10.0),
    ("Release, slow", "680 ms", "50.8 ms", 50.8/680.0),
]
y = 0.9
for label, old, new, ratio in rows:
    ax2.text(0.0, y, label, color=MUTE, fontsize=10.5, transform=ax2.transAxes, va="center")
    ax2.text(0.0, y - 0.075, f"guessed {old}", color="#777", fontsize=9.5, transform=ax2.transAxes, va="center")
    arrow_color = RED if ratio > 1.3 or ratio < 0.7 else GREEN
    ax2.text(0.62, y - 0.075, f"→  {new}", color=arrow_color, fontsize=11, fontweight="bold",
             transform=ax2.transAxes, va="center")
    y -= 0.23

ax2.text(0.0, 0.02, "Release's slow end was guessed 13x too long.", color=ORANGE, fontsize=9,
         transform=ax2.transAxes, va="bottom", style="italic")

# ---- Bottom strip: stereo discovery + provenance ----
ax3 = fig.add_subplot(gs[2, :]); ax3.axis("off")
ax3.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax3.transAxes, facecolor=PANEL, edgecolor=GRID, linewidth=1))

stats = [
    ("NEW THIS SESSION", "Stereo width\nmeasurement", MUTE, TEXT),
    ("MID rate", "7.52 Hz", MUTE, CYAN),
    ("WIDTH rate", "12.60 Hz", MUTE, ORANGE),
    ("WIDTH depth", "13.83 dB", MUTE, ORANGE),
    ("Correlation", "+0.57", MUTE, TEXT),
]
n = len(stats)
for i, (label, value, lc, vc) in enumerate(stats):
    x = 0.03 + i * (0.94 / (n - 1)) if i > 0 else 0.03
    x = 0.02 + i * 0.23
    ax3.text(x, 0.68, label, color=lc, fontsize=9.5, transform=ax3.transAxes, ha="left", va="center")
    ax3.text(x, 0.32, value, color=vc, fontsize=15 if i > 0 else 12, fontweight="bold",
            transform=ax3.transAxes, ha="left", va="center",
            fontfamily="monospace" if i > 0 else None)

fig.text(0.5, 0.012, "Measured live on a Symphonic chorus (LFO Speed=60, Depth=100) via SonicLens's Live Effects monitor  ·  motifeditor repo, branch Modern",
         color="#666", fontsize=8.5, ha="center")

fig.savefig(f"{DESKTOP}/hero_2026-08-27.jpg", dpi=160, facecolor=fig.get_facecolor())
print("wrote hero_2026-08-27.jpg")
