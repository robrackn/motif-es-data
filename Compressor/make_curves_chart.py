import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SC = "/private/tmp/claude-501/-Users-richard-Developer-sysex-MotifEditorApp/62f30f13-0da7-4fc3-a41f-bb6173284061/scratchpad"
DESKTOP = "/Users/richard/Desktop"

def load(name):
    return json.load(open(f"{SC}/curve_{name}.json"))

BG = "#0d0d0f"; PANEL = "#141417"; GRID = "#2a2a30"; TEXT = "#e8e8ec"; MUTE = "#9a9aa4"

# Only the two settings that were dedicated attack/release tests (the
# batch's endpoint cases) -- "baseline_mid" held both fixed while varying
# threshold/ratio instead, so its curve shape isn't a clean third point
# along this range, just a noisier version of one of these two.
attack_series = [
    ("attack_fast", "Attack raw = 0 (fast)", 0, "#4dd0ff"),
    ("attack_slow", "Attack raw = 19 (slow)", 19, "#ff5c5c"),
]
release_series = [
    ("release_fast", "Release raw = 0 (fast)", 0, "#4dd0ff"),
    ("release_slow", "Release raw = 15 (slow)", 15, "#ff5c5c"),
]

fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), facecolor=BG)

def plot_family(ax, series, key, title, xmax):
    ax.set_facecolor(PANEL)
    ax.axvline(0, color="#555", linestyle=":", linewidth=1)
    for file_label, series_label, raw, color in series:
        d = load(file_label)
        curve = d.get(key)
        if not curve: continue
        # extract_curves.swift already windows samples relative to the
        # trace's own precomputed transition marker (t=0), not array start.
        pts = sorted((c["t"] * 1000, c["db"]) for c in curve)  # ms
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, linewidth=2.2, label=series_label)
    ax.set_title(title, color=TEXT, fontsize=13, fontweight="bold", loc="left")
    ax.set_xlabel("Time relative to transition onset (ms)", color=MUTE, fontsize=10)
    ax.set_ylabel("Gain reduction (dB)", color=MUTE, fontsize=10)
    ax.tick_params(colors=MUTE, labelsize=9)
    for s in ax.spines.values(): s.set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.6)
    leg = ax.legend(facecolor=PANEL, labelcolor=TEXT, fontsize=9.5, loc="best", framealpha=0.9)
    leg.get_frame().set_edgecolor(GRID)

plot_family(axes[0], attack_series, "attack", "Attack -- real measured gain-reduction curves", 250)
plot_family(axes[1], release_series, "release", "Release -- real measured gain-reduction curves", 800)

fig.suptitle("Compressor Attack/Release: actual curve shapes across the raw range (real Motif ES6 hardware, 2026-08-27)",
             color="white", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f"{DESKTOP}/compressor_attack_release_curves.jpg", dpi=150, facecolor=fig.get_facecolor())
print("wrote compressor_attack_release_curves.jpg")
