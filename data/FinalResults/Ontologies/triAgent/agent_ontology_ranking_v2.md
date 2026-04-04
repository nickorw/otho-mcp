# triAgent EDIFACT Ontology Evaluation — Ranked Report

**Evaluation Date:** 2026-03-08
**Ontology Group:** triAgent (11 ontologies)
**Domain:** UN/EDIFACT INVOIC message (EDI procurement invoice)
**Evaluator methodology:** Multi-dimensional weighted scoring across CQ Coverage (40%), Structural Ratios (20%), Design Patterns (15%), Axiom Complexity (15%), Lexical & Annotation Quality (10%).

---

## Evaluation Criteria Weights

| Dimension | Weight | Description |
|---|---|---|
| CQ Coverage | 40% | Coverage of 14 competency questions derived from the INVOIC domain |
| Structural Ratios (OntoQA) | 20% | Relationship Richness (RR), Attribute Richness (AR), Inheritance Richness (IR) |
| Design Patterns | 15% | Correct use of pivot/reification, clean subsumption hierarchies, OWL disjointness |
| Axiom Complexity | 15% | Axiom Diversity score and appropriate use of advanced OWL constructs |
| Lexical & Annotation | 10% | Naming convention compliance, label coverage, comment coverage |

---

### Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|---|---|---|---|---|---|---|---|---|
| 1 | `EDIFACT_ontology_20260303_070100.owl` | 14/14 | 4.3 | 4.0 | 4.2 | 4.5 | 5.0 | **4.33** |
| 2 | `EDIFACT_ontology_20260303_061520.owl` | 14/14 | 4.4 | 4.0 | 4.0 | 4.0 | 5.0 | **4.26** |
| 3 | `EDIFACT_ontology_20260302_140235.owl` | 14/14 | 4.4 | 4.5 | 3.5 | 3.5 | 5.0 | **4.21** |
| 4 | `EDIFACT_ontology_20260302_082612.owl` | 14/14 | 4.0 | 3.5 | 3.5 | 4.0 | 5.0 | **3.93** |
| 5 | `EDIFACT_ontology_20260302_073654.owl` | 14/14 | 4.0 | 2.5 | 3.0 | 4.5 | 5.0 | **3.73** |
| 6 | `EDIFACT_ontology_20260303_091850.owl` | 14/14 | 3.9 | 3.0 | 3.5 | 3.5 | 5.0 | **3.71** |
| 7 | `EDIFACT_ontology_20260302_124024.owl` ❌ OOPS | 14/14 | 3.8 | 2.5 | 3.5 | 3.0 | 5.0 | **3.50** |
| 8 | `EDIFACT_ontology_20260302_133553.owl` | 14/14 | 3.7 | 2.5 | 2.5 | 3.5 | 4.5 | **3.33** |
| 9 | `EDIFACT_ontology_20260303_094621.owl` ❌ OOPS | 14/14 | 3.5 | 3.0 | 2.0 | 3.5 | 5.0 | **3.33** |
| 10 | `EDIFACT_ontology_20260303_085821.owl` ❌ OOPS | 14/14 | 3.5 | 2.5 | 2.5 | 3.5 | 5.0 | **3.30** |
| 11 | `EDIFACT_ontology_20260302_081000.owl` | 13/14 | 3.8 | 2.5 | 2.5 | 1.5 | 5.0 | **3.12** |

> Ranks 8 and 9 share the same weighted score (3.33). `EDIFACT_ontology_20260302_133553.owl` is placed higher due to OOPS validation passing, giving it a quality assurance advantage over the OOPS-failing `20260303_094621.owl`.

---

### Top 3 Detailed Analysis

#### Rank 1: `EDIFACT_ontology_20260303_070100.owl`
**Weighted score:** 4.33 / 5.00
**Validation:** OOPS ✅ | HermiT ✅ | Pellet ✅

**CQ Coverage Analysis:**
- CQ1 (What EDIFACT message type is modeled?) — Covered ✅ — `InvoiceMessage` class explicitly represents the INVOIC message type.
- CQ2 (Which organizations are involved in an invoice?) — Covered ✅ — `RoleAssignment` pivot with `involvesOrganization someValuesFrom Organization`; InvoiceMessage linked via `allValuesFrom RoleAssignment`.
- CQ3 (What role does each organization play?) — Covered ✅ — `hasAgentRole` property on `RoleAssignment` links to `AgentRole`; pivot provides role context per-invoice.
- CQ4 (Who is the buyer organization?) — Partially covered ⚠️ — No `BuyerRole` or `DeliveryPartyRole` subclasses defined; buyer identity relies on instance-level `AgentRole` assignments rather than class-based typing.
- CQ5 (What is an organization's identifying information?) — Covered ✅ — `hasOrganizationName`, `hasGLN` data properties; `Identifier` class with `hasIdentifier` property.
- CQ6 (What is an organization's address?) — Covered ✅ — `Address` hierarchy with `WarehouseAddress` and `HeadquartersAddress` subclasses; `hasAddressLine` data property; `hasAddress` object property on Organization.
- CQ7 (What items appear on an invoice?) — Covered ✅ — `LineItem` pivot with `describesItem someValuesFrom Item`; `InvoiceDetail allValuesFrom LineItem`.
- CQ8 (What are the item details: description, quantity?) — Covered ✅ — `hasItemDescription` and `hasQuantity` data properties on `LineItem`.
- CQ9 (What is the net price of a line item?) — Covered ✅ — `hasNetPrice` data property on `LineItem`.
- CQ10 (What are the invoice sections?) — Covered ✅ — `InvoiceMessage owl:disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` provides a strong semantic partition.
- CQ11 (What is the total invoice amount?) — Covered ✅ — `hasInvoiceAmount` data property; `InvoiceSummary someValuesFrom Tax` ✅.
- CQ12 (What is the invoice reference number?) — Covered ✅ — `hasInvoiceNumber` and `hasReferenceNumber` data properties explicitly modeled.
- CQ13 (Which fields are mandatory?) — Covered ✅ — `hasMandatoryIdentifier` data property provides a literal hook for mandatory field annotation; could be deeper but the mechanism is present.
- CQ14 (What business process does the invoice belong to?) — Covered ✅ — `BusinessProcess` class with `assignedToBusinessProcess` object property on `InvoiceMessage`.

**Structural Ratios (OntoQA):**
- **RR:** 0.8718 — Strong relationship richness; the ontology models interactions through object properties generously, placing it well above the 0.8 ideal threshold.
- **AR:** 0.5000 — Best attribute richness in the entire triAgent group. Twelve data properties (hasDocumentDate, hasReferenceNumber, hasInvoiceNumber, hasOrganizationName, hasAddressLine, hasGLN, hasNetPrice, hasQuantity, hasInvoiceAmount, hasTaxAmount, hasItemDescription, hasMandatoryIdentifier) provide thorough literal-value coverage for SPARQL-queryable facts.
- **IR:** 0.2083 — Below the ideal 0.3–0.6 band; the taxonomy is relatively flat. The address hierarchy (Warehouse/HQ subclasses) and the Segment hierarchy are present but the overall inheritance depth is shallow (Max Depth = 1, Avg Depth = 0.21).

**Design Patterns & Domain Representation:**
The `owl:disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` constraint on `InvoiceMessage` is the cleanest structural partitioning among all triAgent ontologies — it guarantees sections are mutually exclusive and exhaustive parts of the invoice. The `RoleAssignment` pivot correctly reifies the ternary relationship between invoice, organization, and role using `owl:equivalentClass` with `someValuesFrom` restrictions. The `WarehouseAddress` and `HeadquartersAddress` subclass hierarchy is domain-accurate for the warehouse-delivery/buyer-HQ distinction common in EDIFACT INVOIC scenarios. The sole structural weakness is the absence of `BuyerRole` and `DeliveryPartyRole` named subclasses of `AgentRole`, which forces buyer identification to rely on instance data rather than class-level inference.

**Axiom Complexity:**
Axiom Diversity = 7 (tied highest in triAgent group), employing `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:inverseOf`, `owl:disjointWith`, and `owl:disjointUnionOf` — the full spectrum of OWL RL/EL constructs used in a meaningful and semantically justified way on pivot classes, section partitions, and property chains.

**Lexical & Annotation Quality:**
Name Strict = 1.0, Label Coverage = 1.0, Comment Coverage = 1.0. All classes and properties follow strict CamelCase/camelCase conventions, and every entity has both an `rdfs:label` and `rdfs:comment`. No annotation deficiencies.

**Most Critical Defect:**
The absence of `BuyerRole` and `DeliveryPartyRole` as named subclasses of `AgentRole` prevents class-level reasoning about buyer-specific constraints and forces CQ3/CQ4 competency to rely entirely on instance-level assertions rather than ontology-level entailments.

---

#### Rank 2: `EDIFACT_ontology_20260303_061520.owl`
**Weighted score:** 4.26 / 5.00
**Validation:** OOPS ✅ | HermiT ✅ | Pellet ✅

**CQ Coverage Analysis:**
- CQ1 (What EDIFACT message type is modeled?) — Covered ✅ — `InvoiceMessage` class is the central message type.
- CQ2 (Which organizations are involved in an invoice?) — Covered ✅ — `RoleAssignment` pivot reifies `involvesOrganization someValuesFrom Organization`; `InvoiceMessage` linked via `allValuesFrom RoleAssignment`.
- CQ3 (What role does each organization play?) — Covered ✅ — `hasAgentRole` property on the `RoleAssignment` pivot resolves the role per invoice context.
- CQ4 (Who is the buyer organization?) — Partially covered ⚠️ — No explicit `BuyerRole` subclass; a direct `playsRole` shortcut from `Organization` to `AgentRole` blurs the context-specific role assignment.
- CQ5 (What is an organization's identifying information?) — Covered ✅ — `Organization owl:equivalentClass` restriction with `hasIdentifier someValuesFrom Identifier`; `GLNIdentifier` as a named subclass of `Identifier` provides strong GLN typing.
- CQ6 (What is an organization's address?) — Covered ✅ — `Address` class, `hasAddress` on `Organization`, `addressLine`, `postalCode`, `cityName`, `countryCode` data properties.
- CQ7 (What items appear on an invoice?) — Covered ✅ — `LineItem` pivot with `describesItem someValuesFrom Item`; `InvoiceDetail` links to `LineItem`.
- CQ8 (What are the item details?) — Covered ✅ — `hasQuantity` and `lineItemNetPrice` data properties on `LineItem`.
- CQ9 (What is the net price of a line item?) — Covered ✅ — `hasNetPrice` / `lineItemNetPrice` data property explicitly present.
- CQ10 (What are the invoice sections?) — Covered ✅ — `InvoiceMessage owl:disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` ✅; sections are independent classes (no problematic super-class inheritance).
- CQ11 (What is the total invoice amount?) — Covered ✅ — `hasInvoiceAmount` data property; `InvoiceSummary` scoped to summary-level aggregates.
- CQ12 (What is the invoice reference number?) — Covered ✅ — `ReferenceNumber` class; `referenceValue` data property; `hasInvoiceNumber` (via `ReferenceNumber`).
- CQ13 (Which fields are mandatory?) — Covered ✅ — `ValidationConstraint` class with `constraintDescription` data property; `hasMandatoryIdentifier` provides a direct hook for mandatory identifier modeling.
- CQ14 (What business process does the invoice belong to?) — Covered ✅ — `BusinessProcess` class with `assignedToBusinessProcess` object property.

**Structural Ratios (OntoQA):**
- **RR:** 0.9048 — Highest relationship richness in the triAgent group. The ontology uses object properties extensively, with 38 object properties across 24 classes.
- **AR:** 0.4583 — Strong attribute coverage; 11 data properties cover addresses, GLN values, prices, quantities, reference values, tax amounts, and constraint descriptions.
- **IR:** 0.1667 — Lowest inheritance richness in the group (Max Depth = 1, Avg Depth = 0.17). The flat taxonomy is deliberate — sections are standalone classes without a shared parent, which is semantically cleaner but reduces inheritance expressiveness.

**Design Patterns & Domain Representation:**
The `owl:disjointUnionOf` on `InvoiceMessage` is correctly applied and matches the approach of Rank 1, ensuring sections are modeled as exhaustive-exclusive parts of the invoice at the schema level. The `GLNIdentifier` as a named subclass of `Identifier` is the cleanest identifier hierarchy in the group, enabling GLN-specific reasoning. The `Organization owl:equivalentClass` restriction (requiring both `hasAddress` and `hasIdentifier`) adds necessary conditions, strengthening organizational identity. The one structural concern is the direct `playsRole` property from `Organization` to `AgentRole`, which bypasses the pivot and allows role assertions outside invoice context — this is a minor but semantically meaningful shortcut that weakens context-bound role reasoning.

**Axiom Complexity:**
Axiom Diversity = 6, employing `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:inverseOf`, and `owl:disjointWith`. Advanced constructs are applied on pivot classes and the invoice message partition, demonstrating purposeful OWL usage rather than superficial decoration.

**Lexical & Annotation Quality:**
Name Strict = 1.0, Label Coverage = 1.0, Comment Coverage = 1.0. All entities follow standard naming conventions and are fully annotated.

**Most Critical Defect:**
The `playsRole` shortcut property linking `Organization` directly to `AgentRole` — bypassing the `RoleAssignment` pivot — allows role assignments to be made outside the context of any specific invoice, undermining the context-bounded role modeling that the pivot pattern was designed to enforce.

---

#### Rank 3: `EDIFACT_ontology_20260302_140235.owl`
**Weighted score:** 4.21 / 5.00
**Validation:** OOPS ✅ | HermiT ✅ | Pellet ✅

**CQ Coverage Analysis:**
- CQ1 (What EDIFACT message type is modeled?) — Covered ✅ — `InvoiceMessage` as the central class.
- CQ2 (Which organizations are involved in an invoice?) — Covered ✅ — `OrganizationRoleAssignment` pivot; `isRoleAssignmentOf` links assignment to `InvoiceMessage`.
- CQ3 (What role does each organization play?) — Covered ✅ — `assignedRole someValuesFrom AgentRole` on `OrganizationRoleAssignment`.
- CQ4 (Who is the buyer organization?) — Covered ✅ — `BuyerRole` and `DeliveryPartyRole` as explicit named subclasses of `AgentRole`; `AgentRole owl:disjointUnionOf (BuyerRole DeliveryPartyRole)` enforces disjointness.
- CQ5 (What is an organization's identifying information?) — Covered ✅ — `organizationName`, `hasGlobalLocationNumber` data properties on `Organization`.
- CQ6 (What is an organization's address?) — Covered ✅ — `Address` class; richest address data in the group: `addressLine`, `postalCode`, `city`, `countryCode` data properties.
- CQ7 (What items appear on an invoice?) — Covered ✅ — `InvoiceItemDetail` pivot with `hasItem functional` property linking to `Item`.
- CQ8 (What are the item details?) — Covered ✅ — `itemDescription`, `quantityValue` data properties; `hasQuantity` functional on `InvoiceItemDetail`.
- CQ9 (What is the net price of a line item?) — Covered ✅ — `netPrice` data property on `InvoiceItemDetail`; `hasPrice functional` on the pivot.
- CQ10 (What are the invoice sections?) — Covered ✅ — `Section` parent class; `HeaderSection`, `DetailSection`, `SummarySection` as subclasses of `Section`.
- CQ11 (What is the total invoice amount?) — Covered ✅ — `InvoiceAmount` class; `invoiceAmountValue` data property; `TaxAmount` with `taxAmountValue`.
- CQ12 (What is the invoice reference number?) — Covered ✅ — `ReferenceNumber` class; `referenceNumberValue` data property.
- CQ13 (Which fields are mandatory?) — Covered ✅ — `ValidationConstraint` class; `constraintDescription` data property for constraint annotations.
- CQ14 (What business process does the invoice belong to?) — Covered ✅ — `BusinessProcess` and `P2PCoreClass`; `assignedToProcess` object property.

**Structural Ratios (OntoQA):**
- **RR:** 0.7843 — Good relationship richness, slightly below the ideal 0.8 threshold, but acceptable given the 40 object properties across 29 classes.
- **AR:** 0.4828 — Second-highest attribute richness in the group. Fourteen data properties provide the most granular literal-level coverage: address fields, item description, net price, quantity value, reference number, document date, tax amount, invoice amount, constraint description, GLN, and organization name. This is the ontology's greatest strength.
- **IR:** 0.3793 — Healthiest inheritance richness in the triAgent group (Max Depth = 2, Avg Depth = 0.38), sitting squarely in the ideal 0.3–0.6 band.

**Design Patterns & Domain Representation:**
The `OrganizationRoleAssignment` and `InvoiceItemDetail` pivot classes are correctly implemented with `owl:equivalentClass` and `owl:someValuesFrom` restrictions. The `AgentRole owl:disjointUnionOf (BuyerRole DeliveryPartyRole)` constraint is the strongest role-subclass pattern in the group and enables class-level reasoning about buyer identity. The critical architectural flaw is that `HeaderSection`, `DetailSection`, and `SummarySection` are declared as subclasses of both `Section` AND `InvoiceMessage` — this creates logical overloading where every section instance is also typed as an invoice, violating the part-whole intuition and introducing potential inconsistency with `InvoiceMessage`-level restrictions.

**Axiom Complexity:**
Axiom Diversity = 5, with `owl:equivalentClass`, `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:inverseOf`, `owl:disjointWith`, `owl:disjointUnionOf`, and the unusual `owl:AsymmetricProperty` annotation on select properties. The asymmetric property usage, while not standard for this domain, reflects an attempt to express directional semantics. The `InvoiceMessage equivalentClass allValuesFrom Section` restriction is logically weak (allValuesFrom on an existential context should be accompanied by someValuesFrom to assert existence).

**Lexical & Annotation Quality:**
Name Strict = 1.0, Label Coverage = 1.0, Comment Coverage = 1.0. All 29 classes and all properties are fully named, labeled, and commented.

**Most Critical Defect:**
`HeaderSection`, `DetailSection`, and `SummarySection` inherit from both `Section` and `InvoiceMessage` simultaneously — semantically asserting that every invoice section is itself a complete invoice — which is logically unsound and will cause unintended entailments in any reasoner that propagates `InvoiceMessage`-level restrictions to the section level.

---

### Bottom Ontologies: Summary

**`EDIFACT_ontology_20260302_082612.owl` (Rank 4, Score: 3.93):** This ontology achieves the highest relationship richness in the triAgent group (RR = 0.913) and implements two clean `owl:equivalentClass` pivot classes — `PivotOrganizationRole` (linking organization and role via `someValuesFrom`) and `PivotItemInvoice` (linking item, price, and quantity) — which are among the best-formed pivots in the group. The `Invoice owl:equivalentClass` restriction with `hasHeader`, `hasDetail`, and `hasSummary` properties is logically sound. However, the ontology commits the significant design error of modeling `HeaderSection`, `DetailSection`, and `SummarySection` as subclasses of `Invoice` rather than as parts or components — making every section an instance of Invoice, which is semantically incorrect. Buyer, Supplier, and DeliveryParty are instances of `AgentRole` rather than named subclasses, limiting class-level reasoning for CQ3/CQ4. Attribute richness is moderate (AR = 0.2273), and the very flat inheritance (IR = 0.1818) limits taxonomic depth.

**`EDIFACT_ontology_20260302_073654.owl` (Rank 5, Score: 3.73):** This ontology stands out for the most sophisticated use of OWL constructs in the group — Axiom Diversity = 7 (tied highest), employing `owl:equivalentClass`, `owl:disjointUnionOf`, `owl:FunctionalProperty`, and `owl:allValuesFrom` in combination. The `OrganizationRoleAssignment` and `InvoiceLineItem` pivot classes are well-formed, and the `disjointUnionOf` on `AgentRole` correctly constrains role subclasses. It also includes a `P2PAlignment` class for process alignment and domain-relevant classes like `Price`, `Quantity`, `TaxAmount`, and `InvoiceAmount`. Despite this expressive richness, the ontology contains a critical semantic error: `Address` is modeled as a subclass of `Organization`, which logically entails that every address is also an organization — a fundamental conceptual inversion that would corrupt any reasoning over organizational identity or address-based queries. Additionally, Attribute Richness is critically low (AR = 0.0741, only 2 data properties: `hasDocumentDate` and `mandatoryIdentifier`), making literal-level CQ answering effectively impossible.

**`EDIFACT_ontology_20260303_091850.owl` (Rank 6, Score: 3.71):** The strongest feature of this ontology is its three-way pivot class `PivotOrganizationRoleAssignment`, which is unique in the group for linking three dimensions: `assignedRole someValuesFrom AgentRole`, `assignedOrganization someValuesFrom Organization`, AND `roleContext someValuesFrom InvoiceMessage`. This roleContext binding is the most sophisticated role-context modeling in the triAgent set, explicitly tying role assignments to their invoice context. The ontology also includes `hasWarehouseAddress` and `hasHeadquartersAddress` properties for address subtyping. However, the `HeaderSection`, `DetailSection`, and `SummarySection` classes are incorrectly modeled as subclasses of `Segment` rather than as invoice partitions — a serious structural error. No `BuyerRole` or `DeliveryPartyRole` subclasses are defined, and attribute richness is low (AR = 0.1818, only 4 data properties). These limitations significantly reduce its practical utility.

**`EDIFACT_ontology_20260302_124024.owl` (Rank 7, Score: 3.50) — OOPS FAILED ❌:** This ontology has a clean conceptual architecture: a `Section` parent class with `HeaderSection`, `DetailSection`, `SummarySection` as proper subclasses (the cleaner section modeling approach), well-formed `RoleAssignment` and `LineItem` pivot classes with `owl:equivalentClass` restrictions, explicit `BuyerRole` and `DeliveryPartyRole` subclasses of `AgentRole`, and a `ValidationConstraint` class. The structural logic is sound. However, three issues prevent a higher ranking: (1) OOPS validation fails, indicating unresolved ontology pitfalls (likely missing domain/range declarations on some properties and disconnected entities); (2) Attribute Richness is the lowest in the group at AR = 0.0667 (only 2 data properties), making it impossible to answer any CQ requiring literal values for prices, quantities, addresses, or reference numbers at the data level; (3) Axiom Diversity is low at 4. The conceptual skeleton is one of the better designs, but the practical execution is severely underdeveloped.

**`EDIFACT_ontology_20260302_133553.owl` (Rank 8, Score: 3.33):** This ontology includes notable alignment classes (`EN16931Compliance`, `P2POAlignment`, `SHACLConstraint`) and a `Delimiter` class for EDIFACT-specific syntax detail, showing domain awareness beyond core invoice semantics. However, it suffers from multiple deficiencies. First, naming convention violations: `BGM_Segment`, `NAD_Segment`, and `Pivot_OrganizationRoleAssignment` use underscores instead of CamelCase, resulting in a Name Strict score of 0.9444. Second, `HeaderSection`, `DetailSection`, and `SummarySection` are incorrectly typed as subclasses of `Segment`. Third, the pivot class uses only `owl:allValuesFrom` restrictions (semantically weak — asserting that IF a role assignment exists its values must be of the given type, but not asserting that any role assignment exists) rather than the stronger `owl:someValuesFrom`. Attribute richness is low (AR = 0.1071, only 3 data properties).

**`EDIFACT_ontology_20260303_094621.owl` (Rank 9, Score: 3.33) — OOPS FAILED ❌:** This ontology introduces an unusual dual role hierarchy — both `AgentRole` and `OrganizationRole` exist as separate root classes, with `BuyerRole` and `DeliveryPartyRole` subclassing `OrganizationRole` rather than `AgentRole`. The relationship between these two role hierarchies is undefined, creating confusion about which properties should use which root. Additionally, `LineItem` is typed as a subclass of `Item`, which misrepresents the semantics (a line item is a billing record referencing an item, not a type of item). The `AgentRoleAssignment` pivot has only a single `inContextOfInvoice` restriction, making it structurally incomplete. OOPS validation fails. The ontology also includes `WarehouseAddress` and `HeadquartersAddress` subclasses (a positive feature) and both `EN16931Alignment` and `P2POAlignment` classes. Despite 30 classes (third-highest in the group), design incoherence limits its score severely.

**`EDIFACT_ontology_20260303_085821.owl` (Rank 10, Score: 3.30) — OOPS FAILED ❌:** This ontology contains a reasonably well-formed `OrganizationRoleAssignment` pivot with `owl:equivalentClass` and `someValuesFrom` on both `assignedOrganization` and `assignedRole`, and an `Invoice owl:equivalentClass` restriction linking to organizations and business processes. It includes `BuyerRole` and `DeliveryPartyRole` subclasses of `AgentRole`, an `EN16931Alignment` class, and a `P2POCoreClass` for process alignment. However, `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` are all subclasses of `Segment` — placing structural containers at the same level as individual EDIFACT segments. OOPS validation fails. Attribute richness is very low (AR = 0.1111, only 3 data properties), and the ontology uses the name `INVOICMessage` (non-standard) rather than `InvoiceMessage`. These compounding issues place it second-to-last.

**`EDIFACT_ontology_20260302_081000.owl` (Rank 11, Score: 3.12):** The lowest-ranked ontology in the triAgent group. Its primary distinction is the largest class count (37 classes), achieved through highly granular EDIFACT segment specialization — `DTM137DocumentDate`, `DTM35DeliveryDate`, `DTM11DespatchDate`, `MOA77InvoiceAmount`, `MOA176TotalTax` — which models the EDIFACT message syntax rather than the business semantics. This segment-centric approach produces two major design flaws: `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` are modeled as subclasses of `CompositeDataElement` (placing invoice sections at the EDIFACT element level), and `Buyer`, `Supplier`, and `DeliveryParty` are instances of `AgentRole` rather than named subclasses, preventing class-level role reasoning. Axiom Diversity is the lowest in the group at 2 — almost no OWL constructs beyond declarations and subClassOf assertions, with no `owl:equivalentClass`, `owl:someValuesFrom`, or `owl:disjointWith`. Relationship richness is also the lowest at RR = 0.5769. CQ13 (mandatory field validity) is not explicitly modeled. Despite passing all validation checks, this ontology's near-total absence of advanced OWL axioms makes it more a structured vocabulary than a formal ontology.

---

## Key Cross-Cutting Observations

### Recurring Design Flaw: Sections as Subclasses
The most pervasive design flaw across the triAgent group is incorrect modeling of invoice sections (`HeaderSection`, `DetailSection`, `SummarySection`). Seven of eleven ontologies mistype sections as subclasses of `Segment` (ranks 6, 8, 10), `CompositeDataElement` (rank 11), `Invoice`/`InvoiceMessage` (rank 4), or a dual `Section`+`InvoiceMessage` inheritance (rank 3). Only ranks 1, 2, 7, and partially 9 (via the `Section` parent class) model sections as independent partition classes of the invoice, with the `owl:disjointUnionOf` pattern on `InvoiceMessage` in ranks 1 and 2 being the semantically correct formulation.

### Role Subclass Patterns
Only four ontologies define named role subclasses (`BuyerRole`, `DeliveryPartyRole`) as proper children of `AgentRole`: ranks 3, 5, 7, and 10. Of these, ranks 3 and 7 additionally apply `owl:disjointUnionOf` to enforce role exclusivity. The majority of ontologies rely on instance-level role assignment, which limits the reasoner's ability to infer buyer-specific constraints from the ontology schema alone.

### Attribute Richness Deficiency
Six of eleven ontologies have AR below 0.25, indicating critical underdevelopment of data properties. This limits practical SPARQL query answering for facts like prices, quantities, addresses, dates, and reference numbers. The top three ontologies (AR = 0.50, 0.46, 0.48) demonstrate that comprehensive data property coverage is achievable within the same domain scope.

### OOPS Validation
Three ontologies fail OOPS validation (`20260302_124024`, `20260303_094621`, `20260303_085821`), indicating unresolved ontology pitfalls such as missing domain/range declarations, disconnected components, or structurally problematic axioms. All three rank in the bottom half of the group (ranks 7, 9, 10 respectively).
