# Ontology Quality Report

> Generated automatically from `generate_ontology_report.py`  
> Date: 2026-03-08

---

**Validation Results**

| File | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| `A.owl` | ✅ | ✅ | ✅ | ✅ |
| `B.owl` | ✅ | ❌ | ❌ | ✅ |
| `C.owl` | ✅ | ✅ | ✅ | ✅ |
| `D.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| `A.owl` | 24 | 34 | 12 | 0 | 411 | 1 | 0.21 | 2 | 21 | 0.8718 | 0.5 | 0.2083 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `B.owl` | 74 | 69 | 46 | 0 | 1045 | 4 | 0.77 | 8 | 55 | 0.6509 | 0.6216 | 0.5 | 6 | 0.6085 | 0.3915 | 0.0 | 0.5291 | 0.3862 |
| `C.owl` | 19 | 36 | 14 | 0 | 386 | 5 | 1.74 | 4 | 12 | 0.7826 | 0.7368 | 0.5263 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `D.owl` | 22 | 30 | 12 | 0 | 340 | 1 | 0.41 | 4 | 18 | 0.7692 | 0.5455 | 0.4091 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

---

## Metric Definitions

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
