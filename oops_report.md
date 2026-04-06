# OOPS! Pitfall Analysis Report

**Generated:** 2026-04-05 21:08:13  
**Ontologies analysed:** 80  
**Groups:** dualAgent, singleAgent, triAgent, workflow

---

## Overall Summary

| Group | Total | ✅ Passed | 🟡 Passed w/ Minor Pitfalls | 🟠 Serious Pitfalls | ❌ Failed |
|-------|-------|-----------|----------------------------|---------------------|---------|
| dualAgent | 20 | 20 | 0 | 0 | 0 |
| singleAgent | 20 | 19 | 0 | 0 | 1 |
| triAgent | 20 | 11 | 6 | 1 | 2 |
| workflow | 20 | 1 | 7 | 7 | 5 |
| **Total** | **80** | **51** | **13** | **8** | **8** |

---

## dualAgent

**Ontologies analysed:** 20  
**Path:** `data/FinalResults/Ontologies/dualAgent/All`

| Result | Count |
|--------|-------|
| ✅ Passed | 20 |
| 🟡 Passed w/ Minor Pitfalls | 0 |
| 🟠 Serious Pitfalls | 0 |
| ❌ Failed | 0 |
| **Total** | **20** |

### ✅ Passed — No Pitfalls Detected

- `EDIFACT_ontology_20260301_215700.owl`
- `EDIFACT_ontology_20260301_215924.owl`
- `EDIFACT_ontology_20260301_220437.owl`
- `EDIFACT_ontology_20260301_220832.owl`
- `EDIFACT_ontology_20260301_221113.owl`
- `EDIFACT_ontology_20260301_221332.owl`
- `EDIFACT_ontology_20260301_221725.owl`
- `EDIFACT_ontology_20260301_221940.owl`
- `EDIFACT_ontology_20260301_222236.owl`
- `EDIFACT_ontology_20260301_222534.owl`
- `EDIFACT_ontology_20260301_223501.owl`
- `EDIFACT_ontology_20260301_223750.owl`
- `EDIFACT_ontology_20260301_224212.owl`
- `EDIFACT_ontology_20260301_224527.owl`
- `EDIFACT_ontology_20260301_224922.owl`
- `EDIFACT_ontology_20260301_225145.owl`
- `EDIFACT_ontology_20260301_225409.owl`
- `EDIFACT_ontology_20260301_225732.owl`
- `EDIFACT_ontology_20260301_230018.owl`
- `EDIFACT_ontology_20260301_230338.owl`

### ❌ Failed — Unable to Analyse

_None_

### 🟡 Passed w/ Minor Pitfalls

_None_

### 🟠 Serious Pitfalls

_None_

---

## singleAgent

**Ontologies analysed:** 20  
**Path:** `data/FinalResults/Ontologies/singleAgent/All`

| Result | Count |
|--------|-------|
| ✅ Passed | 19 |
| 🟡 Passed w/ Minor Pitfalls | 0 |
| 🟠 Serious Pitfalls | 0 |
| ❌ Failed | 1 |
| **Total** | **20** |

### ✅ Passed — No Pitfalls Detected

- `EDIFACT_ontology_20260304_062606.owl`
- `EDIFACT_ontology_20260304_063345.owl`
- `EDIFACT_ontology_20260304_070119.owl`
- `EDIFACT_ontology_20260304_071618.owl`
- `EDIFACT_ontology_20260304_071919.owl`
- `EDIFACT_ontology_20260304_072404.owl`
- `EDIFACT_ontology_20260304_072939.owl`
- `EDIFACT_ontology_20260304_073706.owl`
- `EDIFACT_ontology_20260304_074731.owl`
- `EDIFACT_ontology_20260304_075320.owl`
- `EDIFACT_ontology_20260304_075831.owl`
- `EDIFACT_ontology_20260304_085410.owl`
- `EDIFACT_ontology_20260304_090528.owl`
- `EDIFACT_ontology_20260304_092221.owl`
- `EDIFACT_ontology_20260304_093001.owl`
- `EDIFACT_ontology_20260304_094903.owl`
- `EDIFACT_ontology_20260304_110544.owl`
- `EDIFACT_ontology_20260304_111526.owl`
- `EDIFACT_ontology_20260304_112519.owl`

### ❌ Failed — Unable to Analyse

#### `EDIFACT_ontology_20260304_063821.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)


### 🟡 Passed w/ Minor Pitfalls

_None_

### 🟠 Serious Pitfalls

_None_

---

## triAgent

**Ontologies analysed:** 20  
**Path:** `data/FinalResults/Ontologies/triAgent/All`

| Result | Count |
|--------|-------|
| ✅ Passed | 11 |
| 🟡 Passed w/ Minor Pitfalls | 6 |
| 🟠 Serious Pitfalls | 1 |
| ❌ Failed | 2 |
| **Total** | **20** |

### ✅ Passed — No Pitfalls Detected

- `EDIFACT_ontology_20260302_073654.owl`
- `EDIFACT_ontology_20260302_081000.owl`
- `EDIFACT_ontology_20260302_082612.owl`
- `EDIFACT_ontology_20260302_130930.owl`
- `EDIFACT_ontology_20260302_140235.owl`
- `EDIFACT_ontology_20260303_061520.owl`
- `EDIFACT_ontology_20260303_064029.owl`
- `EDIFACT_ontology_20260303_070100.owl`
- `EDIFACT_ontology_20260303_091850.owl`
- `EDIFACT_ontology_20260303_093322.owl`
- `EDIFACT_ontology_20260303_093956.owl`

### ❌ Failed — Unable to Analyse

#### `EDIFACT_ontology_20260302_071802.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

#### `EDIFACT_ontology_20260302_133553.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)


### 🟡 Passed w/ Minor Pitfalls

#### `EDIFACT_ontology_20260302_124024.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 1 |
| **Total** | **1** |

##### Detailed Findings

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 27

#### `EDIFACT_ontology_20260302_142221.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 1 |
| **Total** | **1** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 10

#### `EDIFACT_ontology_20260303_063400.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 1 |
| **Total** | **1** |

##### Detailed Findings

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_ontology_20260303_072631.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 1 |
| **Total** | **1** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 9

#### `EDIFACT_ontology_20260303_085821.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 1 |
| **Total** | **1** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

#### `EDIFACT_ontology_20260303_094621.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 3

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 3

### 🟠 Serious Pitfalls

#### `EDIFACT_ontology_20260302_075401.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 1 |
| 🟡 Minor | 2 |
| **Total** | **3** |

##### Detailed Findings

###### 🟠 P12 — Equivalent properties not explicitly declared `[Important]`

**Description:** The ontology lacks information about equivalent properties (owl:equivalentProperty) in the cases of duplicated relationships and/or attributes.	

**Affected elements:** 2

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 4

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

## workflow

**Ontologies analysed:** 20  
**Path:** `data/FinalResults/Ontologies/workflow/All`

| Result | Count |
|--------|-------|
| ✅ Passed | 1 |
| 🟡 Passed w/ Minor Pitfalls | 7 |
| 🟠 Serious Pitfalls | 7 |
| ❌ Failed | 5 |
| **Total** | **20** |

### ✅ Passed — No Pitfalls Detected

- `EDIFACT_combined_turtle_20260405_085248.owl`

### ❌ Failed — Unable to Analyse

#### `EDIFACT_combined_turtle_20260405_062718.owl`

> **Error:** Failed to convert Turtle to RDF/XML: at line 445 of <>:
Bad syntax (objectList expected) at ^ in:
"...b'rse declaration (P13 fix)\n    owl:inverseOf :involvesInvoice'^b' .\n\n:hasInvoiceRole a owl:ObjectProperty ;\n    rdfs:domain :'..."

#### `EDIFACT_combined_turtle_20260405_065755.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

#### `EDIFACT_combined_turtle_20260405_071828.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

#### `EDIFACT_combined_turtle_20260405_084038.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

#### `EDIFACT_combined_turtle_20260405_092928.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)


### 🟡 Passed w/ Minor Pitfalls

#### `EDIFACT_combined_turtle_20260405_061829.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **4** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 27

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_071057.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_072425.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

##### Detailed Findings

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 30

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_083242.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **3** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 2

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 19

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_090030.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **3** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 12

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_091438.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **2** |

##### Detailed Findings

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 54

#### `EDIFACT_combined_turtle_20260405_093420.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **3** |

##### Detailed Findings

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 37

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

### 🟠 Serious Pitfalls

#### `EDIFACT_combined_turtle_20260405_063353.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 2 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **6** |

##### Detailed Findings

###### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 12

###### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 10

###### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 1

###### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 2

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_064211.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 2 |
| **Total** | **3** |

##### Detailed Findings

###### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 57

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_064934.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 3 |
| **Total** | **5** |

##### Detailed Findings

###### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 56

###### 🟠 P10 — Missing disjointness `[Important]`

**Description:** The ontology lacks disjoint axioms between classes or between properties that should be defined as disjoint. This pitfall is related with the guidelines provided in [6], [2] and [7].	

**Affected elements:** 0

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 35

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_070335.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 3 |
| **Total** | **5** |

##### Detailed Findings

###### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

###### 🟠 P12 — Equivalent properties not explicitly declared `[Important]`

**Description:** The ontology lacks information about equivalent properties (owl:equivalentProperty) in the cases of duplicated relationships and/or attributes.	

**Affected elements:** 1

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 5

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 45

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_084605.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **4** |

##### Detailed Findings

###### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 1

###### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 19

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 4

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_090738.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **4** |

##### Detailed Findings

###### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 2

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 2

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 12

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

#### `EDIFACT_combined_turtle_20260405_092220.owl`

##### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 3 |
| **Total** | **4** |

##### Detailed Findings

###### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 2

###### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 1

###### 🟡 P20 — Misusing ontology annotations `[Minor]`

**Description:** The contents of some annotation properties are swapped or misused. This pitfall might affect annotation properties related to natural language information (for example, annotations for naming such as rdfs:label or for providing descriptions such as rdfs:comment). Other types of annotation could also be affected as temporal, versioning information, among others.	

**Affected elements:** 1

###### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---
