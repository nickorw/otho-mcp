# Run Timing Analysis

## Branch: `retrofic-main-benchmark-OOpsFix`

This branch is a minor revision of `retrofit-main-benchmark`, incorporating fixes to the OOPS pitfall correction logic. The pipeline structure and timing semantics are otherwise identical.

Duration data for this branch is derived from a single artifact produced by the pipeline:

**Generator JSON log** (`logs/EDIFACT_generator_<ts>.json`): Each file contains a `duration_seconds` field written by `create_generator_log_node` (source: `otho.py`, line 575): `duration_seconds = time.time() - story_start_time`, where `story_start_time` is set by `time.time()` in `get_story_node` (line 81) at the very beginning of the pipeline, immediately before story loading. `create_generator_log_node` executes after `final_reasoner_validation_node` completes — and therefore after all LLM generation, CQ-level OWL validation, ontology combination, combined-ontology validation, pitfall correction (if triggered), and HermiT/Pellet reasoner checks. The only pipeline activity excluded from `duration_seconds` is the final `end_node`, which performs no file I/O and only prints a summary to stdout; its contribution to wall-clock time is negligible.

`duration_seconds` is therefore the **authoritative end-to-end pipeline duration** for this branch.

**Run start time** is inferred from the run timestamp embedded in the log filename (e.g., `EDIFACT_generator_20260405_061829.json` → `06:18:29`). This timestamp is set by `log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")` in `get_story_node` (line 80), immediately before `story_start_time = time.time()`. The two captures are consecutive Python statements with sub-millisecond separation, so the timestamp accurately represents the start of the pipeline. **Run end time** is derived as `start_time + duration_seconds`.

**Caveats:** (1) The validation logger on this branch is re-instantiated inside `final_reasoner_validation_node` *after* all validation has already completed; consequently, `start_time` and `end_time` in `logs/EDIFACT_validation_<ts>.json` differ by only ~1 ms and do not reflect the actual validation duration. The reasoner execution times recorded in `aggregate.timing_breakdown_seconds` (HermiT + Pellet) are measured separately and are already subsumed within `duration_seconds`. (2) The ~8-minute gap between run 9 (end ~07:24:24) and run 10 (start 08:32:42) reflects a deliberate batch boundary: the 20 runs were executed in two batches of 9 and 10 (with one anomalous run, see below), with a manual pause between batches. This idle interval is not included in any individual `duration_seconds` value. (3) Run `20260405_072425` has a saved output ontology (`data/output/ontologies/EDIFACT_combined_turtle_20260405_072425.owl`, 51793 chars) and a partial validation log, but **no generator log was produced**, so `duration_seconds` is unavailable for this run. The cause of the missing log is unknown; it is included in the table for completeness but excluded from any aggregate statistics.

| Run | Start | End | Duration (s) | Duration (min) | Notes |
|-----|-------|-----|--------------|----------------|-------|
| 20260405_061829 | 06:18:29 | 06:27:18 | 529.855 | 8.83 | |
| 20260405_062718 | 06:27:18 | 06:33:52 | 394.679 | 6.58 | |
| 20260405_063353 | 06:33:53 | 06:42:10 | 497.566 | 8.29 | |
| 20260405_064211 | 06:42:11 | 06:49:34 | 443.195 | 7.39 | |
| 20260405_064934 | 06:49:34 | 06:57:55 | 501.057 | 8.35 | |
| 20260405_065755 | 06:57:55 | 07:03:34 | 339.546 | 5.66 | |
| 20260405_070335 | 07:03:35 | 07:10:57 | 442.069 | 7.37 | |
| 20260405_071057 | 07:10:57 | 07:18:28 | 451.757 | 7.53 | |
| 20260405_071828 | 07:18:28 | 07:24:24 | 356.582 | 5.94 | |
| 20260405_072425 | — | — | — | — | Ontology saved; generator log missing |
| 20260405_083242 | 08:32:42 | 08:40:37 | 475.239 | 7.92 | |
| 20260405_084038 | 08:40:38 | 08:46:05 | 327.006 | 5.45 | |
| 20260405_084605 | 08:46:05 | 08:52:48 | 403.304 | 6.72 | |
| 20260405_085248 | 08:52:48 | 09:00:30 | 462.233 | 7.70 | |
| 20260405_090030 | 09:00:30 | 09:07:37 | 427.817 | 7.13 | |
| 20260405_090738 | 09:07:38 | 09:14:37 | 419.588 | 6.99 | |
| 20260405_091438 | 09:14:38 | 09:22:20 | 462.770 | 7.71 | |
| 20260405_092220 | 09:22:20 | 09:29:27 | 427.332 | 7.12 | |
| 20260405_092928 | 09:29:28 | 09:34:19 | 291.953 | 4.87 | |
| 20260405_093420 | 09:34:20 | 09:41:04 | 404.228 | 6.74 | |

All 20 runs took place on 2026-04-05. Runs 1–9 form the first batch (06:18–07:24); run 10 (`072425`) has anomalous logging behaviour; runs 11–20 form the second batch (08:32–09:41). The 19 timed runs have a mean duration of 431.4 s (7.19 min).

---

## Branch: `retrofit-independent-v2-benchmark`

Duration data for this branch is derived from two complementary artifacts produced by the pipeline:

1. **Agent JSON log** (`logs/EDIFACT_agent_<ts>.json`): Each file contains an ISO 8601 `start_time` and `end_time` field recorded by the pipeline orchestrator with microsecond precision (e.g., `2026-03-04T06:21:17.860017`). The difference between these two timestamps yields the **agent execution time**, which encompasses the full LLM generation loop: all ReAct iterations, intermediate tool calls (scratchpad reads/writes, inline syntax and pitfall checks), and any model latency. This is the dominant component of total run time.

2. **Validation JSON** (`data/output/EDIFACT_validation_<ts>.json`): Each file contains an `aggregate.total_execution_time_seconds` field recorded by the `ValidationLogger` immediately after agent completion. This covers the **post-generation validation phase**: RDFLib syntax parsing, OOPS pitfall detection, and two reasoner consistency checks (HermiT and Pellet). Across all runs this phase accounts for 1.2–2.8 s, representing less than 1.5% of total wall-clock time and is therefore negligible relative to generation time.

**Total run duration** is computed as:

> *T*<sub>total</sub> = (*end\_time* − *start\_time*) + *aggregate.total\_execution\_time\_seconds*

The output file timestamp (e.g., `_062606`) is used as the join key between the two artifacts, as it corresponds to the agent's `end_time` truncated to the nearest second and simultaneously serves as the `start_time` of the validation phase.

**Caveats:** Agent execution time includes non-LLM overhead such as tool dispatch latency and Python process overhead; pure LLM inference time is not separately recorded and cannot be isolated from existing logs.

| Run | Start | End | Gen. Time (s) | Val. Time (s) | Total (s) | Total (min) | Notes |
|-----|-------|-----|---------------|---------------|-----------|-------------|-------|
| 20260304_062606 | 06:21:17 | 06:26:06 | 289.010 | 1.578 | 290.588 | 4.84 | |
| 20260304_063345 | 06:30:48 | 06:33:45 | 176.771 | 1.777 | 178.548 | 2.98 | |
| 20260304_063821 | 06:36:30 | 06:38:21 | 110.893 | 1.191 | 112.084 | 1.87 | |
| 20260304_070119 | 06:56:50 | 07:01:19 | 268.911 | 1.440 | 270.351 | 4.51 | |
| 20260304_071618 | 07:10:17 | 07:16:18 | 361.073 | 1.960 | 363.033 | 6.05 | |
| 20260304_071919 | 07:17:00 | 07:19:19 | 138.659 | 1.525 | 140.184 | 2.34 | |
| 20260304_072404 | 07:21:41 | 07:24:04 | 142.644 | 1.338 | 143.982 | 2.40 | |
| 20260304_072939 | 07:27:44 | 07:29:39 | 115.167 | 1.737 | 116.904 | 1.95 | |
| 20260304_073706 | 07:35:07 | 07:37:06 | 119.295 | 1.376 | 120.671 | 2.01 | |
| 20260304_074731 | 07:44:09 | 07:47:31 | 201.588 | 1.943 | 203.531 | 3.39 | |
| 20260304_075320 | 07:50:44 | 07:53:20 | 155.847 | 1.154 | 157.001 | 2.62 | |
| 20260304_075831 | 07:55:19 | 07:58:31 | 192.596 | 1.458 | 194.054 | 3.23 | |
| 20260304_085410 | 08:50:48 | 08:54:10 | 201.587 | 1.446 | 203.033 | 3.38 | |
| 20260304_090528 | 09:02:29 | 09:05:28 | 178.891 | 1.822 | 180.713 | 3.01 | |
| 20260304_092221 | 09:18:23 | 09:22:21 | 238.465 | 1.775 | 240.240 | 4.00 | |
| 20260304_093001 | 09:26:19 | 09:30:01 | 221.732 | 1.403 | 223.135 | 3.72 | |
| 20260304_094903 | 09:46:36 | 09:49:03 | 146.265 | 1.885 | 148.150 | 2.47 | |
| 20260304_110544 | 11:02:27 | 11:05:44 | 196.968 | 2.834 | 199.802 | 3.33 | |
| 20260304_111526 | 11:06:31 | 11:15:26 | 534.810 | 1.455 | 536.265 | 8.94 | |
| 20260304_112519 | 11:20:29 | 11:25:19 | 289.515 | 2.545 | 292.060 | 4.87 | |

All 20 agent runs took place on 2026-03-04.

---

## Branch: `retrofit-dual-agent-benchmark`

This branch introduces a second node in the graph: a **reviewer agent** that inspects the generator's output after each iteration and produces structured feedback (stored in `data/output/reviews/`). Each run follows a fixed cycle: generator iteration 1 → reviewer cycle 1 → generator iteration 2 → reviewer cycle 2 → validation. Both review cycles are present in every run, confirmed by the presence of `EDIFACT_review_iter1_<ts>.json` and `EDIFACT_review_iter2_<ts>.json` for all 20 runs.

Duration data is derived from three complementary sources, with source code analysis used to verify the precise semantics of each field:

1. **Generator JSON log** (`logs/EDIFACT_generator_<ts>.json`): Contains per-iteration `start_time` and `end_time` fields. **Generation time** is computed as the sum of individual iteration durations (Σ(*iter\_end* − *iter\_start*)). The `run_start_time` and `run_end_time` fields record when the `AgentLogger` was initialised and when `save_json_log()` was called respectively; `run_end_time` coincides with `iter2_end`, i.e. the generator log closes *before* the second review cycle and validation occur. These fields are therefore not suitable for computing total duration.

2. **Review times** are inferred from inter-process boundary gaps: *review1\_time* = *iter2\_start* − *iter1\_end* (cross-validated against the `timestamp` field in `EDIFACT_review_iter1_<ts>.json`, which falls within this interval); *review2\_time* = *val\_start* − *iter2\_end* (confirmed analogously by `EDIFACT_review_iter2_<ts>.json`). Each review call — a single synchronous `llm.invoke()` in `advisory_review_node` — takes approximately 7–12 s.

3. **Validation logger JSON** (`logs/EDIFACT_validation_<ts>.json`): The `story_timing.duration_seconds` field is written by the `end_node` function (source: `src/agents/nodes.py`, line 1016): `story_duration = time.time() - story_start_time`, where `story_start_time` is set by `time.time()` in `get_story_node` at the very beginning of the pipeline, before even the Excel story is loaded. `end_node` executes after `validate_and_save_node` completes and all output files are written. The computed value is then patched into the validation JSON log. This was cross-verified against `val_end − run_start` across all 20 runs, yielding differences of 0.02–0.83 s (attributable to sub-second pipeline overhead and the story-loading step not captured by `run_start_time`). `story_timing.duration_seconds` is therefore the **authoritative end-to-end wall-clock duration** for the full pipeline.

**Total run duration** is taken directly from:

> *T*<sub>total</sub> = `story_timing.duration_seconds` = *end\_node* completion − *get\_story\_node* start

which decomposes as:

> *T*<sub>total</sub> ≈ *story\_load\_time* + *gen\_time* + *review1\_time* + *review2\_time* + *val\_time* + *file\_save\_overhead*

All 20 runs completed successfully. Every run performed exactly 2 generator iterations and 2 reviewer cycles.

| Run | Start | End | Gen. Time (s) | Review 1 (s) | Review 2 (s) | Val. Time (s) | Total (s) | Total (min) |
|-----|-------|-----|---------------|--------------|--------------|---------------|-----------|-------------|
| 20260301_215700 | 21:57:00 | 21:59:24 | 127.3 | 7.2 | 7.7 | 1.7 | 144.0 | 2.40 |
| 20260301_215924 | 21:59:24 | 22:04:37 | 295.0 | 9.1 | 7.4 | 1.5 | 313.1 | 5.22 |
| 20260301_220437 | 22:04:37 | 22:08:32 | 213.9 | 10.7 | 7.5 | 2.5 | 234.6 | 3.91 |
| 20260301_220832 | 22:08:32 | 22:11:13 | 138.2 | 9.1 | 11.8 | 1.6 | 160.7 | 2.68 |
| 20260301_221113 | 22:11:13 | 22:13:32 | 118.6 | 9.6 | 9.4 | 1.5 | 139.0 | 2.32 |
| 20260301_221332 | 22:13:32 | 22:17:25 | 216.9 | 7.3 | 7.5 | 1.8 | 233.5 | 3.89 |
| 20260301_221725 | 22:17:25 | 22:19:40 | 115.4 | 8.8 | 8.5 | 1.5 | 134.4 | 2.24 |
| 20260301_221940 | 22:19:40 | 22:22:36 | 158.5 | 8.8 | 7.3 | 2.0 | 176.6 | 2.94 |
| 20260301_222236 | 22:22:36 | 22:25:34 | 158.6 | 8.0 | 9.0 | 1.8 | 177.5 | 2.96 |
| 20260301_222534 | 22:25:34 | 22:28:18 | 147.8 | 7.9 | 6.5 | 1.6 | 163.8 | 2.73 |
| 20260301_223501 | 22:35:02 | 22:37:50 | 148.6 | 8.5 | 8.9 | 2.0 | 168.9 | 2.81 |
| 20260301_223750 | 22:37:50 | 22:42:12 | 241.9 | 9.2 | 9.2 | 1.8 | 262.1 | 4.37 |
| 20260301_224212 | 22:42:12 | 22:45:27 | 177.1 | 8.5 | 8.1 | 1.6 | 195.3 | 3.25 |
| 20260301_224527 | 22:45:27 | 22:49:22 | 214.7 | 9.2 | 9.2 | 1.6 | 234.7 | 3.91 |
| 20260301_224922 | 22:49:22 | 22:51:45 | 122.6 | 10.1 | 8.2 | 2.0 | 143.0 | 2.38 |
| 20260301_225145 | 22:51:45 | 22:54:09 | 125.6 | 9.1 | 7.4 | 1.5 | 143.7 | 2.39 |
| 20260301_225409 | 22:54:09 | 22:57:32 | 182.5 | 10.5 | 8.4 | 1.5 | 202.9 | 3.38 |
| 20260301_225732 | 22:57:32 | 23:00:18 | 148.5 | 8.9 | 7.7 | 1.5 | 166.6 | 2.78 |
| 20260301_230018 | 23:00:18 | 23:03:38 | 181.8 | 8.7 | 7.6 | 1.5 | 199.7 | 3.33 |
| 20260301_230338 | 23:03:38 | 23:07:08 | 190.4 | 8.8 | 8.5 | 2.2 | 210.0 | 3.50 |

All 20 runs took place on 2026-03-01.

---

## Branch: `tri-agent-gen-edifact`

This branch extends the graph with a third agent node. The pipeline structure differs from the dual-agent branch in two key ways: (1) the generator may perform a variable number of iterations per run (observed range: 3–8), and (2) the two reviewer cycles execute in the gap after the *final* generator iteration, with `review_iter1` overlapping the tail of the last generator iteration (i.e., running concurrently rather than sequentially). Both review files (`EDIFACT_review_iter1_<ts>.json` and `EDIFACT_review_iter2_<ts>.json`) are present for all 20 runs.

**Total run duration** is computed as:

> *T*<sub>total</sub> = *val\_end* − *run\_start\_time*

where `run_start_time` is the `AgentLogger` initialisation timestamp (microsecond precision), and `val_end` is the `end_time` field in `logs/EDIFACT_validation_<ts>.json`. This is equivalent to `story_timing.duration_seconds` for 19 of 20 runs (difference ≤ 1.1 s). The exception is run `20260302_073654`, where `story_timing` is inflated by 652.6 s of inter-run idle time: inspection shows that `story_start_time` (set by `time.time()` in `get_story_node`) was captured at the end of the preceding run in the same batch loop, before a ~11-minute pause before the `AgentLogger` was initialised. For this run, `val_end − run_start_time` (374.3 s) is used as the authoritative total.

**Generation time** is the sum of individual iteration durations (Σ(*iter\_end* − *iter\_start*)). **Review + overhead time** is the residual: *T*<sub>total</sub> − *gen\_time* − *val\_time*, and subsumes both reviewer LLM calls, any concurrent overlap between review1 and the final generator iteration, and minor pipeline overhead. **Validation time** is `val_end − val_start` from `logs/EDIFACT_validation_<ts>.json`.

| Run | Start | End | Iters | Gen. Time (s) | Review+OH (s) | Val. Time (s) | Total (s) | Total (min) |
|-----|-------|-----|-------|---------------|---------------|---------------|-----------|-------------|
| 20260302_071802 | 07:18:02 | 07:36:54 | 8 | 1109.1 | 19.9 | 2.5 | 1131.5 | 18.86 |
| 20260302_073654 | 07:47:47 | 07:54:01 | 4 | 353.4 | 19.3 | 1.6 | 374.3 | 6.24 |
| 20260302_075401 | 07:54:01 | 08:10:00 | 3 | 938.6 | 17.5 | 2.8 | 958.9 | 15.98 |
| 20260302_081000 | 08:10:00 | 08:26:12 | 7 | 946.4 | 22.8 | 2.9 | 972.1 | 16.20 |
| 20260302_082612 | 08:26:12 | 08:45:53 | 5 | 1157.1 | 21.4 | 2.2 | 1180.7 | 19.68 |
| 20260302_124024 | 12:40:25 | 13:09:30 | 7 | 1716.1 | 26.1 | 3.2 | 1745.4 | 29.09 |
| 20260302_130930 | 13:09:30 | 13:35:53 | 6 | 1563.2 | 17.5 | 2.4 | 1583.1 | 26.39 |
| 20260302_133553 | 13:35:53 | 14:02:35 | 6 | 1583.4 | 15.5 | 3.2 | 1602.1 | 26.70 |
| 20260302_140235 | 14:02:35 | 14:22:21 | 5 | 1161.6 | 21.6 | 2.0 | 1185.2 | 19.75 |
| 20260302_142221 | 14:22:21 | 14:38:15 | 3 | 932.1 | 20.3 | 1.9 | 954.3 | 15.91 |
| 20260303_061520 | 06:15:21 | 06:34:00 | 6 | 1096.4 | 19.8 | 2.7 | 1118.9 | 18.65 |
| 20260303_063400 | 06:34:00 | 06:40:29 | 3 | 357.6 | 29.8 | 1.7 | 389.1 | 6.49 |
| 20260303_064029 | 06:40:29 | 07:01:00 | 4 | 1209.0 | 19.8 | 2.7 | 1231.5 | 20.52 |
| 20260303_070100 | 07:01:00 | 07:26:31 | 6 | 1507.5 | 21.3 | 1.7 | 1530.5 | 25.51 |
| 20260303_072631 | 07:26:31 | 07:52:47 | 6 | 1537.2 | 36.9 | 2.2 | 1576.3 | 26.27 |
| 20260303_085821 | 08:58:23 | 09:18:50 | 7 | 1205.3 | 19.6 | 2.6 | 1227.5 | 20.46 |
| 20260303_091850 | 09:18:50 | 09:33:22 | 4 | 847.7 | 22.0 | 2.4 | 872.1 | 14.53 |
| 20260303_093322 | 09:33:22 | 09:39:56 | 3 | 372.9 | 20.3 | 1.6 | 394.8 | 6.58 |
| 20260303_093956 | 09:39:56 | 09:46:21 | 3 | 360.5 | 22.6 | 2.4 | 385.5 | 6.42 |
| 20260303_094621 | 09:46:21 | 09:56:37 | 4 | 594.0 | 20.1 | 1.7 | 615.8 | 10.26 |

All 20 runs took place on 2026-03-02 (runs 1–10) and 2026-03-03 (runs 11–20).
