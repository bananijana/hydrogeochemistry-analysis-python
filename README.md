# hydrogeochemistry-analysis-python

A Python workflow for processing and visualising hydrogeochemical field data. Focused on water quality parameter analysis, statistical interpretation, and groundwater facies identification from multi-sample datasets.

---

## Overview

This repository implements a complete data analysis pipeline for hydrogeochemical datasets collected from groundwater monitoring programmes. It addresses common challenges in field data processing — including outlier screening, parameter correlation, and water type classification — using reproducible Python code.

Developed in the context of hydrogeological research on fluvial aquifer systems in West Bengal, India.

---

## What This Does

- Computes descriptive statistics for all water quality parameters including coefficient of variation
- Screens samples for anomalous values using the IQR method
- Generates a full Pearson correlation matrix to identify geochemical associations
- Plots parameter distributions to assess data normality and spread
- Compares parameter ranges across different hydrochemical water types
- Produces a pairplot to visualise inter-parameter relationships
- Validates the EC–TDS relationship through linear regression

---

## Project Structure

```
hydrogeochemistry-analysis-python/
│
├── dataset.csv          # Hydrogeochemical dataset (80 groundwater samples)
├── analysis.py          # Analysis and visualisation script
├── outputs/             # All generated figures and reports
│   ├── descriptive_statistics.csv
│   ├── outlier_report.csv
│   ├── correlation_matrix.png
│   ├── histograms.png
│   ├── boxplots_by_watertype.png
│   ├── pairplot.png
│   └── EC_vs_TDS.png
└── README.md
```

---

## Dataset Description

80 groundwater samples with 15 measured/derived parameters:

| Parameter Group | Variables |
|---|---|
| Major cations | Ca²⁺, Mg²⁺, Na⁺, K⁺ (mg/L) |
| Major anions | HCO₃⁻, Cl⁻, SO₄²⁻, NO₃⁻ (mg/L) |
| Field parameters | pH, EC (µS/cm), TDS (mg/L), Temperature (°C) |
| Derived index | Total Hardness – TH (mg/L as CaCO₃) |
| Trace elements | Fe, Mn (mg/L) |
| Water facies | Ca-HCO₃, Ca-Cl, Na-HCO₃, Na-Cl |

Water type classification follows the dominant cation–anion approach, reflecting the hydrochemical evolution from recharge to discharge zones.

---

## Dependencies

```
pandas
numpy
matplotlib
seaborn
scipy
```

```bash
pip install pandas numpy matplotlib seaborn scipy
```

---

## Running the Analysis

```bash
# Generate or prepare the input dataset
python dataset.py

# Execute the full analysis pipeline
python analysis.py
```

Figures and reports are written to `outputs/`.

---

## Key Outputs and Interpretation

**Correlation Matrix** — Identifies ion pairs with strong geochemical associations. EC–TDS correlation validates measurement consistency. Ca–TH coupling confirms carbonate hardness dominance in certain samples.

**Boxplots by Water Type** — Visualises how major ion concentrations vary between Ca-HCO₃, Ca-Cl, Na-HCO₃, and Na-Cl facies. Useful for identifying facies-specific contamination thresholds.

**Histogram Grid** — Reveals skewed distributions in Fe and Mn, consistent with redox-controlled trace metal behaviour in shallow alluvial aquifers.

**EC vs TDS** — The regression line and R² value provide a site-specific conversion factor for field estimation of TDS from portable EC meter readings.

---

## Research Context

This workflow was developed as part of dissertation fieldwork along the Hooghly–Rupnarayan river corridor, West Bengal, where shallow aquifer geochemistry is influenced by river–groundwater interaction, sediment lithology, and monsoon recharge dynamics. The analysis framework is generalisable to any multi-parameter groundwater dataset.

---

## Author

**Banani Jana**  
ORCID: https://orcid.org/0009-0007-0146-4535

---

## Citation
If you use this methodology or implementation logic in academic or technical work,
please cite this repository. A formal citation file and DOI will be provided
in subsequent releases.

DOI: https://doi.org/10.5281/zenodo.19563831

## License

MIT License
