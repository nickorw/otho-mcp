# OOPS! Pitfall Analysis Report

**Generated:** 2026-04-05 10:22:48  
**Ontologies analysed:** 20  
**Path:** `data/output/ontologies`

---

## Summary

| Result | Count |
|--------|-------|
| ✅ Passed (no pitfalls) | 1 |
| ⚠️ Pitfalls found | 14 |
| ❌ Unable to analyse | 5 |
| **Total** | **20** |

---

## ✅ Passed — No Pitfalls Detected

- `EDIFACT_combined_turtle_20260405_085248.owl`

---

## ❌ Unable to Analyse

### `EDIFACT_combined_turtle_20260405_062718.owl`

> **Error:** Failed to convert Turtle to RDF/XML: at line 445 of <>:
Bad syntax (objectList expected) at ^ in:
"...b'rse declaration (P13 fix)\n    owl:inverseOf :involvesInvoice'^b' .\n\n:hasInvoiceRole a owl:ObjectProperty ;\n    rdfs:domain :'..."

### `EDIFACT_combined_turtle_20260405_065755.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

### `EDIFACT_combined_turtle_20260405_071828.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

### `EDIFACT_combined_turtle_20260405_084038.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

### `EDIFACT_combined_turtle_20260405_092928.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

---

## ⚠️ Pitfalls Found

### `EDIFACT_combined_turtle_20260405_061829.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **4** |

#### Detailed Findings

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 27

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_063353.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 2 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **6** |

#### Detailed Findings

##### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 12

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 10

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 2

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_064211.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **3** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 57

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_064934.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 3 |
| **Total** | **5** |

#### Detailed Findings

##### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 56

##### 🟠 P10 — Missing disjointness `[Important]`

**Description:** The ontology lacks disjoint axioms between classes or between properties that should be defined as disjoint. This pitfall is related with the guidelines provided in [6], [2] and [7].	

**Affected elements:** 0

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 35

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_070335.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 3 |
| **Total** | **5** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

##### 🟠 P12 — Equivalent properties not explicitly declared `[Important]`

**Description:** The ontology lacks information about equivalent properties (owl:equivalentProperty) in the cases of duplicated relationships and/or attributes.	

**Affected elements:** 1

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 5

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 45

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_071057.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

#### Detailed Findings

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_072425.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

#### Detailed Findings

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 30

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_083242.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **3** |

#### Detailed Findings

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 2

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 19

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_084605.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **4** |

#### Detailed Findings

##### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 1

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 19

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 4

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_090030.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **3** |

#### Detailed Findings

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 12

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_090738.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **4** |

#### Detailed Findings

##### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 2

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 2

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 12

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_091438.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

#### Detailed Findings

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 54

---

### `EDIFACT_combined_turtle_20260405_092220.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **4** |

#### Detailed Findings

##### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 2

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 1

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260405_093420.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **3** |

#### Detailed Findings

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

##### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 37

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---
