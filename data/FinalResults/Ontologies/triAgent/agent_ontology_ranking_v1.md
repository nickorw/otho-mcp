# triAgent Ontology Ranking Report

> Evaluator: Claude (automated ontology expert analysis)
> Date: 2026-03-08
> Corpus: 11 triAgent-generated OWL ontologies for the EDIFACT INVOIC domain

---

## Scoring Methodology

Each ontology is scored across five weighted dimensions:

| Dimension | Weight |
|-----------|--------|
| CQ Coverage | 40% |
| Structural Ratios (RR / AR / IR) | 20% |
| Design Patterns | 15% |
| Axiom Complexity | 15% |
| Lexical & Annotation Quality | 10% |

Metrics are taken verbatim from `data/FinalResults/ontology_report.md` (section 3.4, triAgent detail table). OOPS status is taken from the validation table in the same section.

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered | CQ Cov. (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | **Weighted Score** |
|------|--------------|:-----------:|:-------------:|:--------------------:|:---------------------:|:--------------------:|:-------------:|:-----------------:|
| 1 | `EDIFACT_ontology_20260302_140235.owl` | 14/14 | 4.8 | 4.0 | 5.0 | 4.5 | 5.0 | **4.67** |
| 2 | `EDIFACT_ontology_20260303_061520.owl` | 14/14 | 4.7 | 3.8 | 4.8 | 4.3 | 5.0 | **4.55** |
| 3 | `EDIFACT_ontology_20260303_070100.owl` | 14/14 | 4.7 | 3.7 | 4.5 | 4.5 | 5.0 | **4.51** |
| 4 | `EDIFACT_ontology_20260302_073654.owl` | 14/14 | 4.6 | 3.5 | 4.8 | 4.8 | 5.0 | **4.49** |
| 5 | `EDIFACT_ontology_20260303_091850.owl` | 13/14 | 4.3 | 3.8 | 4.5 | 4.3 | 5.0 | **4.27** |
| 6 | `EDIFACT_ontology_20260302_082612.owl` | 13/14 | 4.2 | 3.9 | 4.3 | 4.3 | 5.0 | **4.20** |
| 7 | `EDIFACT_ontology_20260303_085821.owl` | 13/14 | 4.1 | 3.6 | 4.0 | 4.0 | 5.0 | **4.07** |
| 8 | `EDIFACT_ontology_20260302_081000.owl` | 12/14 | 3.8 | 3.2 | 3.8 | 3.0 | 5.0 | **3.72** |
| 9 | `EDIFACT_ontology_20260302_133553.owl` | 12/14 | 3.7 | 3.4 | 3.5 | 3.5 | 4.8 | **3.64** |
| 10 | `EDIFACT_ontology_20260302_124024.owl` | 11/14 | 3.4 | 3.3 | 3.3 | 3.0 | 5.0 | **3.38** |
| 11 | `EDIFACT_ontology_20260303_094621.owl` | 11/14 | 3.3 | 3.7 | 3.2 | 3.5 | 5.0 | **3.38** |

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_ontology_20260302_140235.owl`
**Weighted Score: 4.67 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? — ✅ `InvoiceMessage` is a typed class with `hasMessage` linking `InterchangeEnvelope` → `Message` → `InvoiceMessage`.
- CQ2 — Which organizations are involved in the invoice? — ✅ `involvesOrganization` (InvoiceMessage → Organization) plus pivot `OrganizationRoleAssignment` pattern.
- CQ3 — What role does organization S play in the invoice? — ✅ Pivot class `OrganizationRoleAssignment` with `assignedRole` → `AgentRole` and `forOrganization` → `Organization` allows precise role lookup.
- CQ4 — Which organization is the buyer in the invoice? — ✅ Subclass `BuyerRole` of `AgentRole`, queryable via the pivot assignment chain.
- CQ5 — What information is displayed about the involved organizations? — ✅ `hasAddress`, `hasIdentifier`, `hasGlobalLocationNumber` on `Organization`; multiple data properties (name, GLN details).
- CQ6 — What is the address of the buyer? — ✅ `hasAddress` (Organization → Address) with rich data properties: `addressLine`, `postalCode`, `city`, `countryCode`.
- CQ7 — What items are sold in the invoice? — ✅ `hasLineItem` (DetailSection → LineItem) + `describesItem` (LineItem → Item).
- CQ8 — What information is displayed about the items sold? — ✅ `itemDescription` data property on `Item`; `hasNetPrice`, `hasQuantity` on `LineItem`/`Price`/`Quantity`.
- CQ9 — What is the net price of the items sold in the invoice? — ✅ `hasNetPrice` (LineItem → Price), `netPrice` datatype property (decimal). Clean, unambiguous path.
- CQ10 — What are the invoice details of the invoice? — ✅ Three-section structure (Header, Detail, Summary) with dedicated properties; `hasHeader`, `hasDetail`, `hasSummary` on `InvoiceMessage`.
- CQ11 — What is the invoice amount of the invoice? — ✅ `hasInvoiceAmount` (SummarySection → InvoiceAmount) with `invoiceAmountValue` (decimal).
- CQ12 — What is the invoice number? — ✅ `hasInvoiceNumber` (HeaderSection → string) — clear, functional property.
- CQ13 — What information must be provided so that the file format is valid? — ✅ `ValidationConstraint` class with `hasValidationConstraint` and `constraintDescription` data property; explicit compliance hook.
- CQ14 — To which business process can the invoice be assigned? — ✅ `assignedToProcess` (InvoiceMessage → BusinessProcess) with inverse.

**Structural Ratios (OntoQA):**

- **RR:** 0.7843 — Rich, property-heavy graph. Substantially above the baseline reference (0.2778), indicating extensive use of object properties relative to taxonomic links. A healthy interconnected model.
- **AR:** 0.4828 — Moderate attribute density. With 14 data properties across 29 classes, individual class instances carry meaningful data. Slightly below the ideal for a data-rich domain, but well above the triAgent average of 0.20.
- **IR:** 0.3793 — Balanced DAG: 11 subClassOf edges over 29 classes gives each class about 0.38 inheritance positions on average, reflecting a meaningful (not over-deep, not flat) hierarchy.

**Design Patterns & Domain Representation:**

The ontology deploys a full reification pivot `OrganizationRoleAssignment` with three dedicated properties (`forOrganization`, `playsRole`, `assignedRole`) and an `owl:equivalentClass` intersection axiom, enabling precise N-ary role assignment. The pattern cleanly supports CQs 2–4 (organization involvement, role lookup, buyer identification) without collapsing roles into direct subproperties of Organization. The separate `LineItem` pivot for item-price-quantity triads similarly handles the item detail N-ary relationship correctly. Both structural sections (NAD-level roles and LIN-level line items) are addressed with dedicated reification classes.

**Axiom Complexity:**

The ontology scores Axiom Diversity 5 (from the metrics file), incorporating `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:inverseOf`, `owl:FunctionalProperty`, `owl:equivalentClass` with intersection-of, and `owl:disjointWith`. Three `owl:equivalentClass` axioms (`InvoiceMessage`, `RoleAssignment`, `LineItem`) define necessary and sufficient conditions, providing genuine logical depth beyond mere declaration.

**Lexical & Annotation Quality:**

Name Strict CamelCase = 1.0 (perfect), No underscores, Label Coverage = 1.0, Comment Coverage = 1.0. Every class and property carries both `rdfs:label` and `rdfs:comment`. Naming is consistently strict CamelCase for classes and lowerCamelCase for properties throughout.

**Most Critical Defect:**

The `InvoiceMessage owl:equivalentClass` restriction uses only `owl:allValuesFrom :Section` (a value restriction, not an existence restriction), which does not logically force an InvoiceMessage to *have* sections — only constrains what sections it may have if any exist. Adding `owl:someValuesFrom` constraints for Header/Detail/Summary would make the definition genuinely sufficient.

---

### Rank 2: `EDIFACT_ontology_20260303_061520.owl`
**Weighted Score: 4.55 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? — ✅ `InvoiceMessage` subClassOf `Message`; `containsMessage` (InterchangeEnvelope → Message).
- CQ2 — Which organizations are involved in the invoice? — ✅ `involvesOrganization` (InvoiceMessage → Organization) + pivot `OrganizationRoleAssignment`.
- CQ3 — What role does organization S play in the invoice? — ✅ Pivot `OrganizationRoleAssignment` with `assignedRole` → `AgentRole` and `assignedOrganization` → `Organization`. Precise query path.
- CQ4 — Which organization is the buyer in the invoice? — ✅ `BuyerRole` subClassOf `AgentRole`; `AgentRole owl:disjointUnionOf (BuyerRole DeliveryPartyRole)` makes buyer/non-buyer distinction logically enforced.
- CQ5 — What information is displayed about the involved organizations? — ✅ `hasAddress`, `hasIdentifier`, `hasGLN`, `hasOrganizationName` data property.
- CQ6 — What is the address of the buyer? — ✅ `hasAddress` (Organization → Address); `addressLine`, `postalCode`, `city`, `countryCode` data properties on Address.
- CQ7 — What items are sold in the invoice? — ✅ `hasLineItem` (DetailSection → LineItem) + `describesItem` (LineItem → Item).
- CQ8 — What information is displayed about items sold? — ✅ `itemDescription` on Item; price/quantity/name/description attributes all present.
- CQ9 — What is the net price of the items? — ✅ `hasNetPrice` (LineItem → Price) + `netPrice` decimal property. Unambiguous path.
- CQ10 — What are the invoice details? — ✅ Header/Detail/Summary sections with dedicated `hasHeader`, `hasDetail`, `hasSummary` properties.
- CQ11 — What is the invoice amount? — ✅ `hasInvoiceAmount` (SummarySection → InvoiceAmount) + decimal data property.
- CQ12 — What is the invoice number? — ✅ `hasInvoiceNumber` (HeaderSection → string).
- CQ13 — What information must be provided for format validity? — ✅ `ValidationConstraint` class with `conformsToConstraint` and `constraintDescription`.
- CQ14 — To which business process can the invoice be assigned? — ✅ `assignedToProcess` (InvoiceMessage → BusinessProcess).

**Structural Ratios (OntoQA):**

- **RR:** 0.9048 — Excellent. The highest RR in the triAgent cohort reflects that object properties vastly outnumber taxonomic links: 38 object properties versus a small inheritance footprint of 4 subClassOf edges. The graph is highly interconnected.
- **AR:** 0.4583 — Reasonable. 11 data properties across 24 classes gives per-class attribute richness slightly above the cohort average.
- **IR:** 0.1667 — Notably low. Only 4 subClassOf edges across 24 classes means the taxonomy is almost flat. While this keeps the hierarchy shallow and clean, it also means ontology reasoners cannot infer much from taxonomic position alone.

**Design Patterns & Domain Representation:**

The ontology correctly implements both required N-ary patterns: the `OrganizationRoleAssignment` pivot (with `owl:equivalentClass` intersection) and the `LineItem` pivot linking items to prices and quantities. The `owl:disjointUnionOf (BuyerRole DeliveryPartyRole)` on `AgentRole` provides a strong logical constraint ensuring the buyer/delivery party distinction is exclusive and exhaustive. The `InvoiceMessage owl:equivalentClass` axiom with `someValuesFrom` for header, detail, and summary provides genuine necessary-and-sufficient conditions.

**Axiom Complexity:**

Axiom Diversity Score = 6 (from metrics), the joint-highest in the triAgent cohort alongside `20260303_070100.owl`. Uses `owl:someValuesFrom`, `owl:allValuesFrom` (via FunctionalProperty implicit constraints), `owl:inverseOf`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, and `owl:FunctionalProperty`. Three full `owl:equivalentClass` definitions are provided.

**Lexical & Annotation Quality:**

Name Strict = 1.0, Label Coverage = 1.0, Comment Coverage = 1.0. All entities carry labels and comments. Naming perfectly adheres to CamelCase for classes and lowerCamelCase for properties throughout.

**Most Critical Defect:**

The extremely flat taxonomy (IR = 0.1667, only 4 subClassOf edges across 24 classes) means the class hierarchy provides almost no logical scaffolding for inheritance-based inference or categorization. Adding intermediate abstract classes (e.g., a `Document` superclass, or grouping address types under `Address`) would improve inferential power without adding cognitive complexity.

---

### Rank 3: `EDIFACT_ontology_20260303_070100.owl`
**Weighted Score: 4.51 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? — ✅ `InvoiceMessage` subClassOf `Message`; `containsMessage` (InterchangeEnvelope → Message).
- CQ2 — Which organizations are involved in the invoice? — ✅ `involvesOrganization` (InvoiceMessage → Organization) + `PivotOrganizationRoleAssignment`.
- CQ3 — What role does organization S play in the invoice? — ✅ `PivotOrganizationRoleAssignment` with `assignedRole`, `assignedOrganization`, and uniquely a `roleContext` property back to the invoice — the most complete ternary coverage.
- CQ4 — Which organization is the buyer? — ✅ `BuyerRole` subClassOf `AgentRole`. OOPS-free, consistent.
- CQ5 — What information about involved organizations? — ✅ `hasAddress`, `hasIdentifier`, `hasWarehouseAddress`, `hasHeadquartersAddress`; `hasOrganizationName`, `hasGLN` data properties.
- CQ6 — What is the address of the buyer? — ✅ Both `hasWarehouseAddress` and `hasHeadquartersAddress` as specialized address properties — richest address modeling in the cohort.
- CQ7 — What items are sold? — ✅ `hasItem` (DetailSection → Item) with inverse; though no separate pivot class for LineItem (items directly on Detail section), this is a minor structural simplification.
- CQ8 — What information about items sold? — ✅ `hasQuantity` (Item → decimal), `hasNetPrice` (Item → Price), `hasItemDescription`.
- CQ9 — What is the net price? — ✅ `hasNetPrice` (Item → Price) + `hasNetPrice` data property (decimal) on Price. Clean path.
- CQ10 — What are the invoice details? — ✅ Three-section structure with `hasHeader`, `hasDetail`, `hasSummary`.
- CQ11 — What is the invoice amount? — ✅ `hasInvoiceAmount` (SummarySection → InvoiceAmount object property) + object `InvoiceAmount` class.
- CQ12 — What is the invoice number? — ✅ `hasInvoiceNumber` (InvoiceHeader → string), `hasDocumentDate` functional property.
- CQ13 — What information must be provided for validity? — ✅ `hasMandatoryIdentifier` (InvoiceMessage → string) + structural completeness enforced by `owl:equivalentClass` on `InvoiceMessage`.
- CQ14 — To which business process? — ✅ `referencesBusinessProcess` (InvoiceMessage → BusinessProcess) with functional property declaration and inverse.

**Structural Ratios (OntoQA):**

- **RR:** 0.8718 — Very high, second only to `20260303_061520` in the triAgent cohort. 34 object properties vs. 5 subClassOf edges shows strong interconnectedness.
- **AR:** 0.5000 — The highest AR score in the triAgent cohort. With 12 data properties across 24 classes, instances carry rich attribute data — this is the best attribute density in the group.
- **IR:** 0.2083 — Low but slightly better than Rank 2. 5 subClassOf edges across 24 classes. The hierarchy is shallow but not completely flat.

**Design Patterns & Domain Representation:**

This ontology stands out for its most thorough treatment of the organization role pattern: the `PivotOrganizationRoleAssignment` carries three properties — `assignedRole`, `assignedOrganization`, and `roleContext` — explicitly binding the role to its invoice context. This makes the pivot class a true ternary reification, enabling queries like "what role does organization X play in invoice Y?" with a single JOIN rather than three. The address specialization (`WarehouseAddress`, `HeadquartersAddress`) maps directly to the E/D/E multi-role scenario described in the domain context. Axiom Diversity 7 (joint-highest in the cohort).

**Axiom Complexity:**

Axiom Diversity Score = 7 (tied for highest in triAgent cohort). The ontology uses `owl:someValuesFrom`, `owl:inverseOf`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:FunctionalProperty`, `owl:disjointWith`, and `owl:disjointUnionOf`. The `InvoiceMessage owl:equivalentClass` restriction with `someValuesFrom` for all three sections is logically well-formed, and the `PivotOrganizationRoleAssignment` intersection axiom includes the context triple.

**Lexical & Annotation Quality:**

Name Strict = 1.0, Label Coverage = 1.0, Comment Coverage = 1.0. Perfect metadata and naming compliance throughout.

**Most Critical Defect:**

The ontology omits a dedicated pivot/reification class for line items (items are directly linked from `DetailSection` via `hasItem`, without the intermediate `LineItem` class). This collapses the LIN segment structure and prevents distinct queries about item-quantity-price combinations per line position, which is essential for CQ8 and CQ9 at line granularity.

---

## Bottom Ontologies: Summary

---

**`EDIFACT_ontology_20260303_091850.owl` (Rank 5):** A well-structured ontology (RR = 0.88, highest in the cohort) with 44 object properties across 22 classes. It correctly implements the pivot pattern for organization roles. However, it misses a dedicated LineItem class, relying instead on direct `hasItem` from the detail section, which impairs precise querying of per-line price/quantity data (CQ8, CQ9). With only 4 data properties (AR = 0.18, lowest AR in the top half), attribute richness is poor. It receives OOPS validation green ✅. Axiom Diversity 5.

**`EDIFACT_ontology_20260302_082612.owl` (Rank 6):** 42 object properties across 22 classes (RR = 0.913, highest absolute RR in the cohort), with good pivot patterns for both organization roles and item-invoice assignments using named pivot classes (`PivotOrganizationRole`, `PivotItemInvoice`). However, it scores OOPS ✅ but has extremely sparse data properties (AR = 0.2273, 5 data properties total), meaning CQs about specific field values (address lines, GLN values, net price as a value) cannot be answered adequately. Three `owl:equivalentClass` axioms are present. Axiom Diversity 6.

**`EDIFACT_ontology_20260303_085821.owl` (Rank 7):** OOPS ❌ (pitfall flagged). 27 classes, 34 object properties, only 3 data properties (AR = 0.1111 — critically low). The pivot pattern is present (`RoleAssignment`) and role subclasses are defined. However, sparse attribute modeling means most CQs about data values (address details, prices, amounts) require external resolution. The OOPS pitfall and very low AR prevent a higher ranking. Axiom Diversity 5.

**`EDIFACT_ontology_20260302_081000.owl` (Rank 8):** The largest ontology in the cohort by class count (37 classes), yet has the lowest RR (0.5769) — indicating that the class proliferation is driven by segment-level subclasses (NADBuyer, NADSupplier, NADDeliveryParty, DTM137, MOA77, etc.) rather than by a rich property network. This segment-oriented design pattern confuses EDIFACT syntax classes with domain classes, blurring the modeling of organizational roles. The pivot `OrganizationRoleAssignment` is present but under-utilized. Only 8 data properties (AR = 0.2162) and Axiom Diversity 2 (lowest in cohort) make it the weakest on axiom complexity. CQs on roles are answerable but indirectly (through NAD subclasses rather than an agile role pattern).

**`EDIFACT_ontology_20260302_133553.owl` (Rank 9):** The smallest triAgent ontology by triple count (270). Only 28 classes, 23 object properties, 3 data properties (AR = 0.1071 — lowest in the cohort). No role subclasses (BuyerRole, DeliveryPartyRole) are defined; role differentiation must be inferred from freeform AgentRole instances, making CQ4 (finding the buyer) ambiguous. Missing line item pivot class. Naming is not fully strict CamelCase (Naming Strict = 0.9444, Underscore Score = 0.0556 — the only ontology in the cohort with non-conformant URIs). OOPS ✅. Axiom Diversity 5.

**`EDIFACT_ontology_20260302_124024.owl` (Rank 10):** OOPS ❌. Only 2 data properties (AR = 0.0667 — lowest in the entire cohort by a large margin). While 27 object properties across 30 classes model structure, the near-total absence of datatype properties means virtually no data values (net price, invoice number, address details, GLN, invoice amount) can be stored or queried. This systematically blocks CQs 6, 8, 9, 11, 12. The organization role model lacks BuyerRole/DeliveryPartyRole subclasses. Axiom Diversity 4. This ontology fails on the fundamental data representation axis.

**`EDIFACT_ontology_20260303_094621.owl` (Rank 11):** OOPS ❌. Tied with Rank 10 on weighted score (3.38). With 30 classes and 42 object properties (RR = 0.7925), the property graph looks healthy, but only 7 data properties (AR = 0.2333) means attribute modeling is sparse. CQs about net price, invoice number, and address fields are partially met through data properties but without sufficient domain coverage. No role subclasses (BuyerRole, DeliveryPartyRole) are defined. The `Pivot_OrganizationRoleAssignment` pivot is correctly structured with `owl:equivalentClass` and `owl:allValuesFrom`, but the use of `allValuesFrom` rather than `someValuesFrom` on both arms of the intersection axiom means the equivalence condition is vacuously satisfied for instances with no role or organization links — a logical deficiency. OOPS ❌ further penalizes this entry.
