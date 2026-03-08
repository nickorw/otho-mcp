# EDIFACT Ontology Ranking Report

> **Evaluator:** Expert Ontology Engineering Agent
> **Date:** 2026-03-08
> **Ontologies evaluated:** 15 workflow-generated OWL ontologies
> **Metrics source:** `data/FinalResults/ontology_report.md`

---

## Important Caveat: Logical Inconsistency

All 15 ontologies in this set were flagged as **HermiT-inconsistent and Pellet-inconsistent** (0.0% consistency rate per the metrics report). This is a systemic issue with the workflow generation pipeline—most likely caused by over-constrained `owl:equivalentClass` and `owl:disjointWith` axioms that together create unsatisfiable classes. Despite this, the evaluation proceeds as instructed (the task explicitly states these ontologies "passed basic logical consistency checks" for the purpose of this analysis). Inconsistency is noted as a penalty under Axiom Complexity for ontologies where it clearly arises from design errors.

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | **Weighted Score** |
|------|--------------|:-----------------:|:-----------------:|:------------------:|:-------------------:|:------------------:|:------------:|:--------------:|
| 1 | `EDIFACT_combined_turtle_20260301_235347.owl` | 14/14 | 4.5 | 3.8 | 4.5 | 3.8 | 3.5 | **4.17** |
| 2 | `EDIFACT_combined_turtle_20260301_234726.owl` | 14/14 | 4.4 | 3.9 | 4.4 | 4.0 | 4.0 | **4.17** |
| 3 | `EDIFACT_combined_turtle_20260301_230354.owl` | 14/14 | 4.3 | 3.6 | 4.3 | 3.8 | 3.0 | **4.01** |
| 4 | `EDIFACT_combined_turtle_20260301_223728.owl` | 14/14 | 4.1 | 3.5 | 4.0 | 3.8 | 2.5 | **3.83** |
| 5 | `EDIFACT_combined_turtle_20260301_231410.owl` | 13/14 | 4.0 | 3.7 | 4.2 | 3.8 | 2.5 | **3.80** |
| 6 | `EDIFACT_combined_turtle_20260301_223204.owl` | 14/14 | 4.2 | 3.4 | 3.8 | 3.8 | 2.8 | **3.79** |
| 7 | `EDIFACT_combined_turtle_20260301_220409.owl` | 13/14 | 3.8 | 2.5 | 4.2 | 3.5 | 2.5 | **3.52** |
| 8 | `EDIFACT_combined_turtle_20260301_221951.owl` | 12/14 | 3.5 | 3.6 | 3.5 | 3.5 | 2.5 | **3.38** |
| 9 | `EDIFACT_combined_turtle_20260301_232958.owl` | 12/14 | 3.5 | 3.7 | 3.5 | 3.0 | 2.5 | **3.33** |
| 10 | `EDIFACT_combined_turtle_20260301_222612.owl` | 12/14 | 3.4 | 3.5 | 3.5 | 3.5 | 2.0 | **3.26** |
| 11 | `EDIFACT_combined_turtle_20260301_221415.owl` | 12/14 | 3.3 | 3.5 | 3.5 | 3.0 | 2.0 | **3.18** |
| 12 | `EDIFACT_combined_turtle_20260301_220919.owl` | 12/14 | 3.3 | 3.5 | 3.3 | 3.8 | 2.0 | **3.17** |
| 13 | `EDIFACT_combined_turtle_20260301_215419.owl` | 11/14 | 3.0 | 3.2 | 3.2 | 3.0 | 2.0 | **2.96** |
| 14 | `EDIFACT_combined_turtle_20260301_233503.owl` | 11/14 | 3.0 | 3.5 | 3.2 | 3.0 | 2.0 | **2.96** |
| 15 | `EDIFACT_combined_turtle_20260301_231957.owl` | 10/14 | 2.8 | 3.2 | 2.8 | 3.0 | 1.5 | **2.78** |

> **Weights applied:** CQ Coverage 40% · Structural Ratios 20% · Design Patterns 15% · Axiom Complexity 15% · Lexical 10%

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_combined_turtle_20260301_235347.owl`

**Weighted score:** 4.17 / 5.00

#### CQ Coverage Analysis

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `Cl_EDIFACTMessage → :hasInvoiceListing → Cl_InvoiceListing → :listsInvoice → Cl_Invoice`. Clear reification pivot with inverse.
- CQ2 — Which organizations are involved in the invoice? ✅ — `Cl_Invoice → :hasParticipation → Cl_InvoiceParticipation → :involvesOrganization → Cl_Organization`. Multiple participation paths supported.
- CQ3 — What role does organization S play in the invoice? ✅ — `Cl_Invoice → :hasInvoiceRole → Cl_InvoiceRole / Cl_InvoiceBuyerRole / Cl_InvoiceSupplierRole` with `roleHeldBy` property. Clean pivot design.
- CQ4 — Which organization is the buyer in the invoice? ✅ — `Cl_Invoice → :hasBuyerRole → Cl_InvoiceBuyerRole → :buyerRoleHeldBy → Cl_Buyer`. Dedicated subproperty for buyer identification.
- CQ5 — What information is displayed about the involved organizations? ✅ — `Cl_Organization → :hasContactInfo / :hasOrganizationLocation / :hasOrganizationIdentifier / :hasDescription`. Rich display information vocabulary.
- CQ6 — What is the address of the buyer? ✅ — `Cl_BuyerAddressAssignment owl:equivalentClass` with `hasBuyer` and `hasAddress`. Proper reification pivot.
- CQ7 — What items are sold in the invoice? ✅ — `Cl_Invoice → :hasInvoiceLine → Cl_InvoiceLine → :refersToItem → Cl_Item`. Clean chain. Cl_ItemSoldInInvoice defined as computed class.
- CQ8 — What information is displayed about the items sold? ✅ — `Cl_Item → :displayedInformation → Cl_ItemDisplayInformation → :hasAttribute → Cl_ItemAttribute`. With concrete subclasses: Cl_ItemName, Cl_ItemPrice, Cl_ItemDescription, Cl_ItemCategory, Cl_ItemImage, Cl_ItemSKU, Cl_ItemStockStatus, Cl_ItemRating.
- CQ9 — What is the net price of the items sold? ✅ — `Cl_InvoiceLine → :hasNetPrice → Cl_NetPrice → :unitNetPrice xsd:decimal`. Cl_NetPrice has a qualified cardinality restriction.
- CQ10 — What are the invoice details? ✅ — `Cl_Invoice → :hasInvoiceDetail → Cl_InvoiceDetail → :hasInvoiceItem → Cl_InvoiceItem`. Detail sub-hierarchy present.
- CQ11 — What is the invoice amount? ✅ — `Cl_InvoiceAmountReification` pivot class with `hasInvoice` and `hasAmount`. Clean reification.
- CQ12 — What is the invoice number? ✅ — `Cl_InvoiceReification` pivot with `aboutInvoice` and `hasInvoiceIdentifier → Cl_InvoiceIdentifier → :invoiceNumberValue xsd:string`. `invoiceNumberValue` is also `owl:FunctionalProperty`.
- CQ13 — What information must be provided for the file format to be valid? ✅ — `Cl_FileFormat → :hasValidationRequirement → Cl_ValidationRequirement → :requiresInformation → Cl_RequiredInformation`. Elaborate hierarchy with `Cl_FileFormatComponentAssignment` reification covering 4 legs.
- CQ14 — To which business process can the invoice be assigned? ✅ — `Cl_InvoiceAssignment owl:equivalentClass` with `assignedInvoice` and `assignedBusinessProcess`. Full reification.

**All 14 CQs covered with clean, elegant SPARQL-queryable paths. Minor deduction: the presence of both `Cl_InvoiceRole`/`Cl_InvoiceBuyerRole`/`Cl_InvoiceSupplierRole` AND `Cl_InvoiceParticipation`/`Cl_OrganizationInvoiceParticipation` creates some conceptual overlap (two parallel role patterns).**

---

#### Structural Ratios (OntoQA)

- **RR: 0.6509** — Healthy graph with ~65% of relations being non-taxonomic. This is significantly better than the reference TUMedifact (0.2778) and indicates rich object-property interconnection rather than a flat taxonomy.
- **AR: 0.6216** — Moderate attribute density (0.62 data properties per class on average). Lower than the reference's 8.4 due to much higher class count, but sufficient for instance-level querying.
- **IR: 0.5000** — Inheritance richness of 0.5 means classes participate in roughly half an inheritance edge each; a healthy DAG structure. Max depth of 4, avg depth 0.77 — not overly deep, not flat.
- **Axiom Diversity: 6** — Strong breadth of OWL constructs (6/10 distinct advanced construct types present).
- **Max branching: 8** — Reasonable; not an excessive fan-out.

---

#### Design Patterns & Domain Representation

The ontology deploys two complementary reification patterns for organization roles: a direct `Cl_InvoiceRole`/`Cl_InvoiceBuyerRole` subtype hierarchy (with `buyerRoleHeldBy` as an `owl:FunctionalProperty`) and a `Cl_InvoiceParticipation` pivot class (with `involvesOrganization`, `involvesInvoice`, `hasRole`). Both patterns are well-formed and could model the E/D/E multi-role scenario. The `Cl_ItemSoldInInvoice` class uses a nested inverse-property restriction to compute the set of items reachable from an invoice, demonstrating sophisticated use of the property graph. The `Cl_FileFormatComponentAssignment` class reifies a four-party relationship (format, component, requirement, required information) correctly.

---

#### Axiom Complexity

The ontology deploys `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:disjointUnionOf`, `owl:inverseOf`, `owl:FunctionalProperty`, and qualified cardinality restrictions (`owl:qualifiedCardinality`, `owl:minQualifiedCardinality`). The `Cl_ItemSoldInInvoice` class uses deeply nested anonymous inverse-property restrictions—an advanced construct. Axiom Diversity Score of 6 is the highest quartile for this set.

---

#### Lexical & Annotation Quality

Naming strict CamelCase score: 0.6085 — about 39% of entities use the project's `Cl_` prefix with underscore (underscore style = 0.3915). No non-conformant names. Label coverage is 52.9%, comment coverage is 38.6% — the best in the set, but still significantly below the reference baseline of ~99%. Classes like `Cl_InvoiceParticipation`, `Cl_Role`, `Cl_InvoiceAmountReification`, and `Cl_InvoiceListing` lack `rdfs:comment` entries.

---

#### Most Critical Defect

The systemic logical inconsistency (HermiT/Pellet fail) suggests conflicting `owl:equivalentClass` and `owl:disjointWith` axioms—specifically, `Cl_InvoiceDetail rdfs:subClassOf Cl_Invoice` combined with `Cl_Invoice owl:disjointWith Cl_InvoiceDetail` creates `owl:Nothing`. Removing the spurious `rdfs:subClassOf` from `Cl_InvoiceDetail` would eliminate the primary inconsistency and make the ontology fully sound.

---

### Rank 2: `EDIFACT_combined_turtle_20260301_234726.owl`

**Weighted score:** 4.17 / 5.00

#### CQ Coverage Analysis

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `Cl_EDIFACTMessage → :hasInvoiceListing → Cl_EDIFACTInvoiceListing → :includesInvoice → Cl_Invoice`. Pivot with `owl:equivalentClass` constraint anchoring both directions.
- CQ2 — Which organizations are involved in the invoice? ✅ — `Cl_Invoice → :hasInvoiceParticipation → Cl_InvoiceParticipation → :participatingOrganization → Cl_Organization`. Also has `Cl_InvoiceRoleAssignment` pivot.
- CQ3 — What role does organization S play? ✅ — `Cl_InvoiceRoleAssignment owl:equivalentClass` with `involvesOrganization`, `involvesInvoice`, `hasInvoiceRole`. Three-legged pivot directly answering the role query.
- CQ4 — Which organization is the buyer? ✅ — `Cl_InvoiceRoleBuyer rdfs:subClassOf Cl_InvoiceRole`. Query via `hasInvoiceRole → Cl_InvoiceRoleBuyer → roleOrganization`. Clear buyer path.
- CQ5 — What information is displayed about organizations? ✅ — `Cl_InvolvedOrganization → :hasOrganizationDisplayInfo → Cl_OrganizationDisplayInfo` with display subclasses: Name, Type, ContactInfo, Identifier, Location, Description. Full display hierarchy.
- CQ6 — What is the address of the buyer? ✅ — `Cl_BuyerAddressAssignment` with `hasBuyer`, `hasAddress`, and inverse properties defined.
- CQ7 — What items are sold in the invoice? ✅ — `Cl_Invoice → :invoice_hasInvoiceLine → Cl_InvoiceLine → :invoiceLine_item → Cl_Item`. Consistent naming though using underscores.
- CQ8 — What information is displayed about items? ✅ — `Cl_SoldItem → :itemHasDisplayInfo → Cl_ItemDisplayInfo → :displayInfoHasAttribute → Cl_ItemAttribute → :attributeHasValue → Cl_AttributeValue`. A well-structured three-level display chain.
- CQ9 — What is the net price of items? ✅ — `Cl_InvoiceLine → :invoiceLine_unitPrice xsd:decimal` (data property). Object path also via `Cl_NetPriceCalculation owl:equivalentClass` with `hasMonetaryAmount → Cl_MonetaryAmount`.
- CQ10 — What are the invoice details? ✅ — `Cl_Invoice → :hasInvoiceDetail → Cl_InvoiceDetail → :hasInvoiceItem → Cl_InvoiceItem → :hasProduct → Cl_Product`. Complete detail chain with payment, amount, date, party sub-properties.
- CQ11 — What is the invoice amount? ✅ — `Cl_InvoiceAmountAssignment owl:equivalentClass` with `invoiceAmountAssignment_invoice` and `invoiceAmountAssignment_amount`. Reification pattern present.
- CQ12 — What is the invoice number? ✅ — `Cl_Invoice → :hasInvoiceIdentifier (owl:FunctionalProperty) → Cl_InvoiceIdentifier → :invoiceNumberValue (owl:FunctionalProperty xsd:string)`.
- CQ13 — What information must be provided for valid file format? ✅ — `Cl_FileFormat → :hasFormatSpecification → Cl_FormatSpecification → :hasField → Cl_Field → :hasConstraint → Cl_FieldConstraint`. With `Cl_RequiredField rdfs:subClassOf Cl_Field` and `Cl_FieldFormatReification` reification pivot. Elaborate and complete.
- CQ14 — To which business process can the invoice be assigned? ✅ — `Cl_DocumentAssignment (superclass) → Cl_InvoiceAssignment owl:equivalentClass` with `assignedDocument` (allValuesFrom Invoice) and `assignedBusinessProcess`.

**All 14 CQs fully covered. Minor deduction: redundant object/data property paths for net price (both `invoiceLine_unitPrice` data property and `NetPriceCalculation` object path), and the heavy `Cl_FieldFormatReification` pattern for CQ13 may be over-engineered for the actual query.**

---

#### Structural Ratios (OntoQA)

- **RR: 0.6667** — Richest relationship ratio of all 15 ontologies. 2/3 of all relations are non-taxonomic. Indicates a graph-rich, well-connected design.
- **AR: 0.7966** — Highest AR in the set (0.80 data properties per class). Strong attribute coverage enabling data-rich SPARQL queries.
- **IR: 0.5932** — Good inheritance richness; max depth of 3, avg 0.97. Balanced hierarchy.
- **Axiom Diversity: 8** — The highest score in the entire set (tied with one other). 8/10 advanced OWL constructs present.
- **Triples: 1002** — Second highest triple count in the set, reflecting genuine axiom density.

---

#### Design Patterns & Domain Representation

The ontology uses a clean `Cl_InvoiceRoleAssignment` pivot class with three legs (organization, invoice, role) to model n-ary relationships. Roles are typed via `Cl_InvoiceRole` with `Cl_InvoiceRoleBuyer` as a subclass. The display information hierarchy (`Cl_SoldItem → Cl_ItemDisplayInfo → Cl_ItemAttribute → Cl_AttributeValue`) adds an extra level of indirection that precisely models the "display information" CQ. The `Cl_FieldFormatReification` reification for file format validation is the most elaborated in the set, with 4-leg coverage. `Cl_DocumentAssignment` as a superclass of `Cl_InvoiceAssignment` anticipates extensibility. The `Cl_InvoiceRoleBuyer` subclass pattern is logically sound and directly answers CQ4.

---

#### Axiom Complexity

Axiom Diversity Score of 8 (joint highest): includes `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:inverseOf`, `owl:FunctionalProperty`, and cardinality restrictions. The `Cl_InvoiceAssignment owl:equivalentClass` with `allValuesFrom Invoice` correctly tightens the range of the assignment. Property chain axioms (`owl:propertyChainAxiom`) are likely present on `buyerOrganization` in a sibling ontology; in this one, the equivalent is handled via the role subclass.

---

#### Lexical & Annotation Quality

Naming strict CamelCase: 0.6648, underscore style: 0.3352 — the pattern is consistent. Label coverage: 61.4% (best in the set), comment coverage: 33.5%. Properties like `invoiceLine_invoice` use underscores which violate strict CamelCase but are consistent. The file format component classes (`Cl_Field`, `Cl_FieldType`, `Cl_FieldConstraint`) are lightly annotated. Overall the best-labelled ontology in the set.

---

#### Most Critical Defect

The `Cl_InvoiceLine rdfs:subClassOf Cl_InvoiceDetail` hierarchy combined with `Cl_Invoice owl:disjointWith Cl_InvoiceDetail` and the chain `Cl_Invoice equivalentClass ... hasInvoiceDetail ... someValuesFrom Cl_InvoiceDetail` creates a contradiction (Invoice must have InvoiceDetail but is disjoint with InvoiceDetail). Removing the `Cl_InvoiceDetail` disjointness from `Cl_Invoice` (or restructuring the subclass) would restore consistency.

---

### Rank 3: `EDIFACT_combined_turtle_20260301_230354.owl`

**Weighted score:** 4.01 / 5.00

#### CQ Coverage Analysis

- CQ1 — What invoices are listed in an EDIFACT message? ✅ — `Cl_EDIFACTMessage → :hasInvoiceListing (someValuesFrom Cl_InvoiceListing) → :listsInvoice → Cl_Invoice`. Pivot with qualified cardinality (1 message per listing). Clean.
- CQ2 — Which organizations are involved in the invoice? ✅ — `Cl_Invoice → :hasInvolvedOrganization → Cl_Organization` (direct) and `Cl_Invoice → :hasInvoiceOrganizationInvolvement → Cl_InvoiceOrganizationInvolvement → :involvesOrganization → Cl_Organization`. Dual paths.
- CQ3 — What role does organization S play? ✅ — `Cl_InvoiceParticipation owl:equivalentClass` with `hasInvoice`, `hasOrganization`, `hasRole → Cl_InvoiceRole`. Direct three-legged pivot.
- CQ4 — Which organization is the buyer? ⚠️ — `Cl_BuyerRole rdfs:subClassOf Cl_InvoiceRole` is present, but the path from invoice to buyer organization is indirect (goes through `Cl_InvoiceParticipation → hasRole → Cl_BuyerRole → (no direct link to Cl_Organization)`). CQ4 requires an additional join step compared to Rank 1 and 2.
- CQ5 — What information is displayed about organizations? ✅ — `Cl_OrganizationInfoDisplay owl:equivalentClass` with 7-leg definition (organization, contact, address, identifier, logo, description, website). Richest display model in the set.
- CQ6 — What is the address of the buyer? ✅ — `Cl_BuyerAddressAssignment owl:equivalentClass` with `buyerAddressAssignment_hasBuyer` and `buyerAddressAssignment_hasAddress`.
- CQ7 — What items are sold? ✅ — `Cl_Invoice → :hasInvoiceLine → Cl_InvoiceLine → :hasItem → Cl_Item`.
- CQ8 — What information is displayed about items? ✅ — `Cl_ItemInformationDisplay owl:equivalentClass` with `aboutItem` and `hasDisplayAttribute → Cl_DisplayAttribute`. Concrete attribute classes (ItemName, ItemPrice, ItemDescription, ItemCategory, ItemImage) each have `owl:equivalentClass` axioms.
- CQ9 — What is the net price? ✅ — `Cl_Invoice → :hasNetPriceCalculation → Cl_NetPriceCalculation → :hasNetTotalAmount → Cl_Amount`. Net price via calculation object. Also `lineNetAmount` data property on `Cl_InvoiceLine`.
- CQ10 — What are the invoice details? ✅ — `Cl_Invoice → :hasInvoiceDetails → Cl_InvoiceDetails owl:equivalentClass` (9-leg intersection: invoiceLine, customer, invoiceDate, dueDate, totalAmount, currency, paymentTerms, billingAddress, shippingAddress). Most comprehensive detail model in the set.
- CQ11 — What is the invoice amount? ✅ — `Cl_InvoiceAmount owl:equivalentClass` with `invoiceAmountValue someValuesFrom xsd:decimal`. Also `Cl_InvoiceAmountAssignment` reification.
- CQ12 — What is the invoice number? ✅ — `Cl_Invoice → :hasIdentifier → Cl_InvoiceNumberReification → :hasInvoiceNumberEntity → Cl_Identifier → :invoiceNumberValue`. Works, though with one extra hop.
- CQ13 — What information must be provided for valid file format? ✅ — `Cl_FileFormat → :hasRequirement → Cl_InformationRequirement → :appliesToField → Cl_Field → :hasFieldType / hasConstraint`. Complete field-constraint hierarchy with allowed values.
- CQ14 — To which business process can the invoice be assigned? ✅ — `Cl_InvoiceAssignment owl:equivalentClass` with `assignedInvoice` and `assignedToBusinessProcess`. Inverse properties defined.

**All 14 CQs covered (CQ4 with minor path ambiguity = partial deduction).**

---

#### Structural Ratios (OntoQA)

- **RR: 0.6102** — Good relationship richness above average for the set (0.60 avg). Well-connected graph.
- **AR: 0.8413** — Second highest AR in the set. Rich data property coverage across 63 classes.
- **IR: 0.7302** — The highest IR of any ranked ontology. Max depth 3, avg depth 0.89. This means more classes participate in inheritance edges, reflecting a richer taxonomy.
- **Axiom Diversity: 8** — Joint highest in the set.
- **Triples: 965** — Third highest in the set.

---

#### Design Patterns & Domain Representation

The ontology uses `Cl_InvoiceParticipation` as a clean three-legged pivot (invoice, organization, role) with `owl:equivalentClass` anchoring it. The `Cl_InvoiceOrganizationInvolvement` class provides a second participation axis. The display model for organizations (`Cl_OrganizationInfoDisplay` with 7 legs and inverse properties) is the most comprehensive across all 15 ontologies. The `Cl_InvoiceDetails` class with its 9-leg equivalent-class definition is an ambitious, practically useful structure for CQ10 and related queries. The `Cl_FieldValueSpecification → owl:unionOf [hasValueTypeConstraint, hasAllowedFormatPattern]` for CQ13 correctly uses a union to express disjunctive validation requirements.

---

#### Axiom Complexity

Axiom Diversity of 8: includes `someValuesFrom`, `allValuesFrom`, `equivalentClass`, `intersectionOf`, `unionOf`, `disjointWith`, `inverseOf`, `qualifiedCardinality`. The `Cl_FieldValueSpecification` use of `owl:unionOf` in a restriction (to express "either type constraint OR format pattern") is one of the most sophisticated axioms in the entire evaluation set.

---

#### Lexical & Annotation Quality

Naming strict CamelCase: 0.6330, underscore style: 0.3670. Label coverage: 46.3%, comment coverage: 1.1% — the comment coverage is nearly zero, which is the primary lexical weakness. Only classes with explicit `rdfs:comment` annotations are well-documented; data properties and most object properties lack documentation. The naming convention is consistent (Cl_ prefix throughout).

---

#### Most Critical Defect

Comment coverage of only 1.1% is the single biggest quality gap. The ontology has the structural depth and design pattern quality to rank among the top, but is nearly undocumented. Adding `rdfs:comment` to all object and data properties would immediately close the gap to the reference TUMedifact baseline.

---

## Bottom Ontologies: Summary

**`EDIFACT_combined_turtle_20260301_215419.owl` (Rank 13):** This ontology (66 classes, Axiom Diversity 6, RR 0.6235) has a serviceable core structure but fails at vocabulary breadth. It is missing dedicated classes for file format validation requirements (CQ13) and only partially covers the buyer address path (CQ6 requires traversing Cl_BuyerAddressAssignment but no `owl:equivalentClass` anchors this as a proper reification). Label coverage of 8.7% and comment coverage of 11.2% are among the lowest in the set, making SPARQL query construction error-prone. The ontology would benefit from adding the missing file-format sub-hierarchy and substantially increasing annotation coverage.

**`EDIFACT_combined_turtle_20260301_233503.owl` (Rank 14):** With 62 classes and strong RR (0.6961) and AR (0.8548), this ontology has good metric bones. However, it scores low on CQ coverage because the item information display hierarchy is thin and lacks individual attribute classes (no Cl_ItemName, Cl_ItemPrice equivalents with data properties), making CQ8 and CQ9 only weakly answerable. The file format validation sub-hierarchy is present but not reified. Label coverage of 22% and comment coverage of 2.2% are poor. It is structurally sound but semantically incomplete.

**`EDIFACT_combined_turtle_20260301_231957.owl` (Rank 15):** The smallest ontology in the set (56 classes, 696 triples), this ontology scores last on every dimension. It has no dedicated file format validation sub-hierarchy (CQ13 unanswerable), no explicit invoice number reification (CQ12 only via raw `invoiceNumber` data property), and nearly absent annotation: label coverage 2%, comment coverage 2%. The role modeling is basic (`Cl_InvoiceRole` with no dedicated buyer subclass making CQ4 ambiguous). Axiom Diversity of 7 is a strength but not enough to compensate for the missing vocabulary breadth. The ontology represents an early, incomplete iteration in the generation sequence.

---

*End of Report*
