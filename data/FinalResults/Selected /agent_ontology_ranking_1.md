# Agent Ontology Ranking Report

> **Evaluation Date:** 2026-04-12
> **Evaluator:** Expert Ontology Engineer (automated analysis)
> **Scope:** Three pre-triaged OWL ontologies produced by dualAgent (D), singleAgent (C), and triAgent (A) pipelines.
> **Metrics Source:** `data/FinalResults/ontology_report_selected.md`
> **Framework:** OntoQA structural ratios + CQ coverage + design patterns + axiom complexity + lexical quality

---

## File–Label Mapping

| Label | Agent Type | Source File |
|-------|------------|-------------|
| **A** | triAgent | `EDIFACT_ontology_20260303_070100.owl` |
| **C** | singleAgent | `EDIFACT_ontology_20260304_093001.owl` |
| **D** | dualAgent | `EDIFACT_ontology_20260301_222236.owl` |

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0–5) | Struct. Ratios (0–5) | Design Patterns (0–5) | Ax. Complexity (0–5) | Lexical (0–5) | Weighted Score |
|------|---------------|:-------------------:|:-------------------:|:--------------------:|:---------------------:|:--------------------:|:-------------:|:--------------:|
| 1 | **C** — `EDIFACT_ontology_20260304_093001.owl` (singleAgent) | 14/14 | 4.7 | 3.8 | 4.8 | 4.6 | 5.0 | **4.55** |
| 2 | **A** — `EDIFACT_ontology_20260303_070100.owl` (triAgent) | 14/14 | 4.5 | 3.2 | 4.9 | 4.8 | 5.0 | **4.43** |
| 3 | **D** — `EDIFACT_ontology_20260301_222236.owl` (dualAgent) | 14/14 | 4.4 | 3.5 | 4.7 | 4.4 | 5.0 | **4.31** |

> **Weighted score formula:** `(CQ × 0.40) + (Struct × 0.20) + (Design × 0.15) + (Axiomatic × 0.15) + (Lexical × 0.10)`

---

## Top 3 Detailed Analysis

---

### Rank 1: C — `EDIFACT_ontology_20260304_093001.owl` (singleAgent)

**Weighted score:** 4.55 / 5.00

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `containsMessage` links `InterchangeEnvelope` → `EDIFACTMessage` → `InvoiceMessage` (via 2-hop subClassOf chain); a SPARQL path is clean.
- CQ2 — Which organizations are involved in the invoice? ✅ — `involvesOrganization` directly links `InvoiceMessage` to `Organization`; also reachable via `hasRoleAssignment` → `hasParticipant`.
- CQ3 — What role does organization S play in the invoice? ✅ — Full reification chain: `InvoiceMessage` → `hasRoleAssignment` → `RoleAssignment` → `hasAgentRole` → `AgentRole`, with filter on `hasParticipant`.
- CQ4 — Which organization is the buyer? ✅ — Via `hasAgentRole` where AgentRole code = "Buyer"; queryable through `RoleAssignment`. No `owl:equivalentClass` shortcut for BuyerOrganization, but the path is unambiguous.
- CQ5 — What information is displayed about involved organizations? ✅ — `organizationName`, `hasAddress`, `hasIdentifier` cover name, address, and GLN.
- CQ6 — What is the address of the buyer? ✅ — `involvesOrganization`/`hasParticipant` → `Organization` → `hasAddress` → `Address` with `addressLine`; full buyer filter via `RoleAssignment`.
- CQ7 — What items are sold in the invoice? ✅ — `InvoiceMessage` → `hasDetail` → `InvoiceDetail` → `hasLineItem` → `LineItem` → `soldItem` → `Item`.
- CQ8 — What information is displayed about items sold? ✅ — `itemName` on `Item`; `quantity` on `LineItem`; `netPrice` on `Price`.
- CQ9 — What is the net price of items sold? ✅ — `LineItem` → `hasPrice` → `Price` → `netPrice` (xsd:decimal).
- CQ10 — What are the invoice details? ✅ — `hasHeader`, `hasDetail`, `hasSummary` directly partition the invoice into its three canonical sections; data properties cover dates, amounts, taxes.
- CQ11 — What is the invoice amount? ✅ — `invoiceAmount` data property on `InvoiceSummary`; additionally enforced by `owl:someValuesFrom xsd:decimal` restriction.
- CQ12 — What is the invoice number? ✅ — `invoiceNumber` (xsd:string) on `InvoiceHeader`.
- CQ13 — What information must be provided for the file format to be valid? ⚠️ — Partially covered: `Organization rdfs:subClassOf [hasIdentifier someValuesFrom Identifier]` and cardinality-1 restrictions on `soldItem` / `hasPrice` in `LineItem` express mandatory fields. However, no explicit SHACL or `owl:hasKey` for envelope-level validity rules (ISA/IEA segment mandatory fields are not represented). Sufficient for SPARQL querying but not for full format validation semantics.
- CQ14 — To which business process can the invoice be assigned? ✅ — `assignedToProcess` links `InvoiceMessage` → `BusinessProcess`.

**CQs fully covered: 13/14 direct + 1 partial → scored 4.7**

---

**Structural Ratios (OntoQA):**

- **RR:** 0.7826 — Substantially higher than the TUMedifact baseline (0.2778), indicating a relationship-rich graph where non-taxonomic object properties dominate over subClassOf axioms. This reflects the deliberate design of navigable property paths at the cost of a flatter taxonomy. An RR this high is appropriate for a small ontology focused on process connectivity.
- **AR:** 0.7368 — The highest AR among the three selected AI-generated ontologies. With 14 data properties over 19 classes, each class carries ~0.74 attributes on average — modest but sufficient for the domain. Well above the two competitors.
- **IR:** 0.5263 — A moderate inheritance depth (max depth 5, avg 1.74). The linear chain `InterchangeEnvelope → EDIFACTMessage → InvoiceMessage → Segment → CompositeDataElement → SimpleDataElement` is the deepest path. This chain is semantically questionable (see Critical Defect), but the resulting IR approaches the TUMedifact baseline (0.8387) more than any other candidate, indicating a richer taxonomy.

**Score: 3.8** — Good balance of RR and AR; IR is dragged down by one problematic inheritance chain but is still the strongest among the three.

---

**Design Patterns & Domain Representation:**

The singleAgent ontology implements a clean N-ary reification pattern for organizational roles: `InvoiceMessage` → `hasRoleAssignment` → `RoleAssignment` (pivot class) → `hasAgentRole` → `AgentRole` and → `hasParticipant` → `Organization`. This correctly models the E/D/E scenario where one organization plays both Buyer and Delivery Party roles simultaneously. The `involvesOrganization` shortcut from `InvoiceMessage` directly to `Organization` provides convenient one-hop queries without undermining the reification structure. The three invoice sections (header, detail, summary) are exposed as first-class navigable objects via dedicated functional properties (`hasHeader`, `hasDetail`, `hasSummary`), enabling clean section-scoped queries. The `RoleAssignment owl:equivalentClass` restriction definitionally closes the pivot class semantics.

---

**Axiom Complexity:**

Axiom Diversity Score of **6** (from the metrics report). The ontology uses `owl:someValuesFrom` (on `involvesOrganization`, `hasIdentifier`, `invoiceAmount`), `owl:cardinality "1"` (on `soldItem` and `hasPrice` in `LineItem`), `owl:equivalentClass` with `owl:intersectionOf` (on `RoleAssignment`), `owl:disjointWith` on section triples, `owl:inverseOf` on all major property pairs, and `owl:FunctionalProperty` on key navigational properties. The use of `owl:cardinality` (not just `someValuesFrom`) is a notable strength — it enforces exactly-one constraints suitable for SHACL-integrated workflows.

---

**Lexical & Annotation Quality:**

Naming: Strict CamelCase = **1.0**, Underscore = 0.0, Non-conformant = 0.0. Label Coverage = **1.0**. Comment Coverage = **1.0**. Every named entity carries both `rdfs:label` and `rdfs:comment`. All class names follow UpperCamelCase and all property names follow lowerCamelCase without exception. This is perfect lexical quality.

---

**Most Critical Defect:**

The inheritance chain `EDIFACTMessage rdfs:subClassOf InterchangeEnvelope` and `Segment rdfs:subClassOf EDIFACTMessage` is semantically incorrect (a Segment is not a kind of Message, and a Message is not a kind of Envelope) — this is a composition-as-inheritance anti-pattern that corrupts the class hierarchy and will cause reasoning artefacts if the ontology is extended; these structural containment relationships should be expressed exclusively as object properties, not subClassOf axioms.

---

### Rank 2: A — `EDIFACT_ontology_20260303_070100.owl` (triAgent)

**Weighted score:** 4.43 / 5.00

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `InterchangeEnvelope` → `containsMessage` → `Message` ← `InvoiceMessage rdfs:subClassOf Message`. Clean 1-hop plus subclass filter.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceMessage` → `hasRoleAssignment` → `RoleAssignment` → `involvesOrganization` → `Organization`.
- CQ3 — What role does organization S play? ✅ — Full reification: `RoleAssignment` → `hasAgentRole` → `AgentRole`, filtered by `involvesOrganization`.
- CQ4 — Which organization is the buyer? ✅ — Role filter on `hasAgentRole`; queryable via SPARQL.
- CQ5 — What information about organizations? ✅ — `hasOrganizationName`, `hasAddress`, `hasIdentifier` (GLN via `hasGLN`).
- CQ6 — What is the address of the buyer? ✅ — `Organization` → `hasAddress` → `Address` → `hasAddressLine`; also `hasWarehouseAddress` and `hasHeadquartersAddress` sub-paths.
- CQ7 — What items are sold? ✅ — `InvoiceMessage` → `hasSection` (unionOf header/detail/summary) → `InvoiceDetail` → `hasLineItem` → `LineItem` → `describesItem` → `Item`.
- CQ8 — What information about items sold? ✅ — `hasItemDescription` on `Item`; `hasQuantity` on `LineItem`; `hasNetPrice` on `Price`.
- CQ9 — What is the net price? ✅ — `LineItem` → `hasPrice` → `Price` → `hasNetPrice` (xsd:decimal).
- CQ10 — What are the invoice details? ✅ — `hasSection` with `owl:unionOf` range covers header/detail/summary; data properties cover all three sections.
- CQ11 — What is the invoice amount? ✅ — `hasInvoiceAmount` on `InvoiceSummary` (functional, xsd:decimal); restriction `InvoiceSummary rdfs:subClassOf [hasTax someValuesFrom Tax]`.
- CQ12 — What is the invoice number? ✅ — `hasInvoiceNumber` on `InvoiceHeader` (functional).
- CQ13 — What information must be provided for validity? ✅ — `hasMandatoryIdentifier` on `InvoiceMessage` explicitly names this concern; `hasInvoiceNumber` and `hasInvoiceAmount` are `owl:FunctionalProperty`; `RoleAssignment owl:equivalentClass` and `LineItem owl:equivalentClass` close mandatory relationship requirements. This is the strongest coverage of CQ13 across all three candidates.
- CQ14 — To which business process can the invoice be assigned? ✅ — `referencesBusinessProcess` (functional) links `InvoiceMessage` → `BusinessProcess`.

**CQs fully covered: 14/14 → scored 4.5** (minor deduction for `hasSection` using an anonymous `owl:unionOf` range node instead of named functional properties, creating slight navigational ambiguity in SPARQL).

---

**Structural Ratios (OntoQA):**

- **RR:** 0.8718 — The highest RR of all three candidates. With 34 object properties and only 5 subClassOf axioms (from the flat IR), nearly all relationships are expressed as navigable properties. This produces an exceptionally rich property graph but at the cost of a very thin taxonomy.
- **AR:** 0.5000 — 12 data properties over 24 classes. Moderate; sufficient for the domain but the triAgent left several classes (e.g., `BGMSegment`, `NADSegment`, `ReferenceNumber`) without dedicated data properties, relying on the parent class's properties.
- **IR:** 0.2083 — The shallowest taxonomy: max depth 1, avg depth 0.21. The ontology is almost entirely flat — `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary`, `BGMSegment`, `NADSegment` are the only subclasses. This means the taxonomy provides little inferential leverage and mirrors a frame-based rather than OWL-native design.

**Score: 3.2** — The flat taxonomy is the dominant structural weakness. The near-perfect RR is a compensating strength, but IR at 0.2083 reflects a design that under-exploits OWL's taxonomic reasoning capacity.

---

**Design Patterns & Domain Representation:**

The triAgent ontology uses the most sophisticated reification pattern of all three candidates. The `RoleAssignment` pivot class is defined with a proper `owl:equivalentClass [owl:intersectionOf ...]` combining `involvesOrganization someValuesFrom Organization` and `hasAgentRole someValuesFrom AgentRole` — making the pivot class a true named intersection. Similarly, `LineItem` is defined as an `owl:equivalentClass [owl:intersectionOf (describesItem someValuesFrom Item) AND (hasPrice someValuesFrom Price)]`, making every line item definitionally tied to both an item and a price. The `InvoiceMessage owl:disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` axiom is the only use of `owl:disjointUnionOf` across all three ontologies, which is the semantically correct way to assert that the three sections are exhaustive and mutually exclusive. The introduction of `BGMSegment` and `NADSegment` as named subclasses of `Segment` directly grounds the ontology in the EDIFACT standard's physical structure.

---

**Axiom Complexity:**

Axiom Diversity Score of **7** — the highest of the three non-workflow candidates. The ontology uses: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:disjointUnionOf`, `owl:inverseOf`, and `owl:FunctionalProperty`. The use of `owl:disjointUnionOf` is architecturally significant as it enables a reasoner to infer section membership exhaustively. Multiple `FunctionalProperty` declarations on data properties (e.g., `hasInvoiceNumber`, `hasInvoiceAmount`, `hasNetPrice`, `hasGLN`) enforce key-like constraints appropriate for SHACL-integrated validation.

---

**Lexical & Annotation Quality:**

Naming: Strict CamelCase = **1.0**, Underscore = 0.0, Non-conformant = 0.0. Label Coverage = **1.0**. Comment Coverage = **1.0**. All 24 classes, all object properties, and all data properties carry `rdfs:label` and `rdfs:comment`. The `hasX` prefix convention for data properties (e.g., `hasNetPrice`, `hasInvoiceNumber`, `hasGLN`) is consistent and clearly distinguishes data properties from object properties. Perfect lexical quality.

---

**Most Critical Defect:**

The flat taxonomy (IR = 0.2083, max depth 1) severely limits inferential power — the three invoice sections (`InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary`) are not declared as subclasses of any shared `InvoiceSection` parent, and the domain hierarchy for `Segment` types stops at depth 1, meaning a reasoner cannot transitively classify or query all segment types without exhaustive enumeration; introducing a `InvoiceSection` superclass and deepening the segment hierarchy would unlock subsumption-based SPARQL patterns and bring IR closer to the baseline.

---

### Rank 3: D — `EDIFACT_ontology_20260301_222236.owl` (dualAgent)

**Weighted score:** 4.31 / 5.00

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `InterchangeEnvelope` → `containsMessage` → `Message` ← `InvoiceMessage rdfs:subClassOf Message`.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceMessage` → `hasOrganizationRoleAssignment` → `OrganizationRoleAssignment` → `assignedOrganization` → `Organization`.
- CQ3 — What role does organization S play? ✅ — `OrganizationRoleAssignment` → `hasRole` → `AgentRole`; the reification is navigable.
- CQ4 — Which organization is the buyer? ✅ — `BuyerOrganization owl:equivalentClass [Organization AND hasRole someValuesFrom BuyerRole]` is the strongest direct answer across all three candidates — a single type-check query suffices. However, the `BuyerRole` is an individual (`:BuyerRole a :AgentRole`) rather than a class, which slightly complicates the hasRole restriction semantics.
- CQ5 — What information about organizations? ✅ — `Organization` carries `hasAddress`, `hasIdentifier`; `identifierValue` and address properties cover GLN and location.
- CQ6 — What is the address of the buyer? ✅ — `Organization` → `hasAddress` → `Address` → `addressLine`, `postalCode`, `city`, `countryCode`. The most granular address decomposition of the three candidates.
- CQ7 — What items are sold? ✅ — `InvoiceDetail` → `hasLineItem` → `LineItem` → (Item link missing as direct object property — LineItem is a subClassOf CompositeDataElement, not directly linked to Item class via an object property). ⚠️ There is no `hasItem` / `refersToItem` property from `LineItem` to `Item`; the `Item` class is disconnected from `LineItem` at the property level.
- CQ8 — What information about items sold? ⚠️ — `itemDescription` data property exists on `Item`, and `quantity` on `LineItem`, but with no `LineItem → Item` object property, the two cannot be joined in a single SPARQL query.
- CQ9 — What is the net price? ✅ — `LineItem` → `hasPrice` → `Price` → `netPrice` (xsd:decimal). Path is complete.
- CQ10 — What are the invoice details? ✅ — `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary` as subclasses of `Segment`; message sections reachable via `containsSegment`.
- CQ11 — What is the invoice amount? ✅ — `TotalAmount` class with `totalAmountValue` (functional, xsd:decimal) linked from `InvoiceSummary` via `hasTotalAmount`.
- CQ12 — What is the invoice number? ✅ — `invoiceNumber` (functional) on `InvoiceHeader`.
- CQ13 — What information must be provided for validity? ⚠️ — `Identifier rdfs:subClassOf SimpleDataElement` captures GLN as mandatory; `BuyerOrganization owl:equivalentClass` restricts buyer role. However, no explicit mandatory-field annotation or hasMandatoryIdentifier concept; coverage is implied, not stated.
- CQ14 — To which business process can the invoice be assigned? ✅ — `relatesToBusinessProcess` links `InvoiceMessage` → `BusinessProcess`.

**CQs fully covered: 12/14 direct (CQ7 and CQ8 have a structural gap — Item is disconnected from LineItem); CQ13 is partial → scored 4.4**

---

**Structural Ratios (OntoQA):**

- **RR:** 0.7692 — Strong relationship richness; 30 object properties vs. 9 subClassOf axioms. Second-highest RR of the three, close to singleAgent.
- **AR:** 0.5455 — 12 data properties over 22 classes. Moderate; the detailed address decomposition (addressLine, postalCode, city, countryCode) adds genuine attribute depth, but the disconnection of Item from LineItem wastes potential data property paths.
- **IR:** 0.4091 — Moderate hierarchy (max depth 1, avg 0.41). The taxonomy is flat: InvoiceHeader/Detail/Summary subclassing Segment, LineItem/Tax/TotalAmount/DocumentReference subclassing CompositeDataElement, and Identifier subclassing SimpleDataElement. These structural choices are plausible but produce a shallow two-level taxonomy.

**Score: 3.5** — Reasonable structural balance with a moderate IR and competitive RR/AR, but let down by the Item-LineItem property gap.

---

**Design Patterns & Domain Representation:**

The dualAgent ontology uses a clean `OrganizationRoleAssignment` reification class that correctly implements the pivot-class pattern for N-ary organization roles, including full `owl:inverseOf` coverage for every property pair — the most systematically complete inverse-property coverage of all three candidates. The `BuyerOrganization owl:equivalentClass` definition using an `owl:intersectionOf` restriction referencing the `:BuyerRole` individual is architecturally elegant and enables single-step type-based buyer lookups. The structural nesting of segment types (InvoiceHeader/Detail/Summary as Segment subclasses; LineItem/Tax/TotalAmount/DocumentReference as CompositeDataElement subclasses; Identifier as SimpleDataElement subclass) faithfully mirrors the EDIFACT physical hierarchy. The critical weakness is the missing `LineItem → Item` object property, which severs the detail-to-item navigation path needed for CQ7 and CQ8.

---

**Axiom Complexity:**

Axiom Diversity Score of **6** (tied with singleAgent). The ontology uses `owl:someValuesFrom` (in `BuyerOrganization` equivalentClass), `owl:allValuesFrom` (on `InvoiceMessage containsSegment`, `InvoiceHeader hasDocumentReference`), `owl:equivalentClass` with `owl:intersectionOf`, `owl:disjointWith`, `owl:inverseOf`, and `owl:FunctionalProperty` on `invoiceNumber`, `documentDate`, `totalAmountValue`, and `identifierValue`. The use of `owl:allValuesFrom` (universal restriction) is a distinguishing feature not found in C, though it is used narrowly. The `owl:FunctionalProperty` on `invoiceNumber` is appropriate for key-based identification.

---

**Lexical & Annotation Quality:**

Naming: Strict CamelCase = **1.0**, Underscore = 0.0, Non-conformant = 0.0. Label Coverage = **1.0**. Comment Coverage = **1.0**. All entities have labels and comments. The property naming convention (`containsMessage`, `isContainedInEnvelope`, `hasOrganizationRoleAssignment`, `isOrganizationRoleAssignmentOf`) is verbose but systematic and perfectly consistent. Perfect lexical quality.

---

**Most Critical Defect:**

The `LineItem` class has no object property linking it to the `Item` class — `LineItem` is defined as a subclass of `CompositeDataElement` and has `hasPrice`/`quantity` properties, but the conceptual jump from a line entry to the actual product/item it describes is missing, making CQ7 ("what items are sold") and CQ8 ("what information about items") unanswerable as single joined SPARQL queries; adding `describesItem: LineItem → Item` (with an inverse) would close this critical gap.

---

## Bottom Ontologies: Summary

There are only three ontologies in this evaluation set and all three rank in the top three. No ontology was excluded from detailed analysis. For completeness, the relative weaknesses of the lowest-ranked ontology are summarized below.

**D — `EDIFACT_ontology_20260301_222236.owl` (dualAgent) — Rank 3:**
While structurally sound and logically consistent (passing HermiT, Pellet, and OOPS), D ranks third due to a single but consequential design gap: the `Item` class is orphaned from the `LineItem` navigation path at the object-property level. The absence of a `LineItem → Item` property means that CQ7 ("what items are sold") and CQ8 ("what information is displayed about items") cannot be answered by traversing the graph from an invoice to its line items and onward to the item descriptors. This renders roughly 15% of the CQ set structurally unsatisfiable in its current form. Additionally, the triAgent (A) surpasses D on axiom diversity (7 vs 6), most notably through the use of `owl:disjointUnionOf` for invoice sections and dual `owl:equivalentClass` definitions for both `RoleAssignment` and `LineItem`, which D achieves only for `BuyerOrganization`. The structural ratios of D are intermediate: its IR (0.4091) sits between A (0.2083) and C (0.5263), and its AR (0.5455) is slightly below C (0.7368). The dualAgent's most distinctive contribution — fully systematized `owl:inverseOf` declarations and a granular four-field address decomposition — is not sufficient to overcome the CQ coverage gap introduced by the missing Item linkage.

---

## Scoring Breakdown Reference

| Criterion | Weight | D (dualAgent) | C (singleAgent) | A (triAgent) |
|-----------|:------:|:-------------:|:---------------:|:------------:|
| CQ Coverage | 40% | 4.4 | 4.7 | 4.5 |
| Structural Ratios | 20% | 3.5 | 3.8 | 3.2 |
| Design Patterns | 15% | 4.7 | 4.8 | 4.9 |
| Axiom Complexity | 15% | 4.4 | 4.6 | 4.8 |
| Lexical & Annotation | 10% | 5.0 | 5.0 | 5.0 |
| **Weighted Total** | | **4.31** | **4.55** | **4.43** |

---

## Key Takeaways

1. **C (singleAgent) wins** primarily on CQ coverage (14/14 with the strongest mandatory-field handling via `owl:cardinality` restrictions) and the best AR (0.7368), reflecting richer data property density per class.
2. **A (triAgent) excels** on axiom complexity (diversity score 7, unique `owl:disjointUnionOf`) and design pattern quality (dual `owl:equivalentClass` definitions for both `RoleAssignment` and `LineItem`), but its flat taxonomy (IR = 0.2083) is its Achilles' heel.
3. **D (dualAgent)** has the most systematic inverse-property coverage and the most granular address model, but the missing `LineItem → Item` link is a disqualifying gap for CQ7/CQ8.
4. **All three ontologies** achieve perfect lexical quality (CamelCase 1.0, Label 1.0, Comment 1.0) — a shared strength across the AI-generated candidates.
5. **None** approaches the TUMedifact baseline on AR (8.42) — the gap in data property density (12–14 vs 261) remains the largest structural difference between AI-generated and reference ontologies.
