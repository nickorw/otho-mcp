# Ontology Quality Report — Selected Ontologies

> Derived from `ontology_report.md`
> Date: 2026-04-05
> Scope: One selected ontology per agent type, representing the best candidate from each run set.

---

## 1. Reference Ontologies (TUMedifact)

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

## 2. Selected Ontologies

| Label | Agent Type | Selected File |
|-------|------------|---------------|
| **D** | **dualAgent** | `EDIFACT_ontology_20260301_222236.owl` |
| **C** | **singleAgent** | `EDIFACT_ontology_20260304_093001.owl` |
| **A** | **triAgent** | `EDIFACT_ontology_20260303_070100.owl` |
| **B** | **workflow** | `EDIFACT_combined_turtle_20260405_085248.owl` |

---

## 3. Validation Results

_OOPS column legend: ✅ no pitfalls · ❌ pitfalls found · ⚠️ OOPS failed to run_

| File | Agent Type | Syntax | HermiT | Pellet | OOPS |
|------|------------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | — | ✅ | — | — | — |
| `EDIFACT_ontology_20260301_222236.owl` | dualAgent | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_093001.owl` | singleAgent | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_070100.owl` | triAgent | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_combined_turtle_20260405_085248.owl` | workflow | ✅ | ❌ | ❌ | ✅ |

> **Note — workflow ontology:** HermiT crashes with `UnsupportedDatatypeException` on `xsd:date` (not in OWL 2 datatype map). Pellet returns inconsistent. This is the best-ranked ontology across the full workflow set of 20; no workflow ontology passes both reasoners.

---

## 4. Structural Metrics

| File | Agent Type | Classes | Obj Props | Data Props | Ann Props | Triples |
|------|------------|:-------:|:---------:|:----------:|:---------:|:-------:|
| **TUMedifact (trimmed)** _(baseline)_ | — | **31** | **10** | **261** | **9** | **2267** |
| `EDIFACT_ontology_20260301_222236.owl` | dualAgent | 22 | 30 | 12 | 0 | 340 |
| `EDIFACT_ontology_20260304_093001.owl` | singleAgent | 19 | 36 | 14 | 0 | 386 |
| `EDIFACT_ontology_20260303_070100.owl` | triAgent | 24 | 34 | 12 | 0 | 411 |
| `EDIFACT_combined_turtle_20260405_085248.owl` | workflow | 68 | 98 | 55 | 0 | 1467 |

---

## 5. Hierarchy Metrics

| File | Agent Type | Max Depth | Avg Depth | Max Branch | Leaves |
|------|------------|:---------:|:---------:|:----------:|:------:|
| **TUMedifact (trimmed)** _(baseline)_ | — | **1** | **0.81** | **21** | **26** |
| `EDIFACT_ontology_20260301_222236.owl` | dualAgent | 1 | 0.41 | 4 | 18 |
| `EDIFACT_ontology_20260304_093001.owl` | singleAgent | 5 | 1.74 | 4 | 12 |
| `EDIFACT_ontology_20260303_070100.owl` | triAgent | 1 | 0.21 | 2 | 21 |
| `EDIFACT_combined_turtle_20260405_085248.owl` | workflow | 3 | 0.93 | 28 | 55 |

---

## 6. OntoQA Structural Ratios

| File | Agent Type | RR | AR | IR |
|------|------------|:--:|:--:|:--:|
| **TUMedifact (trimmed)** _(baseline)_ | — | **0.2778** | **8.4194** | **0.8387** |
| `EDIFACT_ontology_20260301_222236.owl` | dualAgent | 0.7692 | 0.5455 | 0.4091 |
| `EDIFACT_ontology_20260304_093001.owl` | singleAgent | 0.7826 | 0.7368 | 0.5263 |
| `EDIFACT_ontology_20260303_070100.owl` | triAgent | 0.8718 | 0.5000 | 0.2083 |
| `EDIFACT_combined_turtle_20260405_085248.owl` | workflow | 0.6577 | 0.8088 | 0.7500 |

---

## 7. Axiom Complexity & Lexical Quality

| File | Agent Type | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|------------|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | — | **2** | **0.987** | **0.000** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260301_222236.owl` | dualAgent | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_093001.owl` | singleAgent | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_070100.owl` | triAgent | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_combined_turtle_20260405_085248.owl` | workflow | 8 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

---

## 8. Comparison with Reference Ontologies

Values compared against **TUMedifact (full)** (2670 triples, 31 classes) and **TUMedifact (trimmed)** (2267 triples, 31 classes).

| File | Agent Type | Triples | vs Full | vs Trimmed | Classes | vs Full | vs Trimmed |
|------|------------|:-------:|:-------:|:----------:|:-------:|:-------:|:----------:|
| `EDIFACT_ontology_20260301_222236.owl` | dualAgent | 340 | -2330 | -1927 | 22 | -9 | -9 |
| `EDIFACT_ontology_20260304_093001.owl` | singleAgent | 386 | -2284 | -1881 | 19 | -12 | -12 |
| `EDIFACT_ontology_20260303_070100.owl` | triAgent | 411 | -2259 | -1856 | 24 | -7 | -7 |
| `EDIFACT_combined_turtle_20260405_085248.owl` | workflow | 1467 | -1203 | -800 | 68 | +37 | +37 |

---

## 9. Key Observations

- **dualAgent** (`222236`): Fully consistent (HermiT ✅, Pellet ✅, OOPS ✅). Compact at 22 classes / 340 triples. Lowest axiom diversity (6) of the selected set.
- **singleAgent** (`093001`): Fully consistent. Deepest hierarchy of the selected set (max depth 5, avg depth 1.74). Highest AR (0.7368) among non-workflow selections. 19 classes / 386 triples.
- **triAgent** (`070100`): Fully consistent. Highest RR (0.8718) of the selected set. Very flat taxonomy (max depth 1, avg depth 0.21). 24 classes / 411 triples. Also highest axiom diversity (7).
- **workflow** (`085248`): Best-ranked across 20 workflow ontologies but fails both reasoners — HermiT crashes on `xsd:date` (OWL 2 DL violation), Pellet finds inconsistency. Substantially larger (68 classes / 1467 triples). OOPS clean. Highest axiom diversity (8) and AR (0.8088) of the selected set.

---

## 10. Metric Definitions

### Structural Ratios (OntoQA Framework)
- **RR (Relationship Richness)** = `|ObjectProperties| / (|subClassOf axioms| + |ObjectProperties|)`. Ratio of non-taxonomic to all relations.
- **AR (Attribute Richness)** = `|DatatypeProperties| / |Classes|`. Average number of data properties per class.
- **IR (Inheritance Richness)** = `|subClassOf triples| / |all named classes|`. Average inheritance edges per class.

### Axiom Complexity
- **Axiom Diversity Score** (0–10): Count of distinct advanced OWL constructs present, out of: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, `owl:equivalentClass`, `owl:unionOf`, `owl:intersectionOf`, `owl:hasValue`, and cardinality restrictions (counted as one).

### Lexical & Annotation Quality
- **Naming: Strict CamelCase** (0.0–1.0): Fraction of named entities matching UpperCamelCase (classes) / lowerCamelCase (properties), no underscores.
- **Naming: Underscore Style** (0.0–1.0): Fraction following camelCase with underscores (e.g. `Cl_Invoice`).
- **Naming: Non-conformant** (0.0–1.0): Fraction matching neither pattern. The three fractions sum to 1.0.
- **Label Coverage** (0.0–1.0): Fraction of named entities with at least one `rdfs:label`.
- **Comment Coverage** (0.0–1.0): Fraction of named entities with at least one `rdfs:comment`.

### Hierarchy Metrics
- **Max Depth**: Longest `rdfs:subClassOf` chain from root to leaf.
- **Avg Depth**: Mean depth across all named classes.
- **Max Branching**: Highest number of direct subclasses any single class has.
- **Avg Branching**: Mean direct subclasses per non-leaf class.
- **Leaf Classes**: Classes with no direct subclasses.
