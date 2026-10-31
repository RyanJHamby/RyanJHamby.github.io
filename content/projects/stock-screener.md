+++
title = "Intelligent Stock Screener"
weight = 4
aliases = []
[params]
tags_line = "Python · GitHub Actions"
status = "Nov 2025 – Present"
+++

**Nov 2025 - Present**

[GitHub repository](https://github.com/RyanJHamby/stock-screener)

Fully automated stock screening system scanning 3,800+ US stocks daily using Mark Minervini's Trend Template methodology. Identifies high-conviction buy/sell signals via phase-based trend classification, relative strength momentum, and fundamental quality filters.

<div class="achievement">
Automated daily scans of <span class="metric">3,800+ stocks</span> with <span class="metric">74% API reduction</span> via Git-based fundamental caching and GitHub Actions automation
</div>

<div class="achievement">
Phase-based classification identifying Phase 2 uptrend breakouts passing 7 of 8 Minervini criteria (50>150>200 SMA alignment, relative strength ≥70, volume confirmation)
</div>

<div class="achievement">
Risk-managed position management with <span class="metric">max 10% risk, min 2:1 R:R ratio</span>, automated stop-loss trailing, and tax-aware filtering for long-term positions
</div>

*Figures on this project are from the repo README, not a captured run.*

## Core Features

**Phase-Based Trend Classification:**
- Phase 1 (Base): Consolidation after decline
- Phase 2 (Uptrend): Confirmed uptrend with 50>150>200 SMA alignment — **BUY ZONE**
- Phase 3 (Distribution): Topping pattern with weakening momentum
- Phase 4 (Downtrend): Declining trend — **AVOID**

**Volatility Contraction Pattern (VCP):**
- Identifies price consolidation before explosive breakout
- Formula: Range_i = ((High_i - Low_i) / Close_i) × 100
- VCP_Score = (∑ Contractions / Total_Periods) × Trend_Quality
- Example: 13 contractions (6.5% → 5.8% → 7.6% → 6.0%) with 54/100 quality score indicates imminent breakout

**Intelligent Market Regime Filtering:**
- Only generates buy signals when SPY in Phase 1/2 with ≥15% of stocks in Phase 2
- Avoids low-probability trades in declining markets
- Sell signals always generated (can exit any market)

**Smart Caching Strategy:**
- Fundamentals stored in Git repository as JSON with metadata
- Earnings season (6 weeks): refresh if >7 days old
- Normal periods: refresh if >90 days old
- Result: 74% fewer API calls, 15-20 min faster scans

## Sample Output

<details>
<summary>View sample scan output (Jan 9, 2026)
</summary>

```
OPTIMIZED FULL MARKET SCAN - ALL US STOCKS
Scan Date: 2026-01-09
Generated: 2026-01-09 14:04:49

SCANNING STATISTICS
Total Universe: 3,819 stocks
Analyzed: 1,188 stocks
Buy Signals: 370 | Sell Signals: 111
Error Rate: 0.26%

SPY Trend: Phase 2 - Uptrend (Bullish)
  • 50 SMA: $678.39 (slope: 0.0563)
  • 200 SMA: $626.72 (slope: 0.0982)
  • Confidence: 85%

Market Breadth (n=1,188):
  • Phase 1 (Base): 560 (47.1%)
  • Phase 2 (Uptrend): 504 (42.4%)
  • Phase 3 (Distribution): 1 (0.1%)
  • Phase 4 (Downtrend): 123 (10.4%)

Market Regime: RISK-ON (Strong)

BUY #1: WWD | Score: 104.5/110
  Phase: 2 | Entry Quality: Good | R:R: 3.2:1
  Stop Loss: $299.25
  • 11.1% above 50 SMA (strong breakout)
  • Revenue: +16.5% YoY | EPS: +64% YoY
  • Volume confirmation (1.17 ratio)
```

</details>
