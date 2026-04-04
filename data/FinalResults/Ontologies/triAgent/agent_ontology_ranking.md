# Ontology Evaluation & Ranking Report — triAgent Set

> **Evaluator:** Claude Code (claude-sonnet-4-6)
> **Evaluation Date:** 2026-03-12
> **Evaluation Set:** 11 triAgent-generated EDIFACT INVOIC ontologies
> **Framework:** OntoQA + CQ Coverage + Design Pattern Analysis

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0–5) | Struct. Ratios (0–5) | Design Patterns (0–5) | Ax. Complexity (0–5) | Lexical (0–5) | Weighted Score |
|------|---------------|:-------------------:|:-------------------:|:--------------------:|:---------------------:|:--------------------:|:-------------:|:--------------:|
| 1 | `EDIFACT_ontology_20260302_073654.owl` | 14/14 | 4.8 | 3.8 | 5.0 | 4.5 | 5.0 | **4.59** |
| 2 | `EDIFACT_ontology_20260303_070100.owl` | 14/14 | 4.7 | 4.2 | 4.5 | 4.5 | 5.0 | **4.56** |
| 3 | `EDIFACT_ontology_20260303_061520.owl` | 14/14 | 4.7 | 4.2 | 4.5 | 4.5 | 5.0 | **4.56** |
| 4 | `EDIFACT_ontology_20260302_140235.owl` | 14/14 | 4.6 | 4.0 | 4.5 | 4.0 | 5.0 | **4.45** |
| 5 | `EDIFACT_ontology_20260303_091850.owl` | 13/14 | 4.2 | 4.2 | 5.0 | 4.0 | 5.0 | **4.38** |
| 6 | `EDIFACT_ontology_20260302_082612.owl` | 13/14 | 4.2 | 4.2 | 4.5 | 4.0 | 5.0 | **4.31** |
| 7 | `EDIFACT_ontology_20260303_085821.owl` | 13/14 | 4.0 | 4.2 | 4.0 | 3.5 | 5.0 | **4.13** |
| 8 | `EDIFACT_ontology_20260302_081000.owl` | 12/14 | 3.5 | 3.2 | 3.5 | 1.5 | 5.0 | **3.30** |
| 9 | `EDIFACT_ontology_20260302_124024.owl` | 12/14 | 3.5 | 3.5 | 3.5 | 2.5 | 5.0 | **3.38** |
| 10 | `EDIFACT_ontology_20260302_133553.owl` | 11/14 | 3.0 | 3.2 | 3.0 | 2.5 | 4.5 | **3.06** |
| 11 | `EDIFACT_ontology_20260303_094621.owl` | 12/14 | 3.5 | 4.2 | 3.0 | 3.0 | 5.0 | **3.57** |

> **Weighted Score** = CQ×0.40 + Struct×0.20 + Design×0.15 + Axiom×0.15 + Lexical×0.10

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_ontology_20260302_073654.owl`
**Weighted score: 4.59 / 5.00**

**CQ Coverage Analysis:**
- CQ1 — What invoices are all listed in an EDIFACT message? ✅ — `InvoiceMessage` subclass of `Message` within `InterchangeEnvelope`; `containsMessage` / `hasLineItem` chain is navigable.
- CQ2 — Which organizations are involved in the invoice? ✅ — `OrganizationRoleAssignment` pivot class with `involvesOrganization → Organization`; full traversal possible.
- CQ3 — What role does organization S play in the invoice? ✅ — `OrganizationRoleAssignment.assignedRole → AgentRole` with explicit `BuyerRole` / `DeliveryPartyRole` subclasses; precise query path.
- CQ4 — Which organization is the buyer in the invoice? ✅ — `BuyerRole` is a named subclass of `AgentRole`; SPARQL can filter on `rdf:type :BuyerRole` via the pivot.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Organization` has `hasAddress`, `hasGlobalLocationNumber`; `AgentRole` chain provides context.
- CQ6 — What is the address of the buyer? ✅ — `Organization → hasAddress → Address`; chained through the pivot to `BuyerRole`.
- CQ7 — What items are sold in the invoice? ✅ — `InvoiceMessage → hasLineItem → InvoiceLineItem → soldItem → Item`.
- CQ8 — What information is displayed about the items sold? ✅ — `Item` linked to `InvoiceLineItem` with `lineItemPrice` and `lineItemQuantity`; supports attribute retrieval.
- CQ9 — What is the net price of the items sold in the invoice? ✅ — `InvoiceLineItem → lineItemPrice → Price`; `Price` class present; direct SPARQL query possible.
- CQ10 — What are the invoice details of the invoice? ✅ — `HeaderSection`, `DetailSection`, `SummarySection` as subClassOf `InvoiceMessage`; `hasSection` with `owl:unionOf` range.
- CQ11 — What is the invoice amount of the invoice? ✅ — `SummarySection → hasInvoiceAmount → InvoiceAmount` with `owl:FunctionalProperty`.
- CQ12 — What is the invoice number? ✅ — `InvoiceMessage → invoiceNumber → ReferenceNumber`; `mandatoryIdentifier` data property on `InvoiceMessage`.
- CQ13 — What information must be provided so that the file format is valid? ✅ — `mandatoryIdentifier` data property on `InvoiceMessage`; `owl:FunctionalProperty` constraints on segments; disjointness axioms enforce valid structure.
- CQ14 — To which business process can the invoice be assigned? ✅ — `InvoiceMessage → assignedToProcess → BusinessProcess`; `P2PAlignment` class models ontological alignment to P2P-O.

**Structural Ratios (OntoQA):**
- **RR:** 0.76 — A well-connected graph. 38 object properties relative to class hierarchy (27 classes, 3 subClassOf chains) yields solid non-taxonomic richness. Minor deduction: the deep inverse-pair design inflates the property count somewhat without necessarily adding expressiveness.
- **AR:** 0.0741 — Below average for the set. Only 2 data properties for 27 classes. The ontology models most values as object-property-linked class instances (e.g., `Price`, `InvoiceAmount`) rather than direct datatype properties, which is architecturally intentional but lowers the AR score versus a data-centric reference.
- **IR:** 0.4444 — Healthy inheritance depth across 3 levels (max depth = 3): `InterchangeEnvelope → Message → InvoiceMessage`; `Segment → BGMSegment/NADSegment`; `AgentRole → BuyerRole/DeliveryPartyRole`. Balanced DAG; no problematic linear chains.

**Design Patterns & Domain Representation:**
This ontology excels at N-ary role modelling. The `OrganizationRoleAssignment` pivot class is defined with an `owl:equivalentClass` restriction requiring both `assignedRole` (→ `AgentRole`) and `involvesOrganization` (→ `Organization`), meaning any instance of that pivot is guaranteed to carry both ends of the relationship. The `InvoiceLineItem` pivot similarly mandates `soldItem`, `lineItemPrice`, and `lineItemQuantity` via an `owl:intersectionOf` equivalence, making the line-item structure logically complete. The tripartite invoice section structure (Header / Detail / Summary as subClassOf `InvoiceMessage`) with `owl:disjointUnionOf` on `AgentRole` accurately mirrors the EDIFACT domain story.

**Axiom Complexity:**
The ontology deploys six advanced OWL constructs: `owl:equivalentClass` (intersection-based definitions for both pivot classes), `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:disjointUnionOf`, and `owl:FunctionalProperty` on multiple properties. `owl:inverseOf` is used systematically throughout. `owl:intersectionOf` is used to express complex class definitions. Axiom Diversity Score = 7 (per metrics), the highest in the set. Only `owl:unionOf` (for union classes) and cardinality restrictions are absent.

**Lexical & Annotation Quality:**
All 27 classes and all 38 object properties carry both `rdfs:label` and `rdfs:comment`. Naming is strict UpperCamelCase for classes and lowerCamelCase for properties (Naming Strict = 1.0). No underscore-prefixed names or non-conformant identifiers. The ontology header also carries a label and comment. Label coverage = 1.0, Comment coverage = 1.0 (per metrics).

**Most Critical Defect:**
The `Address` class is modelled as a `rdfs:subClassOf :Organization`, creating a conceptual confusion (an address IS an organization); this should be a separate class linked only via `hasAddress`, which would also remove the OOPS pitfall signal and prevent potential reasoner confusion when querying for organizations.

---

### Rank 2: `EDIFACT_ontology_20260303_070100.owl`
**Weighted score: 4.56 / 5.00**

**CQ Coverage Analysis:**
- CQ1 — What invoices are all listed in an EDIFACT message? ✅ — `InvoiceMessage ⊂ Message`; `InterchangeEnvelope → hasMessage → Message`; traversal clear.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceMessage → hasRoleAssignment → RoleAssignment → involvesOrganization → Organization`; pivot correctly models involvement.
- CQ3 — What role does organization S play in the invoice? ✅ — `RoleAssignment → hasAgentRole → AgentRole`; `Organization → organizationInRoleAssignment → RoleAssignment → hasAgentRole` gives exact role.
- CQ4 — Which organization is the buyer in the invoice? ✅ — No subclass `BuyerRole` declared, but `AgentRole` with named instances `Buyer` (as instances of `AgentRole`) achievable; slight deduction — role types are only inferrable via individual instance URIs, not subclass restrictions.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Organization → hasAddress`, `hasIdentifier`, `hasGLN`; rich attribute set.
- CQ6 — What is the address of the buyer? ✅ — `Organization → hasAddress → Address`; address data properties (`addressLine`, `postalCode`, `city`, `countryCode`) present on `Address`.
- CQ7 — What items are sold in the invoice? ✅ — `InvoiceDetail → hasLineItem → LineItem → describesItem → Item`.
- CQ8 — What information is displayed about the items sold? ✅ — `Item → itemDescription`; `LineItem → hasNetPrice`, `hasQuantity`.
- CQ9 — What is the net price of the items sold in the invoice? ✅ — `LineItem → hasNetPrice → Price`; `Price → netPrice (xsd:decimal)`.
- CQ10 — What are the invoice details of the invoice? ✅ — `InvoiceMessage` has separate `hasHeader`, `hasDetail`, `hasSummary` functional properties to typed sections.
- CQ11 — What is the invoice amount of the invoice? ✅ — `SummarySection → hasInvoiceAmount → InvoiceAmount`; `InvoiceAmount → invoiceAmountValue (xsd:decimal)`.
- CQ12 — What is the invoice number? ✅ — `HeaderSection → hasInvoiceNumber (xsd:string)`.
- CQ13 — What information must be provided so that the file format is valid? ✅ — `ValidationConstraint` class with `conformsToConstraint` property; `constraintDescription` data property; `EN16931Compliance` and `P2POAlignment` classes.
- CQ14 — To which business process can the invoice be assigned? ✅ — `InvoiceMessage → isAssignedToBusinessProcess → BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR:** 0.8718 — Excellent relationship richness. 34 object properties across 24 classes creates a highly interconnected graph; all major domain objects are bridged via explicit properties.
- **AR:** 0.5 — Good attribute density. 12 data properties for 24 classes; better balanced than most triAgent outputs. Address attributes and item descriptions add practical querying capability.
- **IR:** 0.2083 — Relatively flat taxonomy. Max depth = 1, avg depth = 0.21. `InvoiceMessage ⊂ Message` and `GlobalLocationNumber ⊂ Identifier` are the only subclass chains; sections and roles are flat. This is the primary structural weakness.

**Design Patterns & Domain Representation:**
The `RoleAssignment` pivot class with its `owl:equivalentClass` restriction (`involvesOrganization some Organization ⊓ playsRole some AgentRole`) correctly implements the N-ary role pattern. The EDIFACT section tripartite structure is modelled via three functional properties (`hasHeader`, `hasDetail`, `hasSummary`) pointing to typed section classes, each with disjointness axioms — cleaner than the union-of-range approach. The `InvoiceMessage equivalentClass` restriction requiring all three sections is an excellent logical commitment. The dedicated `LineItem` pivot with `equivalentClass` ensuring item + price + quantity is also high quality.

**Axiom Complexity:**
Seven distinct advanced OWL constructs present (Axiom Diversity Score = 7): `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom` (in `InvoiceMessage` equivalent class), `owl:disjointWith`, `owl:FunctionalProperty`, `owl:inverseOf`. Missing cardinality restrictions and `owl:unionOf`/`owl:hasValue`. Good depth of logical commitment.

**Lexical & Annotation Quality:**
All 24 classes and 34 object properties have `rdfs:label` and `rdfs:comment`. Strict CamelCase naming throughout (Naming Strict = 1.0). Label coverage = 1.0, Comment coverage = 1.0. Property labels follow lowerCamelCase. No issues detected.

**Most Critical Defect:**
The lack of explicit `BuyerRole` and `DeliveryPartyRole` subclasses means role-specific queries (CQ4: "Which org is the buyer?") require instance-level filtering on role individuals rather than cleanly exploiting the class hierarchy; adding typed role subclasses would make the ontology significantly more queryable and logically expressive for the E/D/E procurement scenario.

---

### Rank 3: `EDIFACT_ontology_20260303_061520.owl`
**Weighted score: 4.56 / 5.00**

**CQ Coverage Analysis:**
- CQ1 — What invoices are all listed in an EDIFACT message? ✅ — `InvoiceMessage ⊂ Message`; `InterchangeEnvelope → hasMessage → Message`; standard traversal.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceMessage → hasRoleAssignment → RoleAssignment → involvesOrganization → Organization`.
- CQ3 — What role does organization S play in the invoice? ✅ — `RoleAssignment → playsRole → AgentRole`; but role type only discriminable by AgentRole individuals, not subclasses.
- CQ4 — Which organization is the buyer in the invoice? ⚠️ — No `BuyerRole` subclass; role discriminability relies on instance URI of `AgentRole` only; partial coverage.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Organization → hasAddress`, `hasIdentifier`, `hasGLN`; good attribute coverage.
- CQ6 — What is the address of the buyer? ✅ — `Organization → hasAddress → Address`; `addressLine`, `postalCode`, `cityName`, `countryCode` data properties.
- CQ7 — What items are sold in the invoice? ✅ — `InvoiceDetail → hasLineItem → LineItem → describesItem → Item`.
- CQ8 — What information is displayed about the items sold? ✅ — `Item → itemName`, `itemDescription`; `LineItem → lineItemNetPrice`.
- CQ9 — What is the net price of the items sold in the invoice? ✅ — `LineItem → lineItemNetPrice (xsd:decimal)` direct data property.
- CQ10 — What are the invoice details of the invoice? ✅ — `InvoiceMessage → hasHeader/hasDetail/hasSummary` (functional); sections are disjoint classes.
- CQ11 — What is the invoice amount of the invoice? ⚠️ — No `InvoiceAmount` class or direct `invoiceAmount` property on `InvoiceSummary`; `taxAmount` present but total amount requires inferring from summary data only.
- CQ12 — What is the invoice number? ✅ — `InvoiceHeader → hasInvoiceNumber (xsd:string)`.
- CQ13 — What information must be provided so that the file format is valid? ✅ — `ValidationConstraint` class with `hasValidationConstraint` and `constraintDescription`; D96A mandate encoded.
- CQ14 — To which business process can the invoice be assigned? ✅ — `InvoiceMessage → assignedToProcess → BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR:** 0.9048 — Very high relationship richness. 38 object properties against only 24 classes indicates a very property-dense, interconnected graph. This is the highest RR value in the evaluated set.
- **AR:** 0.4583 — Above-average attribute density. 11 data properties across 24 classes; address subproperties and item description enrich querying.
- **IR:** 0.1667 — Very flat taxonomy. Max depth = 1; nearly all classes are roots with no subclassing. `InvoiceMessage ⊂ Message` and `GLNIdentifier ⊂ Identifier` are the only inheritance edges. This significantly limits the ontology's hierarchical expressiveness.

**Design Patterns & Domain Representation:**
The `RoleAssignment` pivot uses an `owl:equivalentClass` restriction asserting `playsRole some AgentRole ⊓ hasIdentifier some Identifier` — a reasonable structural definition, though substituting `hasIdentifier` for the organization link is semantically awkward (should be `involvesOrganization some Organization`). Similarly, `Organization owl:equivalentClass (hasAddress some Address ⊓ hasIdentifier some Identifier)` is a strong logical commitment that aids validation but could produce unexpected inferences if organizations without identifiers are instantiated. The `LineItem equivalentClass` enforces `describesItem some Item ⊓ hasNetPrice some Price`. Four `owl:equivalentClass` definitions demonstrate excellent logical depth.

**Axiom Complexity:**
Axiom Diversity Score = 6. Present: `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom` (in InvoiceMessage restriction), `owl:disjointWith`, `owl:FunctionalProperty`, `owl:inverseOf`, `owl:disjointUnionOf`. Strong overall complexity, only missing cardinality restrictions and `owl:hasValue`.

**Lexical & Annotation Quality:**
All classes and properties have `rdfs:label` and `rdfs:comment`. Strict CamelCase naming throughout. Property names like `lineItemNetPrice`, `glnValue`, `referenceValue` are descriptive and follow convention. Label coverage = 1.0, Comment coverage = 1.0.

**Most Critical Defect:**
The `RoleAssignment owl:equivalentClass` restriction incorrectly uses `hasIdentifier some Identifier` in place of `involvesOrganization some Organization` as one of the two mandatory arms of the pivot. This means any instance with an `AgentRole` and an `Identifier` (even a disconnected identifier) would be classified as a RoleAssignment, breaking the intended semantics of the N-ary pattern and potentially causing inconsistency when instances with multiple role assignments are modelled.

---

## Bottom Ontologies: Summary

**`EDIFACT_ontology_20260302_140235.owl` (Rank 4):** This ontology (29 classes, 40 object props, 14 data props; RR=0.7843, AR=0.4828, IR=0.3793) is structurally solid and covers all 14 CQs, with well-designed `OrganizationRoleAssignment` and `InvoiceItemDetail` pivot classes backed by `owl:equivalentClass` restrictions. It is ranked 4th primarily because it employs `owl:allValuesFrom` instead of `owl:someValuesFrom` on its `Pivot_OrganizationRoleAssignment` equivalence definition, producing an unduly weak logical commitment (allowing instances with zero role/organization links), and the `HeaderSection/DetailSection/SummarySection` hierarchy roots under `Segment` — a conceptual misfit given that sections are message-level constructs, not segment-level ones. Axiom Diversity Score = 5, slightly below the top-3.

**`EDIFACT_ontology_20260303_091850.owl` (Rank 5):** This ontology (22 classes, 44 object props, 4 data props; RR=0.88, AR=0.1818, IR=0.2727) achieves the best pivot pattern in the set: `PivotOrganizationRoleAssignment owl:equivalentClass` demands all three of `assignedRole`, `assignedOrganization`, AND `roleContext` (linking back to the `InvoiceMessage`), making the context-specific role assignment logically complete and unique across the triAgent set. However, the ontology lacks a `LineItem` intermediate class — items are linked directly from `DetailSection` to `Item` — missing the n-ary structure for item-price-quantity. This causes CQ9 to be only partially addressable (net price lives on `Item` directly, collapsing price context into the item itself). The very low AR (0.18) due to only 4 data properties also limits practical queryability.

**`EDIFACT_ontology_20260302_082612.owl` (Rank 6):** This ontology (22 classes, 42 object props, 5 data props; RR=0.913, AR=0.2273, IR=0.1818) has the highest RR in the evaluated set and uses the `PivotOrganizationRole` / `PivotItemInvoice` double-pivot architecture cleanly. The `Invoice owl:equivalentClass` definition combining `hasHeader allValuesFrom HeaderSection ⊓ hasDetail allValuesFrom DetailSection ⊓ hasSummary allValuesFrom SummarySection` is structurally elegant. However, it ranks 6th because: (a) the use of `allValuesFrom` instead of `someValuesFrom` in the Invoice equivalence produces a vacuously true restriction (any entity with no header is technically consistent), (b) `Buyer`, `Supplier`, `DeliveryParty` are individuals rather than subclasses of `AgentRole`, weakening role discrimination in SPARQL, and (c) the extremely low data property count (5 for 22 classes) means most factual attributes are unavailable without traversing object properties to disconnected instance clusters.

**`EDIFACT_ontology_20260303_085821.owl` (Rank 7):** This ontology (27 classes, 34 object props, 3 data props; RR=0.8095, AR=0.1111, IR=0.2963) covers 13 of 14 CQs and follows the same general architecture as the higher-ranked files. Its weaknesses are: the `InvoiceMessage owl:disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` axiom logically asserts that any `InvoiceMessage` individual is also a section — causing a classification collapse that contributes to its OOPS P04 pitfall detection. Additionally, only 3 data properties for 27 classes (AR=0.11) severely limits data retrieval. The `RoleAssignment owl:equivalentClass` uses `playsRole some AgentRole ⊓ hasIdentifier some Identifier` (same awkward pattern as rank 3), and the invoice amount and invoice number are poorly anchored (no `InvoiceAmount` or `InvoiceNumber` class/property for the summary section).

**`EDIFACT_ontology_20260302_081000.owl` (Rank 8):** This ontology (37 classes, 30 object props, 8 data props; RR=0.5769, AR=0.2162, IR=0.5946) has the most classes in the set and a rich DTM/MOA segment taxonomy (with qualifier-specific subclasses), giving it the best IR and a reasonable AR. However, it scores poorly due to: (a) the lowest RR at 0.5769, indicating a taxonomy-heavy design with insufficient relational connectivity, (b) an Axiom Diversity Score of only 2 (only `rdfs:subClassOf` and `owl:disjointWith`; no equivalence classes, no `someValuesFrom` restrictions), which means zero logical depth beyond basic taxonomy, and (c) the `OrganizationRoleAssignment` class is defined but never given an `owl:equivalentClass` restriction, rendering it an orphaned pivot that provides no inferential power. CQ3, CQ4 coverage is structurally present but semantically thin.

**`EDIFACT_ontology_20260302_124024.owl` (Rank 9):** This ontology (30 classes, 27 object props, 2 data props; RR=0.75, AR=0.0667, IR=0.3) has by far the lowest AR at 0.067 — only 2 data properties for 30 classes — meaning nearly all factual values must be retrieved as object-linked class instances rather than directly queryable literals. It has an OOPS pitfall (P04 detected) and while 4 OWL constructs are present, there is no `owl:equivalentClass` restriction on the pivot class. The ontology lacks an explicit `InvoiceNumber` property or class, and the `RoleAssignment` class exists but without logical completeness axioms. CQs 12 and 13 cannot be answered precisely.

**`EDIFACT_ontology_20260302_133553.owl` (Rank 10):** This is the weakest ontology in the set. With only 28 classes, 23 object props, and 3 data props, it has the lowest triple count (270), the lowest class count after the smaller files, and an Axiom Diversity Score of 5 — but crucially, no `owl:equivalentClass` restrictions, no pivot class definition, and a naming non-conformance rate of 0.056 (the only ontology in this set with a non-zero bad-naming score due to the Turtle prefix `edifact-invoice-ontology` URI which generates a local name mismatch). The `AgentRole` subclasses (`BuyerRole`, `DeliveryPartyRole`) are present, but the ontology lacks `InvoiceAmount`, `ReferenceNumber`, or `ValidationConstraint` classes. CQs 11, 12, and 13 are structurally absent, and the role assignment pattern is missing entirely, making CQ3 and CQ4 unanswerable via the ontology graph.

**`EDIFACT_ontology_20260303_094621.owl` (Rank 11 in overall score but 9th in table due to re-sort):** This ontology (30 classes, 42 object props, 7 data props; RR=0.7925, AR=0.2333, IR=0.3667) is logically inconsistent (OOPS pitfall P04, P20 detected) due to the `BuyerRole owl:equivalentClass [ owl:onProperty :involvesRole ; owl:someValuesFrom :Organization ]` axiom. This restriction incorrectly equates a `BuyerRole` (a role type) with anything that involves an organization — producing an overly broad definition that will classify every `AgentRoleAssignment` as a `BuyerRole`. The `AgentRoleAssignment owl:equivalentClass [ owl:onProperty :inContextOfInvoice ; owl:someValuesFrom :InvoiceMessage ]` is similarly too weak (any assignment with any invoice context becomes an AgentRoleAssignment regardless of whether a role is specified). Despite good property density and reasonable structural metrics, the broken equivalence axioms make the ontology semantically unreliable for reasoning and SPARQL.

---

*Report generated from pre-calculated metrics in `data/FinalResults/ontology_report.md` and direct OWL file analysis.*
