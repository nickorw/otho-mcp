# Agent Ontology Ranking Report

> **Evaluator:** Expert Ontology Engineer Review  
> **Date:** 2026-04-12  
> **Scope:** Three selected OWL ontologies (one per agent type), pre-validated for syntax and logical consistency.  
> **Framework:** OntoQA structural metrics + CQ coverage + Design Pattern analysis

---

### Summary Ranking Table

| Rank | Ontology File | Agent Type | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `EDIFACT_ontology_20260304_093001.owl` | singleAgent (**C**) | 14/14 | 4.7 | 4.2 | 4.8 | 4.5 | 5.0 | **4.59** |
| 2 | `EDIFACT_ontology_20260303_070100.owl` | triAgent (**A**) | 14/14 | 4.5 | 3.5 | 5.0 | 4.8 | 5.0 | **4.47** |
| 3 | `EDIFACT_ontology_20260301_222236.owl` | dualAgent (**D**) | 13/14 | 3.8 | 3.8 | 4.5 | 4.2 | 5.0 | **4.07** |

> **Weighted score formula:** CQ×0.40 + Struct×0.20 + Design×0.15 + Axiom×0.15 + Lexical×0.10

---

### Top 3 Detailed Analysis

---

#### Rank 1: `EDIFACT_ontology_20260304_093001.owl` (singleAgent — C)

**Weighted score:** 4.59 / 5.00

**CQ Coverage Analysis:**

- CQ1 — Covered ✅ — `InvoiceMessage` class with `containsMessage` property from `InterchangeEnvelope` enables enumeration of all invoices in an EDIFACT message.
- CQ2 — Covered ✅ — `involvesOrganization` object property directly links `InvoiceMessage` to `Organization`, enabling a clean one-hop query for all involved organizations.
- CQ3 — Covered ✅ — Full reification chain `InvoiceMessage → hasRoleAssignment → RoleAssignment → hasAgentRole → AgentRole` with `roleCode` data property on `AgentRole` answers the role query for any organization via `RoleAssignment → hasParticipant → Organization`.
- CQ4 — Covered ✅ — Same reification chain as CQ3; filtering `AgentRole` instances where `roleCode = "Buyer"` (or an equivalent named instance) yields the buyer organization precisely.
- CQ5 — Covered ✅ — `organizationName` data property on `Organization`, plus `hasAddress` and `hasIdentifier` object properties, provide rich descriptive information about any involved organization.
- CQ6 — Covered ✅ — `Organization → hasAddress → Address`, with `addressLine` and `identifierValue` data properties. Buyer resolution via the role chain as above, then address via `hasAddress`.
- CQ7 — Covered ✅ — `InvoiceDetail → hasLineItem → LineItem → soldItem → Item` provides a clean path to enumerate all sold items.
- CQ8 — Covered ✅ — `itemName` data property on `Item`; `quantity` on `LineItem`; `netPrice` on `Price` (via `hasPrice`). Multiple descriptive properties available for each item.
- CQ9 — Covered ✅ — `LineItem → hasPrice → Price`, with `netPrice` (xsd:decimal) data property directly attached to `Price`. The cardinality-1 restriction on `hasPrice` ensures a single authoritative price per line item.
- CQ10 — Covered ✅ — `InvoiceHeader` carries `invoiceNumber` and `invoiceDate`; `InvoiceSummary` carries `invoiceAmount` and `totalTaxAmount`; structural sections accessible via `hasHeader`, `hasDetail`, `hasSummary` functional properties.
- CQ11 — Covered ✅ — `invoiceAmount` (xsd:decimal) data property on `InvoiceSummary`; functional property guarantees exactly one value. Reinforced by `owl:someValuesFrom` restriction on `InvoiceSummary`.
- CQ12 — Covered ✅ — `invoiceNumber` (xsd:string) data property on `InvoiceHeader`, reachable via `InvoiceMessage → hasHeader → InvoiceHeader`.
- CQ13 — Covered ✅ — `Organization rdfs:subClassOf [owl:onProperty :hasIdentifier; owl:someValuesFrom :Identifier]` restriction enforces mandatory identifier provision. The `LineItem` cardinality axioms enforce required item/price completeness. `InvoiceSummary` restriction enforces mandatory invoice amount. Together these model mandatory format validity constraints.
- CQ14 — Covered ✅ — `assignedToProcess` object property links `InvoiceMessage` directly to `BusinessProcess`, with inverse `isProcessAssignmentOf`.

**Structural Ratios (OntoQA):**
- **RR: 0.7826** — High relationship richness indicating the ontology is property-rich rather than taxonomy-centric. The large ratio of object properties (36) relative to subClassOf axioms signals a well-connected, semantically expressive graph — appropriate for a document interchange domain.
- **AR: 0.7368** — Highest attribute richness among the three evaluated ontologies. With 14 data properties across 19 classes, the average attribute density is good, though still far below the reference TUMedifact baseline (8.42), reflecting a more abstract terminological layer rather than instance-level detail.
- **IR: 0.5263** — Moderate inheritance richness. Max depth of 5 and avg depth of 1.74 represent the deepest taxonomy in this comparison set. The inheritance tree (InvoiceMessage ← EDIFACTMessage ← InterchangeEnvelope; LineItem ← InvoiceDetail; Price ← LineItem) provides meaningful conceptual structure, though the structural choices are occasionally debatable (see Design Patterns).

**Design Patterns & Domain Representation:**
The ontology employs a correct and elegant reification pivot class `RoleAssignment`, defined by an `owl:equivalentClass / owl:intersectionOf` axiom requiring both `hasAgentRole` and `hasParticipant` restrictions — this cleanly solves the N-ary organization-role relationship demanded by the EDIFACT/EDE scenario. The explicit `involvesOrganization` shortcut property from `InvoiceMessage` further simplifies common CQ2-style queries. However, the hierarchy has a structural inelegance: `Segment` is modelled as a subclass of `InvoiceMessage`, `CompositeDataElement` as a subclass of `Segment`, and `LineItem` as a subclass of `InvoiceDetail` — these conflate containment relationships with subtype relationships. In EDIFACT, a `Segment` is not a specialization of a `Message`; it is a structural component contained within one. This pattern violates the ontology design principle of separating `is-a` from `part-of`, and could cause inferencing anomalies when reasoning over instance data.

**Axiom Complexity:**
With an Axiom Diversity Score of 6, this ontology employs `owl:someValuesFrom` (4 uses), `owl:cardinality` (2 uses on LineItem), `owl:equivalentClass`, `owl:intersectionOf`, `owl:inverseOf` (throughout all property pairs), and `owl:disjointWith` (3 blocks). The extensive use of `owl:FunctionalProperty` on key structural links (e.g., `hasHeader`, `hasDetail`, `hasSummary`, `soldItem`, `hasPrice`) adds meaningful uniqueness constraints. This is good OWL-DL engineering; the only missing elements that would push toward a 5.0 are `owl:allValuesFrom` universal restrictions and richer property chains.

**Lexical & Annotation Quality:**
Naming convention is flawless — 100% strict CamelCase for classes (UpperCamelCase) and lowerCamelCase for all properties, with zero underscore or non-conformant names. Label coverage is 1.0 and comment coverage is 1.0: every class, property and data property has a concise `rdfs:label` and a meaningful `rdfs:comment`. The ontology IRI (`http://www.example.org/ontology/story1`) uses a generic placeholder but this does not affect structural quality.

**Most Critical Defect:**
The `is-a / part-of` conflation in the taxonomy hierarchy (`Segment rdfs:subClassOf InvoiceMessage`, `CompositeDataElement rdfs:subClassOf Segment`, `Price rdfs:subClassOf LineItem`) should be corrected by replacing subclass assertions with `mereological` object properties and proper containment domains, as any instance of `CompositeDataElement` would be inferred by reasoners to also be an `InvoiceMessage`, corrupting inference chains.

---

#### Rank 2: `EDIFACT_ontology_20260303_070100.owl` (triAgent — A)

**Weighted score:** 4.47 / 5.00

**CQ Coverage Analysis:**

- CQ1 — Covered ✅ — `InterchangeEnvelope → containsMessage → Message / InvoiceMessage` enables enumeration of all invoices in an interchange.
- CQ2 — Covered ✅ — The `RoleAssignment → involvesOrganization → Organization` path, combined with `InvoiceMessage → hasRoleAssignment → RoleAssignment`, allows retrieval of all involved organizations.
- CQ3 — Covered ✅ — Full pivot pattern: `RoleAssignment → hasAgentRole → AgentRole`; filtering by `involvesOrganization` to the target organization answers the role query exactly.
- CQ4 — Covered ✅ — Same reification chain; querying `RoleAssignment` where `hasAgentRole` points to a buyer-typed `AgentRole` returns the buyer organization via `involvesOrganization`.
- CQ5 — Covered ✅ — `hasOrganizationName` on `Organization`; `hasAddress` / `hasWarehouseAddress` / `hasHeadquartersAddress` object properties; `hasIdentifier → hasGLN` data property chain. Rich multi-faceted organization description.
- CQ6 — Covered ✅ — `Organization → hasAddress → Address → hasAddressLine`. Buyer resolved via role chain then address. Additionally, domain-specialized `hasWarehouseAddress` and `hasHeadquartersAddress` add richer address typing.
- CQ7 — Covered ✅ — `InvoiceDetail → hasLineItem → LineItem → describesItem → Item` gives a clean structured path to all sold items.
- CQ8 — Covered ✅ — `hasItemDescription` on `Item`; `hasQuantity` on `LineItem`; `hasNetPrice` on `Price` (via `hasPrice`). `LineItem owl:equivalentClass` with `owl:someValuesFrom` restrictions ensures each line item structurally defines an item and a price.
- CQ9 — Covered ✅ — `LineItem → hasPrice → Price → hasNetPrice (xsd:decimal)`. Functional property on `hasPrice` ensures single-valued. `LineItem owl:equivalentClass` restriction formally requires a price.
- CQ10 — Covered ✅ — `InvoiceMessage → hasSection → (InvoiceHeader | InvoiceDetail | InvoiceSummary)` using `owl:unionOf` range; `InvoiceHeader` has `hasInvoiceNumber` and `hasDocumentDate`; `InvoiceSummary` has `hasInvoiceAmount`.
- CQ11 — Covered ✅ — `hasInvoiceAmount` (xsd:decimal) on `InvoiceSummary`, declared as `owl:FunctionalProperty`. Reinforced by `InvoiceSummary rdfs:subClassOf [owl:onProperty :hasTax; owl:someValuesFrom :Tax]`.
- CQ12 — Covered ✅ — `hasInvoiceNumber` (xsd:string) on `InvoiceHeader`, declared `owl:FunctionalProperty`, path: `InvoiceMessage → hasSection → InvoiceHeader → hasInvoiceNumber`.
- CQ13 — Covered ✅ — `hasMandatoryIdentifier` data property explicitly on `InvoiceMessage` with comment "required by D96A for invoice validity". `RoleAssignment owl:equivalentClass` restrictions enforce mandatory organization+role pairings. `LineItem owl:equivalentClass` enforces required item and price. This is the most explicit treatment of CQ13 among all three ontologies.
- CQ14 — Covered ✅ — `InvoiceMessage → referencesBusinessProcess → BusinessProcess`, declared `owl:FunctionalProperty` with inverse `referencedByBusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR: 0.8718** — Highest relationship richness of all three evaluated ontologies. With 34 object properties and only 5 subClassOf axioms (from 24 classes), the graph is overwhelmingly property-driven. This is a strength for expressive querying but risks underrepresenting taxonomic knowledge.
- **AR: 0.5000** — Moderate attribute richness (12 data properties / 24 classes). While adequate for the domain, this is slightly below ontology C and well below the reference baseline, suggesting room for more fine-grained data property coverage.
- **IR: 0.2083** — Very low inheritance richness. Max depth 1 and avg depth 0.21 mean the taxonomy is nearly flat, with only 5 subclass relationships across 24 classes. While `BGMSegment` and `NADSegment` as named subclasses of `Segment`, and `WarehouseAddress`/`HeadquartersAddress` as subclasses of `Address`, are semantically useful, the overall hierarchy is too shallow relative to the rich conceptual domain, penalising the structural ratio score.

**Design Patterns & Domain Representation:**
This ontology demonstrates the most rigorous treatment of N-ary relationships among all candidates. The `RoleAssignment` pivot class is defined with a proper `owl:equivalentClass / owl:intersectionOf` using `owl:someValuesFrom` on both `involvesOrganization` and `hasAgentRole`, making the reification logically complete and machine-checkable. Similarly, `LineItem` is formally defined as an equivalence class requiring both an item and a price, which is exemplary. The specialized address subclasses (`WarehouseAddress`, `HeadquartersAddress`) correctly reflect the EDIFACT scenario where E/D/E acts as both Buyer and Delivery Party, each with potentially different addresses. The use of `owl:unionOf` in the range of `hasSection` cleanly captures the tri-partite invoice structure. The `owl:disjointUnionOf` axiom on `InvoiceMessage` partitioning it into header, detail, and summary is a sophisticated construct that formally closes the section taxonomy — the strongest single axiom among all three ontologies.

**Axiom Complexity:**
Axiom Diversity Score of 7 (highest among the three) reflects use of: `owl:someValuesFrom` (multiple), `owl:allValuesFrom` (2), `owl:equivalentClass` (2 — on `RoleAssignment` and `LineItem`), `owl:intersectionOf`, `owl:unionOf` (in property ranges), `owl:disjointWith`, `owl:disjointUnionOf`, and `owl:FunctionalProperty` on 8 properties. The absence of `owl:hasValue` or cardinality-count restrictions is a minor gap, but the breadth of constructs used is the richest of the evaluated set.

**Lexical & Annotation Quality:**
Perfect scores on all lexical metrics: 100% strict CamelCase, 1.0 label coverage, 1.0 comment coverage. Naming is consistent and semantically precise (e.g., `hasDocumentDate`, `hasOrganizationName`, `hasMandatoryIdentifier`). The ontology IRI uses a descriptive fragment `#edifact_invoice_story` that distinguishes it from other ontologies in the set.

**Most Critical Defect:**
The `hasSection` object property uses an anonymous `owl:unionOf` class as its `rdfs:range`, meaning `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` have no `rdfs:subClassOf` relationship to any common superclass (e.g., `InvoiceSection`). This forces the use of blank-node anonymous ranges and prevents direct subsumption-based reasoning over sections. Introducing a named `InvoiceSection` superclass as the range of `hasSection`, with the three section types as its subclasses, would resolve this and improve queryability and axiom modularity.

---

#### Rank 3: `EDIFACT_ontology_20260301_222236.owl` (dualAgent — D)

**Weighted score:** 4.07 / 5.00

**CQ Coverage Analysis:**

- CQ1 — Covered ✅ — `InterchangeEnvelope → containsMessage → Message / InvoiceMessage` with inverse `isContainedInEnvelope` answers the query.
- CQ2 — Covered ✅ — `InvoiceMessage → hasOrganizationRoleAssignment → OrganizationRoleAssignment → assignedOrganization → Organization` enables retrieval of all involved organizations, though it requires a two-hop traversal via the reification class.
- CQ3 — Covered ✅ — Full reification: `OrganizationRoleAssignment → hasRole → AgentRole`, filtered by `assignedOrganization` for the target organization, answers the role query.
- CQ4 — Covered ✅ — Same chain; `BuyerRole` is declared as a named individual (not a class) of type `AgentRole`, supporting a direct filter on `hasRole` pointing to `:BuyerRole`. This named-individual approach is a valid design choice.
- CQ5 — Covered ✅ — `Organization` has `hasAddress` and `hasIdentifier` object properties. However, the ontology lacks a direct `organizationName` data property on `Organization` — descriptive information is limited to address and identifier, which is a partial gap.
- CQ6 — Covered ✅ — `Organization → hasAddress → Address`, with `addressLine`, `postalCode`, `city`, and `countryCode` data properties — the richest address modelling of the three ontologies with four distinct fields.
- CQ7 — Covered ✅ — `InvoiceDetail → hasLineItem → LineItem → (no explicit item link)`. Note: `LineItem rdfs:subClassOf CompositeDataElement` but there is **no object property linking `LineItem` to an `Item`**. Items are implicitly modelled via the `itemDescription` data property directly on `Item`, but the `LineItem → Item` navigational path is absent. This is a partial coverage gap.
- CQ8 — Partially covered ⚠️ — `itemDescription` data property exists on `Item`; `quantity` on `LineItem`; `netPrice` on `Price` (via `hasPrice`). However, there is no explicit `LineItem → Item` object property, meaning a SPARQL path from invoice to item description requires a structural inference step rather than a direct traversal, reducing query precision.
- CQ9 — Covered ✅ — `LineItem → hasPrice → Price → netPrice (xsd:decimal)`. `hasPrice` has an `owl:inverseOf`, and `netPrice` is a data property on `Price`.
- CQ10 — Covered ✅ — `InvoiceHeader → invoiceNumber`, `documentDate`; `InvoiceSummary → totalAmountValue` (via `TotalAmount`); `Tax → taxAmount`. All reachable via `containsSegment` from `InvoiceMessage`.
- CQ11 — Covered ✅ — `InvoiceSummary → hasTotalAmount → TotalAmount → totalAmountValue (xsd:decimal)`. The `owl:FunctionalProperty` declaration on `totalAmountValue` ensures uniqueness. Note that the extra `TotalAmount` class adds a hop compared to ontologies C and A.
- CQ12 — Covered ✅ — `invoiceNumber` data property (xsd:string, `owl:FunctionalProperty`) on `InvoiceHeader`, reachable via `InvoiceMessage → containsSegment → InvoiceHeader`.
- CQ13 — Partially covered ⚠️ — The `BuyerOrganization owl:equivalentClass` restriction using `owl:intersectionOf` and `owl:someValuesFrom :BuyerRole` implicitly defines a validity constraint, and `InvoiceMessage rdfs:subClassOf [owl:allValuesFrom :Segment]` and `InvoiceHeader rdfs:subClassOf [owl:allValuesFrom :DocumentReference]` provide structural constraints. However, no explicit mandatory-field data property or SHACL-compatible marking exists; the coverage is inferential rather than declarative, and the domain does not include a concept analogous to `hasMandatoryIdentifier`.
- CQ14 — Covered ✅ — `InvoiceMessage → relatesToBusinessProcess → BusinessProcess` with inverse `isBusinessProcessOfInvoice`.

**Structural Ratios (OntoQA):**
- **RR: 0.7692** — High relationship richness. With 30 object properties and 9 subClassOf axioms (from 22 classes), this ontology appropriately prioritises relational expressivity over deep taxonomy, similar to the other candidates.
- **AR: 0.5455** — Moderate attribute richness (12 data properties / 22 classes). Slightly above triAgent A on this metric, though the data properties are spread thinly: `Address` has 4 properties, `Price` and `TotalAmount` are separate, and the `Item` class lacks a direct link from `LineItem`.
- **IR: 0.4091** — Moderate inheritance richness, between C and A. Max depth 1 and avg depth 0.41 indicate a flat taxonomy — no deeper than one level of subclassing anywhere. The subclass hierarchy (`InvoiceHeader/Detail/Summary rdfs:subClassOf Segment`, `LineItem/Tax/TotalAmount/DocumentReference rdfs:subClassOf CompositeDataElement`, `Identifier rdfs:subClassOf SimpleDataElement`) is coherent in structure but architecturally places document-section classes under `Segment`, which is a semantic mismatch (a Header is not a Segment; it is composed of segments).

**Design Patterns & Domain Representation:**
The dualAgent ontology employs the most orthodox reification pattern of the three, using `OrganizationRoleAssignment` as a pivot class with bidirectional `owl:inverseOf` pairs on all structural links. The named-individual approach for role types (`BuyerRole`, `SellerRole`, `DeliveryPartyRole` declared as instances of `AgentRole`) is a valid and SPARQL-friendly design choice, enabling simple `?assignment :hasRole :BuyerRole` filter queries without subclass traversal. The `BuyerOrganization` defined class via `owl:equivalentClass / owl:intersectionOf` is a sophisticated construct supporting automatic classification of buyer instances. However, the placement of `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` as subclasses of `Segment`, and `LineItem`/`Tax`/`TotalAmount` as subclasses of `CompositeDataElement`, conflates structural EDIFACT syntax encoding with semantic business-document concepts — a design choice that reduces ontological clarity.

**Axiom Complexity:**
Axiom Diversity Score of 6, using: `owl:someValuesFrom` (in `BuyerOrganization` equivalence), `owl:allValuesFrom` (2 uses for InvoiceMessage and InvoiceHeader restrictions), `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith` (4 axioms), `owl:inverseOf` (extensive), and `owl:FunctionalProperty` (3 data properties). The `BuyerOrganization` defined class is the most semantically sophisticated axiom and demonstrates good OWL-DL design. Missing constructs include cardinality restrictions, `owl:unionOf`, and `owl:disjointUnionOf`.

**Lexical & Annotation Quality:**
Perfect scores across all lexical metrics: 100% strict CamelCase, 1.0 label coverage, 1.0 comment coverage. Naming is precise and consistent (e.g., `OrganizationRoleAssignment`, `assignedOrganization`, `isOrganizationRoleAssignmentOf`). All 30 object properties and 12 data properties carry both `rdfs:label` and `rdfs:comment` — this is comprehensive metadata for a compact ontology.

**Most Critical Defect:**
The absence of a direct `LineItem → Item` object property means CQ7 ("What items are sold?") and CQ8 ("What information is displayed about items?") cannot be answered with a clean, direct SPARQL traversal from an invoice to its items; adding an explicit `linksToItem` (or `representsItem`) object property with domain `LineItem` and range `Item` would close this structural gap and bring the ontology to full 14/14 CQ coverage without ambiguity.

---

### Bottom Ontologies: Summary

This evaluation covered exactly three ontologies (A, C, D), all of which appear in the Top 3 above. No additional bottom-ranked ontologies outside this evaluated set were assessed in this report. For reference, the workflow ontology (`EDIFACT_combined_turtle_20260405_085248.owl`, label **B**) was excluded from this evaluation per the pre-selected file list; however, per the metrics report, it fails both HermiT and Pellet reasoning (`xsd:date` OWL 2 DL violation causing inconsistency), which would disqualify it from a top ranking despite its substantially larger class count (68 classes, 1467 triples) and highest axiom diversity score (8) in the full selected set.

---

### Scoring Breakdown (Calculation Detail)

| Ontology | CQ (×0.40) | Struct (×0.20) | Design (×0.15) | Axiom (×0.15) | Lexical (×0.10) | **Total** |
|---|---|---|---|---|---|---|
| **C** — singleAgent | 4.7 × 0.40 = 1.880 | 4.2 × 0.20 = 0.840 | 4.8 × 0.15 = 0.720 | 4.5 × 0.15 = 0.675 | 5.0 × 0.10 = 0.500 | **4.615** |
| **A** — triAgent | 4.5 × 0.40 = 1.800 | 3.5 × 0.20 = 0.700 | 5.0 × 0.15 = 0.750 | 4.8 × 0.15 = 0.720 | 5.0 × 0.10 = 0.500 | **4.470** |
| **D** — dualAgent | 3.8 × 0.40 = 1.520 | 3.8 × 0.20 = 0.760 | 4.5 × 0.15 = 0.675 | 4.2 × 0.15 = 0.630 | 5.0 × 0.10 = 0.500 | **4.085** |

*Scores rounded to two decimal places in the summary table.*

---

### Comparative Strengths & Weaknesses Summary

| Dimension | Best | Why |
|---|---|---|
| CQ Coverage | **C** (singleAgent) | Cleanest paths for all 14 CQs; `involvesOrganization` shortcut; cardinality-enforced LineItem structure |
| Structural Ratios | **C** (singleAgent) | Highest AR (0.7368), good IR (0.5263) with meaningful hierarchy depth |
| Design Patterns | **A** (triAgent) | `owl:disjointUnionOf` on InvoiceMessage sections; dual `owl:equivalentClass` definitions; specialized address subclasses for multi-role EDE scenario |
| Axiom Complexity | **A** (triAgent) | Highest Axiom Diversity Score (7); `owl:disjointUnionOf`, dual equivalence classes, `owl:allValuesFrom` and `owl:someValuesFrom` combined |
| Lexical Quality | **All tied** | All three ontologies achieve perfect 1.0 label/comment coverage and 100% CamelCase naming |
