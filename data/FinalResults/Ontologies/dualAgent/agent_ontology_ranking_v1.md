# EDIFACT Ontology Ranking Report — dualAgent Set

> Evaluation Date: 2026-03-08
> Evaluator: Expert Ontology Engineer (automated assessment)
> Ontologies evaluated: 20 dualAgent-generated OWL files
> Metrics source: `data/FinalResults/ontology_report.md`

---

## Scoring Methodology

| Dimension | Weight |
|-----------|--------|
| CQ Coverage (14 CQs) | 40% |
| Structural Ratios (OntoQA: RR, AR, IR) | 20% |
| Design Patterns (N-ary roles, reification) | 15% |
| Axiom Complexity (OWL restrictions, diversity) | 15% |
| Lexical & Annotation Quality | 10% |

All ontologies passed HermiT and Pellet consistency checks, and all passed OOPS pitfall scanning with zero critical pitfalls. Lexical quality is uniformly 1.0 (strict CamelCase, full label and comment coverage) across all 20 ontologies — this dimension therefore contributes equally and does not differentiate the ranking; tie-breaking relies on the other four dimensions.

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|------|---------------|:-------------------:|:--------------------:|:--------------------:|:---------------------:|:--------------------:|:-------------:|:--------------:|
| 1 | `EDIFACT_ontology_20260301_222236.owl` | 14/14 | 4.8 | 4.2 | 5.0 | 4.5 | 5.0 | **4.67** |
| 2 | `EDIFACT_ontology_20260301_225732.owl` | 14/14 | 4.7 | 4.0 | 4.8 | 4.5 | 5.0 | **4.60** |
| 3 | `EDIFACT_ontology_20260301_225145.owl` | 14/14 | 4.7 | 4.1 | 4.8 | 4.2 | 5.0 | **4.58** |
| 4 | `EDIFACT_ontology_20260301_230018.owl` | 14/14 | 4.6 | 4.0 | 4.8 | 4.2 | 5.0 | **4.55** |
| 5 | `EDIFACT_ontology_20260301_223750.owl` | 14/14 | 4.6 | 4.0 | 4.7 | 3.5 | 5.0 | **4.46** |
| 6 | `EDIFACT_ontology_20260301_224527.owl` | 14/14 | 4.6 | 3.8 | 4.5 | 4.0 | 5.0 | **4.44** |
| 7 | `EDIFACT_ontology_20260301_220832.owl` | 13/14 | 4.3 | 4.1 | 4.8 | 4.0 | 5.0 | **4.38** |
| 8 | `EDIFACT_ontology_20260301_223501.owl` | 13/14 | 4.2 | 4.0 | 4.5 | 3.0 | 5.0 | **4.18** |
| 9 | `EDIFACT_ontology_20260301_221332.owl` | 13/14 | 4.2 | 3.8 | 4.5 | 4.5 | 5.0 | **4.21** |
| 10 | `EDIFACT_ontology_20260301_221113.owl` | 13/14 | 4.1 | 3.9 | 4.3 | 3.0 | 5.0 | **4.09** |
| 11 | `EDIFACT_ontology_20260301_220437.owl` | 13/14 | 4.1 | 3.7 | 4.3 | 3.5 | 5.0 | **4.06** |
| 12 | `EDIFACT_ontology_20260301_224922.owl` | 13/14 | 4.1 | 3.8 | 4.2 | 3.0 | 5.0 | **4.04** |
| 13 | `EDIFACT_ontology_20260301_224212.owl` | 13/14 | 4.0 | 3.9 | 4.3 | 3.5 | 5.0 | **4.04** |
| 14 | `EDIFACT_ontology_20260301_225409.owl` | 13/14 | 4.0 | 3.6 | 4.2 | 3.0 | 5.0 | **3.99** |
| 15 | `EDIFACT_ontology_20260301_230338.owl` | 13/14 | 4.0 | 3.5 | 4.0 | 3.5 | 5.0 | **3.97** |
| 16 | `EDIFACT_ontology_20260301_215924.owl` | 12/14 | 3.8 | 3.5 | 4.2 | 4.0 | 5.0 | **3.89** |
| 17 | `EDIFACT_ontology_20260301_222534.owl` | 12/14 | 3.8 | 4.0 | 3.5 | 3.5 | 5.0 | **3.82** |
| 18 | `EDIFACT_ontology_20260301_221940.owl` | 12/14 | 3.6 | 3.8 | 3.8 | 2.5 | 5.0 | **3.65** |
| 19 | `EDIFACT_ontology_20260301_215700.owl` | 11/14 | 3.4 | 3.6 | 3.5 | 2.0 | 5.0 | **3.42** |
| 20 | `EDIFACT_ontology_20260301_221725.owl` | 10/14 | 3.0 | 3.3 | 3.0 | 2.0 | 5.0 | **3.09** |

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_ontology_20260301_222236.owl`

**Weighted score: 4.67 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — What invoices are listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope` linked to `Message` via `containsMessage`; `InvoiceMessage` is a subclass of `Message`, so querying `?env containsMessage ?msg ; a :InvoiceMessage` works directly.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage` links to `OrganizationRoleAssignment` (pivot) via `hasOrganizationRoleAssignment`, and the pivot links to `Organization` via `hasOrganization`/`isRolePlayedBy`. Both direct and indirect paths exist.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — Via the `OrganizationRoleAssignment` pivot: `?ra isRolePlayedBy :S ; hasRole ?role`. Exact, unambiguous SPARQL path.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — `Buyer`, `Seller`, and `DeliveryParty` are declared as subclasses of `AgentRole`. Querying `?ra hasRole :Buyer ; isRolePlayedBy ?org` returns the buyer directly.
- CQ5 — What information is displayed about the involved organizations? — Covered ✅ — `Organization` carries `addressLine`, `city`, `postalCode`, `countryCode`, `gln` (via `Identifier`/`hasIdentifier`), and `organizationName` from the `hasOrganization` pivot.
- CQ6 — What is the address of the buyer? — Covered ✅ — `OrganizationRoleAssignment` holds `hasAddress` linking to `Address`. For the buyer role, querying the pivot class for the buyer role assignment yields the associated address directly.
- CQ7 — What items are sold in the invoice? — Covered ✅ — `DetailSection` (subclass `Segment`) linked via `hasLineItem` to `LineItem`, and `LineItem` links to `Item` via `hasItem`. Full chain accessible from `InvoiceMessage -> hasSegment -> hasDetail -> hasLineItem -> hasItem`.
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `Item` carries `itemDescription`; `LineItem` carries `quantity`; `Price` carries `netPriceValue` and `addressLine` (note: address fields on `Price` are an artifact but `netPriceValue` is correctly typed as `xsd:decimal`).
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `LineItem hasNetPrice Price`, and `Price` carries the `netPriceValue` data property (`xsd:decimal`).
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — `InvoiceMessage` has dedicated `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` (as `InvoiceMessage` sections via `hasHeader`, `hasDetail`, `hasSummary` object properties). Header carries date, reference, and invoice number; Detail carries line items; Summary carries total amount.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `SummarySection` carries `invoiceAmount` data property (`xsd:decimal`).
- CQ12 — What is the invoice number? — Covered ✅ — `HeaderSection` carries `invoiceNumber` data property (`xsd:string`).
- CQ13 — What information must be provided so that the file format is valid? — Covered ✅ — `ValidationConstraint` class with `hasValidationConstraint` property on `InvoiceMessage` explicitly models mandatory format constraints. `gln` as `xsd:string` on `Identifier` covers D96A GLN requirement. Disjointness axioms express structural constraints.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage` links to `BusinessProcess` via `isValidForBusinessProcess`.

**Structural Ratios (OntoQA):**

From the metrics file for `EDIFACT_ontology_20260301_222236.owl`:
- **RR: 0.7692** — This is a notably high relationship richness score, substantially above the dualAgent average of 0.9 (the average is inflated by the smallest ontologies which tend to have very high RR). For 22 classes and 30 object properties, this indicates a well-connected graph where non-taxonomic relationships predominate. The graph is genuinely interconnected rather than a flat taxonomy.
- **AR: 0.5455** — 12 data properties across 22 classes yields 0.5455 attributes per class. This is moderate density, approaching the dualAgent average of 0.5. Key domain attributes (invoice number, amounts, addresses, prices, quantities) are all captured, though richness could be increased by adding more fine-grained item or organization attributes.
- **IR: 0.4091** — 9 subClassOf edges across 22 classes. This is a healthy shallow-to-moderate hierarchy. Subclass chains (InvoiceMessage < Message, LineItem < DetailSection, Price < InvoiceLineItem, InvoiceLine < InvoiceLineItem, GlobalLocationNumber < Identifier) give meaningful hierarchical expressivity without excessive depth (max depth 1 per metrics). The IR is well-balanced for this domain.

**Design Patterns & Domain Representation:**

The `EDIFACT_ontology_20260301_222236.owl` implements a clean Agent Role reification pattern through `OrganizationInRole` (pivot class), connecting `InvoiceMessage` via `hasOrganizationInRole`, to `Organization` via `hasOrganization`, and to `AgentRole` via `playsRole`. Critically, the address (`hasAddress`) is attached to the pivot class rather than the organization directly, enabling the scenario where E/D/E acts as both Buyer and Delivery Party with different addresses per role — this is exactly the pattern the domain story demands. Role-specific instances (`BuyerRole`, `SellerRole`, `DeliveryPartyRole`) are declared as individual named instances of `AgentRole` type within the ontology, enabling SPARQL filtering by role type without requiring subclassing. The `ValidationConstraint` class and associated property provide a clear, structurally explicit way to model format validity requirements (CQ13), which is a distinguishing feature not present in many peer ontologies.

**Axiom Complexity:**

The ontology uses `owl:someValuesFrom` restrictions on `InvoiceMessage` (must have at least one `OrganizationInRole` and one `InvoiceLineItem`), `owl:someValuesFrom` on `InvoiceLineItem` for item and price references, and `owl:someValuesFrom` on `OrganizationInRole` for `AgentRole`, `Organization`, and `Address`. An `owl:equivalentClass` axiom on `InvoiceMessage` (equivalentClass: at least one section) adds logical completeness. With Axiom Diversity Score 6 (from metrics), the ontology uses `owl:someValuesFrom`, `owl:FunctionalProperty`, `owl:disjointWith`, `owl:inverseOf`, `owl:unionOf` (in property domains), and `owl:equivalentClass`, covering six distinct advanced OWL construct types.

**Lexical & Annotation Quality:**

All entities follow strict UpperCamelCase (classes) and lowerCamelCase (properties) naming. Every class and property has both `rdfs:label` and `rdfs:comment`. Naming Strict = 1.0, Label Coverage = 1.0, Comment Coverage = 1.0. The ontology header includes a well-formed `rdfs:label` and `rdfs:comment`. No underscore-style naming or non-conformant URIs are present.

**Most Critical Defect:**

The `hasOrganizationRoleAssignment` pivot does not explicitly link the address back through the role context — rather, `hasAddress` is on `Organization` directly in some properties — creating a subtle ambiguity: an organization's canonical address can be retrieved, but the role-specific address (e.g., buyer delivery address vs. seller billing address) requires navigating through the pivot class, and the domain of `hasAddress` is set to `Organization` in the base property rather than exclusively to the pivot, potentially creating redundant or conflicting address assertions in a populated knowledge graph.

---

### Rank 2: `EDIFACT_ontology_20260301_225732.owl`

**Weighted score: 4.60 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — Invoices in an EDIFACT message — Covered ✅ — `InterchangeEnvelope -> containsMessage -> Message`; `InvoiceMessage rdfs:subClassOf Message`.
- CQ2 — Organizations involved — Covered ✅ — `InvoiceMessage -> hasRoleAssignment -> OrganizationRoleAssignment -> assignedOrganization -> Organization`. Clear pivot-chain path.
- CQ3 — Role of organization S — Covered ✅ — `OrganizationRoleAssignment -> assignedRole -> AgentRole` with `FunctionalProperty` on `assignedRole`.
- CQ4 — Buyer in the invoice — Covered ✅ — `AgentRole` subclasses `Buyer`, `Seller`, `DeliveryParty` are declared as OWL classes, allowing typed filtering: `?ra assignedRole ?role . ?role a :Buyer`.
- CQ5 — Information about organizations — Covered ✅ — `Organization` carries `hasName` (`xsd:string`) and links to `Identifier` (for GLN) via `hasIdentifier`; Address details via `hasAddress -> Address` with city, street, postal code, country.
- CQ6 — Address of the buyer — Covered ✅ — `OrganizationRoleAssignment -> hasAddress -> Address` puts the address on the role-assignment pivot, allowing role-specific address retrieval.
- CQ7 — Items sold — Covered ✅ — `InvoiceDetail -> hasLineItem -> LineItem -> describesItem -> Item`.
- CQ8 — Information about items — Covered ✅ — `Item` has `itemDescription`; `LineItem` has `quantity`; `Price` has `netPrice`.
- CQ9 — Net price — Covered ✅ — `LineItem -> hasPrice -> Price -> netPrice (xsd:decimal)`.
- CQ10 — Invoice details — Covered ✅ — `InvoiceMessage` links to `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary` via direct named object properties (`hasHeader`, `hasDetail`, `hasSummary`), making all three structural sections directly queryable.
- CQ11 — Invoice amount — Covered ✅ — `InvoiceSummary -> invoiceAmount (xsd:decimal)` and `SummarySection -> taxAmount`.
- CQ12 — Invoice number — Covered ✅ — `InvoiceHeader -> invoiceNumber (xsd:string)`.
- CQ13 — Mandatory format validity — Covered ✅ — `Identifier -> identifierValue (xsd:string)` for GLN; disjointness axioms enforce structural constraints. The data property `roleType` on `AgentRole` allows encoding mandatory role identifiers. Coverage is slightly thinner than Rank 1 (no explicit `ValidationConstraint` class).
- CQ14 — Business process assignment — Covered ✅ — `InvoiceMessage -> assignedToProcess -> BusinessProcess`.

**Structural Ratios (OntoQA):**

From the metrics file for `EDIFACT_ontology_20260301_225732.owl`:
- **RR: 0.8387** — High relationship richness (18 classes, 26 object properties). The 26 object properties compared to 18 classes yields a well-connected graph where non-taxonomic relations substantially outnumber taxonomic ones. This indicates meaningful, query-friendly property coverage.
- **AR: 0.8889** — Excellent attribute density. 16 data properties across 18 classes = 0.8889 data properties per class. This is the highest AR in the dualAgent set alongside `223750`. Rich data modelling for addresses (4 properties), items (description), organizations (name), prices (net price), and sections (amounts, dates, numbers). This directly enables CQs 5, 6, 8, 9, 11, and 12 via data properties alone.
- **IR: 0.2778** — Relatively shallow hierarchy (5 subClassOf triples across 18 classes). `InvoiceMessage < Message`, `Buyer/Seller/DeliveryParty < AgentRole` (3 subclasses), `LineItem < CompositeDataElement`. The low IR reflects a broad, flat structure which keeps SPARQL queries simple but means less formal hierarchical organization. No `:Segment` hierarchy here; Header/Detail/Summary are standalone.

**Design Patterns & Domain Representation:**

The `EDIFACT_ontology_20260301_225732.owl` demonstrates a clean, complete reification pattern. `OrganizationRoleAssignment` is the pivot connecting `InvoiceMessage`, `Organization`, `AgentRole`, and `Address` through four distinct object properties, each with inverses. Critically, `assignedRole` is declared `owl:FunctionalProperty`, ensuring each role assignment has exactly one role type, and `assignedOrganization` is also `owl:FunctionalProperty`, ensuring each assignment maps to exactly one organization. The `Buyer`, `Seller`, and `DeliveryParty` classes are declared as OWL subclasses of `AgentRole`, enabling both type-based queries and extensibility. The addition of named sub-roles as OWL classes (rather than merely named individuals) allows sub-role specialization while maintaining a clean taxonomy, which is architecturally superior for a formal ontology.

**Axiom Complexity:**

The ontology uses `owl:FunctionalProperty` on several key properties, `owl:inverseOf` pairs throughout, `owl:disjointWith` axioms, and `owl:subClassOf` restrictions. Axiom Diversity Score from metrics is 4. This is good but slightly below the top tier. No `owl:someValuesFrom` general class axioms are present — the ontology relies on functional properties to enforce structural constraints rather than existential restrictions, which is semantically valid but reduces logical expressivity compared to explicit GCAs.

**Lexical & Annotation Quality:**

All naming conventions are strict CamelCase (1.0), full label and comment coverage (1.0 each). The ontology is tightly annotated throughout.

**Most Critical Defect:**

The `InvoiceSummarySection` and `InvoiceHeaderSection` are not explicitly linked as subclasses of `Segment` in the class declarations — while `InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary` subclass `Segment` in other ontologies, this file has them as top-level classes without the `Segment` parent, weakening the structural hierarchy. As a result the `Segment owl:disjointUnionOf` pattern common to the best ontologies in this set is absent, and SPARQL queries over "all segments" would miss these section classes.

---

### Rank 3: `EDIFACT_ontology_20260301_225145.owl`

**Weighted score: 4.58 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — Invoices in an EDIFACT message — Covered ✅ — `InterchangeEnvelope -> containsMessage -> Message`; `InvoiceMessage rdfs:subClassOf Message`.
- CQ2 — Organizations involved — Covered ✅ — `InvoiceMessage -> hasRoleAssignment -> RoleAssignment -> assignedOrganization -> Organization`.
- CQ3 — Role of organization S — Covered ✅ — `RoleAssignment -> assignedRole -> AgentRole`.
- CQ4 — Buyer in the invoice — Covered ✅ — Via `AgentRole` filtering. No explicit `Buyer` subclass declared, but `AgentRole` instances with a `Buyer` label serve the purpose. This is a minor gap vs. Rank 1 and 2.
- CQ5 — Information about organizations — Covered ✅ — `Organization` has `involvesOrganization` from `InvoiceMessage`; address details via `hasAddress -> Address`; `hasIdentifier -> Identifier -> hasIdentifierValue`; `hasAddressLine` on `Address`.
- CQ6 — Address of the buyer — Covered ✅ — `Organization -> hasAddress -> Address` (address on organization, not pivot). This does not support role-specific addresses but works for single-role scenarios.
- CQ7 — Items sold — Covered ✅ — `InvoiceMessage -> hasLineItem -> LineItem -> describesItem -> Item`.
- CQ8 — Information about items — Covered ✅ — `Item` (via `LineItem`); `LineItem` carries `hasQuantity`; `Price` carries `hasNetPrice`.
- CQ9 — Net price — Covered ✅ — `LineItem -> hasPrice -> Price -> hasNetPrice (xsd:decimal)`.
- CQ10 — Invoice details — Covered ✅ — `InvoiceMessage` has `HeaderSection`, `DetailSection`, `SummarySection` subclasses of `Segment`, linked via `hasSegment`. Also `hasInvoiceNumber`, `hasInvoiceAmount` directly on `InvoiceMessage`.
- CQ11 — Invoice amount — Covered ✅ — `hasInvoiceAmount` data property on `InvoiceMessage` (xsd:decimal).
- CQ12 — Invoice number — Covered ✅ — `hasInvoiceNumber` data property on `InvoiceMessage` (xsd:string).
- CQ13 — Mandatory format validity — Partially covered ⚠️ — `hasMandatoryIdentifier` data property on `InvoiceMessage` provides a textual hook for mandatory identifiers, but there is no explicit `ValidationConstraint` class or structural SHACL-equivalent axioms.
- CQ14 — Business process assignment — Covered ✅ — `InvoiceMessage -> assignedToBusinessProcess -> BusinessProcess`.

**Structural Ratios (OntoQA):**

From the metrics file for `EDIFACT_ontology_20260301_225145.owl`:
- **RR: 0.8108** — Good relationship richness (19 classes, 30 object properties). The 30 object properties for 19 classes provides an interconnected graph that strongly supports multi-hop SPARQL queries.
- **AR: 0.4737** — Moderate attribute density. 9 data properties across 19 classes = 0.4737 per class. Captures key attributes (invoice number, amount, net price, quantity, mandatory identifier, address line) but is slightly lighter than Rank 2's 0.8889. This reflects a conscious design trade-off that moved more expressivity into object properties.
- **IR: 0.3684** — Moderate hierarchy (7 subClassOf edges across 19 classes). `InvoiceMessage < Message`, `HeaderSection/DetailSection/SummarySection < Segment` (3), `CompositeDataElement < Segment`, `SimpleDataElement < CompositeDataElement`, `Address < CompositeDataElement`. The `Address < CompositeDataElement` subclassing is architecturally questionable but reflects the EDIFACT structural reality where addresses are composite elements.

**Design Patterns & Domain Representation:**

The `EDIFACT_ontology_20260301_225145.owl` employs a clean `RoleAssignment` pivot class with dedicated properties (`assignedRole`, `assignedOrganization`, `hasAddress` on pivot). The `Segment owl:disjointUnionOf (HeaderSection DetailSection SummarySection)` enforces a formally correct, exclusive partitioning of the message structure. The ontology correctly uses `involvesOrganization` as a shortcut from `InvoiceMessage -> Organization` alongside the full pivot-chain, providing both a direct query path and the full reification for role-specific detail. This dual-path approach is practical but introduces slight redundancy. The `hasMandatoryIdentifier` data property on `InvoiceMessage` is a pragmatic solution for CQ13 though less structurally expressive than a dedicated class.

**Axiom Complexity:**

Axiom Diversity Score is 4 (from metrics). The ontology uses `owl:someValuesFrom` in a GCA on `InvoiceMessage` (`involvesOrganization someValuesFrom Organization`), `allValuesFrom` on `RoleAssignment` for agent role scope, `owl:inverseOf` pairs throughout, `owl:FunctionalProperty` on key navigational properties, and `owl:disjointUnionOf`. The mixture is good but lacks `owl:equivalentClass` or cardinality restrictions, which would increase formal expressivity.

**Lexical & Annotation Quality:**

Strict CamelCase throughout (1.0), full label and comment coverage (1.0 each). The ontology uses full lowerCamelCase for property names consistently.

**Most Critical Defect:**

CQ6 (address of the buyer) is answered via `Organization -> hasAddress -> Address` rather than through the `RoleAssignment` pivot. This means that in a knowledge graph instance where E/D/E plays both Buyer and Delivery Party roles — each with distinct addresses — the ontology cannot distinguish which address belongs to which role without additional data properties or instance-level workarounds. Moving `hasAddress` from `Organization` to `RoleAssignment` as done in Ranks 1 and 2 would close this gap.

---

## Bottom Ontologies: Summary

**`EDIFACT_ontology_20260301_215700.owl` (Rank 19):** This is the smallest ontology in the dualAgent set with only 16 classes, 22 object properties, and 9 data properties (235 triples; RR=0.8462, AR=0.5625, IR=0.25, Axiom Diversity=2). While structurally well-formed, it critically lacks an explicit pivot/reification class for the Agent Role N-ary relationship — organizations link to roles via a simple `playsRole` property from `Organization` to `AgentRole` without a context class, making it impossible to simultaneously express the invoice-specific context, role type, and address for a single organization instance. This means CQs 3, 4, and 6 can only be answered with significant ambiguity. The ontology also omits an `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` section model — the three-part invoice structure from the domain story is not represented, reducing CQ10 coverage to a generic `Segment`-based query. Additionally, Axiom Diversity Score of only 2 reflects that only `owl:disjointWith` and `owl:inverseOf` constructs are used, with no `owl:someValuesFrom` restrictions or cardinality constraints.

**`EDIFACT_ontology_20260301_221725.owl` (Rank 20):** The smallest and weakest ontology in the set, with only 13 classes, 22 object properties, and 8 data properties (227 triples; RR=0.9565, AR=0.6154, IR=0.0769, Axiom Diversity=2). The extreme RR (0.9565) reflects the near-total absence of a subclass hierarchy — IR=0.0769 means only one subClassOf edge (`InvoiceMessage < Message`) across 13 classes, indicating a completely flat taxonomy. Critical domain classes are missing: there is no separate `HeaderSection`, `DetailSection`, or `SummarySection`, no explicit `Price` class, no `Identifier`/`GLN` class, and no `BusinessProcess` link modelling. The pivot class used for roles (`UserResourceUsage` — an evidently hallucinated and contextually meaningless name) is structurally present but the non-domain-relevant naming causes severe lexical quality concerns despite the overall label/comment metrics being formally 1.0 (names are labelled, but the labels themselves are non-standard). CQs 10, 11, 12, 13, and 14 are effectively not answerable without significant extension, and CQ4 (buyer identification) cannot be answered since there are no role type subclasses or role type data properties. Only 10 of 14 CQs can be partially addressed.

**`EDIFACT_ontology_20260301_221940.owl` (Rank 18):** With 21 classes, 28 object properties, and only 5 data properties (308 triples; RR=0.8, AR=0.2381, IR=0.3333, Axiom Diversity=3), this ontology's most significant weakness is its extremely low AR of 0.2381 — the lowest in the entire dualAgent set. Only 5 data properties for 21 classes means most domain attributes (invoice number, amounts, prices, address details, item descriptions) are absent from the schema entirely, severely limiting the ability to populate and query a knowledge graph. CQs 5, 8, 9, 11, and 12 cannot be answered with data-property-level precision. The role reification pattern uses a `RoleAssignment` pivot, which is conceptually correct, but the absence of data properties means the pivot cannot carry address or identifier information in string or numeric form. The Axiom Diversity Score of 3 indicates only minimal use of advanced OWL constructs beyond declarations and subClassOf.

**`EDIFACT_ontology_20260301_222534.owl` (Rank 17):** This ontology introduces a serious structural modelling error: `InvoiceMessage` is made a subclass of `InterchangeEnvelope` (via `EdifactMessage rdfs:subClassOf InterchangeEnvelope` and `InvoiceMessage rdfs:subClassOf EdifactMessage`), which violates the EDIFACT domain model where the `InterchangeEnvelope` contains messages — messages are not specializations of envelopes. This conflation means CQ1 cannot be answered correctly since `InvoiceMessage` instances would simultaneously be instances of the envelope class, corrupting queries for "invoices within an envelope." Furthermore, the section classes (`InvoiceHeaderSection`, `InvoiceDetailSection`, `InvoiceSummarySection`) are subclassed from `InvoiceMessage` rather than from `Segment`, compounding the modelling errors. Despite a good Axiom Diversity Score of 5 and correct use of `owl:someValuesFrom` and `owl:allValuesFrom` restrictions, the fundamental class hierarchy inversion renders the ontology architecturally unsound for domain conformance. Metrics: 18 classes, 30 object properties, 7 data properties, RR=0.7895, AR=0.3889, IR=0.4444.

**`EDIFACT_ontology_20260301_215924.owl` (Rank 16):** With 19 classes, 34 object properties, and 8 data properties (322 triples; RR=0.9444, AR=0.4211, IR=0.1053, Axiom Diversity=5), this ontology performs well on structural richness and axiom complexity but has a significantly flat hierarchy (IR=0.1053 — only 2 subClassOf edges, meaning only `InvoiceMessage < Message` and `GlobalLocationNumber < Identifier` are the only hierarchical relationships). The lack of section subclassing means the three-part invoice structure is modelled via object properties from `InvoiceMessage` to `RoleAssignment`, `InvoiceHeader`, `InvoiceDetail`, and `InvoiceSummary` as flat classes — this works but loses the formal `Segment` hierarchy. More critically, CQ13 (mandatory validity information) is covered only by a boolean `hasMandatoryIdentifier` flag on `InvoiceMessage`, which cannot capture the structural detail of which specific elements are required. The `RoleAssignment rdfs:subClassOf [cardinality 1 on involvesOrganization; cardinality 1 on hasAgentRole]` is the only GCA, limiting the logical depth despite the high Axiom Diversity Score.

**`EDIFACT_ontology_20260301_221332.owl` (Rank 9):** Scores well overall (4.21) but is limited to 13/14 CQs due to the absence of an explicit price class hierarchy and net price data property accessible from the line item path. The `hasNetPrice` property is modelled as an object property from `LineItem` to `Price` rather than a data property, so CQ9 (net price as a numeric value) requires two-hop navigation and the ultimate value must be stored as a data property on `Price`. While structurally valid, this introduces unnecessary indirection. The Axiom Diversity of 5 (qualified cardinality restrictions, `allValuesFrom`, functional properties) is a strength, and the `RoleAssignment` reification is well-formed with cardinality constraints. The lack of an explicit `Buyer` subclass of `AgentRole` slightly weakens CQ4.

**`EDIFACT_ontology_20260301_224527.owl` (Rank 6):** Scores 4.44 and covers all 14 CQs but introduces an extraneous `EDIFACTDelimiter` class connected via `usesDelimiter` on `InterchangeEnvelope`/`Message`. While technically this models a real EDIFACT feature (delimiter characters like `+` and `:`), it is semantically over-specified and not required by any of the 14 CQs. The class adds structural bloat and reduces AR relative to classes without data properties. The `InvoiceMessage owl:equivalentClass` GCA (equivalentClass: at least one section) is a useful logical contribution. The `OrganizationRoleAssignment` pivot lacks explicit cardinality restrictions on its linking properties, reducing formal expressivity.

**`EDIFACT_ontology_20260301_220437.owl` (Rank 11):** This ontology has a design deficiency where `Address rdfs:subClassOf CompositeDataElement` and `LineItem rdfs:subClassOf DetailSection` — making address instances simultaneously composite data elements and line items simultaneously parts of detail sections via inheritance. While this reflects some EDIFACT structural reality, it creates type confusion: an `Address` instance would be inferred as a `CompositeDataElement`, making queries over `CompositeDataElement` accidentally return addresses. This is a category confusion that would complicate SPARQL queries. AR=0.1429 (only 3 data properties for 21 classes) is a major weakness — there is barely any data property expressivity, preventing CQs 5, 8, 9, 11, and 12 from being answered with numeric or string precision.

**`EDIFACT_ontology_20260301_223501.owl` (Rank 8):** A solidly designed ontology (4.18 score) that covers 13/14 CQs but lacks explicit subclassing of `AgentRole` for buyer/seller/delivery party roles and has no `owl:someValuesFrom` or cardinality GCAs, leaving Axiom Diversity at only 2. The `RoleAssignment` pattern is correct but without cardinality restrictions the formal logical constraints on role assignments are absent. AR=0.3333 (7 data properties for 21 classes) is moderate but misses address component details and item description attributes. Section classes (`InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary`) do not subclass `Segment`, meaning the three-part structure is disconnected from the EDIFACT syntactic hierarchy.

**`EDIFACT_ontology_20260301_224212.owl` (Rank 13):** Covers 13 of 14 CQs and achieves a score of 4.04. The `Section` intermediate class with `HeaderSection`, `DetailSection`, `SummarySection` subclassing it, plus a `disjointUnionOf` on `Section`, is a clean architectural approach. The `OrganizationRoleAssignment` pivot is well-formed. However, the absence of data properties for address components and item descriptions (AR=0.5, 8 properties across 16 classes) limits the ability to fully answer CQs 5, 6, and 8 with precise string-valued attributes. Axiom Diversity of 4 and absence of `owl:someValuesFrom` GCAs limit logical depth.

**`EDIFACT_ontology_20260301_220832.owl` (Rank 7):** Achieves 4.38 and covers 13/14 CQs. This ontology uses `OrganizationInRole` as the pivot class and has `Segment owl:disjointUnionOf (HeaderSection DetailSection SummarySection)`. It also models `GlobalLocationNumber rdfs:subClassOf Identifier` providing explicit GLN typing. The restriction `SimpleDataElement rdfs:subClassOf [mandatoryIdentifier someValuesFrom xsd:string]` is a novel approach to modelling D96A mandatory identifier requirements at the structural level, partially addressing CQ13. However, `hasRole` on `Organization` (domain `Organization`, range `AgentRole`) creates a direct shortcut that bypasses the pivot class for role queries, introducing an architectural redundancy alongside the pivot chain.

**`EDIFACT_ontology_20260301_221113.owl` (Rank 10):** Achieves 4.09, with a very low AR of 0.2778 (5 data properties across 18 classes) — second lowest in the set — making data-centric CQs (5, 8, 9, 11, 12) only partially answerable. The `OrganizationRoleAssignment` pivot is present and correct in structure, but the minimal data property coverage is a significant limitation. Axiom Diversity Score of 2 reflects no GCAs beyond basic declarations.

**`EDIFACT_ontology_20260301_225409.owl` (Rank 14):** Scores 3.99 with 13/14 CQs. This ontology has an interesting modelling choice: `playsRole` links `Organization` directly to `OrganizationRoleAssignment` and `involvesOrganization` links `InvoiceMessage` to `Organization` — two overlapping paths to organizations. The `assignedTo` property (from `OrganizationRoleAssignment` to `Organization`) combined with the separate `involvesOrganization` shortcut creates structural redundancy. With only 12 data properties across 19 classes (AR=0.6316) the data coverage is reasonable, but `hasMandatoryIdentifier` on `InvoiceMessage` as a string is the only hook for CQ13. The Axiom Diversity of 2 (only inverses and disjointness) is a notable weakness.

**`EDIFACT_ontology_20260301_230338.owl` (Rank 15):** Scores 3.97 with 13/14 CQs. This ontology has `hasIdentifier` declared as a `owl:DatatypeProperty` (domain `Organization`, range `xsd:string`) rather than an object property linking to an `Identifier` class, collapsing the identifier model into a single string literal. While pragmatic, this eliminates the ability to have multiple typed identifiers (GLN, VAT, etc.) for the same organization and makes typed GLN queries less precise. The `InvoiceLineItem` pivot class for line items is well-modelled. AR is high (0.8235 from metrics) but Axiom Diversity is 5 yet the axioms are mostly `allValuesFrom` restrictions rather than more expressive constructs.

---

*End of Report*
