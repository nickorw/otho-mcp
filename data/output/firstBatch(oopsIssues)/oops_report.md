# OOPS! Pitfall Analysis Report

**Generated:** 2026-04-04 18:22:59  
**Ontologies analysed:** 20  
**Path:** `data/output/ontologies`

---

## Summary

| Result | Count |
|--------|-------|
| ✅ Passed (no pitfalls) | 0 |
| ⚠️ Pitfalls found | 16 |
| ❌ Unable to analyse | 4 |
| **Total** | **20** |

---

## ✅ Passed — No Pitfalls Detected

_None_

---

## ❌ Unable to Analyse

### `EDIFACT_combined_turtle_20260301_223204.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

### `EDIFACT_combined_turtle_20260301_230929.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

### `EDIFACT_combined_turtle_20260301_232450.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

### `EDIFACT_combined_turtle_20260301_234726.owl`

> **Error:** OOPS could not analyse the ontology (wrong_execution response)

---

## ⚠️ Pitfalls Found

### `EDIFACT_combined_turtle_20260301_214840.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 4 |
| **Total** | **6** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 1

##### 🟠 P11 — Missing domain or range in properties `[Important]`

**Description:** Object and/or datatype properties without domain or range (or none of them) are included in the ontology. 	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 9

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 172

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 52

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_215419.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 5 |
| **Total** | **6** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 6

##### 🟡 P02 — Creating synonyms as classes `[Minor]`

**Description:** Several classes whose identifiers are synonyms are created and defined as equivalent (owl:equivalentClass) in the same namespace. This pitfall is related to the guidelines presented in [2], which explain that synonyms for the same concept do not represent different classes.	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 8

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 150

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 34

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_215907.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 1 |
| 🟡 Minor | 3 |
| **Total** | **4** |

#### Detailed Findings

##### 🟠 P24 — Using recursive definitions `[Important]`

**Description:** An ontology element (a class, an object property or a datatype property) is used in its own definition. Some examples of this would be: (a) the definition of a class as the enumeration of several classes including itself;  (b) the appearance of a class within its owl:equivalentClass or rdfs:subClassOf axioms; (c) the appearance of an object property in its rdfs:domain or range rdfs:range definitions; or (d) the appearance of a datatype property in its rdfs:domain definition.	

**Affected elements:** 1

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 166

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 41

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_220409.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 0 |
| 🟡 Minor | 5 |
| **Total** | **5** |

#### Detailed Findings

##### 🟡 P02 — Creating synonyms as classes `[Minor]`

**Description:** Several classes whose identifiers are synonyms are created and defined as equivalent (owl:equivalentClass) in the same namespace. This pitfall is related to the guidelines presented in [2], which explain that synonyms for the same concept do not represent different classes.	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 2

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 159

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 49

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_220919.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **5** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 3

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 7

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 163

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 34

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_221415.owl`

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

**Affected elements:** 1

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 7

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 6

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 170

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 45

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_221951.owl`

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

**Affected elements:** 1

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 5

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 173

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 27

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_222612.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 4 |
| **Total** | **6** |

#### Detailed Findings

##### 🔴 P05 — Defining wrong inverse relationships `[Critical]`

**Description:** Two relationships are defined as inverse relations when they are not necessarily inverse.	

**Affected elements:** 2

##### 🟠 P12 — Equivalent properties not explicitly declared `[Important]`

**Description:** The ontology lacks information about equivalent properties (owl:equivalentProperty) in the cases of duplicated relationships and/or attributes.	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 8

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 163

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 36

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_223728.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 1 |
| 🟡 Minor | 5 |
| **Total** | **6** |

#### Detailed Findings

##### 🟠 P11 — Missing domain or range in properties `[Important]`

**Description:** Object and/or datatype properties without domain or range (or none of them) are included in the ontology. 	

**Affected elements:** 1

##### 🟡 P02 — Creating synonyms as classes `[Minor]`

**Description:** Several classes whose identifiers are synonyms are created and defined as equivalent (owl:equivalentClass) in the same namespace. This pitfall is related to the guidelines presented in [2], which explain that synonyms for the same concept do not represent different classes.	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 4

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 191

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 51

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_230354.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 4 |
| **Total** | **6** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 4

##### 🟠 P24 — Using recursive definitions `[Important]`

**Description:** An ontology element (a class, an object property or a datatype property) is used in its own definition. Some examples of this would be: (a) the definition of a class as the enumeration of several classes including itself;  (b) the appearance of a class within its owl:equivalentClass or rdfs:subClassOf axioms; (c) the appearance of an object property in its rdfs:domain or range rdfs:range definitions; or (d) the appearance of a datatype property in its rdfs:domain definition.	

**Affected elements:** 2

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 4

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 186

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 56

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_231410.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **5** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 6

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 148

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 47

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_231957.owl`

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

**Affected elements:** 2

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 6

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 147

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 43

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_232958.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 Important | 1 |
| 🟡 Minor | 4 |
| **Total** | **5** |

#### Detailed Findings

##### 🟠 P12 — Equivalent properties not explicitly declared `[Important]`

**Description:** The ontology lacks information about equivalent properties (owl:equivalentProperty) in the cases of duplicated relationships and/or attributes.	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 10

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 174

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 42

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_233503.owl`

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

**Affected elements:** 1

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 2

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 4

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 182

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 49

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_234116.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 1 |
| 🟡 Minor | 4 |
| **Total** | **6** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 3

##### 🟠 P12 — Equivalent properties not explicitly declared `[Important]`

**Description:** The ontology lacks information about equivalent properties (owl:equivalentProperty) in the cases of duplicated relationships and/or attributes.	

**Affected elements:** 1

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 4

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 168

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 47

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---

### `EDIFACT_combined_turtle_20260301_235347.owl`

#### Severity Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Important | 0 |
| 🟡 Minor | 4 |
| **Total** | **5** |

#### Detailed Findings

##### 🔴 P19 — Defining multiple domains or ranges in properties `[Critical]`

**Description:** The domain or range (or both) of a property (relationships and attributes) is defined by stating more than one rdfs:domain or rdfs:range statements. In OWL multiple rdfs:domain or rdfs:range axioms are allowed, but they are interpreted as conjunction, being, therefore, equivalent to the construct owl:intersectionOf. This pitfall is related to the common error that appears when defining domains and ranges described in [7].	

**Affected elements:** 8

##### 🟡 P04 — Creating unconnected ontology elements `[Minor]`

**Description:** Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.	

**Affected elements:** 9

##### 🟡 P08 — Missing annotations `[Minor]`

**Description:** This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].	

**Affected elements:** 122

##### 🟡 P13 — Inverse relationships not explicitly declared `[Minor]`

**Description:** This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.	

**Affected elements:** 54

##### 🟡 P22 — Using different naming conventions in the ontology `[Minor]`

**Description:** The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as "-" or "_") . Some notions about naming conventions are provided in [2].	

**Affected elements:** 1

---
