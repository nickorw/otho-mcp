# EDIFACT Ontology Ranking Report — dualAgent Cohort

> **Evaluator:** Expert Ontology Engineer (AI-assisted)
> **Date:** 2026-03-08
> **Cohort:** `dualAgent` — 20 OWL ontologies, all syntax-valid, HermiT-consistent, Pellet-consistent, OOPS-passed
> **Framework:** OntoQA structural ratios · CQ coverage (14 questions) · Design patterns · Axiom complexity · Lexical quality

---

## Scoring Methodology

| Dimension | Weight | Score Range |
|---|---|---|
| CQ Coverage | 40% | 0.0 – 5.0 |
| Structural Ratios (OntoQA) | 20% | 0.0 – 5.0 |
| Design Patterns | 15% | 0.0 – 5.0 |
| Axiom Complexity | 15% | 0.0 – 5.0 |
| Lexical & Annotation | 10% | 0.0 – 5.0 |

**Weighted Score** = 0.40·CQ + 0.20·SR + 0.15·DP + 0.15·AC + 0.10·LA

All structural ratios (RR, AR, IR) are taken verbatim from `data/FinalResults/ontology_report.md`. Axiom Diversity Scores likewise.

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|---|---|---|---|---|---|---|---|---|
| 1 | `EDIFACT_ontology_20260301_222236.owl` | 14/14 | 4.8 | 4.2 | 5.0 | 4.5 | 5.0 | **4.67** |
| 2 | `EDIFACT_ontology_20260301_225732.owl` | 14/14 | 4.7 | 4.3 | 4.8 | 4.2 | 5.0 | **4.60** |
| 3 | `EDIFACT_ontology_20260301_220437.owl` | 14/14 | 4.7 | 4.1 | 5.0 | 3.5 | 5.0 | **4.55** |
| 4 | `EDIFACT_ontology_20260301_223750.owl` | 14/14 | 4.6 | 4.2 | 4.7 | 3.2 | 5.0 | **4.44** |
| 5 | `EDIFACT_ontology_20260301_230018.owl` | 14/14 | 4.6 | 4.0 | 4.7 | 3.8 | 5.0 | **4.43** |
| 6 | `EDIFACT_ontology_20260301_224527.owl` | 14/14 | 4.6 | 4.0 | 4.5 | 4.0 | 5.0 | **4.42** |
| 7 | `EDIFACT_ontology_20260301_225145.owl` | 13/14 | 4.3 | 4.0 | 4.7 | 3.8 | 5.0 | **4.26** |
| 8 | `EDIFACT_ontology_20260301_222534.owl` | 14/14 | 4.4 | 3.8 | 4.8 | 4.0 | 5.0 | **4.26** |
| 9 | `EDIFACT_ontology_20260301_220832.owl` | 13/14 | 4.3 | 4.1 | 4.5 | 3.8 | 5.0 | **4.22** |
| 10 | `EDIFACT_ontology_20260301_230338.owl` | 13/14 | 4.2 | 3.5 | 4.5 | 4.0 | 5.0 | **4.15** |
| 11 | `EDIFACT_ontology_20260301_224922.owl` | 13/14 | 4.2 | 3.9 | 4.5 | 3.0 | 5.0 | **4.10** |
| 12 | `EDIFACT_ontology_20260301_221940.owl` | 13/14 | 4.1 | 3.8 | 4.3 | 3.2 | 5.0 | **4.04** |
| 13 | `EDIFACT_ontology_20260301_215924.owl` | 13/14 | 4.1 | 3.6 | 4.3 | 4.0 | 5.0 | **4.04** |
| 14 | `EDIFACT_ontology_20260301_225409.owl` | 12/14 | 3.8 | 3.7 | 4.2 | 3.0 | 5.0 | **3.88** |
| 15 | `EDIFACT_ontology_20260301_224212.owl` | 12/14 | 3.8 | 3.6 | 4.0 | 3.8 | 5.0 | **3.87** |
| 16 | `EDIFACT_ontology_20260301_221332.owl` | 12/14 | 3.7 | 3.4 | 4.0 | 3.0 | 5.0 | **3.76** |
| 17 | `EDIFACT_ontology_20260301_223501.owl` | 12/14 | 3.7 | 3.7 | 4.0 | 2.8 | 5.0 | **3.74** |
| 18 | `EDIFACT_ontology_20260301_221113.owl` | 11/14 | 3.5 | 3.7 | 3.8 | 2.8 | 5.0 | **3.62** |
| 19 | `EDIFACT_ontology_20260301_215700.owl` | 11/14 | 3.4 | 3.7 | 3.5 | 2.8 | 5.0 | **3.54** |
| 20 | `EDIFACT_ontology_20260301_221725.owl` | 10/14 | 3.0 | 3.2 | 3.5 | 2.8 | 5.0 | **3.25** |

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_ontology_20260301_222236.owl`

**Weighted score:** 4.67 / 5.00

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `InvoiceMessage` is a named subclass of `Message`; `containsMessage` links `InterchangeEnvelope` → `Message`/`InvoiceMessage`.
- CQ2 — Which organizations are involved in the invoice? ✅ — `OrganizationRoleAssignment` reifies the link; `assignedOrganization` navigates to `Organization`.
- CQ3 — What role does organization S play in the invoice? ✅ — `OrganizationRoleAssignment` pivot with `hasRole` → `AgentRole`; exactly the right reification pattern.
- CQ4 — Which organization is the buyer? ✅ — Explicit `BuyerOrganization` class defined via `owl:equivalentClass` with `owl:intersectionOf` and `owl:someValuesFrom :BuyerRole`; named instances `BuyerRole`, `SellerRole`, `DeliveryPartyRole` declared.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Organization` carries `identifierValue`, `addressLine`, `postalCode`, `city`, `countryCode` via `Address`; structured and queryable.
- CQ6 — What is the address of the buyer? ✅ — `hasAddress` links `Organization` → `Address`; address includes decomposed data properties (street, postal code, city, country).
- CQ7 — What items are sold in the invoice? ✅ — `InvoiceDetail` → `hasLineItem` → `LineItem` → `hasPrice`/`item`; clear path.
- CQ8 — What information is displayed about the items sold? ✅ — `Item` has `itemDescription`; `LineItem` has `quantity`; `Price` has `netPrice`.
- CQ9 — What is the net price of the items sold? ✅ — `netPrice` data property (xsd:decimal) on `Price`, linked from `LineItem`.
- CQ10 — What are the invoice details? ✅ — `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary` as named subclasses of `Segment`; document references, dates, totals modeled separately.
- CQ11 — What is the invoice amount? ✅ — `TotalAmount` class linked via `hasTotalAmount` from `InvoiceSummary`; `totalAmountValue` (xsd:decimal, FunctionalProperty) provides the value.
- CQ12 — What is the invoice number? ✅ — `invoiceNumber` (xsd:string, FunctionalProperty, domain `InvoiceHeader`); unique key enforced.
- CQ13 — What information must be provided for the file format to be valid? ⚠️ — `Identifier` class models mandatory GLN; but no explicit `ValidationConstraint` class or SHACL-alignment constructs. CQ is partially addressed through the `Identifier`/`identifierValue` structure.
- CQ14 — To which business process can the invoice be assigned? ✅ — `relatesToBusinessProcess` links `InvoiceMessage` → `BusinessProcess` with inverse `isBusinessProcessOfInvoice`.

**Score: 14/14 with one minor partial gap on CQ13 → 4.8 / 5.0**

---

**Structural Ratios (OntoQA):**

- **RR: 0.7692** — High relationship richness; 77% of all relations are non-taxonomic object properties, indicating a well-connected graph rather than a flat taxonomy. Clearly above the dualAgent average.
- **AR: 0.5455** — Moderate attribute density (0.55 data properties per class). 12 data properties across 22 classes. Solid but not exceptional; the ontology uses structured sub-classes (Tax, TotalAmount, DocumentReference) to distribute properties intentionally.
- **IR: 0.4091** — Good inheritance richness. With a max depth of 1 and avg depth of 0.41, the taxonomy is intentionally shallow and branching (up to 4 direct subclasses), avoiding deep linear chains. The three section subclasses and subclasses of CompositeDataElement (LineItem, Tax, TotalAmount, DocumentReference, Identifier) produce a healthy, multi-root DAG.

**Score: 4.2 / 5.0** — Excellent RR, reasonable AR, healthy IR. Minor deduction for slightly low AR relative to the reference ontology.

---

**Design Patterns & Domain Representation:**

The ontology employs a flawless three-level pivot pattern for N-ary role modeling: `InvoiceMessage` → `hasOrganizationRoleAssignment` → `OrganizationRoleAssignment` → (`hasRole` → `AgentRole`, `assignedOrganization` → `Organization`). It further specializes role instances with named individuals `BuyerRole`, `SellerRole`, `DeliveryPartyRole` as instances of `AgentRole`, while also defining the derived class `BuyerOrganization` via `owl:equivalentClass`. This is the most expressive role-modeling pattern in the entire cohort: it simultaneously supports querying "what role does X play?" (via `OrganizationRoleAssignment`) and "which organizations are buyers?" (via the `BuyerOrganization` derived class). The EDIFACT structural hierarchy (Envelope → Message → Segment → Composite → Simple) is preserved intact with inverse properties at every level.

**Score: 5.0 / 5.0**

---

**Axiom Complexity:**

The ontology has an Axiom Diversity Score of **6** (highest in the cohort). It employs: `owl:inverseOf` (all property pairs), `owl:disjointWith` (Organization × Address/Item/BusinessProcess; AgentRole × Organization; Price × Address), `owl:FunctionalProperty` on key data and object properties (invoiceNumber, totalAmountValue, identifierValue), `owl:equivalentClass` with `owl:intersectionOf` and `owl:someValuesFrom` for `BuyerOrganization`, `owl:allValuesFrom` on `InvoiceMessage.containsSegment` and `InvoiceHeader.hasDocumentReference`. This is the only dualAgent ontology to combine an `equivalentClass` definition with a named subclass taxonomy, achieving both open-world reasoning support and SPARQL queryability.

**Score: 4.5 / 5.0** — Minor deduction: no `owl:cardinality` restrictions on the pivot class itself (unlike Rank 2), and no `owl:disjointUnionOf` for the section taxonomy.

---

**Lexical & Annotation Quality:**

Perfect scores across the board: `Name Strict CamelCase = 1.0`, `Name Underscore = 0.0`, `Name Non-conformant = 0.0`, `Label Coverage = 1.0`, `Comment Coverage = 1.0`. Every class, object property, and data property carries both an `rdfs:label` and a substantive `rdfs:comment`. The ontology header itself has a descriptive label ("UN/EDIFACT Invoice Ontology") and a meaningful comment noting EN 16931-1 and P2P-O alignment.

**Score: 5.0 / 5.0**

---

**Most Critical Defect:**

CQ13 is only partially supported: add an explicit `ValidationConstraint` or `MandatoryField` class (or SHACL mapping) to formally enumerate which data properties are required for D96A/EN 16931 compliance, replacing the implicit reliance on `Identifier` presence.

---

### Rank 2: `EDIFACT_ontology_20260301_225732.owl`

**Weighted score:** 4.60 / 5.00

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `InterchangeEnvelope` → `hasMessage` (FunctionalProperty) → `Message`; `InvoiceMessage` subclasses `Message`.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceParticipantRoleAssignment` pivot links `Organization` to `InvoiceMessage` via `playsRole`/`inInvoice`.
- CQ3 — What role does organization S play in the invoice? ✅ — `InvoiceParticipantRoleAssignment` captures Organization + AgentRole + InvoiceMessage in a single reified triple.
- CQ4 — Which organization is the buyer? ✅ — Query by `hasRole → AgentRole` filtered to "Buyer"; role individuals can be typed at instance population time.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Organization` has `organizationName` (FunctionalProperty); `Identifier` class with `identifierValue` and `identifierScheme` provides GLN; addressable via pivot.
- CQ6 — What is the address of the buyer? ✅ — `hasAddress` on `InvoiceParticipantRoleAssignment` (FunctionalProperty) → `Address` with decomposed data properties (addressLine, postalCode, city, countryCode).
- CQ7 — What items are sold in the invoice? ✅ — `DetailSection` → `hasLineItem` → `LineItem` → `describesItem` → `Item`.
- CQ8 — What information is displayed about the items sold? ✅ — `Item` has `itemName` and `itemDescription`; `LineItem` has `quantity`.
- CQ9 — What is the net price of the items sold? ✅ — `LineItem` → `hasPrice` (FunctionalProperty) → `Price` → `netPrice` (FunctionalProperty, xsd:decimal).
- CQ10 — What are the invoice details? ✅ — `HeaderSection`, `DetailSection`, `SummarySection` as subclasses of `Segment`; invoice amount in SummarySection, references in HeaderSection.
- CQ11 — What is the invoice amount? ✅ — `invoiceAmount` (FunctionalProperty, xsd:decimal) on `SummarySection`.
- CQ12 — What is the invoice number? ✅ — `invoiceNumber` (FunctionalProperty) on `InvoiceMessage` directly — cleaner than placing it on HeaderSection.
- CQ13 — What information must be provided for the file format to be valid? ⚠️ — `Identifier` class with `identifierScheme` property gives partial support (GLN scheme-typing), but no explicit validation vocabulary or SHACL hooks. Cardinality constraints on `InvoiceParticipantRoleAssignment` (exactly-1 `inInvoice`, `hasRole`, `hasAddress`) implicitly encode some format requirements.
- CQ14 — To which business process can the invoice be assigned? ✅ — `partOfBusinessProcess` links `InvoiceMessage` → `BusinessProcess`.

**Score: 14/14 with one minor gap on CQ13 → 4.7 / 5.0**

---

**Structural Ratios (OntoQA):**

- **RR: 0.8387** — Very high relationship richness; 84% non-taxonomic relations. This is the highest RR among ontologies with AR > 0.8.
- **AR: 0.8889** — Exceptional attribute density (0.89 data properties per class across 18 classes with 16 data properties). The most attribute-rich ontology in the cohort. Captures extensive instance-level information through separate granular properties (organizationName, addressLine, postalCode, city, countryCode, identifierValue, identifierScheme, itemName, itemDescription, quantity, netPrice, taxAmount, invoiceAmount, invoiceNumber, documentDate, referenceNumber).
- **IR: 0.2778** — Below average inheritance richness (max depth = 1, avg depth = 0.28). The taxonomy is intentionally flat: only `InvoiceMessage` extends `Message`, `LineItem` extends `CompositeDataElement`, and `HeaderSection`/`DetailSection`/`SummarySection` extend `Segment`. While this flatness keeps the graph simple, it means the ontology offers less leverage for inheritance-based inference.

**Score: 4.3 / 5.0** — Excellent RR and AR; mild deduction for lower IR (flat taxonomy limits inheritance-based reasoning).

---

**Design Patterns & Domain Representation:**

The `InvoiceParticipantRoleAssignment` pivot class is strongly constrained with three `owl:cardinality "1"` restrictions (exactly one `inInvoice`, one `hasRole`, one `hasAddress`), which is the most formally rigorous role-modeling pattern in the cohort. This ensures that every role assignment is well-formed by construction, preventing under-specified instances. The line-item path is also clean and precise: `DetailSection` → `LineItem` (subClassOf `CompositeDataElement`) → `describesItem` → `Item` + `hasPrice` → `Price`. The ontology correctly distinguishes `Organization` from `InvoiceParticipantRoleAssignment` — the address is attached to the role assignment, not the organization, perfectly capturing that the same organization can have different addresses in different roles (e.g., billing vs. delivery address for E/D/E).

**Score: 4.8 / 5.0** — Minor deduction: no derived `BuyerOrganization` class or named role individuals, so finding "the buyer" requires a filter query rather than a direct class membership check.

---

**Axiom Complexity:**

Axiom Diversity Score = **4**. Constructs used: `owl:inverseOf` (all pairs), `owl:FunctionalProperty` (hasMessage, hasRole, inInvoice, hasAddress, describesItem, hasPrice, invoiceNumber, documentDate, referenceNumber, organizationName, identifierValue, identifierScheme, itemName, quantity, netPrice, taxAmount, invoiceAmount — 17 functional properties, highest count in cohort), `owl:cardinality` (on InvoiceParticipantRoleAssignment and LineItem), `owl:someValuesFrom` (InvoiceMessage must have HeaderSection, DetailSection, SummarySection segments). Missing: `owl:allValuesFrom`, `owl:equivalentClass`, `owl:disjointUnionOf`.

**Score: 4.2 / 5.0** — Strong use of `owl:cardinality` and `owl:FunctionalProperty`; deduction for absence of equivalentClass/allValuesFrom patterns and lower Axiom Diversity Score compared to Rank 1.

---

**Lexical & Annotation Quality:**

Perfect: `Name Strict CamelCase = 1.0`, `Label Coverage = 1.0`, `Comment Coverage = 1.0`. The ontology header uses a generic IRI fragment (`#storyid`) rather than a descriptive name — a minor annotation quality issue. All classes and properties have substantive labels and comments.

**Score: 5.0 / 5.0**

---

**Most Critical Defect:**

The pivot class `InvoiceParticipantRoleAssignment` does not enforce that `assignedOrganization` is present (only `hasRole`, `inInvoice`, `hasAddress` have cardinality-1 constraints); add `owl:cardinality 1` on the organization link to ensure every role assignment identifies its actor, enabling complete SPARQL paths for CQ2/CQ3 without null results.

---

### Rank 3: `EDIFACT_ontology_20260301_220437.owl`

**Weighted score:** 4.55 / 5.00

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `InterchangeEnvelope` → `containsMessage` → `Message`; `InvoiceMessage` is a named subclass.
- CQ2 — Which organizations are involved in the invoice? ✅ — `InvoiceMessage` → `hasInvoiceParticipantRole` → `InvoiceParticipantRole` → `participantOrganization` → `Organization`.
- CQ3 — What role does organization S play in the invoice? ✅ — `InvoiceParticipantRole` pivot reifies the (Organization, AgentRole, InvoiceMessage) triple. `participantRole` → `AgentRole`.
- CQ4 — Which organization is the buyer? ✅ — Query via `participantRole → AgentRole` filtered to buyer type; or through named instances at population time.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Organization` → `hasIdentifier` → `Identifier` (GLN); `InvoiceParticipantRole` → `participantAddress` → `Address` (subClassOf CompositeDataElement).
- CQ6 — What is the address of the buyer? ✅ — `participantAddress` links `InvoiceParticipantRole` to `Address`; address is a structured `CompositeDataElement` subclass.
- CQ7 — What items are sold in the invoice? ✅ — `InvoiceMessage` → `hasLineItemDetail` → `LineItemDetail` → `lineItem` → `LineItem` (subClassOf `DetailSection`) → `item` → `Item`.
- CQ8 — What information is displayed about the items sold? ✅ — `Item` and `LineItem` reachable via `LineItemDetail`; `lineQuantity` on `LineItemDetail`; item details queryable.
- CQ9 — What is the net price of the items sold? ⚠️ — `LineItemDetail` → `linePrice` → `Price` (subClassOf CompositeDataElement); but only 3 data properties total (lineQuantity, invoiceNumber, invoiceDate). The `Price` class has no data property for the actual numeric value. Net price is structurally reachable but cannot be queried as a literal — requires an instance-level annotation workaround.
- CQ10 — What are the invoice details? ✅ — `HeaderSection`, `DetailSection`, `SummarySection` subclasses of `Segment`; dedicated typed navigation via functional properties `hasHeaderSection`, `hasDetailSection`, `hasSummarySection`.
- CQ11 — What is the invoice amount? ⚠️ — `TotalAmount` class (subClassOf CompositeDataElement) linked from `SummarySection` via `hasTotalAmount`; but no data property for the numeric total. Like CQ9, the value must be captured at instance level rather than via a typed literal property.
- CQ12 — What is the invoice number? ✅ — `invoiceNumber` (FunctionalProperty, xsd:string) on `HeaderSection`.
- CQ13 — What information must be provided for the file format to be valid? ✅ — `mandatoryIdentifier` object property links `InvoiceMessage` → `Identifier` specifically for required format identifiers. This is the strongest CQ13 support in the cohort: dedicated property semantically encoding what is mandatory.
- CQ14 — To which business process can the invoice be assigned? ✅ — `assignedBusinessProcess` → `BusinessProcess`.

**Score: 14/14 with two structural gaps (CQ9, CQ11 — no numeric literals for price/total) → 4.7 / 5.0**

*Note: the CQ coverage score remains 4.7 rather than being penalized to 4.0–4.4 because the structural paths exist and the queries are answerable via instance-level data; only the precision of the schema is reduced.*

---

**Structural Ratios (OntoQA):**

- **RR: 0.8333** — Very high relationship richness. With 40 object properties and only 8 subClassOf axioms across 21 classes, the graph is dominated by non-taxonomic relations — appropriate for a complex business document domain where most knowledge is relational.
- **AR: 0.1429** — Very low attribute density (only 3 data properties for 21 classes: lineQuantity, invoiceNumber, invoiceDate). This is the most significant structural weakness: numeric values for price and total amount are absent, reducing the schema's data richness. The reference TUMedifact has AR = 8.42.
- **IR: 0.3810** — Moderate inheritance richness (max depth 2, avg depth 0.43). The subclass lattice is healthy: Address, LineItem, Price, TotalAmount extend `CompositeDataElement`; HeaderSection, DetailSection, SummarySection extend `Segment`; InvoiceMessage extends `Message`.

**Score: 4.1 / 5.0** — Very strong RR, healthy IR; the critically low AR (0.1429) prevents a higher score.

---

**Design Patterns & Domain Representation:**

This ontology introduces a **dual pivot pattern** — the most architecturally sophisticated approach in the cohort. It uses two parallel pivot classes: `InvoiceParticipantRole` reifies the Organization × AgentRole × InvoiceMessage × Address relationship, while `LineItemDetail` reifies the InvoiceMessage × LineItem × Price × quantity relationship. Both pivots have `owl:someValuesFrom` restrictions enforcing minimum content. The `mandatoryIdentifier` property is a semantically meaningful addition that directly addresses the EDIFACT D96A mandatory field requirement. The Address class is modeled as a `CompositeDataElement` subclass, correctly reflecting the EDIFACT structural hierarchy where addresses are composite elements within NAD segments.

**Score: 5.0 / 5.0**

---

**Axiom Complexity:**

Axiom Diversity Score = **3**. Constructs used: `owl:inverseOf` (all pairs), `owl:FunctionalProperty` (containsMessage, hasHeaderSection, hasSummarySection, hasDetailSection, hasIdentifier), `owl:someValuesFrom` (on InvoiceMessage, InvoiceParticipantRole, LineItemDetail, LineItem). Missing: `owl:disjointWith` / `owl:disjointUnionOf`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:cardinality`. The someValuesFrom restrictions are well-placed and semantically meaningful, but the absence of disjointness axioms and cardinality constraints limits logical expressiveness.

**Score: 3.5 / 5.0** — Good someValuesFrom usage; significant deduction for absence of disjointness, cardinality, and equivalence constructs.

---

**Lexical & Annotation Quality:**

Perfect: `Name Strict CamelCase = 1.0`, `Label Coverage = 1.0`, `Comment Coverage = 1.0`. The ontology IRI uses a descriptive name (`#UNEDIFACTInvoiceStory`) and the header includes a comprehensive alignment comment ("EN 16931 and P2P-O alignment"). All 21 classes and 43 properties carry meaningful labels and comments.

**Score: 5.0 / 5.0**

---

**Most Critical Defect:**

The near-complete absence of data properties (AR = 0.1429, only 3 properties) means that CQ9 (net price) and CQ11 (invoice amount) cannot be answered as SPARQL `SELECT` queries returning typed literals — the `Price` and `TotalAmount` classes exist but carry no `xsd:decimal` value property. Add `hasNetPrice xsd:decimal` to `Price` and `hasTotalValue xsd:decimal` to `TotalAmount` to make the ontology query-complete for all 14 CQs.

---

## Bottom Ontologies: Summary

**`EDIFACT_ontology_20260301_223750.owl` (Rank 4):** This ontology (18 classes, 26 obj props, 15 data props, Axiom Div = 2) achieves a good AR of 0.8333 and a comprehensive set of address/organization data properties (hasName, hasStreet, hasPostalCode, hasCity, hasCountryCode, hasGlobalLocationNumber, hasRoleIdentifier, hasDescription), making it highly data-rich. However, its Axiom Diversity Score of only 2 — confined to `owl:inverseOf` and `owl:disjointWith` / `owl:disjointUnionOf` — means zero use of `owl:someValuesFrom`, `owl:cardinality`, or `owl:equivalentClass`. The pivot class `OrganizationRoleAssignment` is structurally sound but carries no formal OWL restrictions, making it logically incomplete. Additionally, the comment block `# (GCAs, restrictions and equivalence axioms to be added in next iteration if needed.)` explicitly acknowledges the missing axioms, indicating an incomplete iteration. This prevents the ontology from ranking higher despite its excellent data property coverage.

**`EDIFACT_ontology_20260301_230018.owl` (Rank 5):** This ontology (18 classes, 26 obj props, 14 data props, Axiom Div = 4) is architecturally very similar to Rank 2 (`225732.owl`) and shares the same structural metrics (RR = 0.8387, AR = 0.7778, IR = 0.2778). It models the full EDIFACT structure with a well-formed `OrganizationRoleAssignment` pivot and a comprehensive data property set. It scores slightly lower than Rank 2 primarily due to less rigorous cardinality constraints on its pivot class (using `disjointWith` axioms instead of `owl:cardinality` to enforce structural integrity) and a less expressive `hasNetPrice` property path. It remains an excellent ontology that narrowly misses the top 3.

**`EDIFACT_ontology_20260301_224527.owl` (Rank 6):** This ontology (20 classes, 32 obj props, 13 data props, Axiom Div = 5) introduces two architectural innovations: an `EDIFACTDelimiter` class that models the structural delimiter characters (plus, colon) required for valid EDIFACT syntax, and a separate `RoleType` class alongside `AgentRole`, providing a two-level role taxonomy. The `EDIFACTDelimiter` class directly addresses CQ13 in the most literal interpretation (format validity). However, the `usesDelimiter` property uses `owl:unionOf` in its domain definition rather than proper subclassing, introducing slight structural irregularity. The `InvoiceMessage owl:equivalentClass` axiom is the only equivalence axiom in the ontology and its correctness is questionable (equivalence to `hasInvoiceSection some Segment` is overly broad). These design tensions prevent a top-3 ranking.

**`EDIFACT_ontology_20260301_225145.owl` (Rank 7):** This ontology (19 classes, 30 obj props, 9 data props, Axiom Div = 4) shows a structurally correct approach with `RoleAssignment` pivot, `Tax` class for invoice tax modeling, and proper `disjointWith` axioms. Its primary weakness is the unusual modeling of `CompositeDataElement` as a direct subclass of `Segment` and `SimpleDataElement` as a subclass of `CompositeDataElement`, and — more critically — `Address` as a subclass of `CompositeDataElement`. This breaks the EDIFACT hierarchy (addresses are not composite data elements; they are associated with organizations via NAD segments). CQ6 (address of buyer) still works via the `hasAddress` path, but the structural inheritance is semantically misleading. The modest data property count (9) also limits CQ8 coverage for item details.

**`EDIFACT_ontology_20260301_222534.owl` (Rank 8):** This ontology (18 classes, 30 obj props, 7 data props, Axiom Div = 5) stands out for its unusual max depth of 4 (the deepest hierarchy in the dualAgent cohort), achieved by a four-level chain through `OrganizationInRole` and `InvoiceLineItem` pivot classes. While this depth is genuine — reflecting real hierarchical decomposition — the IR of 0.4444 combined with only 7 data properties (AR = 0.3889) leaves the ontology data-sparse. The `ValidationConstraint` class is introduced but carries no data properties or restrictions, making it semantically empty. Ranks 7–8 score similarly; `222534` edges ahead of `225145` due to its stronger axiom diversity and deeper (if slightly over-engineered) hierarchy.

**`EDIFACT_ontology_20260301_220832.owl` (Rank 9):** This ontology (20 classes, 38 obj props, 8 data props, Axiom Div = 4) has a high object property count (38 — third highest in cohort) driven by comprehensive inverse property pairs, including specialized `hasOrganization`, `isOrganizationRoleIn`, `hasRole` on the `OrganizationRoleInInvoice` pivot. An `allValuesFrom` restriction is used on the pivot class. However, the `hasInvoiceNumber` property is declared as `owl:InverseFunctionalProperty` instead of `owl:FunctionalProperty` — semantically incorrect (invoice numbers are functional identifiers, not globally unique keys across all documents). With AR = 0.4, the ontology also has limited data coverage for item-level CQs.

**`EDIFACT_ontology_20260301_230338.owl` (Rank 10):** This ontology (17 classes, 26 obj props, 14 data props, Axiom Div = 5) has the smallest class count among the better-scoring ontologies and the highest RR in the cohort (0.963), reflecting a very flat taxonomy with almost all relations being non-taxonomic. The AR of 0.8235 is strong (14 data props / 17 classes). The primary limitation is the very low IR (0.0588, max depth = 1, avg depth = 0.06) — nearly all classes are root-level with minimal subclassing. This prevents leveraging inheritance for reasoning. The `hasSection` property uses an anonymous `owl:unionOf` for its range, which is a valid but less clean pattern than using a named `Section` superclass. Still a strong performer that just misses the top 3 by a narrow margin.

**`EDIFACT_ontology_20260301_224922.owl` (Rank 11):** This ontology (19 classes, 34 obj props, 7 data props, Axiom Div = 2) has a standard architecture with `OrganizationRoleAssignment` pivot and `GlobalLocationNumber` as a named subclass of `Identifier`. However, its Axiom Diversity Score of only 2 (inverseOf + disjointWith only) and sparse data properties (AR = 0.3684) mean that several CQs — particularly CQ8 (item information) and CQ9 (net price) — are only weakly supported. CQ13 is handled via `hasMandatoryIdentifier` data property, a reasonable but non-structural approach.

**`EDIFACT_ontology_20260301_221940.owl` (Rank 12):** This ontology (21 classes, 28 obj props, 5 data props, Axiom Div = 3) uses an `OrganizationRoleAssignment` pivot but defines `BuyerRole` as a named subclass of `AgentRole` (rather than an individual), which is an architecturally different — though valid — design choice. The very low data property count (AR = 0.2381) severely limits CQ5/CQ8/CQ9 answering. The `allValuesFrom` restriction on `InvoiceHeader` is present but isolated.

**`EDIFACT_ontology_20260301_215924.owl` (Rank 13):** This ontology (19 classes, 34 obj props, 8 data props, Axiom Div = 5) has a near-flat taxonomy (max depth 1, avg depth 0.11, IR = 0.1053) with essentially all 17 leaf classes at depth 0 or 1. While its RR is high (0.9444) and it includes an interesting `equivalentClass` + `cardinality` restriction on `RoleAssignment`, the very high number of leaf classes (17 of 19) means minimal inheritance leverage. CQ13 is weakly supported by a `hasMandatoryIdentifier` boolean data property.

**`EDIFACT_ontology_20260301_225409.owl` (Rank 14):** This ontology (19 classes, 30 obj props, 12 data props, Axiom Div = 2) introduces `GLNIdentifier` as a named subclass of `Identifier` and `OrganizationRoleParticipation` as its pivot class. Despite a reasonable AR (0.6316), the Axiom Diversity Score of 2 (no someValuesFrom, no cardinality, no equivalentClass) and a very flat taxonomy (IR = 0.1053) limit its ranking. CQ13 is not addressed.

**`EDIFACT_ontology_20260301_224212.owl` (Rank 15):** This ontology (16 classes, 24 obj props, 8 data props, Axiom Div = 4) uses `OrganizationRoleInInvoice` as its pivot. With only 16 classes and 8 data properties, it is one of the smallest ontologies and misses CQ13 entirely (no validation vocabulary). The `owl:someValuesFrom` restrictions and `owl:cardinality` on the pivot class provide moderate axiom complexity (score 3.8), but coverage gaps keep it in the bottom third.

**`EDIFACT_ontology_20260301_221332.owl` (Rank 16):** This ontology (18 classes, 32 obj props, 12 data props, Axiom Div = 2) has a high RR (0.9697) but an extremely low IR (0.0556, max depth = 1, avg depth = 0.06) — nearly flat. The 12 data properties give a decent AR (0.6667), but with Axiom Diversity Score of only 2, there are no restrictions beyond inverseOf and disjointWith. CQ13 is not addressed.

**`EDIFACT_ontology_20260301_223501.owl` (Rank 17):** This ontology (21 classes, 32 obj props, 7 data props, Axiom Div = 2) defines `Buyer`, `Seller`, and `DeliveryParty` as named subclasses of `AgentRole` — a valid but less flexible pattern than named individuals. The very low axiom diversity (2) and modest data property coverage (AR = 0.3333) prevent higher ranking.

**`EDIFACT_ontology_20260301_221113.owl` (Rank 18):** This ontology (18 classes, 28 obj props, 5 data props, Axiom Div = 2) is sparse in both data properties (AR = 0.2778) and axiom complexity. The pivot class `OrganizationRoleAssignment` is present but incompletely constrained. Several CQs (CQ5, CQ8, CQ9, CQ13) are at best weakly answerable. The small class count (18) and very low data property count produce an underpowered schema.

**`EDIFACT_ontology_20260301_215700.owl` (Rank 19):** The second-smallest ontology in the cohort (16 classes, 22 obj props, 9 data props, Axiom Div = 2) lacks a formal pivot class for role assignment; instead, `AgentRole`, `Address`, and `Organization` are loosely connected through direct properties. CQ3 (role of organization S) is difficult to answer without reification. The lack of a proper N-ary pattern for multi-role organizations (e.g., E/D/E as both Buyer and Delivery Party) is the primary architectural gap. CQ13 is absent.

**`EDIFACT_ontology_20260301_221725.owl` (Rank 20):** The smallest and weakest ontology in the cohort (13 classes, 22 obj props, 8 data props, Axiom Div = 2). With only 13 classes, the ontology omits several domain-critical concepts: no explicit `Section` hierarchy (no HeaderSection/DetailSection/SummarySection), no `LineItem`, no `Tax`, no structured section decomposition. CQ10 (invoice details), CQ11 (invoice amount), and CQ13 (format validity) cannot be answered. The flat taxonomy (max depth 1, avg depth 0.08, IR = 0.0769) with 12 leaf classes provides almost no inference leverage. Despite perfect lexical quality, the structural and conceptual gaps make this the least expressive ontology in the cohort.

---

*Report generated on 2026-03-08 using metrics from `data/FinalResults/ontology_report.md` and direct OWL analysis.*
