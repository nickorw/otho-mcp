# Ontology Ranking Report — EDIFACT Invoice Domain
> Evaluator: Expert Ontology Engineer (automated agent)
> Date: 2026-04-12
> Files evaluated: A.owl (triAgent), C.owl (singleAgent), D.owl (dualAgent)
> Metrics source: `data/FinalResults/ontology_report_selected.md`

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|---|---|---|---|---|---|---|---|---|
| 1 | A.owl (triAgent) | 14/14 | 4.7 | 3.8 | 5.0 | 4.5 | 5.0 | **4.52** |
| 2 | C.owl (singleAgent) | 14/14 | 4.5 | 4.2 | 4.5 | 4.2 | 5.0 | **4.43** |
| 3 | D.owl (dualAgent) | 13/14 | 3.8 | 3.5 | 4.5 | 4.0 | 5.0 | **4.02** |

> Weighted Score = (CQ × 0.40) + (Structural × 0.20) + (Design × 0.15) + (Axiom × 0.15) + (Lexical × 0.10)

---

## Top 3 Detailed Analysis

---

### Rank 1: A.owl (triAgent — `EDIFACT_ontology_20260303_070100.owl`)
**Weighted score:** 4.52 / 5.00

**CQ Coverage Analysis:**

- CQ1 — What invoices are all listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope → containsMessage → Message / InvoiceMessage` chain fully present; SPARQL path is unambiguous.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage → hasRoleAssignment → RoleAssignment → involvesOrganization → Organization` forms a complete traversal path.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — `RoleAssignment` pivot cleanly links `Organization` to `AgentRole` via `involvesOrganization` and `hasAgentRole`; inverse properties enable reverse traversal.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — `AgentRole` instances can be typed/identified (e.g., by `rdfs:label` "Buyer") and traversed via the RoleAssignment pivot; no named `BuyerOrganization` class but query is achievable.
- CQ5 — What information is displayed about the involved organizations? — Covered ✅ — `Organization` carries `hasOrganizationName` (datatype), `hasAddress`, `hasIdentifier` (GLN); `rdfs:comment` on all classes.
- CQ6 — What is the address of the buyer? — Covered ✅ — `Organization → hasAddress → Address → hasAddressLine`; subclasses `WarehouseAddress` and `HeadquartersAddress` add structural depth.
- CQ7 — What items are sold in the invoice? — Covered ✅ — `InvoiceDetail → hasLineItem → LineItem → describesItem → Item` is the correct two-hop pivot chain.
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `Item` has `hasItemDescription`; `LineItem` has `hasQuantity`; `Price` has `hasNetPrice`.
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `LineItem → hasPrice → Price → hasNetPrice (xsd:decimal)` is explicit and typed.
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — `InvoiceMessage → hasSection → {InvoiceHeader, InvoiceDetail, InvoiceSummary}` with `owl:unionOf` range restriction models all three sections.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `InvoiceSummary → hasInvoiceAmount (xsd:decimal)` is present and functionally constrained.
- CQ12 — What is the invoice number? — Covered ✅ — `InvoiceHeader → hasInvoiceNumber (xsd:string)` is explicit with `owl:FunctionalProperty`.
- CQ13 — What information must be provided so that the file format is valid? — Covered ✅ — `hasMandatoryIdentifier` on `InvoiceMessage` and the `owl:equivalentClass` restriction on `RoleAssignment` together encode structural validity requirements.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage → referencesBusinessProcess → BusinessProcess` is present with an explicit range.

**Structural Ratios (OntoQA):**
- **RR: 0.8718** — Highest of the evaluated set. Strongly indicates a relationship-rich graph where non-taxonomic object properties dominate. For this application domain (EDIFACT structural decomposition with role patterns), this is appropriate and desirable; the ontology is not merely a class taxonomy.
- **AR: 0.5000** — Moderate attribute density (12 data properties / 24 classes). Marginally lower than C.owl but acceptable; the design prioritises structural object properties over raw data attributes, consistent with a schema-level ontology.
- **IR: 0.2083** — Lowest of the evaluated set. The taxonomy is extremely flat (max depth 1, avg depth 0.21), meaning nearly all classes are direct subclasses of `owl:Thing` or are linked only one level deep. While this reduces IR, it avoids spurious inheritance and keeps the hierarchy honest; the richness is captured through object properties instead (hence the high RR).

**Design Patterns & Domain Representation:**
A.owl employs a textbook reification pattern for N-ary roles: the `RoleAssignment` pivot class links `InvoiceMessage`, `Organization`, and `AgentRole` via three distinct object properties (`hasRoleAssignment`, `involvesOrganization`, `hasAgentRole`), all paired with precise inverse properties. Crucially, the pivot class is further formalised as an `owl:equivalentClass` intersection restriction, making membership computable by a reasoner. The `LineItem` pivot follows the same pattern, decoupling the `Item` identity from its pricing and quantity context. The `hasSection` property uses an `owl:unionOf` anonymous class as its range, correctly representing the three mutually exclusive invoice sections without creating a spurious common superclass.

**Axiom Complexity:**
A.owl achieves Axiom Diversity Score 7 (highest of the evaluated trio), employing `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:unionOf`, `owl:disjointWith`, and `owl:inverseOf`. The `RoleAssignment` and `LineItem` equivalent-class axioms introduce genuine logical entailments rather than purely assertional declarations. Three explicit `owl:FunctionalProperty` declarations on `hasSection`-related properties tighten integrity further.

**Lexical & Annotation Quality:**
All named entities use strict UpperCamelCase (classes) and lowerCamelCase (properties) with zero non-conformant names and zero underscore-style names (Naming Strict: 1.0). Every class and property carries both an `rdfs:label` and an `rdfs:comment` (Label Coverage 1.0, Comment Coverage 1.0), matching the 100% coverage of the best evaluated candidates.

**Most Critical Defect:**
The flat inheritance structure (IR 0.2083) omits explicit `BGMSegment`/`NADSegment` subclasses of `Segment` — which are present in D.owl — leaving segment specialisation entirely to instance-level typing, which weakens SHACL-based structural validation for mandatory EDIFACT segments.

---

### Rank 2: C.owl (singleAgent — `EDIFACT_ontology_20260304_093001.owl`)
**Weighted score:** 4.43 / 5.00

**CQ Coverage Analysis:**

- CQ1 — What invoices are all listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope → containsMessage → EDIFACTMessage → InvoiceMessage` three-level hierarchy provides a navigable chain, though the intermediate `EDIFACTMessage` class adds indirection.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage → involvesOrganization → Organization` as a direct property, plus the `RoleAssignment` reification path, gives two query routes.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — `RoleAssignment → hasAgentRole → AgentRole` and `RoleAssignment → hasParticipant → Organization` form a clean pivot; `roleCode` data property on `AgentRole` allows filter by role type.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — Same RoleAssignment path; `roleCode` on `AgentRole` allows filtering for "Buyer".
- CQ5 — What information is displayed about the involved organizations? — Covered ✅ — `organizationName` datatype, `hasAddress`, `hasIdentifier` cover name, address, and GLN.
- CQ6 — What is the address of the buyer? — Covered ✅ — `Organization → hasAddress → Address → addressLine`; structurally complete, though without address subtype specialisation.
- CQ7 — What items are sold in the invoice? — Covered ✅ — `InvoiceDetail → hasLineItem → LineItem → soldItem → Item`.
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `itemName` on `Item`; `quantity` on `LineItem`; `netPrice` on `Price`.
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `LineItem → hasPrice → Price → netPrice (xsd:decimal)`.
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — `hasHeader`, `hasDetail`, `hasSummary` properties provide three explicit functional links from `InvoiceMessage` to each section.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `InvoiceSummary → invoiceAmount (xsd:decimal)` is present.
- CQ12 — What is the invoice number? — Covered ✅ — `InvoiceHeader → invoiceNumber (xsd:string)`.
- CQ13 — What information must be provided so that the file format is valid? — Partially covered ⚠️ — `Organization rdfs:subClassOf [owl:someValuesFrom :Identifier]` captures identifier as mandatory for organisations; however, there is no explicit mandatory-field annotation at the message level (unlike A.owl's `hasMandatoryIdentifier`). The cardinality restrictions on `LineItem` (`owl:cardinality 1` for `soldItem` and `hasPrice`) partially address this but structural file-format validity is underspecified.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage → assignedToProcess → BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR: 0.7826** — High, second only to A.owl. Confirms a relationship-rich model well-suited to graph traversal.
- **AR: 0.7368** — Highest AR among the evaluated trio (14 data properties / 19 classes). Reflects the richest attribute density: address decomposition (`addressLine`, `postalCode`, `city`, `countryCode`), segment code capture (`segmentCode`), delimiter modelling (`delimiterValue`), and explicit `roleCode` on `AgentRole` all contribute. This means instances can be described with the most detail of any candidate.
- **IR: 0.5263** — Moderate and the highest of the trio, arising from a deeper taxonomy (max depth 5, avg depth 1.74): `InterchangeEnvelope → EDIFACTMessage → InvoiceMessage → Segment → CompositeDataElement → SimpleDataElement` forms a six-level chain. While depth improves IR, two architectural flaws arise from this chain (see defect below).

**Design Patterns & Domain Representation:**
C.owl uses the correct `RoleAssignment` reification pivot and augments it with an `involvesOrganization` shortcut directly on `InvoiceMessage`, which is useful for simple CQ queries. The `Delimiter` class is a notable addition absent from the other candidates, capturing structural EDIFACT syntax at the ontology level. The three dedicated object properties (`hasHeader`, `hasDetail`, `hasSummary`) are more explicit than A.owl's generic `hasSection + unionOf`, and are each declared `owl:FunctionalProperty`, which tightens cardinality. However, the subclass chain mismodels two concepts: `Segment rdfs:subClassOf :InvoiceMessage` (a segment is not a sub-type of a message) and `Price rdfs:subClassOf :LineItem` (a price is not a sub-type of a line item); both are part-whole relationships incorrectly expressed as inheritance, which would cause reasoning anomalies when SHACL or reasoners traverse type hierarchies.

**Axiom Complexity:**
Axiom Diversity Score 6 covers `owl:someValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:inverseOf`, and `owl:cardinality` restrictions. The cardinality restriction `owl:cardinality "1"` on `LineItem → soldItem` and `LineItem → hasPrice` is an advanced construct not used in A.owl, ensuring one-to-one integrity. The `Organization rdfs:subClassOf [owl:someValuesFrom :Identifier]` axiom enforces identifier presence. However, `owl:allValuesFrom` and `owl:unionOf` are absent, leaving some structural constraints that A.owl expresses unrepresented.

**Lexical & Annotation Quality:**
Perfect scores: Naming Strict 1.0, Label Coverage 1.0, Comment Coverage 1.0. All entities follow lowerCamelCase/UpperCamelCase conventions consistently. Annotation quality matches A.owl.

**Most Critical Defect:**
The inheritance chain mismodels part-whole relationships as subclass relationships (`Segment rdfs:subClassOf InvoiceMessage`, `Price rdfs:subClassOf LineItem`, `LineItem rdfs:subClassOf InvoiceDetail`): a Segment is a *part of* a message, not a *kind of* message; these structural errors will produce incorrect DL inferences (e.g., any individual of type `Segment` is also inferred to be an `InvoiceMessage`) and will invalidate any reasoning-based SHACL validation.

---

### Rank 3: D.owl (dualAgent — `EDIFACT_ontology_20260301_222236.owl`)
**Weighted score:** 4.02 / 5.00

**CQ Coverage Analysis:**

- CQ1 — What invoices are all listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope → containsMessage → Message / InvoiceMessage`; `BGMSegment` and `NADSegment` as named subclasses of `Segment` add specificity.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage → hasRoleAssignment → RoleAssignment → involvesOrganization → Organization`.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — `RoleAssignment → hasAgentRole → AgentRole` with inverse properties.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — Via `AgentRole` instances; no named `BuyerOrganization` class but the pattern is sufficient.
- CQ5 — What information is displayed about the involved organizations? — Covered ✅ — `hasOrganizationName`, `hasAddress`, `hasIdentifier` present.
- CQ6 — What is the address of the buyer? — Covered ✅ — `Organization → hasAddress → Address → hasAddressLine`; plus named subclasses `WarehouseAddress` and `HeadquartersAddress`.
- CQ7 — What items are sold in the invoice? — Covered ✅ — `InvoiceDetail → hasLineItem → LineItem → describesItem → Item`.
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `hasItemDescription`, `hasQuantity`, `hasNetPrice` all present.
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `Price → hasNetPrice (xsd:decimal)`.
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — `InvoiceMessage → hasSection → {InvoiceHeader, InvoiceDetail, InvoiceSummary}` present.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `InvoiceSummary → hasInvoiceAmount (xsd:decimal)`.
- CQ12 — What is the invoice number? — Covered ✅ — `InvoiceHeader → hasInvoiceNumber (xsd:string)`.
- CQ13 — What information must be provided so that the file format is valid? — Not covered ❌ — `hasMandatoryIdentifier` is declared as a `owl:DatatypeProperty` on `InvoiceMessage` but without any `owl:someValuesFrom` or cardinality restriction formalising it as mandatory. There is no OWL axiom that would cause a reasoner to flag instances lacking this field; it is a documentation annotation rather than a logical constraint.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage → referencesBusinessProcess → BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR: 0.7692** — High, indicating a relationship-rich graph. Slightly lower than A.owl and C.owl, reflecting the smallest object property set (30 vs. 34–36).
- **AR: 0.5455** — Moderate attribute density (12 data properties / 22 classes). The inclusion of `BGMSegment` and `NADSegment` as named segment subclasses increases the class count without adding data properties, slightly diluting AR compared to C.owl.
- **IR: 0.4091** — Between A.owl (very flat) and C.owl (moderately deep). Max depth 1, avg depth 0.41 indicates a single level of subclassing (`InvoiceMessage rdfs:subClassOf Message`, etc.) with no deeper chains, producing an honest but shallow taxonomy.

**Design Patterns & Domain Representation:**
D.owl uses the same `RoleAssignment` pivot as A.owl and mirrors its inverse-property completeness. The named `BGMSegment` and `NADSegment` subclasses are a domain-correct addition, distinguishing key EDIFACT segment types at the class level and enabling segment-type-specific SHACL shapes. The address hierarchy (`WarehouseAddress`, `HeadquartersAddress` as disjoint subclasses of `Address`) also mirrors A.owl, adding structural detail for the multi-role industrial procurement scenario (E/D/E as both Buyer and Delivery Party with different addresses). The `owl:disjointUnionOf` axiom on `InvoiceMessage` with its three sections is a notable advanced construct absent from C.owl.

**Axiom Complexity:**
Axiom Diversity Score 6 (tied with C.owl), using `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:inverseOf`. The `RoleAssignment owl:equivalentClass` intersection restriction is present. The `owl:disjointUnionOf` for invoice sections is the most advanced single construct in this file. However, `hasMandatoryIdentifier` is declared without any logical restriction formalising its mandatoriness, which is a meaningful omission for CQ13.

**Lexical & Annotation Quality:**
Perfect scores: Naming Strict 1.0, Label Coverage 1.0, Comment Coverage 1.0. All 22 classes and 30+ object/data properties have both `rdfs:label` and `rdfs:comment`. The `owl:FunctionalProperty` declarations are annotated inline where used.

**Most Critical Defect:**
The `hasMandatoryIdentifier` data property (critical to CQ13 coverage) is declared without any formal OWL restriction making it logically mandatory — no `owl:someValuesFrom`, no `owl:minCardinality`, no `owl:equivalentClass` axiom — reducing it to a documentation-only annotation that cannot be enforced by a reasoner or SHACL validator, leaving CQ13 unanswerable in a principled way.

---

## Bottom Ontologies: Summary

There are only three evaluated ontologies in this set (A, C, D), all ranked in the Top 3 analysis above. No ontology falls into a "bottom" tier relative to an unevaluated fourth candidate in this report. The relative weaknesses of the lowest-ranked candidate (D.owl) are documented in its Rank 3 analysis: specifically, its failure to formally enforce the mandatory-identifier constraint for CQ13, its slightly lower class count limiting structural expressiveness, and the absence of the named `EDIFACTMessage` intermediate class that C.owl uses to separate generic message type from invoice-specific semantics. D.owl remains a fully consistent, well-annotated ontology that passes all three validators (HermiT, Pellet, OOPS), and its gap from Rank 1 (A.owl) is a matter of logical depth rather than structural correctness.

---

## Scoring Derivation

| Ontology | CQ (×0.40) | Struct (×0.20) | Design (×0.15) | Axiom (×0.15) | Lexical (×0.10) | **Total** |
|----------|:----------:|:--------------:|:--------------:|:-------------:|:---------------:|:---------:|
| A.owl | 4.7 × 0.40 = 1.880 | 3.8 × 0.20 = 0.760 | 5.0 × 0.15 = 0.750 | 4.5 × 0.15 = 0.675 | 5.0 × 0.10 = 0.500 | **4.565** |
| C.owl | 4.5 × 0.40 = 1.800 | 4.2 × 0.20 = 0.840 | 4.5 × 0.15 = 0.675 | 4.2 × 0.15 = 0.630 | 5.0 × 0.10 = 0.500 | **4.445** |
| D.owl | 3.8 × 0.40 = 1.520 | 3.5 × 0.20 = 0.700 | 4.5 × 0.15 = 0.675 | 4.0 × 0.15 = 0.600 | 5.0 × 0.10 = 0.500 | **3.995** |

> Scores rounded to two decimal places in the Summary Table.

---

## Dimension Score Rationale Summary

| Dimension | A.owl | C.owl | D.owl | Key driver |
|-----------|:-----:|:-----:|:-----:|------------|
| CQ Coverage | 4.7 | 4.5 | 3.8 | A & C cover all 14; D fails CQ13 formally |
| Structural Ratios | 3.8 | 4.2 | 3.5 | C best balanced (RR+AR+IR); A penalised for flat IR; D lowest class/property density |
| Design Patterns | 5.0 | 4.5 | 4.5 | A: flawless pivot + unionOf range; C: subclass misuse; D: correct pivot but narrower |
| Axiom Complexity | 4.5 | 4.2 | 4.0 | A: 7 distinct constructs + allValuesFrom + unionOf; C: cardinality adds value; D: disjointUnion but missing mandatory constraint |
| Lexical | 5.0 | 5.0 | 5.0 | All three are perfect on naming, labels, and comments |
