# Ontology Quality Report

> Generated automatically from `generate_ontology_report.py`  
> Date: 2026-04-05

---

## 1. Reference Ontologies (TUMedifact)

These two ontologies serve as the baseline for comparison.

| Metric | TUMedifact (full) | TUMedifact (trimmed) |
|--------|:-----------------:|:--------------------:|
| Syntax valid | ✅ | ✅ |
| Triples (axioms) | 2670 | 2267 |
| Classes | 31 | 31 |
| Object properties | 10 | 10 |
| Data properties | 261 | 261 |
| Annotation properties | 22 | 9 |
| Max inheritance depth | 1 | 1 |
| Avg inheritance depth | 0.8 | 0.8 |
| Max branching factor | 21 | 21 |
| Avg branching factor | 5.2 | 5.2 |
| Leaf classes | 26 | 26 |
| RR (Relationship Richness) | 0.2778 | 0.2778 |
| AR (Attribute Richness) | 8.4194 | 8.4194 |
| IR (Inheritance Richness) | 0.8387 | 0.8387 |
| Axiom Diversity Score | 2 | 2 |
| Naming: Strict CamelCase | 0.9844 | 0.9870 |
| Naming: Underscore Style | 0.0031 | 0.0000 |
| Naming: Non-conformant | 0.0125 | 0.0130 |
| Label Coverage | 0.9564 | 0.9870 |
| Comment Coverage | 0.9408 | 0.9805 |

---

## 2. Generated Ontologies — Summary by Agent Type

Each folder contains 20 generated ontologies for the EDIFACT domain story.

### 2.1 High-level Validation Summary

| Agent Type | N | Syntax Valid | HermiT Consistent | Pellet Consistent | OOPS Passed | No Critical Pitfalls |
|------------|:-:|:------------:|:-----------------:|:-----------------:|:-----------:|:--------------------:|
| **workflow** | 20 | 100.0% | 5.0% | 10.0% | 5.0% | 40.0% |
| **singleAgent** | 20 | 100.0% | 85.0% | 85.0% | 95.0% | 95.0% |
| **dualAgent** | 20 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| **triAgent** | 20 | 100.0% | 85.0% | 70.0% | 55.0% | 85.0% |

### 2.2 Structural Metrics (avg / median)

| Agent Type | Triples avg | Triples med | Classes avg | Classes med | Obj Props avg | Data Props avg | Ann Props avg |
|------------|:-----------:|:-----------:|:-----------:|:-----------:|:-------------:|:--------------:|:-------------:|
| **workflow** | 1344.3 | 1420 | 66.2 | 65 | 100.8 | 49.8 | 0 |
| **singleAgent** | 319.9 | 328.0 | 18.9 | 19.0 | 28.1 | 11.2 | 0.1 |
| **dualAgent** | 316.1 | 323.5 | 18.6 | 18.5 | 29.5 | 9.6 | 0 |
| **triAgent** | 359.4 | 400.5 | 27.2 | 28.0 | 31.8 | 6.3 | 0 |

### 2.3 Structural Range (min–max)

| Agent Type | Triples min | Triples max | Classes min | Classes max |
|------------|:-----------:|:-----------:|:-----------:|:-----------:|
| **workflow** | 817 | 1733 | 59 | 79 |
| **singleAgent** | 224 | 386 | 16 | 21 |
| **dualAgent** | 227 | 373 | 13 | 22 |
| **triAgent** | 3 | 623 | 0 | 39 |

### 2.4 OOPS Pitfall Summary

| Agent Type | Total Pitfall Occurrences | Unique Pitfalls | Most Common |
|------------|:-------------------------:|:---------------:|-------------|
| **workflow** | 50 | 9 | P22 (×13), P20 (×12), P13 (×7), P04 (×6), P05 (×5), P19 (×3), P08 (×2), P10 (×1), P12 (×1) |
| **singleAgent** | 0 | 0 | None |
| **dualAgent** | 0 | 0 | None |
| **triAgent** | 10 | 5 | P04 (×4), P20 (×2), P22 (×2), P12 (×1), P13 (×1) |

### 2.5 Hierarchy Complexity (avg across ontologies in folder)

| Agent Type | Max Depth (max) | Max Depth (avg) | Avg Depth (avg) | Max Branching (max) | Avg Branching (avg) | Leaf Classes (avg) |
|------------|:---------------:|:---------------:|:---------------:|:-------------------:|:-------------------:|:------------------:|
| **workflow** | 6 | 3.5 | 1.2 | 28 | 3.0 | 51.8 |
| **singleAgent** | 5 | 1.8 | 0.5 | 4 | 1.6 | 15.5 |
| **dualAgent** | 4 | 1.2 | 0.3 | 4 | 1.6 | 15.7 |
| **triAgent** | 3 | 1.6 | 0.4 | 22 | 2.5 | 23 |

### 2.6 OntoQA Structural Ratios

| Agent Type | RR avg | AR avg | IR avg |
|------------|:------:|:------:|:------:|
| **workflow** | 0.7000 | 0.8000 | 0.7000 |
| **singleAgent** | 0.8000 | 0.6000 | 0.3000 |
| **dualAgent** | 0.9000 | 0.5000 | 0.3000 |
| **triAgent** | 0.7000 | 0.2000 | 0.4000 |

### 2.7 Axiom Complexity & Lexical Quality

| Agent Type | Axiom Diversity avg | Axiom Diversity max | Naming Strict avg | Naming Underscore avg | Naming Bad avg | Label Coverage avg | Comment Coverage avg |
|------------|:-------------------:|:-------------------:|:-----------------:|:---------------------:|:--------------:|:------------------:|:--------------------:|
| **workflow** | 7.7 | 9 | 0.7000 | 0.3000 | 0.0000 | 0.9000 | 0.8000 |
| **singleAgent** | 4.5 | 7 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 |
| **dualAgent** | 3.4 | 6 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 |
| **triAgent** | 4.2 | 7 | 0.9000 | 0.0000 | 0.0000 | 0.9000 | 0.9000 |

### 2.8 Generator Performance

| Agent Type | Gen Success Rate | Avg Duration (s) | Avg Iterations | Pitfalls During Gen |
|------------|:----------------:|:----------------:|:--------------:|:-------------------:|
| **workflow** | 100.0% | 424.1 | N/A | 0 |
| **singleAgent** | 0.0% | 0 | N/A | 0 |
| **dualAgent** | 100.0% | 180.1 | 2.2 | 9 |
| **triAgent** | 100.0% | 1037.9 | 3.0 | 0 |

---

## 3. Per-Folder Detail

_OOPS column legend: ✅ no pitfalls · ❌ pitfalls found · ⚠️ OOPS failed to run (wrong\_execution or Turtle parse error)_

### 3.1 workflow

**Pellet inconsistent classes (31):** `xml_combined_owl.xml.Cl_InvoiceDetail`, `xml_combined_owl.xml.Cl_Description`, `xml_combined_owl.xml.Cl_InvoiceDetailReification`, `xml_combined_owl.xml.Cl_OrganizationInfo_Display`, `xml_combined_owl.xml.Cl_InvoiceReification`, `xml_combined_owl.xml.Cl_InvoiceAmountAssignment`, `xml_combined_owl.xml.Cl_InvoiceParty`, `xml_combined_owl.xml.Cl_GrossPrice`, `owl.Nothing`, `xml_combined_owl.xml.Cl_StockStatus` ...

**Validation Results**

| File (20) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_combined_turtle_20260405_065755.owl` | ✅ | ❌ | ❌ | ⚠️ |
| `EDIFACT_combined_turtle_20260405_064934.owl` | ✅ | ❌ | ✅ | ❌ |
| `EDIFACT_combined_turtle_20260405_091438.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_063353.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_071057.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_083242.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_085248.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_combined_turtle_20260405_064211.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_090738.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_090030.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_070335.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_072425.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_084038.owl` | ✅ | ❌ | ❌ | ⚠️ |
| `EDIFACT_combined_turtle_20260405_084605.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_092928.owl` | ✅ | ❌ | ❌ | ⚠️ |
| `EDIFACT_combined_turtle_20260405_061829.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_071828.owl` | ✅ | ❌ | ❌ | ⚠️ |
| `EDIFACT_combined_turtle_20260405_092220.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_093420.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_combined_turtle_20260405_062718.owl` | ❌ | ❌ | ❌ | ⚠️ |

**Extracted Details**

| File (20) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_combined_turtle_20260405_065755.owl` | 79 | 60 | 57 | 0 | 911 | 2 | 0.58 | 7 | 60 | 0.566 | 0.7215 | 0.5823 | 8 | 0.5969 | 0.4031 | 0.0 | 0.3622 | 0.0 |
| `EDIFACT_combined_turtle_20260405_064934.owl` | 73 | 147 | 50 | 0 | 1648 | 5 | 1.36 | 7 | 59 | 0.7819 | 0.6849 | 0.5616 | 8 | 0.7296 | 0.2704 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_091438.owl` | 73 | 128 | 54 | 0 | 1590 | 4 | 1.47 | 13 | 55 | 0.7072 | 0.7397 | 0.726 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_063353.owl` | 72 | 136 | 61 | 0 | 1733 | 3 | 0.93 | 7 | 57 | 0.7598 | 0.8472 | 0.5972 | 8 | 0.7235 | 0.2765 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_071057.owl` | 71 | 124 | 50 | 0 | 1655 | 3 | 0.72 | 12 | 56 | 0.7337 | 0.7042 | 0.6338 | 7 | 0.6939 | 0.3061 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_083242.owl` | 68 | 122 | 49 | 0 | 1551 | 3 | 0.83 | 6 | 52 | 0.7673 | 0.7206 | 0.5441 | 8 | 0.6946 | 0.3054 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_085248.owl` | 68 | 98 | 55 | 0 | 1467 | 3 | 0.93 | 28 | 55 | 0.6577 | 0.8088 | 0.75 | 8 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_064211.owl` | 66 | 119 | 52 | 0 | 1420 | 3 | 0.51 | 7 | 53 | 0.8095 | 0.7879 | 0.4242 | 8 | 0.7215 | 0.2785 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_090738.owl` | 66 | 108 | 44 | 0 | 1429 | 4 | 1.03 | 7 | 51 | 0.7059 | 0.6667 | 0.6818 | 9 | 0.6376 | 0.3624 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_090030.owl` | 65 | 108 | 49 | 0 | 1414 | 4 | 1.52 | 12 | 48 | 0.6626 | 0.7538 | 0.8462 | 9 | 0.7072 | 0.2928 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_070335.owl` | 64 | 112 | 41 | 0 | 1450 | 4 | 2.71 | 27 | 53 | 0.6257 | 0.6406 | 1.0469 | 8 | 0.6959 | 0.3041 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_072425.owl` | 63 | 78 | 49 | 0 | 1223 | 4 | 1.3 | 13 | 51 | 0.6142 | 0.7778 | 0.7778 | 7 | 0.6737 | 0.3263 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_084038.owl` | 63 | 67 | 50 | 0 | 819 | 2 | 0.46 | 6 | 53 | 0.7283 | 0.7937 | 0.3968 | 8 | 0.6333 | 0.3667 | 0.0 | 0.1833 | 0.0611 |
| `EDIFACT_combined_turtle_20260405_084605.owl` | 63 | 94 | 56 | 0 | 1359 | 3 | 1.25 | 10 | 51 | 0.6812 | 0.8889 | 0.6984 | 8 | 0.7042 | 0.2958 | 0.0 | 1.0 | 0.9108 |
| `EDIFACT_combined_turtle_20260405_092928.owl` | 63 | 66 | 46 | 0 | 817 | 4 | 0.6 | 6 | 46 | 0.6804 | 0.7302 | 0.4921 | 7 | 0.6286 | 0.3714 | 0.0 | 0.28 | 0.12 |
| `EDIFACT_combined_turtle_20260405_061829.owl` | 61 | 96 | 47 | 0 | 1415 | 4 | 1.32 | 10 | 47 | 0.6667 | 0.7705 | 0.7869 | 7 | 0.6765 | 0.3235 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_071828.owl` | 61 | 70 | 36 | 0 | 917 | 2 | 0.61 | 6 | 48 | 0.6796 | 0.5902 | 0.541 | 6 | 0.6347 | 0.3653 | 0.0 | 0.5389 | 0.479 |
| `EDIFACT_combined_turtle_20260405_092220.owl` | 59 | 101 | 53 | 0 | 1460 | 6 | 1.53 | 9 | 45 | 0.6824 | 0.8983 | 0.7966 | 7 | 0.6291 | 0.3709 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_093420.owl` | 59 | 82 | 47 | 0 | 1263 | 4 | 2.25 | 17 | 45 | 0.5694 | 0.7966 | 1.0508 | 8 | 0.6862 | 0.3138 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_062718.owl` | 0 | 0 | 0 | 0 | 0 | None | None | None | None | None | None | None | None | None | None | None | None | None |

### 3.2 singleAgent

**HermiT inconsistent classes (8):** `ontology.Buyer`, `ontology.Organization`, `ontology.Price`, `ontology.DeliveryParty`, `ontology.AgentRole`, `ontology.OrganizationRoleAssignment`, `ontology.RoleAssignment`, `owl.Nothing`

**Pellet inconsistent classes (8):** `ontology.Buyer`, `ontology.Organization`, `ontology.Price`, `ontology.DeliveryParty`, `ontology.AgentRole`, `ontology.OrganizationRoleAssignment`, `ontology.RoleAssignment`, `owl.Nothing`

**Validation Results**

| File (20) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_ontology_20260304_070119.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_074731.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_ontology_20260304_075831.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_062606.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_063345.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_071919.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_072404.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_112519.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_085410.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_090528.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_093001.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_094903.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_063821.owl` | ✅ | ❌ | ❌ | ⚠️ |
| `EDIFACT_ontology_20260304_071618.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_075320.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_072939.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_092221.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_110544.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_ontology_20260304_111526.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_073706.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File (20) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260304_070119.owl` | 21 | 32 | 13 | 0 | 345 | 4 | 1.29 | 3 | 14 | 0.7442 | 0.619 | 0.5238 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_074731.owl` | 21 | 36 | 12 | 0 | 363 | 1 | 0.19 | 2 | 18 | 0.9 | 0.5714 | 0.1905 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_075831.owl` | 21 | 28 | 13 | 1 | 349 | 1 | 0.33 | 3 | 17 | 0.8 | 0.619 | 0.3333 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_062606.owl` | 20 | 28 | 13 | 0 | 348 | 2 | 0.5 | 3 | 16 | 0.8235 | 0.65 | 0.3 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_063345.owl` | 20 | 32 | 15 | 0 | 362 | 1 | 0.2 | 3 | 18 | 0.8889 | 0.75 | 0.2 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_071919.owl` | 20 | 22 | 14 | 0 | 285 | 1 | 0.3 | 3 | 17 | 0.7857 | 0.7 | 0.3 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_072404.owl` | 20 | 34 | 13 | 0 | 342 | 1 | 0.35 | 3 | 16 | 0.8293 | 0.65 | 0.35 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_112519.owl` | 20 | 28 | 12 | 0 | 302 | 1 | 0.3 | 3 | 16 | 0.8235 | 0.6 | 0.3 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_085410.owl` | 19 | 30 | 9 | 0 | 305 | 1 | 0.05 | 1 | 18 | 0.9677 | 0.4737 | 0.0526 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_090528.owl` | 19 | 30 | 11 | 0 | 341 | 1 | 0.21 | 3 | 17 | 0.8824 | 0.5789 | 0.2105 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_093001.owl` | 19 | 36 | 14 | 0 | 386 | 5 | 1.74 | 4 | 12 | 0.7826 | 0.7368 | 0.5263 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_094903.owl` | 19 | 28 | 15 | 0 | 340 | 2 | 0.37 | 4 | 16 | 0.8235 | 0.7895 | 0.3158 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_063821.owl` | 18 | 13 | 12 | 0 | 224 | 1 | 0.28 | 3 | 15 | 0.7222 | 0.6667 | 0.2778 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_071618.owl` | 18 | 28 | 7 | 0 | 317 | 3 | 0.72 | 3 | 14 | 0.8 | 0.3889 | 0.3889 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_075320.owl` | 18 | 34 | 6 | 0 | 310 | 1 | 0.06 | 1 | 17 | 0.9714 | 0.3333 | 0.0556 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_072939.owl` | 17 | 24 | 8 | 0 | 267 | 1 | 0.24 | 3 | 15 | 0.8571 | 0.4706 | 0.2353 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_092221.owl` | 17 | 28 | 14 | 0 | 339 | 2 | 0.35 | 3 | 14 | 0.8485 | 0.8235 | 0.2941 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_110544.owl` | 17 | 22 | 7 | 0 | 275 | 5 | 1.59 | 4 | 9 | 0.6667 | 0.4118 | 0.6471 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_111526.owl` | 17 | 24 | 9 | 0 | 296 | 1 | 0.06 | 1 | 16 | 0.96 | 0.5294 | 0.0588 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_073706.owl` | 16 | 24 | 8 | 0 | 302 | 1 | 0.06 | 1 | 15 | 0.96 | 0.5 | 0.0625 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

### 3.3 dualAgent

**Validation Results**

| File (20) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_ontology_20260301_222236.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_220437.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221940.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_223501.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_220832.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_224527.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_215924.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_224922.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_225145.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_225409.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221113.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221332.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_222534.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_223750.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_225732.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_230018.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_230338.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_215700.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_224212.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221725.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File (20) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260301_222236.owl` | 22 | 30 | 12 | 0 | 340 | 1 | 0.41 | 4 | 18 | 0.7692 | 0.5455 | 0.4091 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_220437.owl` | 21 | 40 | 3 | 0 | 369 | 2 | 0.43 | 3 | 17 | 0.8333 | 0.1429 | 0.381 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221940.owl` | 21 | 28 | 5 | 0 | 308 | 1 | 0.33 | 3 | 17 | 0.8 | 0.2381 | 0.3333 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_223501.owl` | 21 | 32 | 7 | 0 | 316 | 1 | 0.38 | 3 | 17 | 0.8 | 0.3333 | 0.381 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_220832.owl` | 20 | 38 | 8 | 0 | 352 | 1 | 0.3 | 3 | 16 | 0.8636 | 0.4 | 0.3 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_224527.owl` | 20 | 32 | 13 | 0 | 373 | 1 | 0.2 | 3 | 18 | 0.8889 | 0.65 | 0.2 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_215924.owl` | 19 | 34 | 8 | 0 | 322 | 1 | 0.11 | 1 | 17 | 0.9444 | 0.4211 | 0.1053 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_224922.owl` | 19 | 34 | 7 | 0 | 304 | 1 | 0.32 | 3 | 15 | 0.85 | 0.3684 | 0.3158 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_225145.owl` | 19 | 30 | 9 | 0 | 308 | 2 | 0.47 | 4 | 16 | 0.8108 | 0.4737 | 0.3684 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_225409.owl` | 19 | 30 | 12 | 0 | 315 | 1 | 0.11 | 1 | 17 | 0.9375 | 0.6316 | 0.1053 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221113.owl` | 18 | 28 | 5 | 0 | 261 | 1 | 0.28 | 3 | 15 | 0.8485 | 0.2778 | 0.2778 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221332.owl` | 18 | 32 | 12 | 0 | 327 | 1 | 0.06 | 1 | 17 | 0.9697 | 0.6667 | 0.0556 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_222534.owl` | 18 | 30 | 7 | 0 | 348 | 4 | 1.06 | 3 | 12 | 0.7895 | 0.3889 | 0.4444 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_223750.owl` | 18 | 26 | 15 | 0 | 325 | 1 | 0.22 | 3 | 16 | 0.8667 | 0.8333 | 0.2222 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_225732.owl` | 18 | 26 | 16 | 0 | 338 | 1 | 0.28 | 3 | 15 | 0.8387 | 0.8889 | 0.2778 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_230018.owl` | 18 | 26 | 14 | 0 | 327 | 1 | 0.28 | 3 | 15 | 0.8387 | 0.7778 | 0.2778 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_230338.owl` | 17 | 26 | 14 | 0 | 335 | 1 | 0.06 | 1 | 16 | 0.963 | 0.8235 | 0.0588 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_215700.owl` | 16 | 22 | 9 | 0 | 235 | 1 | 0.25 | 3 | 14 | 0.8462 | 0.5625 | 0.25 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_224212.owl` | 16 | 24 | 8 | 0 | 292 | 1 | 0.25 | 3 | 14 | 0.8571 | 0.5 | 0.25 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221725.owl` | 13 | 22 | 8 | 0 | 227 | 1 | 0.08 | 1 | 12 | 0.9565 | 0.6154 | 0.0769 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

### 3.4 triAgent

**HermiT inconsistent classes (5):** `ontology.BuyerRole`, `ontology.GLNIdentifier`, `ontology.InvoiceMessage`, `owl.Nothing`, `ontology.SimpleDataElement`

**Pellet inconsistent classes (5):** `ontology.BuyerRole`, `ontology.GLNIdentifier`, `ontology.InvoiceMessage`, `owl.Nothing`, `ontology.SimpleDataElement`

**Validation Results**

| File (20) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_ontology_20260302_075401.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260302_081000.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260302_142221.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_ontology_20260303_063400.owl` | ✅ | ❌ | ❌ | ❌ |
| `EDIFACT_ontology_20260302_071802.owl` | ✅ | ✅ | ❌ | ⚠️ |
| `EDIFACT_ontology_20260302_124024.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260303_094621.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260302_140235.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_072631.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260302_130930.owl` | ✅ | ✅ | ❌ | ✅ |
| `EDIFACT_ontology_20260302_133553.owl` | ✅ | ✅ | ✅ | ⚠️ |
| `EDIFACT_ontology_20260302_073654.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_085821.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260303_093322.owl` | ✅ | ✅ | ❌ | ✅ |
| `EDIFACT_ontology_20260303_061520.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_064029.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_ontology_20260303_070100.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260302_082612.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_091850.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_093956.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File (20) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260302_075401.owl` | 39 | 68 | 2 | 0 | 623 | 2 | 0.74 | 16 | 35 | 0.7391 | 0.0513 | 0.6154 | 2 | 0.7982 | 0.2018 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_081000.owl` | 37 | 30 | 8 | 0 | 367 | 2 | 0.81 | 8 | 29 | 0.5769 | 0.2162 | 0.5946 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_142221.owl` | 35 | 0 | 0 | 0 | 165 | 3 | 1.4 | 22 | 31 | 0.0 | 0.0 | 1.0571 | 1 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_063400.owl` | 32 | 40 | 5 | 0 | 427 | 3 | 0.72 | 9 | 25 | 0.6897 | 0.1562 | 0.5625 | 6 | 0.8961 | 0.1039 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_071802.owl` | 30 | 17 | 13 | 0 | 296 | 2 | 0.37 | 6 | 26 | 0.6296 | 0.4333 | 0.3333 | 3 | 0.9667 | 0.0333 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_124024.owl` | 30 | 27 | 2 | 0 | 314 | 1 | 0.3 | 3 | 25 | 0.75 | 0.0667 | 0.3 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_094621.owl` | 30 | 42 | 7 | 0 | 440 | 1 | 0.37 | 3 | 24 | 0.7925 | 0.2333 | 0.3667 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_140235.owl` | 29 | 40 | 14 | 0 | 426 | 2 | 0.38 | 3 | 24 | 0.7843 | 0.4828 | 0.3793 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_072631.owl` | 29 | 2 | 9 | 0 | 173 | 2 | 0.28 | 2 | 24 | 0.2222 | 0.3103 | 0.2414 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_130930.owl` | 28 | 44 | 13 | 0 | 460 | 2 | 0.39 | 3 | 24 | 0.8462 | 0.4643 | 0.2857 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_133553.owl` | 28 | 23 | 3 | 0 | 270 | 1 | 0.25 | 5 | 25 | 0.7667 | 0.1071 | 0.25 | 5 | 0.9444 | 0.0556 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_073654.owl` | 27 | 38 | 2 | 0 | 396 | 3 | 0.74 | 3 | 20 | 0.76 | 0.0741 | 0.4444 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_085821.owl` | 27 | 34 | 3 | 0 | 365 | 1 | 0.3 | 5 | 24 | 0.8095 | 0.1111 | 0.2963 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_093322.owl` | 27 | 36 | 3 | 0 | 360 | 2 | 0.33 | 3 | 22 | 0.8182 | 0.1111 | 0.2963 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_061520.owl` | 24 | 38 | 11 | 0 | 444 | 1 | 0.17 | 2 | 21 | 0.9048 | 0.4583 | 0.1667 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_064029.owl` | 24 | 36 | 11 | 0 | 414 | 1 | 0.29 | 3 | 20 | 0.8372 | 0.4583 | 0.2917 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_070100.owl` | 24 | 34 | 12 | 0 | 411 | 1 | 0.21 | 2 | 21 | 0.8718 | 0.5 | 0.2083 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_082612.owl` | 22 | 42 | 5 | 0 | 405 | 2 | 0.32 | 3 | 20 | 0.913 | 0.2273 | 0.1818 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_091850.owl` | 22 | 44 | 4 | 0 | 429 | 1 | 0.27 | 5 | 20 | 0.88 | 0.1818 | 0.2727 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_093956.owl` | 0 | 0 | 0 | 0 | 3 | 0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

---

## 4. Comparison with Reference Ontologies

Values compared against **TUMedifact (full)** and **TUMedifact (trimmed)**.

| Agent Type | Triples avg | vs Full | vs Trimmed | Classes avg | vs Full | vs Trimmed |
|------------|:-----------:|:-------:|:----------:|:-----------:|:-------:|:----------:|
| **workflow** | 1344.3 | -1326 | -923 | 66.2 | +35 | +35 |
| **singleAgent** | 319.9 | -2350 | -1947 | 18.9 | -12 | -12 |
| **dualAgent** | 316.1 | -2354 | -1951 | 18.6 | -12 | -12 |
| **triAgent** | 359.4 | -2311 | -1908 | 27.2 | -4 | -4 |

_Reference — TUMedifact (full): 2670 triples, 31 classes_  
_Reference — TUMedifact (trimmed): 2267 triples, 31 classes_

---

## 5. Key Observations

- **workflow**: HermiT consistency rate is 5.0% — 19 ontologies are inconsistent.
- **workflow**: 50 OOPS pitfall occurrence(s) detected across runs (most common: P22, P20, P13, P04, P05, P19, P08, P10, P12).
- **workflow**: Average class count is 66.2 (213.5% of reference full ontology's 31 classes).
- **singleAgent**: HermiT consistency rate is 85.0% — 3 ontologies are inconsistent.
- **singleAgent**: Average class count is 18.9 (61.0% of reference full ontology's 31 classes).
- **dualAgent**: Average class count is 18.6 (60.0% of reference full ontology's 31 classes).
- **triAgent**: HermiT consistency rate is 85.0% — 3 ontologies are inconsistent.
- **triAgent**: 10 OOPS pitfall occurrence(s) detected across runs (most common: P04, P20, P22, P12, P13).
- **triAgent**: Average class count is 27.2 (87.7% of reference full ontology's 31 classes).

---

## 6. Metric Definitions

### Structural Ratios (OntoQA Framework)
- **RR (Relationship Richness)** = `|ObjectProperties| / (|subClassOf axioms| + |ObjectProperties|)`. Ratio of non-taxonomic to all relations. Higher values indicate a more interconnected graph rather than a flat taxonomy.
- **AR (Attribute Richness)** = `|DatatypeProperties| / |Classes|`. Average number of data properties per class. Higher values indicate richer per-instance data modelling.
- **IR (Inheritance Richness)** = `|subClassOf triples| / |all named classes|`. Average number of inheritance edges per class (including leaf classes). Distinct from Avg Branching which only considers parent classes.

### Axiom Complexity
- **Axiom Diversity Score** (0–10): Count of distinct advanced OWL constructs present in the ontology, out of: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, `owl:equivalentClass`, `owl:unionOf`, `owl:intersectionOf`, `owl:hasValue`, and cardinality restrictions (`owl:cardinality`, `owl:minCardinality`, `owl:maxCardinality`, counted as one). A score of 0 means the ontology uses only declarations and `rdfs:subClassOf`; a score of 10 means all construct types are present.

### Lexical & Annotation Quality
- **Naming: Strict CamelCase** (0.0–1.0): Fraction of named entities matching strict Semantic Web conventions — UpperCamelCase for classes (`^[A-Z][A-Za-z0-9]*$`), lowerCamelCase for properties (`^[a-z][A-Za-z0-9]*$`). No underscores.
- **Naming: Underscore Style** (0.0–1.0): Fraction that follow camelCase with underscores (e.g. `Cl_Invoice`), a common prefix-based variation that would pass if underscores are allowed but failed the strict check.
- **Naming: Non-conformant** (0.0–1.0): Fraction that match neither pattern. The three fractions sum to 1.0.
- **Label Coverage** (0.0–1.0): Fraction of named entities (classes + all property types) that have at least one `rdfs:label` triple. 1.0 = fully labelled.
- **Comment Coverage** (0.0–1.0): Fraction of named entities that have at least one `rdfs:comment` triple. 1.0 = fully documented.

### Hierarchy Metrics
- **Max Depth**: Length of the longest `rdfs:subClassOf` chain from a root class (no parent) to a leaf class. Computed via BFS.
- **Avg Depth**: Mean depth across all named classes.
- **Max Branching**: Highest number of direct subclasses any single class has.
- **Avg Branching**: Mean number of direct subclasses per class, computed only over classes that have at least one child (excludes leaf classes).
- **Leaf Classes**: Count of classes with no direct subclasses.
