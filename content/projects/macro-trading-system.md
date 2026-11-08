+++
title = "Covariance-Based Macro Trading System"
weight = 5
aliases = []
[params]
tags_line = "C++ · AWS Lambda · FRED"
status = "Aug 2023 – May 2026"
+++

**Aug 2023 - May 2026**

[GitHub repository](https://github.com/RyanJHamby/macro-factor-decomposition)

Systematic ES futures trading system powered by eigendecomposition of economic indicator covariance matrices. Decomposes 8×8 macro factor covariance to identify uncertainty regimes and size positions via macro surprise exposure.

<div class="achievement">
Backtested on real FRED data over <span class="metric">17 years (2007–2024)</span>: <span class="metric">0.28 Sharpe, 2.10% annualized return, 3.2% max drawdown</span> with half-Kelly, regime-adjusted position sizing
</div>

<div class="achievement">
C++ factor decomposition engine (Eigen 3.4.0) processing 8 FRED indicators + VIX with AWS Lambda daily automation
</div>

<div class="achievement">

End-to-end pipeline: FRED API → monthly frequency alignment (downsampling/Hermite interpolation) → spectral decomposition (\(\Sigma = U \Lambda U^{\top}\)) → S3, covered by <span class="metric">240+ unit tests</span>

</div>

## Core Hypothesis

Markets respond to **unexpected** economic information, not levels. Raw covariance is misleading—it captures expected relationships.

Standard assumption: \(\mathbb{E}[r_t \mid X_t] = \alpha + \beta X_t\)

Reality: Markets react to **surprises**: \(\Delta X_t - \mathbb{E}_t[\Delta X_t]\)

Solution: Decompose surprise covariance via PCA to identify 3-4 interpretable macro factors (growth, inflation, policy, volatility) and measure ES exposure across regimes.

## 5-Stage Architecture

1. **Data Acquisition:** FRED API (CPI, GDP, Unemployment, Sentiment, Fed Funds, Treasury yields) + VIX
2. **Temporal Alignment:** Daily → month-end LOCF, Quarterly → Hermite interpolation to monthly
3. **Covariance Estimation:** \(\Sigma_{ij} = \frac{1}{n-1} \sum_t (X_{it} - \bar{X}_i)(X_{jt} - \bar{X}_j)\)
4. **Spectral Decomposition:** \(\Sigma = U \Lambda U^{\top}\) → First 3-4 eigenvalues capture 85-92% variance
5. **Regime Quantification:** Frobenius norm \(\|\Sigma\|_F = \sqrt{\sum_{i,j} \sigma_{ij}^2}\) maps to regime state

**Regime Classification:**
- **Stable** (\(\|\Sigma\|_F < \mu - \sigma\)): Low uncertainty, tight co-movement
- **Neutral** (\(\mu - \sigma \le \|\Sigma\|_F \le \mu + \sigma\)): Moderate uncertainty
- **Elevated** (\(\|\Sigma\|_F > \mu + \sigma\)): High uncertainty, factor decoupling

## Infrastructure

**AWS Stack:**
- EventBridge (cron: daily 12:00 UTC) → Lambda (512MB, 600s) → S3 (versioned, encrypted)
- Native C++ binary with Eigen, AWS SDK, curl
- IaC: AWS CDK 2.x (TypeScript, dev/staging/prod)

**Validation:**
- 240+ unit tests: covariance symmetry, eigenvalue ordering, numerical stability, Sharpe/drawdown/P&L accuracy
- 17-year backtest (2007–2024, 468 trades): 0.28 Sharpe, 3.23% max drawdown, 2.10% annualized return, 87.2% win rate (selectivity, not edge); NASDAQCOM proxy for 2007–2016 equity returns; figures from the repo README, not a captured run

## Data Inputs

8 economic indicators at mixed frequencies:
- CPI (monthly) - Inflation anchor
- Real GDP (quarterly) - Earnings driver
- Unemployment (monthly) - Labor tightness
- Consumer Sentiment (monthly) - Forward demand
- Fed Funds (monthly) - Discount rate
- 10Y/2Y Treasury (daily) - Yield curve
- VIX (daily) - Realized volatility
