# Consolidated Agent Ontology Ranking Report

> **Evaluation Date:** 2026-04-12  
> **Scope:** Three selected OWL ontologies (A = triAgent, C = singleAgent, D = dualAgent), evaluated by four independent agent runs.  
> **Framework:** OntoQA structural ratios + CQ coverage (14 CQs) + OWL design patterns + axiom complexity + lexical quality  
> **Source files:** `agent_ontology_ranking_1.md` through `agent_ontology_ranking_4.md`

---

## File–Label Mapping

| Label | Agent Type | Source File |
|-------|------------|-------------|
| **A** | triAgent | `EDIFACT_ontology_20260303_070100.owl` |
| **C** | singleAgent | `EDIFACT_ontology_20260304_093001.owl` |
| **D** | dualAgent | `EDIFACT_ontology_20260301_222236.owl` |

---

## Per-Run Rankings

| Run | Rank 1 | Score | Rank 2 | Score | Rank 3 | Score |
|-----|--------|:-----:|--------|:-----:|--------|:-----:|
| Run 1 | **C** (singleAgent) | 4.55 | **A** (triAgent) | 4.43 | **D** (dualAgent) | 4.31 |
| Run 2 | **A** (triAgent) | 4.55 | **D** (dualAgent) | 4.12 | **C** (singleAgent) | 3.86 |
| Run 3 | **C** (singleAgent) | 4.59 | **A** (triAgent) | 4.47 | **D** (dualAgent) | 4.07 |
| Run 4 | **A** (triAgent) | 4.52 | **C** (singleAgent) | 4.43 | **D** (dualAgent) | 4.02 |

> **Weighted score formula (all runs):** `(CQ × 0.40) + (Struct × 0.20) + (Design × 0.15) + (Axiom × 0.15) + (Lexical × 0.10)`

---

## Dimension Scores Across Runs

### A — triAgent (`EDIFACT_ontology_20260303_070100.owl`)

| Dimension | Run 1 | Run 2 | Run 3 | Run 4 | Mean |
|-----------|:-----:|:-----:|:-----:|:-----:|:----:|
| CQ Coverage (40%) | 4.5 | 4.7 | 4.5 | 4.7 | **4.60** |
| Structural Ratios (20%) | 3.2 | 3.8 | 3.5 | 3.8 | **3.58** |
| Design Patterns (15%) | 4.9 | 4.8 | 5.0 | 5.0 | **4.93** |
| Axiom Complexity (15%) | 4.8 | 4.6 | 4.8 | 4.5 | **4.68** |
| Lexical Quality (10%) | 5.0 | 5.0 | 5.0 | 5.0 | **5.00** |
| **Weighted Score** | 4.43 | 4.55 | 4.47 | 4.52 | **4.49** |

### C — singleAgent (`EDIFACT_ontology_20260304_093001.owl`)

| Dimension | Run 1 | Run 2 | Run 3 | Run 4 | Mean |
|-----------|:-----:|:-----:|:-----:|:-----:|:----:|
| CQ Coverage (40%) | 4.7 | 4.0 | 4.7 | 4.5 | **4.48** |
| Structural Ratios (20%) | 3.8 | 3.4 | 4.2 | 4.2 | **3.90** |
| Design Patterns (15%) | 4.8 | 3.0 | 4.8 | 4.5 | **4.28** |
| Axiom Complexity (15%) | 4.6 | 4.2 | 4.5 | 4.2 | **4.38** |
| Lexical Quality (10%) | 5.0 | 5.0 | 5.0 | 5.0 | **5.00** |
| **Weighted Score** | 4.55 | 3.86 | 4.59 | 4.43 | **4.36** |

### D — dualAgent (`EDIFACT_ontology_20260301_222236.owl`)

| Dimension | Run 1 | Run 2 | Run 3 | Run 4 | Mean |
|-----------|:-----:|:-----:|:-----:|:-----:|:----:|
| CQ Coverage (40%) | 4.4 | 4.1 | 3.8 | 3.8 | **4.03** |
| Structural Ratios (20%) | 3.5 | 3.5 | 3.8 | 3.5 | **3.58** |
| Design Patterns (15%) | 4.7 | 4.5 | 4.5 | 4.5 | **4.55** |
| Axiom Complexity (15%) | 4.4 | 4.0 | 4.2 | 4.0 | **4.15** |
| Lexical Quality (10%) | 5.0 | 5.0 | 5.0 | 5.0 | **5.00** |
| **Weighted Score** | 4.31 | 4.12 | 4.07 | 4.02 | **4.13** |

---

## Consolidated Ranking (Mean Weighted Scores)

| Rank | Ontology | Agent Type | Mean Score | Rank 1 Wins | Rank 3 Finishes |
|------|----------|------------|:----------:|:-----------:|:---------------:|
| **1** | **A** | triAgent | **4.49** | 2/4 | 0/4 |
| **2** | **C** | singleAgent | **4.36** | 2/4 | 1/4 |
| **3** | **D** | dualAgent | **4.13** | 0/4 | 3/4 |

**A (triAgent) is the consolidated winner** — it scores highest on average and never finishes last. C (singleAgent) is competitive but volatile. D (dualAgent) consistently places last.

---

## Cross-Run Analysis by Dimension

### CQ Coverage
A and C both achieve **14/14 CQ coverage** across most runs (with minor deductions for partial coverage on CQ13). D consistently scores lower due to a structural gap in CQ7/CQ8 (missing `LineItem → Item` object property in runs 1–3) and a formally unenforced `hasMandatoryIdentifier` for CQ13 (run 4).

**Consistent finding across all 4 runs:** D's CQ score is dragged down primarily by:
1. The absent `LineItem → Item` navigational property (CQ7, CQ8) — identified in runs 1, 2, 3
2. `hasMandatoryIdentifier` declared without a logical restriction (CQ13) — flagged in run 4

### Structural Ratios (OntoQA)
All runs agree on the raw metric values:

| Metric | A | C | D |
|--------|:---:|:---:|:---:|
| RR | 0.8718 | 0.7826 | 0.7692 |
| AR | 0.5000 | 0.7368 | 0.5455 |
| IR | 0.2083 | 0.5263 | 0.4091 |

Score variance here is driven by **interpretation**: runs that penalize C's IR heavily (noting it is inflated by is-a/part-of anti-patterns) give C a lower structural score (runs 1, 2 → ~3.4–3.5); runs that reward the raw IR value give C a higher score (runs 3, 4 → 4.2). A's low IR is consistently identified as its structural weakness. D's scores are stable across runs (3.5–3.8).

### Design Patterns
**Most consistent finding:** A scores highest (4.8–5.0) across all four runs. The reasoning is unanimous:
- A uses `owl:disjointUnionOf` for invoice sections — the only use of this construct across all three candidates
- A has dual `owl:equivalentClass` definitions for both `RoleAssignment` and `LineItem`
- C is penalized in all runs for the is-a/part-of conflation (`Segment rdfs:subClassOf EDIFACTMessage`, `Price rdfs:subClassOf LineItem`)
- D's score is stable (4.5–4.7); its `BuyerOrganization owl:equivalentClass` definition is recognized as a strength

**Run 2 outlier:** C receives 3.0 for design patterns — the most severe penalty observed. This run focused most strongly on the is-a/part-of conflation as a disqualifying architectural defect. The other three runs score C at 4.5–4.8, treating the defect as a notable flaw but not a fundamental disqualifier for CQ coverage purposes.

### Axiom Complexity
All four runs assign A the **highest axiom diversity score (7)**, citing:
- `owl:disjointUnionOf` (unique to A among the three)
- Two `owl:equivalentClass` definitions
- Combined use of `owl:allValuesFrom` and `owl:someValuesFrom`

C and D are tied at axiom diversity score **6** in all runs. C's distinguishing strength is `owl:cardinality` restrictions on LineItem (present in all runs); D's distinguishing strength is `owl:BuyerOrganization` equivalentClass with named-individual role references.

### Lexical Quality
**Unanimous across all 4 runs:** All three ontologies score **5.0/5.0**. Perfect CamelCase naming, 1.0 label coverage, 1.0 comment coverage for A, C, and D without exception.

---

## Critical Defects — Cross-Run Consensus

### A — triAgent
**Agreed defect (all 4 runs):** Very flat taxonomy (IR = 0.2083). The lack of a shared `InvoiceSection` superclass for Header/Detail/Summary, and minimal segment class hierarchy, limits subsumption-based reasoning. Run 1 also flags the is-a/part-of chain in C as more severe, so A's defect is considered a missed opportunity rather than a correctness error.

### C — singleAgent
**Agreed defect (all 4 runs):** The is-a/part-of conflation anti-pattern:
- `Segment rdfs:subClassOf EDIFACTMessage` → a Segment is not a kind of Message
- `LineItem rdfs:subClassOf InvoiceDetail` → a LineItem is not a kind of InvoiceDetail
- `Price rdfs:subClassOf LineItem` → a Price is not a kind of LineItem

All four runs flag this as C's most critical structural error. Consequence: any OWL reasoner would infer that instances of `Price` are also instances of `InvoiceDetail` and `EDIFACTMessage`, producing semantically incorrect entailments.

### D — dualAgent
**Agreed defect (all 4 runs):** Missing `LineItem → Item` object property (runs 1–3 frame it as severing CQ7/CQ8 navigation; run 4 treats it differently but still notes CQ13 is formally unenforced). The missing link means D cannot answer "What items are sold?" via a clean joined SPARQL traversal without inferential workarounds.

---

## Recommended Fix Per Ontology

| Ontology | Fix Priority | Recommended Change |
|----------|--------------|--------------------|
| **A** | Moderate | Introduce `InvoiceSection` as a named superclass for `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary`; deepen segment hierarchy with `BGMSegment`, `NADSegment` subclasses |
| **C** | Critical | Replace `Segment rdfs:subClassOf EDIFACTMessage`, `LineItem rdfs:subClassOf InvoiceDetail`, and `Price rdfs:subClassOf LineItem` with object properties (`containsSegment`, `hasLineItem`, `hasPrice`); the current hierarchy produces unsound reasoning |
| **D** | Critical | Add `describesItem: LineItem → Item` object property (with inverse); add a formal `owl:someValuesFrom` or `owl:minCardinality 1` restriction on `hasMandatoryIdentifier` |

---

## Key Takeaways

1. **A (triAgent) is the most consistent top-performer** across all four independent runs, winning Rank 1 in two of four evaluations and never finishing last. Its strengths — highest axiom diversity (score 7), `owl:disjointUnionOf`, dual `owl:equivalentClass` definitions — are recognized unanimously.

2. **C (singleAgent) is competitive but architecturally compromised.** It wins Rank 1 in two runs and has the best AR (0.7368) and a strong CQ coverage path. However, all four runs identify the is-a/part-of conflation as a correctness defect that would produce reasoning anomalies in production use. Its score variance (3.86–4.59) is the highest of the three, reflecting inconsistent treatment of this defect severity.

3. **D (dualAgent) consistently places last.** Its structural gap (missing `LineItem → Item`) is flagged in every run. Without this fix, D cannot answer CQ7 and CQ8 as clean SPARQL joins, which accounts for the majority of its CQ coverage penalty. D's strengths — systematic `owl:inverseOf` coverage, granular four-field address decomposition, named role individuals — are acknowledged but insufficient to overcome the navigation gap.

4. **All three ontologies achieve perfect lexical quality** (CamelCase 1.0, Label 1.0, Comment 1.0) — a shared strength across all AI-generated candidates.

5. **None approaches the TUMedifact AR baseline (8.42).** The AI-generated ontologies range from 0.50–0.74 in attribute richness vs. 8.42 for the reference, indicating a systematic gap in data property density between terminological-layer AI ontologies and a mature domain ontology developed for instance-level detail.

---

## Scoring Summary Reference

| Criterion | Weight | A (triAgent) mean | C (singleAgent) mean | D (dualAgent) mean |
|-----------|:------:|:-----------------:|:--------------------:|:------------------:|
| CQ Coverage | 40% | **4.60** | 4.48 | 4.03 |
| Structural Ratios | 20% | 3.58 | **3.90** | 3.58 |
| Design Patterns | 15% | **4.93** | 4.28 | 4.55 |
| Axiom Complexity | 15% | **4.68** | 4.38 | 4.15 |
| Lexical Quality | 10% | 5.00 | 5.00 | 5.00 |
| **Weighted Total (mean)** | | **4.49** | **4.36** | **4.13** |
