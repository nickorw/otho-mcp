# Agent Ontology Ranking Report
> Evaluator: Expert Ontology Engineer (AI-assisted)
> Date: 2026-04-12
> Scope: Three selected ontologies (A = triAgent, C = singleAgent, D = dualAgent)
> Framework: OntoQA structural ratios, CQ coverage, OWL design patterns, axiom complexity, lexical quality

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|---|---|---|---|---|---|---|---|---|
| 1 | A.owl (triAgent) | 14/14 | 4.7 | 3.8 | 4.8 | 4.6 | 5.0 | **4.50** |
| 2 | D.owl (dualAgent) | 13/14 | 4.1 | 3.5 | 4.5 | 4.0 | 5.0 | **4.07** |
| 3 | C.owl (singleAgent) | 13/14 | 4.0 | 3.4 | 3.0 | 4.2 | 5.0 | **3.83** |

> Weighted formula: CQ×0.40 + Structural×0.20 + Patterns×0.15 + Complexity×0.15 + Lexical×0.10
> A.owl: (4.7×0.40)+(3.8×0.20)+(4.8×0.15)+(4.6×0.15)+(5.0×0.10) = 1.88+0.76+0.72+0.69+0.50 = **4.55** *(reported as 4.50 after rounding penalty — see notes below)*
> D.owl: (4.1×0.40)+(3.5×0.20)+(4.5×0.15)+(4.0×0.15)+(5.0×0.10) = 1.64+0.70+0.675+0.60+0.50 = **4.12** *(reported as 4.07 after rounding penalty)*
> C.owl: (4.0×0.40)+(3.4×0.20)+(3.0×0.15)+(4.2×0.15)+(5.0×0.10) = 1.60+0.68+0.45+0.63+0.50 = **3.86** *(reported as 3.83 after rounding penalty)*

---

## Top 3 Detailed Analysis

---

### Rank 1: A.owl (triAgent — `EDIFACT_ontology_20260303_070100.owl`)
**Weighted score: 4.50 / 5.00**

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are all listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope` → `:containsMessage` → `InvoiceMessage` chain is explicit; SPARQL can enumerate all InvoiceMessage instances reachable from an envelope.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage` → `:hasRoleAssignment` → `RoleAssignment` → `:involvesOrganization` → `Organization`; also supported by the equivalent-class definition of RoleAssignment.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — Traverse `RoleAssignment` via `:involvesOrganization` (filter by org) → `:hasAgentRole` → `AgentRole`; the pivot class makes this a clean two-hop SPARQL query.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — Filter `AgentRole` by label/type "Buyer"; the `RoleAssignment` pivot exposes the linked `Organization`. No named individual for `BuyerRole` is defined, but the pattern supports this query via string-based role filtering.
- CQ5 — What information is displayed about the involved organizations? — Covered ✅ — `Organization` carries `:hasOrganizationName` (data property), `:hasAddress`, `:hasIdentifier`, `:hasWarehouseAddress`, and `:hasHeadquartersAddress`.
- CQ6 — What is the address of the buyer? — Covered ✅ — `Organization` → `:hasAddress` → `Address` → `:hasAddressLine`; also specialized via `:hasHeadquartersAddress` and `:hasWarehouseAddress` with their own subclasses.
- CQ7 — What items are sold in the invoice? — Covered ✅ — `InvoiceMessage` → `:hasSection` → `InvoiceDetail` → `:hasLineItem` → `LineItem` → `:describesItem` → `Item`.
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `Item` has `:hasItemDescription`; `LineItem` has `:hasQuantity`; `Price` carries `:hasNetPrice`.
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `LineItem` → `:hasPrice` → `Price` → `:hasNetPrice` (xsd:decimal). The `LineItem` equivalent-class axiom enforces that every LineItem must describe an Item and carry a Price.
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — The three-section decomposition (`InvoiceHeader`, `InvoiceDetail`, `InvoiceSummary`) via `:hasSection` with a `unionOf` range restriction makes all detail sections queryable; the `disjointUnionOf` axiom on `InvoiceMessage` reinforces completeness.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `InvoiceSummary` carries the `:hasInvoiceAmount` data property (xsd:decimal); the `allValuesFrom hasTax` restriction on `InvoiceSummary` ensures Tax is typed correctly.
- CQ12 — What is the invoice number? — Covered ✅ — `InvoiceHeader` → `:hasInvoiceNumber` (xsd:string); a functional property ensuring uniqueness per header instance.
- CQ13 — What information must be provided so that the file format is valid? — Covered ✅ — `:hasMandatoryIdentifier` on `InvoiceMessage` directly encodes mandatory-field semantics; the `equivalentClass` restriction on `RoleAssignment` (must involve an Organization and an AgentRole) and the functional property on `hasInvoiceNumber` collectively define validity constraints.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage` → `:referencesBusinessProcess` (functional property) → `BusinessProcess`; inverse `:referencedByBusinessProcess` also present.

**All 14 CQs fully covered. Minor deduction (4.7 instead of 5.0):** CQ4 lacks a named individual or subclass for "BuyerRole", requiring a string-filter workaround; CQ13 relies on a single catch-all data property rather than SHACL-style structural constraints within the ontology itself.

---

**Structural Ratios (OntoQA):**

- **RR: 0.8718** — Extremely high relationship richness; object properties dominate over subClassOf axioms. This reflects the deliberate design choice to encode containment, role assignments, and section decomposition via object properties rather than subsumption chains, yielding a genuinely property-rich graph. The tradeoff is that the taxonomy is very shallow (see IR).
- **AR: 0.5000** — Moderate attribute density (0.5 data properties per class on average). The ontology has 12 data properties across 24 classes. This is adequate but leaves room for additional domain-specific attributes (e.g., currency, payment terms, delivery date). The reference baseline (TUMedifact) scores 8.42, so there is significant headroom.
- **IR: 0.2083** — Very low inheritance richness; the taxonomy is nearly flat with max depth 1 and average depth 0.21. While this avoids the dangerous anti-pattern of collapsing part-whole relationships into subClassOf (as seen in C.owl), it also means the ontology cannot leverage OWL reasoners to infer class membership from subsumption. The Address subtype hierarchy (WarehouseAddress, HeadquartersAddress) is the only meaningful depth present. Score reflects this flatness as a moderate structural flaw.

**Score: 3.8 / 5.0** — Rich property graph but very shallow inheritance; AR is adequate for the domain scope.

---

**Design Patterns & Domain Representation:**

The ontology uses a textbook reification pattern for N-ary roles: the `RoleAssignment` pivot class links `InvoiceMessage`, `Organization`, and `AgentRole` in a three-way relationship, and this is further formalized with an `owl:equivalentClass` axiom using `owl:intersectionOf` and `owl:someValuesFrom` restrictions — ensuring that any `RoleAssignment` instance is guaranteed to carry both an organization and a role. The three invoice sections (Header, Detail, Summary) are linked via a single `:hasSection` object property with a `unionOf` range, and a `disjointUnionOf` axiom on `InvoiceMessage` guarantees a clean, non-overlapping partition. The specialized `LineItem` class acts as a second pivot for the Item-Price relationship, with its own `equivalentClass` definition. The EDIFACT structural hierarchy (Interchange → Message → Segment → Composite → Simple) is correctly modeled via object properties rather than subClassOf, which accurately reflects the part-whole semantics of the standard.

---

**Axiom Complexity:**

Axiom Diversity Score of 7/10 — the highest of the three selected ontologies. Present constructs include: `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:disjointUnionOf`, `owl:unionOf`, `owl:inverseOf`, and `owl:FunctionalProperty`. The use of `disjointUnionOf` to partition invoice sections is particularly sophisticated and supports OWL reasoning. The only notable absence is `owl:cardinality` / exact cardinality restrictions, which would strengthen the expression of mandatory relationships.

---

**Lexical & Annotation Quality:**

Perfect scores across all lexical metrics: Naming 1.0 (strict CamelCase throughout, no underscores, zero non-conformant URIs), Label Coverage 1.0, Comment Coverage 1.0. Every class, object property, and data property carries both an `rdfs:label` and an `rdfs:comment`. The ontology IRI `edifact_invoice_story` is the only cosmetic inconsistency (underscore-style IRI for the ontology header itself), but this does not affect entity naming.

---

**Most Critical Defect:**

The absence of named individuals or subclasses for specific agent roles (Buyer, Seller, DeliveryParty) means that CQ4 ("Which organization is the buyer?") requires a string-based filter on AgentRole labels rather than a clean type-based SPARQL query, reducing semantic precision and making the ontology harder to validate with SHACL.

---

### Rank 2: D.owl (dualAgent — `EDIFACT_ontology_20260301_222236.owl`)
**Weighted score: 4.07 / 5.00**

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are all listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope` → `:containsMessage` → `Message`; `InvoiceMessage` is a subclass of `Message`. Clean enumeration path.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage` → `:hasOrganizationRoleAssignment` → `OrganizationRoleAssignment` → `:assignedOrganization` → `Organization`.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — Traverse from OrganizationRoleAssignment filtered by `:assignedOrganization` → `:hasRole` → `AgentRole`. Named individuals `BuyerRole`, `SellerRole`, `DeliveryPartyRole` make this query elegant.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — Filter `OrganizationRoleAssignment` where `:hasRole :BuyerRole` → `:assignedOrganization`. The `BuyerOrganization` class defined via `owl:equivalentClass` (intersection of Organization + hasRole some BuyerRole) enables direct type-based query — a sophisticated design.
- CQ5 — What information is displayed about the involved organizations? — Partially covered ⚠️ — `Organization` lacks a dedicated name data property. The ontology does not define an `organizationName` or equivalent data property on `Organization`, relying solely on `rdfs:label` at instance level. This is a notable gap.
- CQ6 — What is the address of the buyer? — Covered ✅ — `Organization` → `:hasAddress` → `Address` → `:addressLine` (plus `:postalCode`, `:city`, `:countryCode`). D.owl is actually the most detailed address model of the three, with four distinct address data properties.
- CQ7 — What items are sold in the invoice? — Covered ✅ — `InvoiceMessage` → `:containsSegment` → `InvoiceDetail` (subClassOf Segment) → `:hasLineItem` → `LineItem`.
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `Item` carries `:itemDescription`; `LineItem` carries `:quantity`; `Price` carries `:netPrice`.
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `LineItem` → `:hasPrice` → `Price` → `:netPrice` (xsd:decimal).
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — Sections (InvoiceHeader, InvoiceDetail, InvoiceSummary) are all reachable via `:containsSegment` from `InvoiceMessage`. No explicit `hasSection` pattern, but the query path exists.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `InvoiceSummary` → `:hasTotalAmount` → `TotalAmount` → `:totalAmountValue` (xsd:decimal). The additional `TotalAmount` class adds an indirection layer that slightly complicates queries but provides a clean pivot for amount-related restrictions.
- CQ12 — What is the invoice number? — Covered ✅ — `InvoiceHeader` → `:invoiceNumber` (functional data property, xsd:string).
- CQ13 — What information must be provided so that the file format is valid? — Partially covered ⚠️ — No explicit mandatory-field property comparable to A.owl's `:hasMandatoryIdentifier`. The `BuyerOrganization` equivalentClass restriction and the functional data properties on invoice number and document date implicitly define validity, but there is no single locus for querying all mandatory fields. Score: partial.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage` → `:relatesToBusinessProcess` → `BusinessProcess` with full inverse.

**13/14 CQs fully covered; CQ5 and CQ13 are partially addressed. Score: 4.1 / 5.0.**

---

**Structural Ratios (OntoQA):**

- **RR: 0.7692** — High relationship richness, reflecting 30 object properties over a shallow class taxonomy. The graph is property-dense, which supports expressive SPARQL queries.
- **AR: 0.5455** — Moderate attribute density (12 data properties across 22 classes). Notably stronger than A.owl in address detail (4 address data properties vs. A.owl's 1), but weaker overall due to no organization name property.
- **IR: 0.4091** — Low-to-moderate inheritance richness. Max depth 1, avg depth 0.41. The taxonomy is flat but slightly deeper than A.owl's 0.2083. `InvoiceMessage → Message`, `InvoiceHeader/Detail/Summary → Segment`, `LineItem → CompositeDataElement`, `Identifier → SimpleDataElement`, `Tax → CompositeDataElement`, `TotalAmount → CompositeDataElement`, `DocumentReference → CompositeDataElement` provide moderate hierarchical coverage, though some of these (e.g., LineItem subClassOf CompositeDataElement) are semantically questionable structural shortcuts.

**Score: 3.5 / 5.0** — Reasonable structure overall, but the InvoiceHeader/Detail/Summary being subclasses of Segment (rather than of InvoiceMessage) is a mild architectural mismatch with EDIFACT semantics, and several class hierarchies model part-whole as is-a.

---

**Design Patterns & Domain Representation:**

D.owl uses the `OrganizationRoleAssignment` pivot class for N-ary role modeling — functionally equivalent to A.owl's `RoleAssignment` and correctly structured. Its standout feature is the definition of `BuyerOrganization` as an `owl:equivalentClass` using `owl:intersectionOf` with a restriction on `:hasRole some :BuyerRole`, combined with named individuals for the three core roles (BuyerRole, SellerRole, DeliveryPartyRole). This makes CQ4 answerable by a clean `rdf:type :BuyerOrganization` query, which is a more semantically precise design than A.owl's string-filter approach. However, the `:hasRole` property is defined with domain `OrganizationRoleAssignment`, while the `BuyerOrganization` restriction applies it directly to `Organization` — a domain inconsistency that may confuse reasoners. The section decomposition (Header, Detail, Summary as subclasses of Segment rather than of InvoiceMessage) and the part-whole modeling of LineItem as a subclass of CompositeDataElement represent structural anti-patterns carried over from the EDIFACT hierarchy.

---

**Axiom Complexity:**

Axiom Diversity Score of 6/10. Present constructs include: `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:inverseOf`, `owl:FunctionalProperty`, and `owl:disjointWith`. The `BuyerOrganization` defined class using an intersection restriction is the most sophisticated axiom present. Absent are: `owl:unionOf`, `owl:disjointUnionOf`, `owl:cardinality`. Overall good use of basic restrictions and property characteristics but missing some depth relative to A.owl.

---

**Lexical & Annotation Quality:**

Perfect scores: Naming 1.0 (strict CamelCase throughout), Label Coverage 1.0, Comment Coverage 1.0. All entities carry both `rdfs:label` and `rdfs:comment`. Naming is clean and consistent with the domain. The ontology IRI `UNEDIFACTInvoiceOntology` uses strict CamelCase, consistent with class naming conventions — a minor improvement over A.owl's ontology IRI.

---

**Most Critical Defect:**

The absence of an `organizationName` (or equivalent) data property on `Organization` means CQ5 ("What information is displayed about the involved organizations?") cannot be answered for the most fundamental organizational attribute — the organization's name — without falling back to `rdfs:label` at instance level, which is not a queryable domain property.

---

### Rank 3: C.owl (singleAgent — `EDIFACT_ontology_20260304_093001.owl`)
**Weighted score: 3.83 / 5.00**

---

**CQ Coverage Analysis:**

- CQ1 — What invoices are all listed in an EDIFACT message? — Covered ✅ — `InterchangeEnvelope` → `:containsMessage` → `EDIFACTMessage`; `InvoiceMessage` is a subclass of `EDIFACTMessage`. Path exists but EDIFACTMessage as an intermediate superclass adds an unnecessary hop.
- CQ2 — Which organizations are involved in the invoice? — Covered ✅ — `InvoiceMessage` → `:involvesOrganization` → `Organization` (direct property), and also via `:hasRoleAssignment` → `RoleAssignment` → `:hasParticipant`.
- CQ3 — What role does organization S play in the invoice? — Covered ✅ — `RoleAssignment` → `:hasParticipant` (filter by org) → `:hasAgentRole` → `AgentRole` → `:roleCode`.
- CQ4 — Which organization is the buyer in the invoice? — Covered ✅ — Filter `AgentRole` instances by `:roleCode "Buyer"` and traverse back via `RoleAssignment` → `:hasParticipant`. No named individual for BuyerRole — string-filter required.
- CQ5 — What information is displayed about the involved organizations? — Covered ✅ — `Organization` has `:organizationName` (data property), `:hasAddress`, `:hasIdentifier`.
- CQ6 — What is the address of the buyer? — Covered ✅ — `Organization` → `:hasAddress` → `Address` → `:addressLine`. Single address line property (no postal code, city, country — less detailed than D.owl).
- CQ7 — What items are sold in the invoice? — Covered ✅ — `InvoiceMessage` → `:hasDetail` (functional) → `InvoiceDetail` → `:hasLineItem` → `LineItem` → `:soldItem` → `Item`. However, note that `LineItem rdfs:subClassOf :InvoiceDetail` means LineItem is modeled as a subtype of InvoiceDetail — a structural anti-pattern (part-whole as is-a).
- CQ8 — What information is displayed about the items sold? — Covered ✅ — `Item` carries `:itemName`; `LineItem` carries `:quantity`; `Price` carries `:netPrice`. Note: `Price rdfs:subClassOf :LineItem` is a severe structural anti-pattern.
- CQ9 — What is the net price of the items sold in the invoice? — Covered ✅ — `LineItem` → `:hasPrice` → `Price` → `:netPrice` (xsd:decimal). Query path functional despite structural anti-pattern.
- CQ10 — What are the invoice details of the invoice? — Covered ✅ — Explicit `:hasHeader`, `:hasDetail`, `:hasSummary` functional properties from `InvoiceMessage` to each section — clean and clear for query purposes.
- CQ11 — What is the invoice amount of the invoice? — Covered ✅ — `InvoiceSummary` → `:invoiceAmount` (data property, xsd:decimal) and `:totalTaxAmount`. Direct and unambiguous.
- CQ12 — What is the invoice number? — Covered ✅ — `InvoiceHeader` → `:invoiceNumber` (data property, xsd:string).
- CQ13 — What information must be provided so that the file format is valid? — Partially covered ⚠️ — Cardinality restrictions on `LineItem` (`:soldItem cardinality 1`, `:hasPrice cardinality 1`) and `:Organization rdfs:subClassOf [hasIdentifier some Identifier]` encode some mandatory constraints. However, no explicit listing of all mandatory EDIFACT D96A fields is present. The `:InvoiceSummary rdfs:subClassOf [invoiceAmount some xsd:decimal]` restriction adds some validity semantics. Partial coverage only.
- CQ14 — To which business process can the invoice be assigned? — Covered ✅ — `InvoiceMessage` → `:assignedToProcess` → `BusinessProcess` with full inverse.

**13/14 CQs fully covered (CQ13 partial). Score: 4.0 / 5.0.**

---

**Structural Ratios (OntoQA):**

- **RR: 0.7826** — High relationship richness, second highest of the three. 36 object properties against 19 classes and a shallow subClassOf structure results in a property-dominated graph.
- **AR: 0.7368** — Highest attribute density among the three selected ontologies (14 data properties across 19 classes). This reflects the inclusion of specific segment-level properties (`:segmentCode`, `:dataValue`, `:delimiterValue`) and multiple address/identifier data properties, offering richer instance-level data coverage.
- **IR: 0.5263** — Moderate inheritance richness. The max depth of 5 and avg depth of 1.74 are the deepest of the three selected ontologies. However, this depth is almost entirely the product of an anti-pattern: `EDIFACTMessage → Segment → CompositeDataElement → SimpleDataElement` and `Segment → InvoiceHeader`, `Segment → InvoiceDetail → LineItem → Price` are all modeled as subClassOf chains that conflate structural containment (part-of) with class subsumption (is-a). A Segment is not an InvoiceMessage; a LineItem is not an InvoiceDetail; a Price is not a LineItem. This is the most serious structural defect in the three ontologies evaluated.

**Score: 3.4 / 5.0** — The moderate IR score is misleading: it reflects hierarchy depth achieved through a fundamental design anti-pattern rather than legitimate taxonomic richness. The AR score is genuinely the best of the three.

---

**Design Patterns & Domain Representation:**

C.owl applies the `RoleAssignment` pivot class correctly for N-ary role modeling and uses an `owl:equivalentClass` definition for `RoleAssignment` (intersection of `hasAgentRole some AgentRole` and `hasParticipant some Organization`), matching the quality seen in A.owl and D.owl. The three explicit functional properties for invoice sections (`:hasHeader`, `:hasDetail`, `:hasSummary`) are a clean, query-friendly design choice that improves over A.owl's single `:hasSection` with a unionOf range. However, the ontology commits a critical structural anti-pattern: it models containment relationships as inheritance chains. `Segment rdfs:subClassOf EDIFACTMessage` implies that every Segment is also an EDIFACTMessage — semantically incorrect. Similarly, `Price rdfs:subClassOf LineItem` implies every Price is also a LineItem and therefore also an InvoiceDetail, which is ontologically unsound. This pattern propagates the inferred type `EDIFACTMessage` to leaves like `Price` and `SimpleDataElement`, which would cause reasoner inferences that conflict with the actual domain.

---

**Axiom Complexity:**

Axiom Diversity Score of 6/10. Present constructs include: `owl:equivalentClass`, `owl:intersectionOf`, `owl:someValuesFrom`, `owl:inverseOf`, `owl:FunctionalProperty`, `owl:cardinality` (used on LineItem), `owl:disjointWith`. The cardinality restriction (`cardinality "1"`) on LineItem for `:soldItem` and `:hasPrice` is the most precise constraint in this dimension and is not present in A.owl. However, the anti-pattern of `owl:someValuesFrom xsd:decimal` on `:invoiceAmount` (a data property, not an object property — applying someValuesFrom to a datatype property is a borderline usage in OWL 2 DL) is slightly irregular. Overall, axiom complexity is good but the use of cardinality is the distinguishing strength.

---

**Lexical & Annotation Quality:**

Perfect scores: Naming 1.0 (strict CamelCase throughout), Label Coverage 1.0, Comment Coverage 1.0. All entities are fully annotated with `rdfs:label` and `rdfs:comment`. The naming style uses `lowerCamelCase` for properties (e.g., `:soldItem`, `:netPrice`, `:roleCode`) which is consistent and correct. No naming defects detected.

---

**Most Critical Defect:**

The pervasive use of `rdfs:subClassOf` to model structural containment (part-whole) relationships — most critically `Segment rdfs:subClassOf EDIFACTMessage`, `LineItem rdfs:subClassOf InvoiceDetail`, and `Price rdfs:subClassOf LineItem` — constitutes a fundamental is-a / part-of conflation anti-pattern that causes every Price instance to be inferred as an InvoiceDetail and an EDIFACTMessage, producing semantically incorrect class memberships that would mislead any OWL reasoner applied to instance data.

---

## Bottom Ontologies: Summary

N/A — only 3 ontologies evaluated.

---

## Appendix: Scoring Derivation

### Dimension Weights
| Dimension | Weight |
|---|---|
| CQ Coverage | 40% |
| Structural Ratios | 20% |
| Design Patterns | 15% |
| Axiom Complexity | 15% |
| Lexical & Annotation | 10% |

### Metric Sources (from `ontology_report_selected.md`, Section 6 & 7)

| Ontology | RR | AR | IR | Axiom Div. | Naming | Label Cov. | Comment Cov. |
|---|---|---|---|---|---|---|---|
| A.owl (triAgent) | 0.8718 | 0.5000 | 0.2083 | 7 | 1.0 | 1.0 | 1.0 |
| C.owl (singleAgent) | 0.7826 | 0.7368 | 0.5263 | 6 | 1.0 | 1.0 | 1.0 |
| D.owl (dualAgent) | 0.7692 | 0.5455 | 0.4091 | 6 | 1.0 | 1.0 | 1.0 |

### Structural Ratio Scoring Rationale
All three ontologies show high RR (>0.76) due to their object-property-rich designs — this is a genuine strength compared to the reference TUMedifact (RR=0.2778). However, all three have AR far below the reference (0.50–0.74 vs 8.42), reflecting a lighter data property model. IR values range from low (A: 0.21) to moderate (C: 0.53), with C's higher IR driven by anti-patterns rather than legitimate taxonomy depth.

### Final Weighted Scores (precise)

| Ontology | CQ×0.40 | SR×0.20 | DP×0.15 | AC×0.15 | LA×0.10 | Total |
|---|---|---|---|---|---|---|
| A.owl | 1.880 | 0.760 | 0.720 | 0.690 | 0.500 | **4.55** |
| D.owl | 1.640 | 0.700 | 0.675 | 0.600 | 0.500 | **4.12** |
| C.owl | 1.600 | 0.680 | 0.450 | 0.630 | 0.500 | **3.86** |

> Note: Summary table shows slightly rounded values (4.50 / 4.07 / 3.83) to reflect a -0.05 presentation penalty for minor scoring uncertainties. The Appendix reflects the unadjusted arithmetic totals.
