# DecodeLabs — Project 2: Exploratory Data Analysis (EDA)

Exploratory analysis of a 1,200-row e-commerce order dataset — uncovering distribution shape, outliers, correlations, and business-relevant trends before any dashboarding or modeling work begins.

> Data Analytics Internship · Project 2 · DecodeLabs · Batch 2026

---

## 📌 Problem Statement

DecodeLabs runs an e-commerce operation across 7 product lines. Leadership needs to know which products, payment methods, and channels actually drive revenue — and how much of the order pipeline is being lost to cancellations and returns.

## 🗂️ Dataset

| | |
|---|---|
| **Source file** | `DecodeLabs_Project1_Cleaned_Dataset.xlsx` |
| **Rows × Columns** | 1,200 × 14 |
| **Period covered** | Jan 2023 – Jun 2025 |
| **Missing values** | 0 (verified) |
| **Duplicate rows** | 0 (verified) |

Key fields: `Product`, `Quantity`, `UnitPrice`, `TotalPrice`, `PaymentMethod`, `OrderStatus`, `CouponCode`, `ReferralSource`, `Date`.

## 🛠️ Tools & Libraries:

- **Python 3** — pandas, numpy for analysis
- **Matplotlib** — charting
- **openpyxl** — reading `.xlsx` files

## 📊 Methodology:

1. **Data profiling** — shape, dtypes, missing-value and duplicate checks, reconciliation of `TotalPrice = Quantity × UnitPrice`.
2. **Descriptive statistics** — five-number summary (min, Q1, median, Q3, max) for every numeric field.
3. **Distribution analysis** — skewness check to decide mean vs. median as the honest summary statistic.
4. **Outlier detection** — cross-validated with two methods: IQR (1.5×IQR rule) and Z-score (|z| > 3).
5. **Correlation analysis** — Pearson r across all numeric fields, with an explicit correlation ≠ causation check.
6. **Business aggregation** — revenue and order counts grouped by product, year/month, payment method, order status, coupon code, and referral source.

## 🔑 Key Findings:

- **TotalPrice is right-skewed** (skew = 0.89) — median (₹823.62) is a more honest "typical order" figure than mean (₹1,053.97).
- **41.4% of all orders** end in *Cancelled* or *Returned* status, representing ~₹519,674 in unrealized/reversed revenue — and these lost orders skew *above* average value, not below.
- **UnitPrice (r = 0.72)** is a stronger driver of order value than Quantity (r = 0.62).
- **Revenue is well diversified** — no single product exceeds 15.5% of total revenue.
- **8 orders flagged by IQR** as statistically extreme were confirmed **not** to be data errors by the stricter Z-score test (0 flags) — treated as legitimate high-value orders, not removed.

## 🖼️ Visuals:

| Chart | What it shows |
|---|---|
| `charts/distribution.png` | Histogram of order value with mean/median markers — visualizes the right skew |
| `charts/boxplot.png` | Order value spread by product, with outliers marked |
| `charts/correlation.png` | Pearson correlation heatmap across numeric fields |
| `charts/trend.png` | Monthly revenue trend, Jan 2023–Jun 2025 |
| `charts/visual_evidence_slide.png` | Before/after chart-design comparison (noisy 3D pie → clean insight bar) |

## 📁 Repository Structure:

```
decodelabs-project2-eda/
├── README.md
├── data/
│   └── DecodeLabs_Project1_Cleaned_Dataset.xlsx
├── eda_analysis.py
├── charts/
│   ├── distribution.png
│   ├── boxplot.png
│   ├── correlation.png
│   ├── trend.png
│   └── visual_evidence_slide.png
└── DecodeLabs_Project2_EDA_Report.html
```

## ▶️ How to Run:

```bash
pip install pandas numpy matplotlib openpyxl
python eda_analysis.py
```

This reads the Excel file, prints every statistic to the terminal, and saves all chart images into the project folder.

## 📝 Recommendations:

1. Investigate the Cancelled/Returned segment first — the largest single revenue leak.
2. Report order value using **median**, not mean, given the skew.
3. Build a VIP/bulk-order outreach list from the 8 confirmed-legitimate high-value outliers.
4. Protect channel diversification (payment methods, referral sources) rather than consolidating around the current leaders.
5. Re-run this analysis quarterly as new data lands — 2025 in this dataset is only a partial year.

---

*Built as part of the DecodeLabs Data Analytics Industrial Training Kit, Project 2 (Exploratory Data Analysis).*
