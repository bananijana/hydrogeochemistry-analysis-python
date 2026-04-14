"""
Geoscience Data Analysis Script
--------------------------------
Loads hydrogeochemical/geochemical dataset, performs:
  - Basic descriptive statistics
  - Outlier detection (IQR method)
  - Correlation matrix
  - Distribution plots (histograms)
  - Boxplots by group
  - Pairplot of major parameters
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────────────
DATA_PATH   = "dataset.csv"
OUTPUT_DIR  = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUMERIC_COLS = ["Ca", "Mg", "Na", "K", "HCO3", "Cl", "SO4",
                "NO3", "pH", "EC", "TDS", "TH", "Fe", "Mn"]
GROUP_COL    = "WaterType"
PALETTE      = {"Ca-HCO3": "#2196F3", "Ca-Cl": "#4CAF50",
                "Na-HCO3": "#FF9800", "Na-Cl": "#E91E63"}

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"Dataset loaded: {df.shape[0]} samples, {df.shape[1]} columns")
print(f"Water types: {df[GROUP_COL].value_counts().to_dict()}\n")

# ── 1. Descriptive Statistics ────────────────────────────────────────────────
stats_df = df[NUMERIC_COLS].describe().T
stats_df["CV%"] = (stats_df["std"] / stats_df["mean"] * 100).round(2)
stats_df = stats_df.round(3)
stats_df.to_csv(f"{OUTPUT_DIR}/descriptive_statistics.csv")
print("── Descriptive Statistics ──")
print(stats_df[["mean", "std", "min", "max", "CV%"]].to_string())
print()

# ── 2. Outlier Detection (IQR) ───────────────────────────────────────────────
print("── Outlier Detection (IQR method) ──")
outlier_report = {}
for col in NUMERIC_COLS:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    outlier_report[col] = len(outliers)
    if len(outliers) > 0:
        print(f"  {col:>6}: {len(outliers)} outlier(s)  "
              f"[bounds: {lower:.2f} – {upper:.2f}]")

outlier_series = pd.Series(outlier_report, name="outlier_count")
outlier_series.to_csv(f"{OUTPUT_DIR}/outlier_report.csv", header=True)
print()

# ── 3. Correlation Matrix ────────────────────────────────────────────────────
corr = df[NUMERIC_COLS].corr()

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(220, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
            annot=True, fmt=".2f", linewidths=0.4, ax=ax,
            annot_kws={"size": 7})
ax.set_title("Pearson Correlation Matrix – Hydrogeochemical Parameters",
             fontsize=13, pad=14, fontweight="bold")
plt.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/correlation_matrix.png", dpi=180)
plt.close()
print("Saved: correlation_matrix.png")

# ── 4. Histogram Grid ────────────────────────────────────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(16, 13))
axes = axes.flatten()
for i, col in enumerate(NUMERIC_COLS):
    ax = axes[i]
    ax.hist(df[col], bins=18, color="#1565C0", edgecolor="white",
            alpha=0.85, linewidth=0.5)
    ax.set_title(col, fontsize=10, fontweight="bold")
    ax.set_xlabel("mg/L" if col not in ["pH", "EC", "TH"] else
                  ("–" if col == "pH" else "µS/cm" if col == "EC" else "mg/L"),
                  fontsize=8)
    ax.set_ylabel("Frequency", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# hide unused
for j in range(len(NUMERIC_COLS), len(axes)):
    axes[j].set_visible(False)

fig.suptitle("Parameter Frequency Distributions", fontsize=14,
             fontweight="bold", y=1.01)
plt.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/histograms.png", dpi=180, bbox_inches="tight")
plt.close()
print("Saved: histograms.png")

# ── 5. Boxplots by Water Type ────────────────────────────────────────────────
selected = ["Ca", "Mg", "Na", "HCO3", "Cl", "SO4", "EC", "TDS"]
fig, axes = plt.subplots(2, 4, figsize=(18, 9))
axes = axes.flatten()
order = ["Ca-HCO3", "Ca-Cl", "Na-HCO3", "Na-Cl"]

for i, col in enumerate(selected):
    ax = axes[i]
    sns.boxplot(data=df, x=GROUP_COL, y=col, order=order,
                palette=PALETTE, ax=ax, linewidth=1.2,
                flierprops=dict(marker="o", markersize=4,
                                markerfacecolor="grey", alpha=0.6))
    ax.set_title(col, fontsize=11, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("mg/L" if col not in ["EC"] else "µS/cm", fontsize=9)
    ax.tick_params(axis="x", labelsize=8, rotation=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.suptitle("Parameter Distribution by Water Type", fontsize=14,
             fontweight="bold")
plt.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/boxplots_by_watertype.png", dpi=180,
            bbox_inches="tight")
plt.close()
print("Saved: boxplots_by_watertype.png")

# ── 6. Pairplot (key parameters) ─────────────────────────────────────────────
pair_cols = ["Ca", "Na", "HCO3", "Cl", "TDS", GROUP_COL]
pair_df   = df[pair_cols]
g = sns.pairplot(pair_df, hue=GROUP_COL, palette=PALETTE,
                 diag_kind="kde", plot_kws={"alpha": 0.65, "s": 35},
                 diag_kws={"fill": True, "alpha": 0.5})
g.figure.suptitle("Pairplot – Major Hydrogeochemical Parameters",
                  y=1.02, fontsize=13, fontweight="bold")
g.figure.savefig(f"{OUTPUT_DIR}/pairplot.png", dpi=160, bbox_inches="tight")
plt.close()
print("Saved: pairplot.png")

# ── 7. EC vs TDS scatter ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
for wt, grp in df.groupby(GROUP_COL):
    ax.scatter(grp["EC"], grp["TDS"], label=wt, color=PALETTE[wt],
               s=55, alpha=0.8, edgecolors="white", linewidths=0.4)

# regression line
slope, intercept, r, p, _ = stats.linregress(df["EC"], df["TDS"])
x_line = np.linspace(df["EC"].min(), df["EC"].max(), 100)
ax.plot(x_line, slope * x_line + intercept, "k--", linewidth=1.4,
        label=f"Regression  R²={r**2:.3f}")
ax.set_xlabel("EC (µS/cm)", fontsize=11)
ax.set_ylabel("TDS (mg/L)", fontsize=11)
ax.set_title("EC vs TDS – Water Type Classification", fontsize=12,
             fontweight="bold")
ax.legend(fontsize=9, framealpha=0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/EC_vs_TDS.png", dpi=180)
plt.close()
print("Saved: EC_vs_TDS.png")

print("\n✓ All outputs saved to:", OUTPUT_DIR)
