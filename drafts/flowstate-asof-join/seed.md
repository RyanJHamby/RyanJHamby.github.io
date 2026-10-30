# seed.md — Ryan's raw input (human-written only)

Assembled by Claude from text Ryan wrote in the FlowState repo. Each line cites
its source. It is not new testimony: nothing here is added beyond those notes.
Ryan: confirm, correct or extend before the post ships.

## What I believed
- FlowState would be faster than Polars on grouped as-of joins because it exploits market-data invariants: skips sort verification, borrows `&str` keys without allocating, joins symbol groups in parallel with Rayon, and splits large scans into parallel chunks. (FlowState DESIGN.md §3.2 "Why we outperform Polars", written 2026-03-11 at 3c7486a, still present.)
- "pandas falls over at 10M rows." (README at 3c7486a, 2026-03-11.)

## What I actually did
- 2026-03-11: published a README table: grouped as-of join, 1M rows, 1K symbols, "Apple M-series": FlowState 10 ms vs Polars 18 ms, "1.8x". (README at 3c7486a.)
- 2026-10-04: wrote `benchmarks/reproduce.py`, which prints hardware, versions and dataset, checks every engine's output against Polars before timing, and ran it through `pow run`. (journal 2026-10-04 17:29; README Performance section.)
- 2026-10-30: added min and max to the script and captured a 10-run result. (journal.)

## What I expected
- (not written down; Ryan to add)

## What happened / what surprised me
- "Polars is ~1.4x faster than FlowState on grouped backward as-of (1M x 500K and 10M x 5M, 1K symbols)." (journal 2026-10-04 17:29)
- "pandas merge_asof does 10M in 0.76 s, so 'pandas falls over at 10M' was wrong." (journal 2026-10-04 17:29)
- "The earlier README claim of 1.8x over Polars did not reproduce and was removed." (journal 2026-10-04 17:29; README Performance section)

## Dead ends along the way
- "DuckDB ASOF JOIN did not finish at 1M x 1K symbols, so it is opt-in in reproduce.py." (journal)

## My best explanation for the gap
- For why the March number did not reproduce: "Suspect the earlier number came from a stale (March) flowstate_core build or a different dataset; not verified." (journal 2026-10-04 17:29)
- For why Polars is faster today: (not written down; Ryan to add)

## What I'd do instead / next
- "FlowState's value is not raw join speed against Polars: it is the pieces around the join (watermark streaming alignment, the SPSC streaming pipeline, partitioned replay and the temporal feature store)." (README Performance section)

## Open question this raises
- (not written down; Ryan to add)

## Clearances
- Employer-related content: none | cleared by <company> on <YYYY-MM-DD>
- People named (with permission): none
