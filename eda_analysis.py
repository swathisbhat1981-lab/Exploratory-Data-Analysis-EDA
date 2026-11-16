"""
DecodeLabs — Project 2: Exploratory Data Analysis (EDA)
Dataset: DecodeLabs_Project1_Cleaned_Dataset.xlsx
Every operation below is exactly what was run to produce the report figures
and tables (DecodeLabs_Project2_EDA_Report.html).
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# 1. LOAD & PROFILE
# --------------------------------------------------------------------------
df = pd.read_excel('DecodeLabs_Project1_Cleaned_Dataset.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['YearMonth'] = df['Date'].dt.to_period('M')

print(df.shape)                                   # (1200, 14)
print(df.dtypes)
print("Missing values:", df.isna().sum().sum())    # 0
print("Duplicate rows:", df.duplicated().sum())     # 0
print("Duplicate OrderIDs:", df['OrderID'].duplicated().sum())  # 0

# Sanity check: TotalPrice should equal Quantity * UnitPrice
calc = (df['Quantity'] * df['UnitPrice']).round(2)
diff = (df['TotalPrice'] - calc).abs()
print("Max reconciliation diff:", diff.max())       # ~0 (floating point noise only)

# --------------------------------------------------------------------------
# 2. DESCRIPTIVE STATISTICS (Five-Number Summary)
# --------------------------------------------------------------------------
numeric_cols = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']
print(df[numeric_cols].describe().round(2))

# --------------------------------------------------------------------------
# 3. DISTRIBUTION / SKEWNESS
# --------------------------------------------------------------------------
for col in numeric_cols:
    print(col, "skew:", round(df[col].skew(), 3))

# --------------------------------------------------------------------------
# 4. OUTLIER DETECTION — IQR METHOD
# --------------------------------------------------------------------------
for col in numeric_cols:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lo, hi = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = df[(df[col] < lo) | (df[col] > hi)]
    print(f"{col}: bounds=({lo:.2f},{hi:.2f}) "
          f"outliers={len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

# --------------------------------------------------------------------------
# 5. OUTLIER DETECTION — Z-SCORE METHOD
# --------------------------------------------------------------------------
z = (df['TotalPrice'] - df['TotalPrice'].mean()) / df['TotalPrice'].std()
print("TotalPrice |z| > 3 count:", (z.abs() > 3).sum())   # 0

# --------------------------------------------------------------------------
# 6. CORRELATION ANALYSIS
# --------------------------------------------------------------------------
corr = df[numeric_cols].corr()
print(corr.round(3))

# --------------------------------------------------------------------------
# 7. BUSINESS AGGREGATIONS
# --------------------------------------------------------------------------
# Revenue by product
prod = (df.groupby('Product')['TotalPrice']
          .agg(['sum', 'count', 'mean']).round(2)
          .sort_values('sum', ascending=False))
prod['share_pct'] = (prod['sum'] / prod['sum'].sum() * 100).round(2)
print(prod)

# Revenue by year
print(df.groupby('Year')['TotalPrice'].agg(['sum', 'count', 'mean']).round(2))

# Monthly revenue trend
monthly = df.groupby('YearMonth')['TotalPrice'].sum()
print(monthly)

# Average order value by payment method
print(df.groupby('PaymentMethod')['TotalPrice']
        .agg(['mean', 'count']).round(2)
        .sort_values('mean', ascending=False))

# Order status: volume vs revenue impact
status = df.groupby('OrderStatus').agg(
    count=('OrderID', 'count'),
    revenue=('TotalPrice', 'sum'),
    avg=('TotalPrice', 'mean')
).round(2)
print(status.sort_values('count', ascending=False))
print("Cancelled+Returned %:",
      round(df['OrderStatus'].isin(['Cancelled', 'Returned']).mean() * 100, 2))

# Coupon effectiveness
print(df.groupby('CouponCode')['TotalPrice'].agg(['mean', 'count']).round(2))

# Referral source revenue
print(df.groupby('ReferralSource')['TotalPrice']
        .agg(['sum', 'count', 'mean']).round(2)
        .sort_values('sum', ascending=False))

# --------------------------------------------------------------------------
# 8. CHARTS (dark / cyan brand style matching the training-kit deck)
# --------------------------------------------------------------------------
BG, CYAN, RED, WHITE, GRID, GREY = (
    "#0b0f14", "#22d3ee", "#f43f5e", "#e6edf3", "#1f2937", "#3a4a5a"
)
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": WHITE, "axes.labelcolor": WHITE,
    "xtick.color": WHITE, "ytick.color": WHITE,
    "axes.edgecolor": GRID, "grid.color": GRID,
    "font.family": "monospace", "font.size": 11,
})

# Distribution histogram
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df['TotalPrice'], bins=30, color=CYAN, alpha=0.85, edgecolor=BG)
ax.axvline(df['TotalPrice'].mean(), color=RED, ls='--', lw=2, label='Mean')
ax.axvline(df['TotalPrice'].median(), color='white', lw=2, label='Median')
ax.legend()
plt.tight_layout()
plt.savefig('distribution.png', dpi=150)
plt.close()

# Boxplot by product
fig, ax = plt.subplots(figsize=(8, 4.3))
order = df.groupby('Product')['TotalPrice'].median().sort_values(ascending=False).index
data = [df.loc[df['Product'] == p, 'TotalPrice'].values for p in order]
ax.boxplot(data, tick_labels=order, patch_artist=True)
plt.tight_layout()
plt.savefig('boxplot.png', dpi=150)
plt.close()

# Correlation heatmap
fig, ax = plt.subplots(figsize=(5.3, 4.6))
im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.savefig('correlation.png', dpi=150)
plt.close()

# Monthly trend
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(monthly.index.to_timestamp(), monthly.values, color=CYAN, marker='o')
plt.tight_layout()
plt.savefig('trend.png', dpi=150)
plt.close()

print("Done — all figures saved.")
