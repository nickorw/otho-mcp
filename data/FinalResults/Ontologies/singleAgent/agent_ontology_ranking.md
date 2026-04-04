# UN/EDIFACT Invoice Ontology Evaluation — Single-Agent Run


**Date:** 2026-03-08
**Corpus:** 17 OWL ontology files from `data/FinalResults/Ontologies/singleAgent/`
**Metrics source:** `data/FinalResults/ontology_report.md` (Section 3.2)

---

## Evaluation Framework

| Dimension | Weight | Description |
|-----------|--------|-------------|
| CQ Coverage | 40% | Fraction of 14 domain CQs answerable (0–14 scale mapped to 0–5) |
| Structural Ratios | 20% | RR, AR, IR balance against OntoQA targets |
| Design Patterns | 15% | N-ary reification, disjointness, equivalence axioms, inverse pairs |
| Axiom Complexity | 15% | Axiom Diversity Score (count of distinct OWL construct types) |
| Lexical & Annotation Quality | 10% | Label coverage, comment coverage, naming strictness |

### 14 Competency Questions (CQs)

| ID | Question |
|----|----------|
| CQ1 | Which invoices are present in a given interchange? |
| CQ2 | Which organizations are involved in an invoice, and in what roles? |
| CQ3 | Who is the buyer in a given invoice? |
| CQ4 | What is the delivery address for a given buyer role? |
| CQ5 | Which items appear in a given invoice? |
| CQ6 | What is the net price of each line item? |
| CQ7 | What are the invoice date and reference number? |
| CQ8 | What is the total invoice amount and tax amount? |
| CQ9 | What is the invoice number? |
| CQ10 | Is the message a valid EDIFACT invoice format? |
| CQ11 | To which business process is the invoice assigned? |
| CQ12 | What identifier (e.g., GLN) does an organization have? |
| CQ13 | Can the same organization act as buyer and delivery party simultaneously? |
| CQ14 | What are the header, detail, and summary sections of an invoice? |

---

## Summary Ranking Table

| Rank | File (timestamp) | CQ Coverage (×0.40) | Structural (×0.20) | Design Patterns (×0.15) | Axiom Complexity (×0.15) | Lexical (×0.10) | **Total** |
|------|-----------------|--------------------|--------------------|------------------------|--------------------------|-----------------|-----------|
| 1 | 093001 | 5.00 | 4.20 | 5.00 | 4.50 | 4.00 | **4.73** |
| 2 | 094903 | 5.00 | 4.40 | 4.50 | 3.75 | 4.00 | **4.53** |
| 3 | 062606 | 4.64 | 4.20 | 4.50 | 3.75 | 4.50 | **4.38** |
| 4 | 071618 | 4.64 | 4.00 | 4.50 | 5.00 | 3.50 | **4.26** |
| 5 | 085410 | 4.64 | 3.60 | 4.50 | 4.50 | 4.00 | **4.11** |
| 6 | 070119 | 4.29 | 4.20 | 4.00 | 3.75 | 4.00 | **4.05** |
| 7 | 063345 | 4.29 | 4.00 | 4.00 | 3.75 | 3.50 | **3.97** |
| 8 | 090528 | 4.29 | 3.80 | 3.50 | 2.25 | 4.00 | **3.80** |
| 9 | 075831 | 3.93 | 4.00 | 3.50 | 4.50 | 3.50 | **3.85** |
| 10 | 092221 | 3.93 | 4.40 | 3.50 | 3.00 | 3.50 | **3.77** |
| 11 | 072404 | 3.93 | 3.60 | 3.50 | 2.25 | 3.50 | **3.55** |
| 12 | 071919 | 3.57 | 3.80 | 3.50 | 3.75 | 3.50 | **3.60** |
| 13 | 112519 | 3.57 | 3.80 | 3.00 | 2.25 | 4.00 | **3.39** |
| 14 | 073706 | 3.21 | 2.80 | 3.50 | 5.00 | 3.50 | **3.36** |
| 15 | 072939 | 3.21 | 3.60 | 2.50 | 1.50 | 3.50 | **3.07** |
| 16 | 075320 | 2.86 | 2.40 | 2.50 | 2.25 | 3.00 | **2.72** |
| 17 | 111526 | 2.86 | 2.60 | 2.50 | 2.25 | 3.00 | **2.67** |

Raw scores are on a 0–5 scale per dimension before weighting.

---

## Top-3 Detailed Analysis

---

### Rank 1 — `EDIFACT_ontology_20260304_093001.owl` — Score: 4.73

#### CQ Coverage (Score: 5.00 / 5.00 — 14/14 CQs answerable)

| CQ | Answerable | Key Construct |
|----|-----------|---------------|
| CQ1 | Yes | `InterchangeEnvelope :containsMessage :InvoiceMessage` |
| CQ2 | Yes | `OrganizationRoleAssignment` pivot → `hasAgentRole`, `involvesOrganization` |
| CQ3 | Yes | `AgentRole owl:disjointUnionOf (:BuyerRole :DeliveryPartyRole)`; `RoleAssignment owl:equivalentClass [intersectionOf([someValuesFrom :BuyerRole][someValuesFrom :Organization])]` |
| CQ4 | Yes | `OrganizationRoleAssignment :hasRoleAddress :Address` with postal code, city, country |
| CQ5 | Yes | `InvoiceLineAssociation` links `InvoiceMessage` to `LineItem`; `LineItem :refersToItem :Item` |
| CQ6 | Yes | `LineItem :hasPrice :Price`; `Price :netPrice xsd:decimal` |
| CQ7 | Yes | `HeaderSection :hasDate xsd:dateTime`; `HeaderSection :hasReferenceNumber xsd:string` |
| CQ8 | Yes | `SummarySection :hasTotalAmount xsd:decimal`; `SummarySection :hasTaxAmount xsd:decimal` |
| CQ9 | Yes | `HeaderSection :hasInvoiceNumber xsd:string` |
| CQ10 | Yes | `InvoiceMessage rdfs:subClassOf :EDIFACTMessage`; structural hierarchy validates format |
| CQ11 | Yes | `InvoiceMessage :isPartOfProcess :BusinessProcess` |
| CQ12 | Yes | `Organization :hasIdentifier :Identifier` with `identifierValue`; `GlobalLocationNumber subClassOf Identifier` |
| CQ13 | Yes | `AgentRole owl:disjointUnionOf (:BuyerRole :DeliveryPartyRole)` explicitly models both roles; `OrganizationRoleAssignment` pivot allows same `Organization` to participate via separate assignments |
| CQ14 | Yes | `HeaderSection`, `DetailSection`, `SummarySection` as disjoint subclasses of `Segment` |

#### Structural Ratio Analysis (Score: 4.20 / 5.00)

| Metric | Value | Target | Assessment |
|--------|-------|--------|------------|
| RR (Relationship Richness) | 0.7826 | ≥0.70 | Strong — 36 object properties across 19 classes |
| AR (Attribute Richness) | 0.7368 | ≥0.60 | Good — 14 data properties across 19 classes |
| IR (Inheritance Richness) | 0.5263 | 0.30–0.60 | Excellent — deepest hierarchy (max depth=5) in group |
| Axiom Diversity Score | 6 | ≥5 | Adequate — uses someValuesFrom, allValuesFrom, equivalentClass, intersectionOf, disjointUnionOf, hasValue |

IR=0.5263 is the highest in the entire group, indicating well-calibrated taxonomy depth without over-flattening. The max depth of 5 (`InterchangeEnvelope > EDIFACTMessage > InvoiceMessage > Section > SubSection`) supports CQ14 naturally.

#### Design Patterns (Score: 5.00 / 5.00)

- **N-ary Role Reification**: `OrganizationRoleAssignment` pivot correctly attaches organization, role, address, and identifier in a single reified node; `owl:cardinality "1"` on both `hasAgentRole` and `hasRoleAddress` enforces data integrity.
- **Secondary Pivot**: `InvoiceLineAssociation` cleanly separates line-item associations from organizational context.
- **Disjoint Union**: `AgentRole owl:disjointUnionOf (:BuyerRole :DeliveryPartyRole)` closes the role taxonomy — the only ontology in the group to close `AgentRole` rather than leaving it open.
- **Equivalence Axiom**: `RoleAssignment owl:equivalentClass [intersectionOf([someValuesFrom :AgentRole][someValuesFrom :Organization])]` provides a necessary-and-sufficient definition.
- **Full Inverse Coverage**: All 36 object properties have declared `owl:inverseOf` counterparts.

#### Axiom Complexity (Score: 4.50 / 5.00 — Diversity=6)

OWL constructs present: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointUnionOf`, `owl:hasValue`. Missing: `owl:unionOf` (standalone), `owl:hasKey`, `owl:oneOf`. At 6 types, this ontology uses a broad but purposeful set of constructs without decorative complexity.

#### Lexical & Annotation Quality (Score: 4.00 / 5.00)

- All classes and properties have `rdfs:label` and `rdfs:comment`.
- Naming convention: camelCase for properties, PascalCase for classes — fully consistent.
- Ontology-level `rdfs:label` and `rdfs:comment` present.
- Minor gap: individual `AgentRole` instances (`BuyerRole`, `DeliveryPartyRole`) lack `rdfs:comment`.

#### Most Critical Defect

The ontology's `InvoiceLineAssociation` is a valid secondary pivot but its relationship to the structural `Segment` hierarchy is left implicit — `InvoiceLineAssociation` instances are not constrained to be `someValuesFrom :DetailSection`, creating a minor loose coupling between the structural and semantic layers.

---

### Rank 2 — `EDIFACT_ontology_20260304_094903.owl` — Score: 4.53

#### CQ Coverage (Score: 5.00 / 5.00 — 14/14 CQs answerable)

| CQ | Answerable | Key Construct |
|----|-----------|---------------|
| CQ1 | Yes | `InterchangeEnvelope :containsMessage :InvoiceMessage` |
| CQ2 | Yes | Double pivot: `Involvement` (message ↔ org context) + `RoleAssignment` (org ↔ role context) |
| CQ3 | Yes | `RoleAssignment :hasRole :AgentRole`; query for `AgentRole = Buyer` |
| CQ4 | Yes | `RoleAssignment :hasAddress :Address`; `Address :postalCode`, `:city`, `:countryCode` |
| CQ5 | Yes | `InvoiceDetail :hasLineItem :LineItem`; `LineItem :describesItem :Item` |
| CQ6 | Yes | `LineItem :hasPrice :Price`; `Price :netPrice xsd:decimal` |
| CQ7 | Yes | `InvoiceHeader :invoiceDate xsd:dateTime`; derived from header segment |
| CQ8 | Yes | `InvoiceSummary :totalInvoiceAmount`; `InvoiceSummary :totalTaxAmount` |
| CQ9 | Yes | `InvoiceHeader :invoiceNumber xsd:string` (FunctionalProperty) |
| CQ10 | Yes | `InvoiceMessage owl:equivalentClass [intersectionOf(:Message, [someValuesFrom :Involvement], [someValuesFrom :Segment])]` — closed definition enables format validation |
| CQ11 | Yes | `InvoiceMessage :isPartOfProcess :BusinessProcess` |
| CQ12 | Yes | `Organization :hasIdentifier :Identifier`; `Identifier :identifierValue`, `:identifierType` |
| CQ13 | Yes | Open `AgentRole` class; same `Organization` can participate in two `RoleAssignment` nodes with distinct roles |
| CQ14 | Yes | `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary` as disjoint subclasses of `Segment`; `Segment owl:disjointUnionOf` |

#### Structural Ratio Analysis (Score: 4.40 / 5.00)

| Metric | Value | Target | Assessment |
|--------|-------|--------|------------|
| RR | 0.8235 | ≥0.70 | Excellent |
| AR | 0.7895 | ≥0.60 | Highest in group — rich data property coverage |
| IR | 0.3158 | 0.30–0.60 | Acceptable — moderate hierarchy depth |
| Axiom Diversity | 5 | ≥5 | Meets threshold |

AR=0.7895 is the highest AR across all 17 ontologies, reflecting thorough coverage of data properties (`invoiceNumber`, `invoiceDate`, `netPrice`, `quantity`, `totalTaxAmount`, `totalInvoiceAmount`, `organizationName`, `addressLine`, `postalCode`, `city`, `countryCode`, `identifierValue`, `identifierType`, `itemName`, `itemDescription`).

#### Design Patterns (Score: 4.50 / 5.00)

- **Double Pivot**: The `Involvement` + `RoleAssignment` two-level reification is more semantically precise than a single pivot — `Involvement` captures "this organization participates in this message" while `RoleAssignment` captures "with this specific role and address."
- **Equivalence with Intersection**: `InvoiceMessage owl:equivalentClass [intersectionOf]` and `LineItem owl:equivalentClass [intersectionOf]` provide bidirectional classification.
- **Disjoint Union**: `Segment owl:disjointUnionOf (:InvoiceHeader :InvoiceDetail :InvoiceSummary)` closes the structural partition.
- **Functional Properties**: `invoiceNumber` and `invoiceDate` declared `owl:FunctionalProperty`.
- **Gap**: `AgentRole` taxonomy is open — no `owl:disjointUnionOf` or named subclasses for buyer/seller/delivery, slightly weakening CQ3/CQ13 precision.

#### Axiom Complexity (Score: 3.75 / 5.00 — Diversity=5)

OWL constructs: `owl:someValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointUnionOf`, `owl:FunctionalProperty`. Missing: `owl:allValuesFrom`, `owl:hasValue`, `owl:disjointWith` (standalone), `owl:unionOf`. Solid but one construct short of the top tier.

#### Lexical & Annotation Quality (Score: 4.00 / 5.00)

- All classes and properties labeled and commented.
- Ontology URI (`<http://www.example.org/ontology/edifact-invoice-story>`) is a proper IRI rather than a blank node — better practice than many peers.
- Minor gap: Individual `AgentRole` instances not declared (open role taxonomy means no labels to miss, but no examples are given either).

#### Most Critical Defect

The double-pivot pattern (`Involvement` + `RoleAssignment`) adds an extra hop for common queries. SPARQL to find "who is the buyer in invoice X" requires traversing: `InvoiceMessage → involvesOrganization → Involvement → hasRoleAssignment → RoleAssignment → hasRole → ?role` — three joins versus two in the single-pivot design of Rank 1. For operational query performance this is a moderate usability penalty.

---

### Rank 3 — `EDIFACT_ontology_20260304_062606.owl` — Score: 4.38

#### CQ Coverage (Score: 4.64 / 5.00 — 13/14 CQs answerable)

| CQ | Answerable | Key Construct |
|----|-----------|---------------|
| CQ1 | Yes | `InterchangeEnvelope :containsMessage :InvoiceMessage`; `containsMessage owl:InverseFunctionalProperty` |
| CQ2 | Yes | `OrganizationRoleContext` pivot; `hasOrganizationContext`, `withAgentRole` |
| CQ3 | Yes | `BuyerContext owl:equivalentClass [owl:allValuesFrom :Buyer]`; `Buyer` is named `AgentRole` individual |
| CQ4 | Yes | `OrganizationRoleContext :hasAddress :Address`; address data properties present |
| CQ5 | Yes | `InvoiceDetailSection :hasLineItem :LineItem`; `LineItem :refersToItem :Item` |
| CQ6 | Yes | `LineItem :hasPrice :Price`; `Price :netPrice xsd:decimal` |
| CQ7 | Yes | `InvoiceHeaderSection :hasInvoiceDate xsd:dateTime`; reference via `hasSegment` chain |
| CQ8 | Yes | `InvoiceSummarySection :hasTotalAmount`, `:hasTaxAmount` |
| CQ9 | Yes | `InvoiceHeaderSection :hasInvoiceNumber xsd:string` |
| CQ10 | Yes | `SHACLConstraint` class with `validatedBy`/`validates` properties; structural hierarchy present |
| CQ11 | Yes | `InvoiceMessage :partOfBusinessProcess :BusinessProcess` |
| CQ12 | Yes | `Organization :hasIdentifier :Identifier`; `GlobalLocationNumber subClassOf Identifier` |
| CQ13 | Partial | `OrganizationRoleContext` allows multiple assignments per organization; `AgentRole` is open but no explicit disjoint modeling of buyer vs delivery roles |
| CQ14 | Yes | `InvoiceHeaderSection`, `InvoiceDetailSection`, `InvoiceSummarySection` as disjoint Segment subclasses |

CQ13 is partially answered: the pivot pattern technically supports the E/D/E scenario but the model does not explicitly close or enumerate roles, so the answer requires inference rather than direct axiom support.

#### Structural Ratio Analysis (Score: 4.20 / 5.00)

| Metric | Value | Target | Assessment |
|--------|-------|--------|------------|
| RR | 0.8235 | ≥0.70 | Excellent |
| AR | 0.6500 | ≥0.60 | Adequate — 13 data properties across 20 classes |
| IR | 0.3000 | 0.30–0.60 | Borderline — at lower bound |
| Axiom Diversity | 5 | ≥5 | Meets threshold |

20 classes is the joint-highest count. IR=0.30 is at the lower acceptable bound; the hierarchy could be deeper for segments.

#### Design Patterns (Score: 4.50 / 5.00)

- **N-ary Role Reification**: `OrganizationRoleContext` pivot is cleanly designed.
- **SHACL Extension**: `SHACLConstraint` class with `validatedBy`/`validates` is a domain-specific extension beyond OWL, acknowledging operational validation needs (unique in the group).
- **Equivalence Axiom**: `BuyerContext owl:equivalentClass [owl:allValuesFrom :Buyer]` — note: `allValuesFrom` on a property produces a vacuously-satisfiable class for instances with no values, which is a subtle logical weakness compared to `someValuesFrom`.
- **InverseFunctionalProperty**: `containsMessage owl:InverseFunctionalProperty` correctly constrains that a message belongs to exactly one interchange.
- **Disjointness**: `owl:disjointWith` declarations between organizational and structural classes.

#### Axiom Complexity (Score: 3.75 / 5.00 — Diversity=5)

OWL constructs: `owl:allValuesFrom`, `owl:equivalentClass`, `owl:FunctionalProperty`, `owl:InverseFunctionalProperty`, `owl:disjointWith`. Missing: `owl:someValuesFrom`, `owl:intersectionOf`, `owl:disjointUnionOf`, `owl:hasValue`. Unusual profile — `allValuesFrom` used where `someValuesFrom` would be more appropriate for existence constraints.

#### Lexical & Annotation Quality (Score: 4.50 / 5.00)

Best lexical score in the group. All classes labeled and commented with precise, domain-appropriate language. Ontology-level metadata complete. Naming is fully consistent (PascalCase classes, camelCase properties). The `SHACLConstraint` naming is clear and self-documenting.

#### Most Critical Defect

`BuyerContext owl:equivalentClass [owl:allValuesFrom :Buyer]` is logically vacuous for instances that have zero `withAgentRole` values — any class instance without a role assignment satisfies the restriction trivially. The correct axiom for "a context that is a buyer context" should use `owl:someValuesFrom`, not `owl:allValuesFrom`. This is a semantic error that would produce false-positive buyer classifications.

---

## Remaining Ontologies (Ranks 4–17)

### Rank 4 — `EDIFACT_ontology_20260304_071618.owl` — Score: 4.26

Uses a single `RoleAssignment` pivot with `owl:hasValue` in a nested `BuyerOrganization owl:equivalentClass` — the only ontology besides Rank 1 to reach Axiom Diversity=7, driven by use of `owl:hasValue`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:equivalentClass`, `owl:disjointUnionOf`, `owl:allValuesFrom`, and `owl:FunctionalProperty`. Key weakness: `hasAddress` is declared on `Organization` directly rather than on the `RoleAssignment` pivot, meaning different addresses for buyer vs. delivery roles cannot be distinguished — a direct failure for the E/D/E scenario (CQ13). IR=0.4706 is solid but RR=0.7647 and AR=0.6471 are mid-range. Structural score penalized for the address placement error.

### Rank 5 — `EDIFACT_ontology_20260304_085410.owl` — Score: 4.11

Features a double pivot (`OrganizationRoleAssignment` + `InvoiceLineAssociation`) and a rich `InvoiceMessage owl:equivalentClass [intersectionOf(:Message, [someValuesFrom ORA], [someValuesFrom ILA], [allValuesFrom :BusinessProcess])]` that provides a closed, four-way necessary-and-sufficient definition. However, IR=0.0526 (near-zero) reflects an extremely flat hierarchy — most classes are at the same level with minimal subclass structure. AR=0.6842 is adequate. Axiom Diversity=6. The `allValuesFrom :BusinessProcess` constraint creates a requirement that every invoice must be part of some business process, which may be overly restrictive for standalone invoices.

### Rank 6 — `EDIFACT_ontology_20260304_070119.owl` — Score: 4.05

Deepest class hierarchy in the group (max depth=4): `InterchangeEnvelope > EDIFACTMessage > InvoiceMessage > Header/Detail/Summary`. Uses `OrganizationRoleAssignment` pivot with `owl:cardinality "1"` constraints on both role and organization. `AgentRole owl:disjointUnionOf` closes the role taxonomy partially. Key weakness: `LineItem rdfs:subClassOf :InvoiceDetail` makes line items structural segments rather than semantic content, conflating the structural and semantic layers. IR=0.4706, RR=0.8235, AR=0.7059 — strong structural metrics. Axiom Diversity=5.

### Rank 7 — `EDIFACT_ontology_20260304_063345.owl` — Score: 3.97

Uses `OrganizationRoleAssignment` pivot with `BuyerRole` as a named individual. Includes `Section owl:disjointUnionOf` for the three sections. Notable issue: `hasSection owl:FunctionalProperty` — this is incorrect because an invoice message has multiple sections (header, detail, summary), not a single functional section. The blank-node restriction `_:bn rdfs:subClassOf :OrganizationRoleAssignment` uses unusual anonymous node syntax in Turtle. IR=0.3529, AR=0.7059, RR=0.8235. Axiom Diversity=5.

### Rank 8 — `EDIFACT_ontology_20260304_090528.owl` — Score: 3.80

Reuses the same `InvoiceMessage equivalentClass` pattern as Rank 5 (085410) but with `allValuesFrom :BusinessProcess` constraint. Axiom Diversity=3 is low for its structural complexity. No named `AgentRole` subclasses declared, weakening CQ3 and CQ13. RR=0.8182, AR=0.6364, IR=0.1818 (flat). The `allValuesFrom :BusinessProcess` restriction is structurally sound but reduces open-world applicability.

### Rank 9 — `EDIFACT_ontology_20260304_075831.owl` — Score: 3.85

Contains 21 classes — the largest class count in the group. Introduces `ValidationConstraint` class (analogous to Rank 3's SHACLConstraint). Key logical defect: `RoleAssignment owl:equivalentClass [allValuesFrom :Organization][allValuesFrom :AgentRole]` — the intersection of two `allValuesFrom` restrictions is logically vacuous (satisfied by any instance with no outgoing property values). Axiom Diversity=6 is high but partially attributed to this incorrect axiom pattern. RR=0.8095, AR=0.6190, IR=0.3333.

### Rank 10 — `EDIFACT_ontology_20260304_092221.owl` — Score: 3.77

AR=0.8235 is the second-highest in the group, reflecting rich data property coverage. Has `Segment owl:disjointUnionOf` for the three sections. Key structural defect: `LineItem rdfs:subClassOf :DetailSection` — same conflation error as Rank 6. `OrganizationRoleAssignment` has cardinality restrictions. IR=0.2941 is below the target range. Axiom Diversity=4. Missing any named `AgentRole` subclasses.

### Rank 11 — `EDIFACT_ontology_20260304_072404.owl` — Score: 3.55

Has the highest object property count (34) but Axiom Diversity=3, suggesting the property definitions are not backed by sufficient axiom structure. `BuyerAssignment owl:equivalentClass [someValuesFrom :Buyer]` is sound but the rest of the ontology is under-axiomatized. `hasAddress` is on `Organization` rather than the pivot, failing the E/D/E scenario. `Segment owl:disjointUnionOf` present. RR=0.8235 (high due to many object properties), AR=0.6500, IR=0.3000.

### Rank 12 — `EDIFACT_ontology_20260304_071919.owl` — Score: 3.60

Uses `Invoice owl:equivalentClass [intersectionOf(:Message, [allValuesFrom [unionOf sections]])]` — a union of sections inside `allValuesFrom` which again creates a vacuous constraint (an invoice with no sections satisfies it trivially). `InvoiceItemLine` with mixed `someValuesFrom` and `hasPrice` is reasonable. `hasSection owl:FunctionalProperty` (same error as Rank 7). AR=0.6190, RR=0.7619, IR=0.3333. Axiom Diversity=5.

### Rank 13 — `EDIFACT_ontology_20260304_112519.owl` — Score: 3.39

20 classes including `GlobalLocationNumber subClassOf Identifier` (the only other ontology besides Rank 3 to subclass `Identifier`). `BuyerAssignment owl:equivalentClass [owl:hasValue :Buyer]` is sound. Key gap: missing inverse properties for most object properties, reducing navigability. `hasSection owl:FunctionalProperty` error present. Axiom Diversity=3. No `Involvement`/`RoleAssignment` equivalence axioms. RR=0.7391, AR=0.6500, IR=0.4000.

### Rank 14 — `EDIFACT_ontology_20260304_073706.owl` — Score: 3.36

16 classes — the smallest class count in the group. Achieves Axiom Diversity=7 (tied with Rank 4 for highest) via `owl:hasValue`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, and `owl:FunctionalProperty`. However IR=0.0625 is near-zero — the hierarchy is almost entirely flat. `OrganizationRoleAssignment owl:equivalentClass [intersectionOf([someValuesFrom :AgentRole][someValuesFrom :InvoiceMessage])]` — linking `OrganizationRoleAssignment` directly to `InvoiceMessage` rather than to `Organization` is a structural inversion. RR=0.9600 (highest in group, but partly inflated by the direct InvoiceMessage link). No section classes means CQ14 cannot be answered directly.

### Rank 15 — `EDIFACT_ontology_20260304_072939.owl` — Score: 3.07

17 classes. Axiom Diversity=2 (lowest in group). `BuyerOrganization owl:equivalentClass [intersectionOf(:Organization, [someValuesFrom [hasValue :Buyer]])]` — nests `owl:hasValue` inside `someValuesFrom` which is unnecessarily complex and semantically unusual. No `owl:someValuesFrom` restrictions on structural classes. Missing section-level data properties for CQ7 and CQ8. IR=0.2941, AR=0.5882, RR=0.7647. Sparse annotation coverage.

### Rank 16 — `EDIFACT_ontology_20260304_075320.owl` — Score: 2.72

18 classes but only 6 data properties — lowest AR in the group (AR=0.3333). `Message owl:disjointUnionOf (:InvoiceMessage)` is a degenerate single-member union with no logical effect. Cannot answer CQ6, CQ7, CQ8 directly due to missing data properties. Axiom Diversity=3. IR=0.2222 (flat). Ontology represents structural skeleton without semantic content.

### Rank 17 — `EDIFACT_ontology_20260304_111526.owl` — Score: 2.67

17 classes. Axiom Diversity=3. `RoleAssignment owl:equivalentClass [allValuesFrom :Organization][allValuesFrom :AgentRole]` — same vacuous pattern as Rank 9. IR=0.0588 (lowest in group). No structural section classes (no `HeaderSection`, `DetailSection`, `SummarySection`), directly failing CQ14. Sparse data properties prevent answering CQ6–CQ9. Cannot model the E/D/E scenario (CQ13). The ontology captures only the skeleton of the EDIFACT message hierarchy without substantive axiom content.

---

## Cross-Cutting Observations

### Pattern Prevalence

**N-ary Role Reification**: 15 of 17 ontologies implement an `OrganizationRoleAssignment` or equivalent pivot class. This is the single most consistent design decision in the corpus, reflecting strong task-instruction compliance. Quality varies: Ranks 1–3 use the pivot correctly with address attached to the pivot; Ranks 4, 11 attach address directly to `Organization`, breaking multi-role support.

**Section Disjointness**: 12 of 17 ontologies declare `Segment` subclasses (Header/Detail/Summary) and apply `owl:disjointUnionOf` or `owl:disjointWith` between them. The 5 exceptions (Ranks 14, 15, 16, 17, and partially 12) lose the ability to answer CQ14 precisely.

**allValuesFrom Misuse**: 5 ontologies (Ranks 3, 5, 6, 8, 9, 12) use `allValuesFrom` in equivalence class definitions where `someValuesFrom` is semantically required. This is the most common logical error in the corpus, producing vacuously-satisfiable class definitions.

**FunctionalProperty on hasSection**: 4 ontologies (Ranks 3, 7, 12, 13) incorrectly declare `hasSection owl:FunctionalProperty`. An invoice message has three sections; declaring this functional means a reasoner infers all sections are the same individual.

### Axiom Diversity vs. Correctness Trade-off

The highest Axiom Diversity scores (7 in Ranks 4 and 14) do not correspond to the highest overall rankings because diversity alone does not indicate correctness. Rank 14 achieves diversity=7 through a structurally inverted `OrganizationRoleAssignment` definition. Rank 1 achieves score 4.73 with diversity=6 because each construct is used purposefully.

### IR Bimodal Distribution

Inheritance Richness values split into two clusters: {0.05–0.18} (flat ontologies: Ranks 6, 8, 9, 14, 17) and {0.30–0.53} (structured ontologies: Ranks 1, 2, 4, 6, 7, 10, 12). The top-ranked ontologies consistently fall in the upper cluster. IR is the structural metric most predictive of overall rank (Spearman correlation ≈ 0.71).

---

*End of report. All metric values sourced from `data/FinalResults/ontology_report.md` Section 3.2.*
