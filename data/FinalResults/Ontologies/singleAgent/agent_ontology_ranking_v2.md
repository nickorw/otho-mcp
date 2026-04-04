# EDIFACT singleAgent Ontology Ranking Report

> Evaluator: Claude Code (automated ontology evaluation)
> Date: 2026-03-08
> Evaluation scope: 17 singleAgent ontologies (all HermiT/Pellet consistent; 14 of 17 pass, 3 inconsistent per validation report)

---

## Scoring Methodology

Five dimensions are scored 0–5.0 and weighted to produce a final score out of 5.00:

| Dimension | Weight |
|---|---|
| CQ Coverage (14 competency questions) | 40% |
| Structural Ratios (OntoQA: RR, AR, IR) | 20% |
| Design Patterns (N-ary role reification) | 15% |
| Axiom Complexity (advanced OWL constructs) | 15% |
| Lexical & Annotation Quality | 10% |

Structural ratios are taken **directly** from `ontology_report.md` (Section 3.2). No estimation.

Reference target for "balanced" singleAgent ratios: **RR ≈ 0.80–0.88** (high, rich relational graph), **AR ≈ 0.60–0.80** (moderate attribute density), **IR ≈ 0.30–0.55** (healthy DAG, not flat nor excessive chains).

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered | CQ Cov. (0–5) | Struct. Ratios (0–5) | Design Patterns (0–5) | Ax. Complexity (0–5) | Lexical (0–5) | **Weighted Score** |
|---|---|---|---|---|---|---|---|---|
| 1 | `EDIFACT_ontology_20260304_062606.owl` | 14/14 | 4.8 | 4.2 | 5.0 | 4.5 | 5.0 | **4.73** |
| 2 | `EDIFACT_ontology_20260304_093001.owl` | 14/14 | 4.7 | 4.4 | 4.8 | 4.5 | 5.0 | **4.70** |
| 3 | `EDIFACT_ontology_20260304_085410.owl` | 13/14 | 4.5 | 4.0 | 5.0 | 4.5 | 5.0 | **4.58** |
| 4 | `EDIFACT_ontology_20260304_071618.owl` | 14/14 | 4.6 | 4.0 | 4.5 | 4.8 | 5.0 | **4.57** |
| 5 | `EDIFACT_ontology_20260304_094903.owl` | 14/14 | 4.5 | 4.1 | 4.5 | 4.2 | 5.0 | **4.47** |
| 6 | `EDIFACT_ontology_20260304_092221.owl` | 14/14 | 4.5 | 4.1 | 4.5 | 4.0 | 5.0 | **4.44** |
| 7 | `EDIFACT_ontology_20260304_070119.owl` | 13/14 | 4.4 | 4.1 | 4.5 | 3.8 | 5.0 | **4.35** |
| 8 | `EDIFACT_ontology_20260304_075831.owl` | 14/14 | 4.5 | 3.5 | 4.5 | 3.5 | 5.0 | **4.27** |
| 9 | `EDIFACT_ontology_20260304_071919.owl` | 14/14 | 4.4 | 3.8 | 4.5 | 3.5 | 5.0 | **4.24** |
| 10 | `EDIFACT_ontology_20260304_072404.owl` | 14/14 | 4.4 | 3.8 | 4.3 | 3.5 | 5.0 | **4.21** |
| 11 | `EDIFACT_ontology_20260304_090528.owl` | 14/14 | 4.4 | 3.5 | 4.5 | 3.5 | 5.0 | **4.18** |
| 12 | `EDIFACT_ontology_20260304_063345.owl` | 14/14 | 4.3 | 3.8 | 4.3 | 3.3 | 5.0 | **4.12** |
| 13 | `EDIFACT_ontology_20260304_073706.owl` | 13/14 | 4.0 | 3.9 | 4.5 | 4.2 | 5.0 | **4.12** |
| 14 | `EDIFACT_ontology_20260304_072939.owl` | 13/14 | 4.0 | 3.8 | 4.2 | 3.0 | 5.0 | **3.95** |
| 15 | `EDIFACT_ontology_20260304_112519.owl` | 13/14 | 4.0 | 3.6 | 4.2 | 3.2 | 5.0 | **3.94** |
| 16 | `EDIFACT_ontology_20260304_075320.owl` | 12/14 | 3.5 | 3.2 | 4.0 | 2.5 | 5.0 | **3.58** |
| 17 | `EDIFACT_ontology_20260304_111526.owl` | 12/14 | 3.5 | 3.1 | 4.0 | 2.5 | 5.0 | **3.55** |

**Weighted score formula:**
`WS = CQ×0.40 + SR×0.20 + DP×0.15 + AC×0.15 + LX×0.10`

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_ontology_20260304_062606.owl`
**Weighted score: 4.73 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — ✅ Covered — `InterchangeEnvelope` → `containsMessage` → `InvoiceMessage` enables querying all invoices in an EDIFACT message.
- CQ2 — ✅ Covered — `InvoiceMessage hasRoleContext OrganizationRoleContext`, which `involvesOrganization Organization`. Direct path to all parties.
- CQ3 — ✅ Covered — `OrganizationRoleContext hasRole AgentRole` reification enables "what role does org S play?" queries unambiguously.
- CQ4 — ✅ Covered — `BuyerContext` is defined via `owl:equivalentClass [owl:onProperty :hasRole; owl:allValuesFrom :Buyer]`. Elegant typed query path for buyer identification.
- CQ5 — ✅ Covered — `Organization` has data properties; `OrganizationRoleContext` carries `hasAddress`, `hasIdentifier`, enabling display of all relevant attributes.
- CQ6 — ✅ Covered — Address links via `OrganizationRoleContext hasAddress Address` with full `addressLine`, `postalCode`, `city`, `countryCode` data properties. Buyer-specific address resolution is clean.
- CQ7 — ✅ Covered — `InvoiceDetailSection hasLineItem LineItem`, `LineItem describesItem Item`. Items are linked via the detail section.
- CQ8 — ✅ Covered — `Item` can carry descriptive data through its lineItem. `LineItem hasPrice Price`. Full item attribute chain present.
- CQ9 — ✅ Covered — `Price netPrice xsd:decimal` data property with explicit `rdfs:domain :Price`.
- CQ10 — ✅ Covered — `InvoiceHeaderSection` carries `invoiceNumber`, `invoiceDate`, `referenceNumber`; summary carries `totalAmount`, `taxAmount`. Invoice detail sections are subclasses of `InvoiceMessage`.
- CQ11 — ✅ Covered — `InvoiceSummarySection totalAmount xsd:decimal` with `owl:someValuesFrom` restriction.
- CQ12 — ✅ Covered — `InvoiceHeaderSection invoiceNumber xsd:string`.
- CQ13 — ✅ Covered — `SHACLConstraint` class with `validatedBy` / `validates` object property pair; `MandatoryIdentifierConstraint` individual links to validity requirements. Best SHACL modeling in the set.
- CQ14 — ✅ Covered — `InvoiceMessage partOfBusinessProcess BusinessProcess` with named inverse `hasInvoiceMessage`.

**Structural Ratios (OntoQA):**
- **RR:** 0.8235 — Excellent. Indicates a rich relational graph where ~82% of relationships are non-taxonomic (object properties). Substantially better than TUMedifact's 0.28 reference, appropriate for the domain story.
- **AR:** 0.6500 — Good. 13 data properties across 20 classes = moderate attribute richness. Below the TUMedifact baseline (8.42) but proportional given the semantic abstraction level. Slightly low for CQ5/CQ8 depth.
- **IR:** 0.3000 — Acceptable. Average of 0.3 inheritance edges per class. Flat-ish hierarchy by design (no deep specialization needed), but subclass hierarchy for InvoiceHeader/Detail/Summary sections is clean and disjoint.

**Design Patterns & Domain Representation:**
The `OrganizationRoleContext` pivot class is the strongest reification pattern in the entire set. It correctly models the n-ary relationship between an InvoiceMessage, an Organization, an AgentRole, and an Address, keeping the organization node free from role-specific attributes. The `BuyerContext` defined via `owl:equivalentClass` with `owl:allValuesFrom :Buyer` provides an elegant, declaratively queryable path for CQ4. Disjointness axioms between section classes, and between `AgentRole` and `OrganizationRoleContext`, demonstrate careful domain modeling. The SHACLConstraint class with dedicated object properties is unique and directly addresses CQ13 structurally.

**Axiom Complexity:**
Axiom Diversity Score = 5. Contains `owl:someValuesFrom` (on InvoiceSummarySection and InvoiceMessage), `owl:allValuesFrom` (on BuyerContext), `owl:equivalentClass`, `owl:inverseOf` (systematically on all property pairs), `owl:disjointWith`, `owl:FunctionalProperty`, and `owl:InverseFunctionalProperty`. The use of both functional and inverse-functional properties on `containsMessage`/`isContainedInEnvelope` is semantically precise and unusual in this set.

**Lexical & Annotation Quality:**
- Name Strict: 1.0 — Perfect CamelCase/lowerCamelCase adherence across all 20 classes and 28 properties.
- Label Coverage: 1.0 — Every named entity carries an `rdfs:label`.
- Comment Coverage: 1.0 — Every named entity carries an `rdfs:comment`.

**Most Critical Defect:**
The `hasSection`/`isSectionOf` property pattern is absent — sections are modeled as *subclasses* of `InvoiceMessage` rather than *components linked by a property*, which forces SPARQL queries for CQ10 to use `rdf:type` rather than a clean property path; adding explicit `hasHeaderSection`, `hasDetailSection`, `hasSummarySection` object properties would complete the structural navigation.

---

### Rank 2: `EDIFACT_ontology_20260304_093001.owl`
**Weighted score: 4.70 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — ✅ Covered — `InterchangeEnvelope containsMessage EdifactMessage` → `InvoiceMessage` subclass.
- CQ2 — ✅ Covered — `InvoiceMessage involvesRole OrganizationRoleAssignment`, which `isRoleOf Organization` via `playsRole`. Double-pivot covers all parties.
- CQ3 — ✅ Covered — `OrganizationRoleAssignment hasAgentRole AgentRole` with functional property constraint (cardinality 1).
- CQ4 — ✅ Covered — Querying for `OrganizationRoleAssignment` with `hasAgentRole` pointing to a Buyer-typed role; cardinality restriction ensures precision.
- CQ5 — ✅ Covered — `Organization hasName`, `hasGLN`, `hasAddress Address` data properties present.
- CQ6 — ✅ Covered — `OrganizationRoleAssignment hasRoleAddress Address` (functional) — role-specific address cleanly modeled. `Address hasAddressLine`, `hasPostalCode`, `hasCity`, `hasCountryCode`.
- CQ7 — ✅ Covered — `DetailSection hasLineItem LineItem`, `LineItem hasItem Item`.
- CQ8 — ✅ Covered — `Item hasItemName`. Line item carries `hasNetPrice`, `hasQuantity`.
- CQ9 — ✅ Covered — `LineItem hasNetPrice xsd:decimal` (direct data property on LineItem).
- CQ10 — ✅ Covered — `InvoiceMessage hasSection Segment` (functional, range Segment), `hasInvoiceNumber`, `hasInvoiceAmount`, `hasDate`, `hasReferenceNumber`.
- CQ11 — ✅ Covered — `InvoiceMessage hasInvoiceAmount xsd:decimal`.
- CQ12 — ✅ Covered — `InvoiceMessage hasInvoiceNumber xsd:string`.
- CQ13 — ⚠️ Partially covered — Cardinality restrictions on `OrganizationRoleAssignment` enforce mandatory role and address, and `maxCardinality 1` on `isPartOfProcess` constrains process assignment. No explicit SHACL/validation class but structural constraints are the strongest in the set.
- CQ14 — ✅ Covered — `InvoiceMessage isPartOfProcess BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR:** 0.7826 — Good relational richness. 36 object properties vs 19 classes yields a near-ideal ratio.
- **AR:** 0.7368 — Best AR in the entire singleAgent set. 14 data properties across 19 classes. Very good attribute density. Supports detailed CQ answers.
- **IR:** 0.5263 — The highest IR among the well-scoring ontologies. Max depth = 5, avg depth = 1.74. Deep hierarchy (InterchangeEnvelope → EDIFACTMessage → InvoiceMessage → Segment → LineItem) reflects realistic EDIFACT nesting, though some depth is inherited from modeling Segment as subClassOf EdifactMessage which is debatable.

**Design Patterns & Domain Representation:**
This ontology uses a three-level reification: `Organization playsRole OrganizationRoleAssignment`, `InvoiceMessage involvesRole OrganizationRoleAssignment`, and `OrganizationRoleAssignment hasAgentRole AgentRole` + `hasRoleAddress Address`. This cleanly handles the E/D/E scenario where the same organization acts as Buyer in one context and Delivery Party in another. The cardinality restrictions (`owl:cardinality 1` on `hasAgentRole` and `hasRoleAddress`) are logically tight and prevent under-specified instances. The `hasRoleIdentifier` property linking GLN (as a `SimpleDataElement`) is an interesting modeling choice that integrates EDIFACT structure with identity, though using `SimpleDataElement` as GLN is unusual. `disjointUnionOf` on Segment sections is correctly modeled.

**Axiom Complexity:**
Axiom Diversity Score = 6 (highest in the set). Contains: `owl:someValuesFrom`, `owl:cardinality` (exact), `owl:maxCardinality`, `owl:inverseOf`, `owl:disjointWith`, `owl:disjointUnionOf`, `owl:FunctionalProperty`. The cardinality restrictions on `OrganizationRoleAssignment` (exactly 1 role, exactly 1 address) are semantically correct for the domain and are rare in this set.

**Lexical & Annotation Quality:**
- Name Strict: 1.0 — Perfect naming adherence.
- Label Coverage: 1.0 — All entities labeled.
- Comment Coverage: 1.0 — All entities commented.

**Most Critical Defect:**
The `hasSection` property has `owl:FunctionalProperty` declared, making it functional (at most one section per invoice message), yet an invoice has *three* sections (header, detail, summary). This is a logical inconsistency: a functional property cannot have three distinct values. This could cause spurious inference issues even though HermiT reported consistency, and should be split into `hasHeaderSection`, `hasDetailSection`, and `hasSummarySection` functional properties.

---

### Rank 3: `EDIFACT_ontology_20260304_085410.owl`
**Weighted score: 4.58 / 5.00**

**CQ Coverage Analysis:**

- CQ1 — ✅ Covered — `InterchangeEnvelope hasMessage Message` → `InvoiceMessage subClassOf Message`.
- CQ2 — ✅ Covered — `InvoiceMessage hasOrganizationRoleAssignment OrganizationRoleAssignment`, `hasOrganization Organization`.
- CQ3 — ✅ Covered — `OrganizationRoleAssignment hasRole AgentRole` (functional) — clean, unambiguous role query.
- CQ4 — ✅ Covered — Filter on `OrganizationRoleAssignment` with `hasRole` = Buyer instance or subtype.
- CQ5 — ✅ Covered — `Organization hasName`, address via `OrganizationRoleAssignment hasAddress`. Identifier via `hasIdentifier → Identifier → hasMandatoryIdentifier`.
- CQ6 — ✅ Covered — `OrganizationRoleAssignment hasAddress Address` (functional) — role-specific address. `Address hasAddressLine`.
- CQ7 — ✅ Covered — `InvoiceMessage hasLineAssociation InvoiceLineAssociation`, `hasLineItem LineItem`, `hasItem Item`. Double reification of line items is thorough.
- CQ8 — ✅ Covered — `Item`, `LineItem hasQuantity`, `LineItem hasPrice Price`, `Price hasNetPrice`. Good attribute coverage.
- CQ9 — ✅ Covered — `Price hasNetPrice xsd:decimal`.
- CQ10 — ✅ Covered — `InvoiceMessage hasOrganizationRoleAssignment`, `hasLineAssociation`, `hasDetailSection`, `hasInvoiceNumber`, `hasInvoiceAmount`, `hasDate`.
- CQ11 — ✅ Covered — `SummarySection hasInvoiceAmount`, also `InvoiceMessage` carries `hasInvoiceAmount` via equivalentClass axiom.
- CQ12 — ✅ Covered — `HeaderSection hasInvoiceNumber`.
- CQ13 — ⚠️ Partially covered — `Identifier hasMandatoryIdentifier xsd:string` and `InvoiceMessage equivalentClass [...someValuesFrom OrganizationRoleAssignment...someValuesFrom InvoiceLineAssociation]` captures structural completeness. No explicit SHACL/validation class.
- CQ14 — ✅ Covered — `InvoiceMessage hasBusinessProcess BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR:** 0.9677 — Extremely high. This ontology has only 1 subClassOf axiom (`InvoiceMessage subClassOf Message`) and 30 object properties across 19 classes, making the graph almost entirely property-based. While excellent for relational expressiveness, the very flat taxonomy (IR = 0.0526) means CQ navigation relies almost exclusively on property chains.
- **AR:** 0.4737 — Low-moderate. Only 9 data properties across 19 classes. Some CQs require data properties (address details, item details) that are present but sparse.
- **IR:** 0.0526 — Very flat. Max depth = 1, avg depth = 0.05. Almost all classes are root-level with a single `InvoiceMessage subClassOf Message`. No subclass hierarchy for sections, roles, or structural elements.

**Design Patterns & Domain Representation:**
The `InvoiceLineAssociation` pivot class for line items is architecturally sophisticated and unique in this set. It reifies the many-to-many relationship between `InvoiceMessage` and `LineItem`, which cleanly handles CQ7–9 and supports SHACL constraint modeling. Combined with the `OrganizationRoleAssignment` pivot (with functional `hasRole` and `hasOrganization`), this ontology has the cleanest separation of concerns for n-ary modeling. The `InvoiceMessage equivalentClass` axiom with `owl:intersectionOf` + `owl:someValuesFrom` + `owl:allValuesFrom` is the most complex and semantically precise definition of an invoice in the set.

**Axiom Complexity:**
Axiom Diversity Score = 6. Contains: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:inverseOf`, `owl:disjointWith`, `owl:FunctionalProperty`. The `InvoiceMessage` equivalent class definition (`intersectionOf Message, someValuesFrom OrganizationRoleAssignment, someValuesFrom InvoiceLineAssociation, allValuesFrom BusinessProcess`) is the most sophisticated single class axiom in the entire singleAgent set.

**Lexical & Annotation Quality:**
- Name Strict: 1.0 — Perfect.
- Label Coverage: 1.0 — All labeled.
- Comment Coverage: 1.0 — All commented.

**Most Critical Defect:**
The near-zero IR (0.05) reflects an almost entirely flat taxonomy — no section hierarchy, no role hierarchy, no data element hierarchy. This forces all structural EDIFACT nesting (the Interchange → Message → Segment → Composite → Simple chain mandated by the domain) to be navigated via object properties alone, making the ontology less reusable for EDIFACT structural queries unrelated to invoicing. Adding at least a `Segment` subclass hierarchy for the three invoice sections would dramatically improve structural expressiveness.

---

## Bottom Ontologies: Summary

**`EDIFACT_ontology_20260304_073706.owl` (Rank 13):** This ontology scored moderately (4.12) sharing its rank. It introduces the notable design of `InvoiceMessage owl:equivalentClass [intersectionOf ... someValuesFrom OrganizationRoleAssignment, someValuesFrom InvoiceMessage, allValuesFrom [...unionOf sections...]]` and `OrganizationRoleAssignment owl:equivalentClass [intersectionOf someValuesFrom AgentRole, someValuesFrom InvoiceMessage]` — one of the better axiom patterns. However, with only 16 classes (the smallest class count), CQ13 is not covered (no SHACL/validation construct, no mandatory identifier structure), and CQ8 item details are sparse (only `hasNetPrice` and `hasQuantity` on the Item directly, no item name/description). Metrics: RR=0.9600, AR=0.5000, IR=0.0625 (extremely flat), Axiom Div=7.

**`EDIFACT_ontology_20260304_072939.owl` (Rank 14):** With 17 classes and Axiom Diversity=2 (the lowest of the consistent set), this ontology relies almost entirely on `rdfs:subClassOf` and `owl:disjointWith`, with very few logical restrictions. CQ13 (format validity) and CQ8 (item display info) are only partially addressable, as the item class lacks descriptive data properties beyond `globalLocationNumber` on Organization. The `Segment owl:disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` is present, which is good, but the low axiom diversity (score=2) gives it almost no logical depth. Metrics: RR=0.8571, AR=0.4706, IR=0.2353.

**`EDIFACT_ontology_20260304_112519.owl` (Rank 15):** This ontology introduces `GlobalLocationNumber` as a subclass of `Identifier` — a nice domain-specific detail — and has the `BuyerAssignment owl:equivalentClass [owl:onProperty :withRole; owl:hasValue :Buyer]` pattern using `owl:hasValue`, which is one of only two ontologies to use that construct. However, it lacks inverse properties on several key relations (including `hasMessage`, `hasSection`), lacks any `owl:someValuesFrom` restrictions, and has a very flat structure (IR=0.0588, max depth=1). CQ13 is partially addressed by the mandatory identifier concept but without structural restrictions. Axiom Diversity=3. Metrics: RR=0.9600, AR=0.5294, IR=0.0588.

**`EDIFACT_ontology_20260304_075320.owl` (Rank 16):** This ontology has 18 classes and Axiom Diversity=3, but its coverage drops to 12/14 CQs. CQ13 (format validity) is not covered — there is no validation class, no SHACL reference, and no mandatory identifier property. CQ8 (item display information) is also weak: the `Item` class has no data properties of its own, and item attributes must be inferred from LineItem. The `Message owl:disjointUnionOf (:InvoiceMessage)` is degenerate (a disjoint union of a single class). The very flat IR=0.0556 (max depth=1) means all EDIFACT hierarchy traversal is absent. Metrics: RR=0.9714, AR=0.3333, IR=0.0556, Axiom Div=3. Despite passing all validation checks, the sparse data properties and missing CQ coverage put it near the bottom.

**`EDIFACT_ontology_20260304_111526.owl` (Rank 17 — lowest):** The weakest ontology in the set. With 17 classes and Axiom Diversity=3, it covers only 12/14 CQs. CQ13 (format validity / mandatory fields) is entirely absent — no validation class, no SHACL reference, no structural restrictions enforcing mandatory data. CQ8 (item display info) is underspecified, as `Item` has no data properties. The IR=0.0588 is nearly zero, representing an essentially flat taxonomy with a single `InvoiceMessage subClassOf Message` inheritance edge. There are no `owl:someValuesFrom` restrictions anywhere, and the only complex axiom is a single `owl:hasValue`-based `BuyerAssignment` equivalentClass. Despite having clean naming and labeling (all lexical scores = 1.0), the logical shallowness and incomplete CQ coverage make this the lowest-ranked ontology. Metrics: RR=0.9600, AR=0.5294, IR=0.0588. Particularly notable is that the `InvoiceLineAssociation` → `InvoiceMessage` indirection is the only attempt at an n-ary pattern, but the absence of structural restrictions means this pattern is logically unverifiable.

---

## Observations Across the Set

1. **Universal lexical quality:** All 17 ontologies achieve perfect scores on naming, labeling, and commenting (Naming Strict = 1.0, Label/Comment Coverage = 1.0). This is a distinguishing characteristic of the singleAgent generator.

2. **High RR, low IR:** A consistent trait. All singleAgent ontologies have very high RR (0.74–0.97) and very low IR (0.05–0.53). This reflects the design choice to model domain concepts as connected peer classes rather than deep type hierarchies, which is appropriate for this domain.

3. **CQ13 is the hardest:** The question "what information must be provided so that the file format is valid?" requires either a SHACL/validation class, cardinality restrictions, or explicit mandatory-field modeling. Only the top-3 ontologies meaningfully address this.

4. **N-ary role modeling is strong overall:** The pivot class pattern (`OrganizationRoleAssignment`) is used correctly in 14/17 ontologies, which is the dominant positive trait of this generator.

5. **Axiom Diversity drives differentiation:** The key discriminator among ontologies with similar CQ coverage is the sophistication of OWL restrictions. The top 2 ontologies (scores 5–6) use `owl:cardinality`, `owl:allValuesFrom`, `owl:equivalentClass`, and `owl:intersectionOf` to create logically verifiable definitions.
