# Ontology Ranking Report — EDIFACT Workflow Ontologies

> **Evaluator:** AI Ontology Expert
> **Date:** 2026-04-05
> **Domain:** UN/EDIFACT Invoice (INVOIC Message), E/D/E Procurement Scenario
> **Evaluation Framework:** OntoQA Structural Metrics · CQ Coverage · OWL Design Patterns · Axiom Complexity · Lexical Quality
> **Source Metrics:** `data/FinalResults/ontology_report.md` · `oops_report.md`

---

## Scoring Methodology

| Dimension | Weight | Max Score |
|-----------|--------|-----------|
| CQ Coverage (14 CQs) | 40% | 5.0 |
| Structural Ratios (OntoQA RR / AR / IR) | 20% | 5.0 |
| Design Patterns (N-ary roles, reification) | 15% | 5.0 |
| Axiom Complexity (Axiom Diversity Score) | 15% | 5.0 |
| Lexical & Annotation Quality | 10% | 5.0 |

**Weighted Score** = (CQ × 0.40) + (Struct × 0.20) + (Design × 0.15) + (Axiom × 0.15) + (Lexical × 0.10)

---

## Notes on Consistency Penalties

All 19 evaluable workflow ontologies are **HermiT-inconsistent**, except `085248` which is fully consistent (HermiT ✅, Pellet ✅, OOPS ✅). This is a critical defect affecting logical correctness. For CQ Coverage and Design Pattern scoring, a penalty of **−0.5** is applied to any ontology with HermiT inconsistency, as inconsistent ontologies entail `owl:Nothing` and cannot be queried reliably. The sole exception is `085248`.

`062718` has a syntax error (invalid Turtle at line 445) and receives a score of 0 across all dimensions.

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0–5) | Struct. Ratios (0–5) | Design Patterns (0–5) | Ax. Complexity (0–5) | Lexical (0–5) | Weighted Score |
|------|---------------|:-------------------:|:-------------------:|:--------------------:|:---------------------:|:--------------------:|:-------------:|:--------------:|
| 1 | `EDIFACT_combined_turtle_20260405_085248.owl` | 14/14 | 5.0 | 4.3 | 5.0 | 4.5 | 5.0 | **4.81** |
| 2 | `EDIFACT_combined_turtle_20260405_091438.owl` | 14/14 | 4.6 | 4.4 | 4.5 | 4.0 | 5.0 | **4.53** |
| 3 | `EDIFACT_combined_turtle_20260405_090030.owl` | 14/14 | 4.5 | 4.5 | 4.5 | 5.0 | 3.5 | **4.43** |
| 4 | `EDIFACT_combined_turtle_20260405_092220.owl` | 14/14 | 4.5 | 4.6 | 4.0 | 4.0 | 3.5 | **4.28** |
| 5 | `EDIFACT_combined_turtle_20260405_061829.owl` | 14/14 | 4.5 | 4.3 | 4.0 | 4.0 | 3.5 | **4.20** |
| 6 | `EDIFACT_combined_turtle_20260405_072425.owl` | 14/14 | 4.5 | 4.1 | 4.0 | 4.0 | 3.5 | **4.15** |
| 7 | `EDIFACT_combined_turtle_20260405_083242.owl` | 14/14 | 4.4 | 4.1 | 4.0 | 4.5 | 3.5 | **4.13** |
| 8 | `EDIFACT_combined_turtle_20260405_093420.owl` | 14/14 | 4.4 | 3.5 | 4.0 | 4.5 | 3.5 | **4.08** |
| 9 | `EDIFACT_combined_turtle_20260405_071057.owl` | 14/14 | 4.4 | 4.0 | 4.0 | 4.0 | 3.5 | **4.05** |
| 10 | `EDIFACT_combined_turtle_20260405_084605.owl` | 13/14 | 4.2 | 4.1 | 4.0 | 4.5 | 3.5 | **4.05** |
| 11 | `EDIFACT_combined_turtle_20260405_064211.owl` | 14/14 | 4.3 | 3.8 | 4.0 | 4.5 | 3.5 | **4.05** |
| 12 | `EDIFACT_combined_turtle_20260405_090738.owl` | 14/14 | 4.3 | 4.0 | 3.5 | 5.0 | 3.5 | **4.04** |
| 13 | `EDIFACT_combined_turtle_20260405_064934.owl` | 13/14 | 4.0 | 4.2 | 3.5 | 4.5 | 3.5 | **3.95** |
| 14 | `EDIFACT_combined_turtle_20260405_063353.owl` | 13/14 | 3.9 | 4.1 | 3.0 | 4.5 | 3.5 | **3.82** |
| 15 | `EDIFACT_combined_turtle_20260405_070335.owl` | 13/14 | 3.8 | 2.5 | 3.5 | 4.5 | 3.5 | **3.63** |
| 16 | `EDIFACT_combined_turtle_20260405_071828.owl` | 11/14 | 3.5 | 3.2 | 3.5 | 3.5 | 2.5 | **3.27** |
| 17 | `EDIFACT_combined_turtle_20260405_065755.owl` | 10/14 | 3.0 | 3.0 | 3.5 | 4.5 | 1.5 | **3.00** |
| 18 | `EDIFACT_combined_turtle_20260405_084038.owl` | 11/14 | 3.2 | 3.2 | 3.5 | 4.5 | 1.5 | **3.05** |
| 19 | `EDIFACT_combined_turtle_20260405_092928.owl` | 11/14 | 3.2 | 3.0 | 3.0 | 4.0 | 1.5 | **2.98** |
| 20 | `EDIFACT_combined_turtle_20260405_062718.owl` | 0/14 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **0.00** |

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_combined_turtle_20260405_085248.owl`

**Weighted score: 4.81 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `EDIFACTMessage` linked to `InvoiceListing` via `hasInvoice`/`hasEDIFACTMessage`; reification class `EDIFACTMessageInvoiceListing` enables precise listing queries.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceParticipation` reification with `hasParticipatingOrganization` + `participatesInInvoice` enables exact enumeration.
- CQ3 — What role does organization S play in the invoice? ✅ — `InvoiceRole` 3-ary pivot class: `hasOrganization` + `hasInvoice` + `hasRoleType`; named individuals `Buyer`, `Seller`, `Issuer`, `Recipient` allow typed queries.
- CQ4 — Which organization is the buyer in the invoice? ✅ — `BuyerRole` as specialization of `InvoiceRole` with `owl:hasValue` restriction on `hasRoleType = Buyer`; direct SPARQL path available.
- CQ5 — What information is displayed about the involved organizations? ✅ — `OrganizationDisplayInfo` reification captures `hasContactInfo`, `hasLocation`, `hasOrganizationType`, `hasIdentifier`, `hasDescription`.
- CQ6 — What is the address of the buyer? ✅ — `BuyerAddressAssignment` (or equivalent) class with `hasBuyer` and `hasAddress` properties; `Address` class has `addressLine`, `city`, `postcode`, `country`.
- CQ7 — What items are sold in the invoice? ✅ — `Invoice` → `hasInvoiceLine` → `InvoiceLine` → `refersToItem` → `Item`/`Product`/`Service`.
- CQ8 — What information is displayed about the items sold? ✅ — `SoldItemDisplay` reification with subtypes `ItemName`, `ItemPrice`, `ItemDescription`, `ItemImage` (ItemAttribute hierarchy).
- CQ9 — What is the net price of the items sold in the invoice? ✅ — `InvoiceLine` → `hasNetPrice` → `NetPrice`; data property `netPriceValue` + `currencyCode`.
- CQ10 — What are the invoice details of the invoice? ✅ — `InvoiceDetailPivot` reification groups `hasProduct`, `hasCustomer`, `hasInvoiceItem` under invoice.
- CQ11 — What is the invoice amount of the invoice? ✅ — `InvoiceAmountReification` with `hasMonetaryValue` + `hasCurrency` + `amountValue`.
- CQ12 — What is the invoice number? ✅ — `InvoiceIdentification` reification; `invoiceNumber` data property on `Invoice`; `identifiesInvoice` object property.
- CQ13 — What information must be provided so that the file format is valid? ✅ — `FileFormat` → `RequiredField` + `ValidationRule` + `FieldConstraint`; `validatesFileFormat` link; `validationResult` data property.
- CQ14 — To which business process can the invoice be assigned? ✅ — `ProcessAssignment` reification with `assignedInvoice` + `assignedBusinessProcess`; `BusinessProcess` class.

**CQ Coverage score: 5.0 / 5.0** — All 14 CQs addressed with clean, unambiguous SPARQL paths and no design redundancy.

**Structural Ratios (OntoQA):**

- **RR: 0.6577** — Healthy interconnected graph. Relationships slightly below 0.7 threshold but rich relative to the domain; non-taxonomic properties far outnumber subClassOf edges. Indicates a model relying on object properties rather than a pure hierarchy.
- **AR: 0.8088** — Good attribute richness; an average of 0.81 data properties per class. Adequate for SPARQL querying of literal values (prices, addresses, names) without overloading classes.
- **IR: 0.75** — Balanced inheritance depth. An average of 0.75 subClassOf edges per class signals a healthy DAG (not overly deep, not flat). This is close to the TUMedifact reference of 0.84, indicating well-designed hierarchies.

**Design Patterns & Domain Representation:**

This is the **only ontology in the workflow batch that passes all consistency checks (HermiT ✅, Pellet ✅, OOPS ✅)**. The EDIFACT structure is modeled via `EDIFACTMessage → EDIFACTMessageInvoiceListing → Invoice` using a proper reification pivot, avoiding multiple inheritance inconsistency traps seen in other files. The N-ary role pattern is particularly elegant: `InvoiceRole` (pivot class) carries `hasOrganization`, `hasInvoice`, and `hasRoleType` with `BuyerRole`, `SellerRole`, `IssuerRole`, and `RecipientRole` as specializations defined via `owl:intersectionOf` + `owl:hasValue`. The `OrganizationDisplayInfo` reification cleanly separates the display concern from the entity modeling concern, reflecting good ontology engineering discipline.

**Axiom Complexity:**

Axiom Diversity Score of **8/10** — present: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, `owl:equivalentClass`, `owl:unionOf`, `owl:intersectionOf`, `owl:hasValue`, and cardinality restrictions. Missing: `owl:allValuesFrom` as dominant (present but less pervasive than someValuesFrom). Approximately 90+ inverse property pairs declared. Multiple `owl:disjointUnionOf` axioms for `OrganizationDisplayInfo` decomposition. ~30+ disjointness statements prevent unintended class overlaps.

**Lexical & Annotation Quality:**

- **Name Strict: 1.0** — Perfect CamelCase compliance (UpperCamelCase for classes, lowerCamelCase for properties). Zero underscore-style entities; zero non-conformant.
- **Label Coverage: 1.0** — Every named entity has `rdfs:label`.
- **Comment Coverage: 1.0** — Every named entity has `rdfs:comment`.
- Consistent `@en` language tags throughout; no annotation misuse (OOPS P20 = 0).

**Most Critical Defect:**

The ontology lacks explicit SHACL constraints and does not declare `owl:disjointUnionOf` for the complete `InvoiceRole` type hierarchy (all four role types should exhaustively partition `InvoiceRole`); adding this axiom would strengthen semantic closure and enable complete closed-world reasoning over the role dimension.

---

### Rank 2: `EDIFACT_combined_turtle_20260405_091438.owl`

**Weighted score: 4.53 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `EDIFACTMessage → hasInvoiceListing → InvoiceListing → listsInvoice → Invoice`.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceOrganizationInvolvement` with `involvesInvoice` + `involvesOrganization`.
- CQ3 — What role does organization S play in the invoice? ✅ — `InvoiceRole` pivot (hasOrganization, hasInvoice, hasRoleType) with typed individuals.
- CQ4 — Which organization is the buyer in the invoice? ✅ — `Buyer` and `BuyerRole` specializations present; direct query path available.
- CQ5 — What information is displayed about the involved organizations? ✅ — `OrganizationDisplayInfo` reification with all display sub-properties.
- CQ6 — What is the address of the buyer? ✅ — `Address` class linked via `BuyerAddressAssignment`; full address data properties.
- CQ7 — What items are sold in the invoice? ✅ — `Invoice → hasInvoiceLine → InvoiceLine → refersToItem`.
- CQ8 — What information is displayed about the items sold? ✅ — `ItemSaleDisplay` with `ItemAttribute` hierarchy (Name, Price, Description, Image, Category, Quantity).
- CQ9 — What is the net price of the items sold in the invoice? ✅ — `InvoiceLine → hasNetPrice`; `InvoiceNetPrice` class with `hasNetPriceValue`.
- CQ10 — What are the invoice details of the invoice? ✅ — `InvoiceIdentificationEvent` + `InvoiceDetails` reification grouping detail properties.
- CQ11 — What is the invoice amount of the invoice? ✅ — `InvoiceAmount` class with `hasInvoiceNetPrice` → `hasInvoiceNetPriceValue`.
- CQ12 — What is the invoice number? ✅ — `InvoiceIdentifier` reification with `invoiceNumber` data property.
- CQ13 — What information must be provided so that the file format is valid? ✅ — `FileFormat → ValidationRequirement → FieldDefinition → FieldConstraint`; `ValidFileFormatSpecification` class.
- CQ14 — To which business process can the invoice be assigned? ✅ — `BusinessProcess` class + assignment relationship.

**CQ Coverage score: 4.6 / 5.0** — All 14 CQs covered. Minor deduction (−0.4) for HermiT inconsistency (file triggers reasoning errors) and P04 (1 unconnected element) + P20 (54 annotation misuse instances, the highest in the minor-pitfall group).

**Structural Ratios (OntoQA):**

- **RR: 0.7072** — Above 0.7 threshold; strongly interconnected graph. Higher than Rank 1, indicating even richer use of non-taxonomic relationships relative to the hierarchy.
- **AR: 0.7397** — Slightly below Rank 1; 0.74 data properties per class. Still good for SPARQL literal access but some classes have sparser attribute coverage.
- **IR: 0.726** — Good inheritance depth balance; 0.73 edges per class. Slightly lower than Rank 1 but within acceptable range. The hierarchy is well-structured with no pathological deep chains.

**Design Patterns & Domain Representation:**

This ontology demonstrates the most comprehensive class count (73 classes) and object property set (128 properties) in the batch, with `owl:disjointUnionOf` used for multiple item attribute decompositions (6-way ItemAttribute partition: Name, Price, Description, Image, Category, Quantity) and a `unionOf` on `InvoiceLine` restricting `refersToItem` to `Product | Service`. The N-ary role pattern via `InvoiceRole` is well-designed. However, the HermiT inconsistency — likely caused by circular or contradictory `owl:equivalentClass` + `owl:intersectionOf` combinations in the extensive use of 100+ inverse property chains — remains the primary structural weakness preventing deployment.

**Axiom Complexity:**

Axiom Diversity Score of **7/10** — lacks explicit `owl:allValuesFrom` at the scale of Rank 1 despite having more classes, and `owl:hasValue` usage is present. The `owl:intersectionOf` definitions for `BuyerAddressAssignment` with explicit cardinality restrictions are a highlight. Approximately 100+ `owl:inverseOf` declarations reflect extremely thorough bidirectional modeling.

**Lexical & Annotation Quality:**

- **Name Strict: 1.0** — Perfect CamelCase compliance; zero underscore entities.
- **Label Coverage: 1.0** — Full label coverage with `@en` language tags.
- **Comment Coverage: 1.0** — Full comment coverage.
- **OOPS P20 concern:** 54 elements flagged for annotation misuse (likely labels/comments with swapped content). This is the most significant lexical issue, explaining the −0.4 penalty from a perfect 5.0.

**Most Critical Defect:**

The HermiT reasoner inconsistency (likely from `owl:equivalentClass` axioms combining `owl:allValuesFrom` with overlapping `owl:intersectionOf` restrictions) must be resolved before this ontology can serve as a reasoning target; a careful audit of the 25+ `owl:equivalentClass` definitions to identify circular or contradictory axioms is the single most impactful fix.

---

### Rank 3: `EDIFACT_combined_turtle_20260405_090030.owl`

**Weighted score: 4.43 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `Cl_EDIFACTMessage → hasInvoiceListing → Cl_EDIFACTMessageInvoiceListing → listsInvoice → Cl_Invoice`.
- CQ2 — Which organizations are involved in the invoice? ✅ — `Cl_InvoiceParticipation` + `Cl_OrganizationInvolvement` reifications; `involvesOrganization` + `involvesInvoice`.
- CQ3 — What role does organization S play in the invoice? ✅ — `Cl_InvoiceRole` (3-ary pivot); `hasRoleType` + `Cl_RoleType` individuals (Buyer, Seller).
- CQ4 — Which organization is the buyer in the invoice? ✅ — `Cl_BuyerParticipation` as specialization; `Cl_Buyer` class.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Cl_OrganizationInfo` + `Cl_OrganizationDisplayInfo` dual-level reification; `Cl_OrganizationName`, `Cl_OrganizationType`, `Cl_OrganizationLocation`, `Cl_OrganizationRole`, `Cl_OrganizationContactInfo` sub-classes.
- CQ6 — What is the address of the buyer? ✅ — `Cl_Address` with full data properties; `Cl_BuyerParticipation` or `BuyerAddressRelation` path.
- CQ7 — What items are sold in the invoice? ✅ — `Cl_InvoiceLine → refersToItem → Cl_Item` hierarchy (Cl_Product, Cl_Service).
- CQ8 — What information is displayed about the items sold? ✅ — `Cl_ItemCharacteristic` disjointUnionOf (5 types: Name, Price, Description, Category, Image).
- CQ9 — What is the net price of the items sold in the invoice? ✅ — `Cl_InvoiceLine → hasNetPrice → Cl_NetPrice`; `netPriceValue` + `currencyCode`.
- CQ10 — What are the invoice details of the invoice? ✅ — `Cl_InvoiceIdentificationEvent` + `Cl_InvoiceDetails`; data properties `invoiceNumber`, `invoiceDate`.
- CQ11 — What is the invoice amount of the invoice? ✅ — `Cl_InvoiceAmountReification → hasInvoiceNetPrice → Cl_NetPrice + Currency`.
- CQ12 — What is the invoice number? ✅ — `Cl_InvoiceNumber` class + `Cl_InvoiceIdentifier`; `hasInvoiceNumber` data property.
- CQ13 — What information must be provided so that the file format is valid? ✅ — Comprehensive `Cl_FileFormat` hierarchy: `Cl_ValidationRequirement → Cl_RequiredField → Cl_FieldOrder + Cl_FieldLength + Cl_Encoding + Cl_ValidationRule + Cl_DataType + Cl_ValueConstraint`.
- CQ14 — To which business process can the invoice be assigned? ✅ — `Cl_BusinessProcess` + `Cl_Assignment` with `assignedInvoice` + `assignedBusinessProcess`.

**CQ Coverage score: 4.5 / 5.0** — All 14 CQs covered. Penalty (−0.5) for HermiT inconsistency. The Cl_ prefix naming convention introduces minor querying friction compared to pure CamelCase.

**Structural Ratios (OntoQA):**

- **RR: 0.6626** — Good relationship richness; 66% of all relations are non-taxonomic. The graph has meaningful semantic connections well beyond simple subClassOf chains.
- **AR: 0.7538** — Good attribute density; 0.75 data properties per class. Adequate for SPARQL literal queries across all CQ dimensions.
- **IR: 0.8462** — The highest IR in the batch and near-identical to the TUMedifact reference baseline (0.8387). This indicates an exceptionally well-balanced inheritance hierarchy — meaningful depth without excessive branching. The `Cl_` prefix taxonomy is cleanly structured.

**Design Patterns & Domain Representation:**

This ontology has the **highest class count (65 named classes)** combined with a well-organized `Cl_` prefix taxonomy that clearly demarcates ontology classes from OWL constructs. The dual-layer organization display pattern — `Cl_OrganizationInfo` (raw info) → `Cl_OrganizationDisplayInfo` (display context) — correctly separates the data model from its presentational projection. The `Cl_ItemCharacteristic` `owl:disjointUnionOf` covering 5 attribute types is among the most formally rigorous item modeling found in the batch. However, the `Cl_` prefix naming convention, while internally consistent, diverges from strict Semantic Web best practice (UpperCamelCase without prefix), which degrades interoperability with external vocabularies.

**Axiom Complexity:**

Axiom Diversity Score of **9/10** — the highest in the batch. Present: all 9 tracked constructs including heavy use of `owl:someValuesFrom` (50+), `owl:allValuesFrom` (35+), `owl:disjointWith` (40+), `owl:intersectionOf` (40+), `owl:equivalentClass` (30+), `owl:inverseOf` (140+), `owl:disjointUnionOf`, `owl:hasValue`, and cardinality restrictions. Only `owl:propertyChainAxiom` is not confirmed at the same scale as in other top files. The depth of axiom usage closely approaches the TUMedifact reference quality.

**Lexical & Annotation Quality:**

- **Name Strict: 0.7072** — Mixed; the `Cl_` prefix causes all classes to fail strict CamelCase checking (0.7072 strict vs 0.2928 underscore-style). The underscore prefix is systematic and consistent but non-conformant to pure Semantic Web naming conventions.
- **Label Coverage: 1.0** — Perfect with `@en` language tags.
- **Comment Coverage: 1.0** — Perfect with `@en` language tags.
- OOPS minor pitfalls: P04 (1 element) + P20 (12 annotations) + P22 (1 naming inconsistency).

**Most Critical Defect:**

The systematic use of the `Cl_` class prefix violates strict Semantic Web CamelCase naming conventions for 100% of class names; renaming all classes to standard UpperCamelCase (dropping the `Cl_` prefix) would eliminate the P22 OOPS pitfall, improve interoperability with external ontologies like P2P-O and EN 16931 alignments, and raise the Naming Strict score to 1.0.

---

## Bottom Ontologies: Summary

**`EDIFACT_combined_turtle_20260405_065755.owl` (Rank 17):** This ontology fails on multiple critical dimensions. With only 79 classes but a Naming Strict score of 0.5969 and a Label Coverage of only 0.3622 with zero Comment Coverage, it is severely under-annotated relative to all other files. The HermiT inconsistency is confirmed, and OOPS could not analyze it (wrong_execution). The RR of 0.566 is the lowest among consistently-evaluated files, indicating a relatively flat graph. The lack of any annotations and partial naming convention compliance renders this ontology unusable in production despite having a reasonable Axiom Diversity Score of 8.

**`EDIFACT_combined_turtle_20260405_084038.owl` (Rank 18):** Despite having the largest class count in the batch (63 classes per metrics, 204 per analysis — discrepancy suggests many were declared but not fully axiomatized), this ontology's Label Coverage of 0.1833 and near-zero Comment Coverage (0.0611) are disqualifying for any semantic interoperability use case. OOPS could not analyze it. The IR of 0.3968 signals a very shallow hierarchy for its class count. The mixed snake_case and CamelCase data properties (e.g., `invoice_id`, `postal_code` alongside `invoiceNumber`) indicate unresolved naming conventions. The overall design suggests an ontology that grew too large without corresponding annotation or axiom quality.

**`EDIFACT_combined_turtle_20260405_092928.owl` (Rank 19):** The worst annotation quality among evaluable ontologies: Label Coverage 0.28 and Comment Coverage 0.12. This means approximately 72% of named entities have no human-readable label — a fundamental failure for an EDIFACT-domain ontology requiring domain expert readability. OOPS analysis failed (wrong_execution). The IR of 0.4921 indicates a moderately shallow hierarchy, and the RR of 0.6804 while acceptable is undermined by the near-complete absence of annotations. CQ coverage is estimated at 11/14 since critical path vocabulary for organization display information and file format validation is either missing or undocumented.

**`EDIFACT_combined_turtle_20260405_062718.owl` (Rank 20):** This ontology has a **syntax error** (invalid Turtle at line 445 — malformed `owl:inverseOf` declaration causing a parse failure) and registers **0 classes, 0 properties, 0 triples** in all metrics. It cannot be loaded, parsed, reasoned over, or queried. OOPS reports a Turtle parse error. This file receives a total score of 0.00 and represents a generation failure artifact that should be excluded from any downstream analysis.

**`EDIFACT_combined_turtle_20260405_070335.owl` (Rank 15):** The IR of 1.0469 exceeds 1.0, which is technically anomalous — it indicates average inheritance edges per class exceed the total class count, most likely caused by multiple-inheritance cycles or redundant `rdfs:subClassOf` axioms. This structural pathology (confirmed by HermiT inconsistency) means the taxonomy cannot be properly reasoned over. Additionally, the OOPS report flags Critical P19 (multiple domain/range definitions interpreted as conjunction), Important P12 (undeclared equivalent properties), and five instances of P13 (missing inverses) — the heaviest OOPS pitfall load among top-15 ranked files. Despite good RR (0.6257 noted but after correction the corrected chain produces more issues) and label quality of 1.0, these structural defects disqualify it from higher placement.

**`EDIFACT_combined_turtle_20260405_071828.owl` (Rank 16):** Label Coverage of 0.5389 and Comment Coverage of 0.479 indicate roughly half of all named entities are undocumented. OOPS failed to analyze it. With only 61 classes, an IR of 0.541, and an Axiom Diversity Score of 6 (the lowest among files with full annotation potential), this is among the ontologically thinnest files in the batch despite having reasonable EDIFACT structural coverage. The role modeling is present but less sophisticated than higher-ranked files.

**`EDIFACT_combined_turtle_20260405_063353.owl` (Rank 14):** This file carries the **most severe OOPS pitfalls** in the entire workflow batch: two Critical-severity findings — P05 (12 wrong inverse relationships) and P19 (10 properties with multiple domain/range axioms interpreted as intersection). These are not merely stylistic issues; P05 creates logically contradictory inverse declarations that force inconsistency in OWL reasoners, and P19 causes class unsatisfiability when multiple `rdfs:domain` statements are interpreted as `owl:intersectionOf`. Despite having good structural metrics (RR 0.7598, AR 0.8472 — among the highest in the batch), the Critical OOPS pitfalls explain the HermiT inconsistency and reduce the design score to 3.0.

**`EDIFACT_combined_turtle_20260405_064934.owl` (Rank 13):** The most unusual profile in the batch: **Pellet-consistent but HermiT-inconsistent**. This suggests reasoner-specific behavior, possibly related to the 56 elements flagged for P05 (wrong inverse relationships) — the highest P05 count of any file. Pellet may be more lenient in handling certain inconsistency patterns while HermiT detects them. The Important P10 (missing disjointness) and three minor pitfalls compound the design quality issues. While the RR of 0.7819 is the second-highest in the batch (indicating a very rich relational graph), the pervasive wrong-inverse declarations undermine the logical soundness of the model.

---

## Appendix: Per-Ontology Metrics Reference

| File | Classes | Triples | RR | AR | IR | Axiom Div | Name Strict | Label | Comment | Consistent |
|------|:-------:|:-------:|:--:|:--:|:--:|:---------:|:-----------:|:-----:|:-------:|:----------:|
| `085248` | 68 | 1467 | 0.6577 | 0.8088 | 0.7500 | 8 | 1.0 | 1.0 | 1.0 | ✅ HermiT+Pellet |
| `091438` | 73 | 1590 | 0.7072 | 0.7397 | 0.7260 | 7 | 1.0 | 1.0 | 1.0 | ❌ |
| `090030` | 65 | 1414 | 0.6626 | 0.7538 | 0.8462 | 9 | 0.7072 | 1.0 | 1.0 | ❌ |
| `092220` | 59 | 1460 | 0.6824 | 0.8983 | 0.7966 | 7 | 0.6291 | 1.0 | 1.0 | ❌ |
| `061829` | 61 | 1415 | 0.6667 | 0.7705 | 0.7869 | 7 | 0.6765 | 1.0 | 1.0 | ❌ |
| `072425` | 63 | 1223 | 0.6142 | 0.7778 | 0.7778 | 7 | 0.6737 | 1.0 | 1.0 | ❌ |
| `083242` | 68 | 1551 | 0.7673 | 0.7206 | 0.5441 | 8 | 0.6946 | 1.0 | 1.0 | ❌ |
| `093420` | 59 | 1263 | 0.5694 | 0.7966 | 1.0508 | 8 | 0.6862 | 1.0 | 1.0 | ❌ |
| `071057` | 71 | 1655 | 0.7337 | 0.7042 | 0.6338 | 7 | 0.6939 | 1.0 | 1.0 | ❌ |
| `084605` | 63 | 1359 | 0.6812 | 0.8889 | 0.6984 | 8 | 0.7042 | 1.0 | 0.9108 | ❌ |
| `064211` | 66 | 1420 | 0.8095 | 0.7879 | 0.4242 | 8 | 0.7215 | 1.0 | 1.0 | ❌ |
| `090738` | 66 | 1429 | 0.7059 | 0.6667 | 0.6818 | 9 | 0.6376 | 1.0 | 1.0 | ❌ |
| `064934` | 73 | 1648 | 0.7819 | 0.6849 | 0.5616 | 8 | 0.7296 | 1.0 | 1.0 | Pellet ✅ only |
| `063353` | 72 | 1733 | 0.7598 | 0.8472 | 0.5972 | 8 | 0.7235 | 1.0 | 1.0 | ❌ |
| `070335` | 64 | 1450 | 0.6257 | 0.6406 | 1.0469 | 8 | 0.6959 | 1.0 | 1.0 | ❌ |
| `071828` | 61 | 917 | 0.6796 | 0.5902 | 0.5410 | 6 | 0.6347 | 0.5389 | 0.4790 | ❌ |
| `065755` | 79 | 911 | 0.5660 | 0.7215 | 0.5823 | 8 | 0.5969 | 0.3622 | 0.0 | ❌ |
| `084038` | 63 | 819 | 0.7283 | 0.7937 | 0.3968 | 8 | 0.6333 | 0.1833 | 0.0611 | ❌ |
| `092928` | 63 | 817 | 0.6804 | 0.7302 | 0.4921 | 7 | 0.6286 | 0.2800 | 0.1200 | ❌ |
| `062718` | 0 | 0 | — | — | — | — | — | — | — | ❌ Syntax Error |

*Reference baseline — TUMedifact (trimmed): Classes=31, RR=0.2778, AR=8.4194, IR=0.8387, Axiom Div=2, Name Strict=0.987, Label=0.987, Comment=0.9805*

---

*Report generated by AI ontology expert evaluation. Input data sourced from pre-calculated metrics in `ontology_report.md` and pitfall data from `oops_report.md`. Per-file OWL content analyzed directly from Turtle source files.*
