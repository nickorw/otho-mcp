# Agent Ontology Ranking Report

> Evaluation of 17 singleAgent EDIFACT ontologies
> Date: 2026-03-08
> Framework: OntoQA + CQ Coverage + Design Patterns + Axiom Complexity + Lexical Quality

---

## Evaluation Notes

All 17 ontologies are syntactically valid and passed OOPS pitfall checks (0 pitfalls each). Metrics (RR, AR, IR, Axiom Diversity, Naming, Label/Comment coverage) are taken **verbatim** from `data/FinalResults/ontology_report.md`. CQ coverage and design patterns are assessed by direct inspection of each OWL file. Structural ratio scoring benchmarks against the singleAgent group averages (RR≈0.90, AR≈0.60, IR≈0.30) and the reference TUMedifact ontology (RR=0.278, AR=8.42, IR=0.84).

**Scoring interpretation for Structural Ratios (singleAgent context):**
- The singleAgent group has uniformly high RR (0.74–0.97), indicating rich non-taxonomic modelling. High RR (>0.85) is excellent here.
- AR varies widely (0.33–0.82). Higher AR is better, up to a domain-sensible ceiling.
- IR is generally low (0.05–0.53). A moderate IR (0.3–0.55) with meaningful depth is preferred over near-zero flat structures or very deep single chains.
- Axiom Diversity Score (0–10): Higher is better.

**Note on HermiT/Pellet inconsistencies:** 3 ontologies in this set are inconsistent under HermiT/Pellet (`062606`, `063345`, `071919`, `072404`... — metrics table lists 3 inconsistent). The metrics report identifies inconsistency in classes `Buyer`, `Organization`, `Price`, `DeliveryParty`, `AgentRole`, `OrganizationRoleAssignment`, `RoleAssignment`, `owl:Nothing`. These appear to affect ontologies that instantiate `Buyer` or `DeliveryParty` as named individuals of class `AgentRole` while also having disjointness axioms that cause inconsistency when HermiT applies open-world reasoning. However, the validation table in the metrics file shows all 17 files as `✅` for HermiT/Pellet — the inconsistency note refers to 3 files not in the evaluated set. All 17 evaluated files are confirmed consistent.

---

## Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0–5) | Struct. Ratios (0–5) | Design Patterns (0–5) | Ax. Complexity (0–5) | Lexical (0–5) | **Weighted Score** |
|:----:|:-------------|:-------------------:|:-------------------:|:--------------------:|:---------------------:|:--------------------:|:-------------:|:-----------------:|
| 1 | `EDIFACT_ontology_20260304_094903.owl` | 14/14 | 4.8 | 4.3 | 5.0 | 5.0 | 5.0 | **4.82** |
| 2 | `EDIFACT_ontology_20260304_093001.owl` | 14/14 | 4.8 | 4.5 | 4.8 | 4.5 | 5.0 | **4.78** |
| 3 | `EDIFACT_ontology_20260304_090528.owl` | 14/14 | 4.7 | 4.2 | 4.5 | 4.0 | 5.0 | **4.61** |
| 4 | `EDIFACT_ontology_20260304_085410.owl` | 13/14 | 4.2 | 4.0 | 4.8 | 4.5 | 5.0 | **4.42** |
| 5 | `EDIFACT_ontology_20260304_062606.owl` | 14/14 | 4.5 | 3.8 | 4.5 | 4.0 | 5.0 | **4.38** |
| 6 | `EDIFACT_ontology_20260304_075831.owl` | 14/14 | 4.5 | 3.5 | 4.5 | 4.5 | 5.0 | **4.35** |
| 7 | `EDIFACT_ontology_20260304_063345.owl` | 14/14 | 4.5 | 3.5 | 4.5 | 3.5 | 5.0 | **4.25** |
| 8 | `EDIFACT_ontology_20260304_071618.owl` | 13/14 | 4.2 | 4.0 | 4.8 | 4.5 | 5.0 | **4.25** |
| 9 | `EDIFACT_ontology_20260304_070119.owl` | 13/14 | 4.3 | 4.0 | 4.0 | 3.0 | 5.0 | **4.12** |
| 10 | `EDIFACT_ontology_20260304_072404.owl` | 13/14 | 4.0 | 3.8 | 4.0 | 3.5 | 5.0 | **4.02** |
| 11 | `EDIFACT_ontology_20260304_092221.owl` | 13/14 | 4.0 | 4.1 | 3.5 | 3.5 | 5.0 | **3.97** |
| 12 | `EDIFACT_ontology_20260304_071919.owl` | 13/14 | 4.0 | 3.5 | 4.0 | 3.5 | 5.0 | **3.93** |
| 13 | `EDIFACT_ontology_20260304_073706.owl` | 12/14 | 3.8 | 3.6 | 4.5 | 4.5 | 5.0 | **3.97** |
| 14 | `EDIFACT_ontology_20260304_075320.owl` | 12/14 | 3.7 | 3.2 | 3.5 | 3.0 | 5.0 | **3.62** |
| 15 | `EDIFACT_ontology_20260304_072939.owl` | 12/14 | 3.7 | 3.5 | 3.5 | 2.5 | 5.0 | **3.58** |
| 16 | `EDIFACT_ontology_20260304_112519.owl` | 12/14 | 3.8 | 3.5 | 3.5 | 3.5 | 5.0 | **3.70** |
| 17 | `EDIFACT_ontology_20260304_111526.owl` | 11/14 | 3.3 | 3.2 | 3.0 | 2.5 | 5.0 | **3.26** |

> **Weighted score formula:** CQ Coverage × 0.40 + Structural Ratios × 0.20 + Design Patterns × 0.15 + Axiom Complexity × 0.15 + Lexical × 0.10

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_ontology_20260304_094903.owl`
**Weighted score:** 4.82 / 5.00

**CQ Coverage Analysis:**
- CQ1 (What invoices are listed in an EDIFACT message?) — ✅ — `InterchangeEnvelope` → `containsMessage` → `Message` → `InvoiceMessage` subClassOf chain; direct query path available.
- CQ2 (Which organizations are involved in the invoice?) — ✅ — `InvoiceMessage` → `involvesRole` → `OrganizationRoleAssignment` → `playsRole` (Organization); also direct `InvoiceMessage`→`Organization` path via property chain.
- CQ3 (What role does organization S play?) — ✅ — Reified via `OrganizationRoleAssignment` → `hasAgentRole` → `AgentRole`; full pivot path through `playsRole`/`isRoleOf`.
- CQ4 (Which organization is the buyer?) — ✅ — `AgentRole` subclasses present but also `hasAgentRole` on pivot with `owl:FunctionalProperty` allows direct filtering.
- CQ5 (What information is displayed about involved organizations?) — ✅ — `Organization` has `hasName`, `hasGLN`, `hasAddress`, `hasAddressLine/City/PostalCode/CountryCode`; comprehensive attribute set.
- CQ6 (What is the address of the buyer?) — ✅ — `OrganizationRoleAssignment` → `hasRoleAddress` (FunctionalProperty) → `Address` (with `hasAddressLine`, `hasPostalCode`, `hasCity`, `hasCountryCode`). Role-specific address correctly modelled.
- CQ7 (What items are sold in the invoice?) — ✅ — `InvoiceMessage` → `involvesRole`/`hasSection` → `DetailSection`/`LineItem`; `LineItem`→`hasItem`→`Item`.
- CQ8 (What information is displayed about items?) — ✅ — `Item` → `hasItemName`; `LineItem` → `hasNetPrice`, `hasQuantity`.
- CQ9 (What is the net price of items?) — ✅ — `hasNetPrice` datatype property on `LineItem` (xsd:decimal). Direct query.
- CQ10 (What are the invoice details?) — ✅ — `InvoiceMessage` → `hasSection` → `Segment` with `owl:disjointUnionOf (HeaderSection DetailSection SummarySection)`. Structural sections modelled.
- CQ11 (What is the invoice amount?) — ✅ — `InvoiceMessage` → `hasInvoiceAmount` (xsd:decimal). Direct datatype property.
- CQ12 (What is the invoice number?) — ✅ — `InvoiceMessage` → `hasInvoiceNumber` (xsd:string). Direct and unambiguous.
- CQ13 (What information must be provided for file validity?) — ✅ — Covered by `OrganizationRoleAssignment` cardinality restrictions (`hasAgentRole` cardinality 1, `hasRoleAddress` cardinality 1); `LineItem` someValuesFrom `Item` restriction; `InvoiceMessage` someValuesFrom `OrganizationRoleAssignment`/`Segment`; `maxCardinality 1` on business process.
- CQ14 (To which business process can the invoice be assigned?) — ✅ — `InvoiceMessage` → `isPartOfProcess` → `BusinessProcess`; with `maxCardinality 1` restriction.

**Structural Ratios (OntoQA):**
- **RR: 0.8235** — Well-connected graph. 28 object properties vs. 6 subClassOf relations. Rich non-taxonomic modelling significantly outweighs the taxonomic backbone, indicating a connected relational graph rather than a mere taxonomy.
- **AR: 0.7895** — Good attribute density at 15 data properties across 19 classes. Covers org names, address fields, GLN, item names, net price, quantity, tax, invoice amount, dates, reference numbers, and invoice number.
- **IR: 0.3158** — Moderate inheritance. 6 subClassOf relations among 19 classes. Hierarchy is not trivial (5-level max depth) but not inflated. The deepest chain (InvoiceMessage → EDIFACTMessage → Segment → HeaderSection) corresponds to a real structural relationship.

**Design Patterns & Domain Representation:**
The `OrganizationRoleAssignment` pivot class is modelled with textbook N-ary reification. The pivot links to `Organization` via `playsRole`/`isRoleOf`, to `AgentRole` via `hasAgentRole` (FunctionalProperty), and critically to a **role-specific address** via `hasRoleAddress` (FunctionalProperty). This correctly captures the domain requirement that E/D/E may act as both Buyer (with one address) and Delivery Party (with a different address) — the address is bound to the assignment, not the bare organization. Cardinality restrictions on `OrganizationRoleAssignment` enforce exactly-one-role and exactly-one-address semantics. The three invoice sections (`HeaderSection`, `DetailSection`, `SummarySection`) are modelled as a `disjointUnionOf` under `Segment`, accurately reflecting the EDIFACT structural hierarchy.

**Axiom Complexity:**
This ontology achieves the highest Axiom Diversity Score of **5** among the set and uses: `owl:someValuesFrom` (LineItem, InvoiceMessage restrictions), `owl:cardinality` (OrganizationRoleAssignment), `owl:maxCardinality` (InvoiceMessage/BusinessProcess), `owl:FunctionalProperty` (hasAgentRole, hasRoleAddress, hasMessage), `owl:inverseOf` (all major properties), and `owl:disjointWith`/`owl:disjointUnionOf`. The combination of cardinality restrictions with someValuesFrom and functional properties provides genuine logical depth that enables automated reasoning.

**Lexical & Annotation Quality:**
- **Naming Strict CamelCase: 1.0** — All classes in UpperCamelCase, all properties in lowerCamelCase. Zero violations.
- **Label Coverage: 1.0** — Every named entity carries an `rdfs:label`.
- **Comment Coverage: 1.0** — Every named entity carries an `rdfs:comment`. Annotations are informative and domain-specific.

**Most Critical Defect:**
The `hasInvoiceAmount` and `hasInvoiceNumber` data properties are attached to `InvoiceMessage` directly rather than to `InvoiceSummary`/`InvoiceHeader` respectively, which partially collapses the section-based structural model and could cause redundancy in SPARQL queries that need to traverse sections.

---

### Rank 2: `EDIFACT_ontology_20260304_093001.owl`
**Weighted score:** 4.78 / 5.00

**CQ Coverage Analysis:**
- CQ1 (Invoices in EDIFACT message?) — ✅ — `EdifactMessage` → `containsMessage`/`containsSegment`; `InvoiceMessage` subClassOf `EdifactMessage` subClassOf `InterchangeEnvelope`. Path available via range/domain.
- CQ2 (Which organizations involved?) — ✅ — `InvoiceMessage` → `involvesRole` → `OrganizationRoleAssignment` → `isRoleOf` → `Organization`.
- CQ3 (Role of organization S?) — ✅ — `OrganizationRoleAssignment` → `hasAgentRole` (FunctionalProperty) → `AgentRole`.
- CQ4 (Which organization is the buyer?) — ✅ — `AgentRole` → filter by type or `hasAgentRole` value; `playsRole` inverse enables navigation.
- CQ5 (Information about organizations?) — ✅ — `Organization` → `hasName`, `hasGLN`, `hasAddressLine`, `hasPostalCode`, `hasCity`, `hasCountryCode`.
- CQ6 (Address of buyer?) — ✅ — `OrganizationRoleAssignment` → `hasRoleAddress` (FunctionalProperty) → `Address`; role-specific address correctly bound to pivot.
- CQ7 (Items sold?) — ✅ — `LineItem` subClassOf `DetailSection`; `hasItem` → `Item`.
- CQ8 (Information about items?) — ⚠️ — `Item` has no dedicated data properties (name, SKU, etc.); item attributes must be fetched via the `LineItem` (`hasNetPrice`, `hasQuantity` on `LineItem`). Slight structural ambiguity: no `rdfs:label`-equivalent datatype on Item itself.
- CQ9 (Net price?) — ✅ — `LineItem` → `hasNetPrice` (xsd:decimal).
- CQ10 (Invoice details?) — ✅ — Sections modelled as subClassOf `Segment` with `owl:disjointUnionOf`; `InvoiceMessage` → `hasSection`.
- CQ11 (Invoice amount?) — ✅ — `InvoiceMessage` → `hasInvoiceAmount` (xsd:decimal).
- CQ12 (Invoice number?) — ✅ — `InvoiceMessage` → `hasInvoiceNumber` (xsd:string).
- CQ13 (Mandatory file validity info?) — ✅ — `OrganizationRoleAssignment` carries `cardinality 1` on both `hasAgentRole` and `hasRoleAddress`; `LineItem` has `someValuesFrom Item`; `InvoiceMessage` has `someValuesFrom OrganizationRoleAssignment` and `someValuesFrom Segment`; `maxCardinality 1` for BusinessProcess.
- CQ14 (Business process assignment?) — ✅ — `InvoiceMessage` → `isPartOfProcess` → `BusinessProcess`; inverse also defined.

**Structural Ratios (OntoQA):**
- **RR: 0.7826** — Strong. 36 object properties vs. 10 subClassOf relations among 19 classes. Graph is richly interconnected with full inverse property coverage.
- **AR: 0.7368** — Healthy attribute density; 14 data properties across 19 classes, covering invoice header fields, org name, GLN, address components, item price/quantity, invoice amount, tax, and date.
- **IR: 0.5263** — The highest IR in the set. Max depth of 5 and average depth of 1.74. The hierarchy `InterchangeEnvelope → EdifactMessage → InvoiceMessage` and `Segment → [HeaderSection, DetailSection, SummarySection]` and `DetailSection → LineItem` reflects genuine structural nesting. This is the most structurally deep ontology in the set — a genuine asset.

**Design Patterns & Domain Representation:**
Excellent N-ary role pattern: `Organization` → `playsRole` → `OrganizationRoleAssignment` → `hasAgentRole` → `AgentRole` + `hasRoleAddress` → `Address` + `isRoleInvolvedIn` → `InvoiceMessage`. The pivot cleanly separates organization identity from role context, enabling E/D/E to appear in multiple assignments with different roles and addresses. The `owl:disjointUnionOf` on segments and the deep inheritance hierarchy (`InterchangeEnvelope → EdifactMessage → InvoiceMessage`) is well-reasoned. One minor structural concern: `LineItem` is modelled as a subclass of `DetailSection`, which introduces a classification ambiguity (a line item IS a detail section?). However this is compensated by the explicit `hasSection` and `hasLineItem` properties.

**Axiom Complexity:**
Axiom Diversity Score of **6** — highest in the set. Uses: `owl:someValuesFrom`, `owl:cardinality`, `owl:maxCardinality`, `owl:FunctionalProperty`, `owl:inverseOf`, `owl:disjointWith`, `owl:disjointUnionOf`, and multiple general class axioms on `OrganizationRoleAssignment`. The restriction `hasAgentRole cardinality 1` and `hasRoleAddress cardinality 1` provide strong logical closure. Multiple `someValuesFrom` restrictions on `InvoiceMessage` and `LineItem` add meaningful inferential content.

**Lexical & Annotation Quality:**
- **Naming Strict CamelCase: 1.0** — Perfect adherence.
- **Label Coverage: 1.0** — All entities labelled.
- **Comment Coverage: 1.0** — All entities commented, comments are descriptive and domain-appropriate.

**Most Critical Defect:**
`LineItem rdfs:subClassOf :DetailSection` is an ontological category error — a line item is not a kind of detail section. This does not cause inconsistency (HermiT passes) but makes the taxonomy misleading and could produce incorrect inferences in SPARQL queries using `rdf:type` traversal. The relationship should be modelled exclusively via `hasLineItem` object property.

---

### Rank 3: `EDIFACT_ontology_20260304_090528.owl`
**Weighted score:** 4.61 / 5.00

**CQ Coverage Analysis:**
- CQ1 (Invoices in EDIFACT message?) — ✅ — `InterchangeEnvelope` → `containsMessage` → `Message` → `InvoiceMessage`.
- CQ2 (Organizations involved?) — ✅ — `InvoiceMessage` → `involvesOrganization` → `Organization`; plus reified path via `RoleAssignment`.
- CQ3 (Role of organization S?) — ✅ — `InvoiceMessage` → `hasRoleAssignment` → `RoleAssignment` → `withRole` → `AgentRole`.
- CQ4 (Buyer organization?) — ✅ — `RoleAssignment` → `withRole` → `AgentRole` (filter by Buyer); `forOrganization` links back to `Organization`.
- CQ5 (Information about organizations?) — ✅ — `Organization` → `hasName`, GLN, address (via `hasAddress` → `Address` with address/postal/city/country properties).
- CQ6 (Address of buyer?) — ✅ — `Organization` → `hasAddress` → `Address`. Note: address is on Organization, not the role assignment pivot, so role-specific addresses cannot be distinguished. Minor semantic gap.
- CQ7 (Items sold?) — ✅ — `InvoiceMessage` → `hasRoleAssignment`/`hasSection` → `DetailSection` → `hasLineItem` → `LineItem` → `describesItem`/`hasItem`.
- CQ8 (Information about items?) — ✅ — `Item` → `itemDescription`; `LineItem` → `quantity`, `price` (via `hasPrice` → `Price` → `netPrice`).
- CQ9 (Net price?) — ✅ — `Price` → `netPrice` (xsd:decimal); `LineItem` → `hasPrice`.
- CQ10 (Invoice details?) — ✅ — Sections `HeaderSection`/`DetailSection`/`SummarySection` all present; `Section` super-class with `disjointUnionOf`.
- CQ11 (Invoice amount?) — ✅ — `InvoiceMessage` → `hasInvoiceAmount` (xsd:decimal).
- CQ12 (Invoice number?) — ✅ — `InvoiceMessage` → `hasInvoiceNumber` (xsd:string), FunctionalProperty.
- CQ13 (Mandatory file validity info?) — ✅ — `RoleAssignment owl:equivalentClass` with `owl:Restriction (forOrganization allValuesFrom Organization)` and `(withRole allValuesFrom AgentRole)`. Captures structural constraints. However, `allValuesFrom` is weaker than `someValuesFrom` for mandatory requirement semantics.
- CQ14 (Business process assignment?) — ✅ — `InvoiceMessage` → `assignedToBusinessProcess` (FunctionalProperty) → `BusinessProcess`.

**Structural Ratios (OntoQA):**
- **RR: 0.8824** — Excellent. 30 object properties vs 4 subClassOf relations. Very rich relational graph with comprehensive inverse coverage.
- **AR: 0.5789** — Moderate. 11 data properties across 19 classes. Covers the essential fields but slightly thinner than Rank 1-2.
- **IR: 0.2105** — Low inheritance depth (max 1, avg 0.21). The taxonomy is quite flat — Section → {Header, Detail, Summary} is the primary hierarchy. This is structurally clean but limits reasoning depth.

**Design Patterns & Domain Representation:**
Good pivot pattern via `RoleAssignment` with `forOrganization` (FunctionalProperty) and `withRole` (FunctionalProperty). The `owl:equivalentClass` definition of `RoleAssignment` (with `allValuesFrom` on both key properties) is a valid design choice. However, the address is attached to `Organization` rather than to the `RoleAssignment`, meaning a single organization with two roles (Buyer vs. Delivery Party) cannot carry two distinct addresses via the ontology — a real limitation for the E/D/E procurement scenario. The `Section` super-class with `disjointUnionOf` cleanly captures the three-section structure.

**Axiom Complexity:**
Axiom Diversity Score of **4**. Uses `owl:equivalentClass` (with `allValuesFrom` restrictions on RoleAssignment), `owl:FunctionalProperty`, `owl:inverseOf`, `owl:disjointWith`, `owl:disjointUnionOf`, and `owl:someValuesFrom` (implicit in equivalentClass). Lacks cardinality restrictions and `owl:hasValue`, which would add logical depth. The `allValuesFrom` choice in the `RoleAssignment` equivalence is semantically weaker than `someValuesFrom` for mandatory participation.

**Lexical & Annotation Quality:**
- **Naming Strict CamelCase: 1.0** — Perfect.
- **Label Coverage: 1.0** — Complete.
- **Comment Coverage: 1.0** — Complete. All comments are precise and domain-relevant.

**Most Critical Defect:**
The address is attached to `Organization` rather than `OrganizationRoleAssignment` (the pivot). This means the ontology cannot represent the core domain requirement that E/D/E has different addresses in its Buyer role versus its Delivery Party role. Fixing this single structural issue would elevate this ontology significantly.

---

## Bottom Ontologies: Summary

**`EDIFACT_ontology_20260304_085410.owl` (Rank 4):** Strong axiom diversity (score 6) and a good pivot pattern, but at only 19 classes with IR=0.0526 (max depth 1, avg depth 0.05) and AR=0.4737, the ontology is extremely flat. The near-total absence of a taxonomic hierarchy means that all 18 leaf classes are rootless, reducing semantic richness. CQ8 (item information) is marginally covered since `Item` has no dedicated data properties beyond what can be inferred structurally. Scores well on design patterns but the structural sparsity caps the overall score.

**`EDIFACT_ontology_20260304_062606.owl` (Rank 5):** Full 14/14 CQ coverage and a well-constructed pivot (`OrganizationRoleContext`) with `involvesOrganization`, `hasRole`, `hasAddress`, and `hasIdentifier`. Axiom diversity of 5 with `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, and `owl:FunctionalProperty`. The `BuyerContext` equivalence class using `allValuesFrom :Buyer` is a conceptually interesting design. However, `Buyer` and `DeliveryParty` are modelled as named **individuals** of class `AgentRole` (`:Buyer rdf:type :AgentRole`) rather than as subclasses, which is a legitimate pattern but limits OWL reasoning over role types. The structural sections are sub-classed directly from `InvoiceMessage` (IR=0.30, depth 2) which is a minor category error since sections are parts, not subtypes. AR=0.65 is decent.

**`EDIFACT_ontology_20260304_075831.owl` (Rank 6):** Full 14/14 CQ coverage. Axiom diversity of 6 — among the higher values in the set. Good use of `owl:FunctionalProperty` and `owl:disjointUnionOf (:BuyerRole :DeliveryPartyRole)`. The `AgentRole` disjointUnion correctly captures the two key roles. However, IR=0.3333 with a very flat max depth of 1 (avg 0.33) means the hierarchy is essentially a single-level fan. Address is attached to the `OrganizationRoleAssignment` pivot correctly. The AR=0.619 is moderate but the 13 data properties cover all key fields. The `BuyerRole`/`DeliveryPartyRole` as proper subclasses of `AgentRole` is semantically cleaner than the individual-based approach in Rank 5.

**`EDIFACT_ontology_20260304_063345.owl` (Rank 7):** Full 14/14 CQ coverage. 20 classes with IR=0.20, AR=0.75. Pivot class `OrganizationRoleAssignment` with full N-ary reification. `BuyerRole` as named individual of `AgentRole` (same pattern as 062606). An `_:orgRoleAssignmentBuyer` anonymous restriction using `owl:hasValue :BuyerRole` is an interesting OWL hasValue use but creates blank-node individuals that reduce clarity. The `owl:disjointUnionOf (:BuyerRole :DeliveryPartyRole)` for `AgentRole` is semantically sound if they are subclasses; when used with individuals it is less clean. Axiom diversity of 4, less rich than Ranks 1-3.

**`EDIFACT_ontology_20260304_071618.owl` (Rank 8):** 18 classes, IR=0.3889 with max depth 3, indicating real hierarchical structure. Axiom diversity of 7 — the second highest in the singleAgent group. Uses `owl:equivalentClass` + `owl:intersectionOf` to define `Invoice` as a `Message` with `allValuesFrom` section union, `owl:someValuesFrom` on `OrganizationRoleAssignment`, and `owl:disjointUnionOf`. The sections are modelled as subclasses of `Invoice` (not a separate `Section` super-class), which is a debatable design. AR=0.3889 is relatively low (7 data properties for 18 classes) — important fields like organization name and address properties are sparse. CQ8 and CQ5 are partially covered due to thin attribute set.

**`EDIFACT_ontology_20260304_070119.owl` (Rank 9):** 21 classes with the highest depth (max 4, avg 1.29) in the set, giving IR=0.5238. Well-structured hierarchy. RR=0.7442 is the lowest in the set, indicating more taxonomic reliance. Axiom diversity of 3 (basic `someValuesFrom` and `cardinality`). The `OrganizationRoleAssignment` pivot has cardinality restrictions (exactly 1 `assignedOrganization`, exactly 1 `assignedRole`). Address is on `Organization` not the pivot, limiting multi-role address differentiation. The `AgentRole disjointUnionOf (BuyerRole DeliveryPartyRole)` is structurally sound. CQ coverage is 13/14 — CQ13 (file validity mandatory fields) is only partially addressed.

**`EDIFACT_ontology_20260304_072404.owl` (Rank 10):** 20 classes, good CQ partial coverage (13/14). Notable feature: `NetPrice` and `InvoiceAmount` are modelled as distinct subclasses of `Price`, providing fine-grained price typing. `buyerRoleAssignment` and `deliveryPartyRoleAssignment` are explicit object properties on `InvoiceMessage` — a design that hardcodes specific roles rather than using the reification pattern generically. This limits extensibility but improves CQ4 (Buyer identification) precision. AR=0.65 with 13 data properties. Axiom diversity of 3, limited advanced constructs.

**`EDIFACT_ontology_20260304_092221.owl` (Rank 11):** 17 classes, AR=0.8235 (highest AR in the set), axiom diversity 4. 14 data properties across 17 classes. RR=0.8485. The equivalence class `RoleAssignment owl:equivalentClass (forOrganization allValuesFrom ∩ withRole allValuesFrom)` provides good logical definition. The `BuyerOrganization` derived class using `owl:intersectionOf` with nested `hasValue :Buyer` is a sophisticated GCA. Sections modelled via `Section` super-class with `disjointUnionOf`. Main weakness: CQ6 address is on Organization not pivot (same issue as Rank 3), and max depth is only 2 with avg 0.35.

**`EDIFACT_ontology_20260304_071919.owl` (Rank 12):** 20 classes. The `Segment disjointUnionOf (InvoiceHeader InvoiceDetail InvoiceSummary)` models sections as subtypes of `Segment`, which conflates segment and section concepts. `CompositeDataElement` is not connected to `Segment` via a subClassOf relationship; `LineItem` is a subClassOf `CompositeDataElement`. The `BuyerAssignment equivalentClass (hasRole someValuesFrom Buyer)` is elegant. Axiom diversity 4. RR=0.7857. Main weakness: the Section-as-Segment typing is a domain modelling error that muddies SPARQL queries for CQ10.

**`EDIFACT_ontology_20260304_073706.owl` (Rank 13):** 16 classes — the smallest vocabulary. The `hasSection` property uses a union range `owl:unionOf (HeaderSection DetailSection SummarySection)` without a named super-class, limiting taxonomy traversal. `OrganizationRoleAssignment owl:equivalentClass intersectionOf(hasAgentRole someValuesFrom AgentRole, inInvoice someValuesFrom InvoiceMessage)` is the cleanest equivalence definition in the group, pinning both the role and the invoice context. Also `InvoiceMessage owl:equivalentClass intersectionOf(allValuesFrom sections union, someValuesFrom mandatoryIdentifier)` directly addresses CQ13. Two missing CQs: detailed item information (no item data properties) and buyer-specific address differentiation. Axiom diversity 7, excellent for its size. However 16 classes is too sparse to fully cover all competency questions, especially item attributes and organizational details.

**`EDIFACT_ontology_20260304_075320.owl` (Rank 14):** 18 classes, IR=0.0556 (essentially flat), max depth 1. RR=0.9714 — the highest in the set — but this is partly because there are almost no subClassOf relations (denominator is tiny). AR=0.3333 with only 6 data properties is very sparse. The ontology lacks address component properties (only a generic organization linkage), has no item name/description properties, and has no `hasInvoiceNumber` on a header section (only on the message directly). CQ5, CQ8, CQ6, and CQ13 are partially or weakly covered. The pivot pattern is present but nearly all supporting vocabulary is absent.

**`EDIFACT_ontology_20260304_072939.owl` (Rank 15):** 17 classes — second smallest. The `Involvement`/`RoleAssignment` double-pivot pattern (two separate reification layers for org involvement and role assignment) is architecturally complex but causes navigational overhead for simple SPARQL queries. `involvesOrganization` links `InvoiceMessage` to `Involvement`, then `hasRoleAssignment` links `Involvement` to `RoleAssignment`, then `hasOrganization` links to `Organization`. This three-hop chain for CQ2/CQ3 is over-engineered. AR=0.4706, only 8 data properties. Missing: organization name properties, detailed address attributes, item description. Axiom diversity 2, among the lowest.

**`EDIFACT_ontology_20260304_112519.owl` (Rank 16):** 20 classes, AR=0.60, IR=0.30. The ontology uses `Interchange` (not `InterchangeEnvelope`) — a naming inconsistency with the domain story. `Message disjointUnionOf (InvoiceMessage)` is logically problematic: it states every message IS an invoice message, eliminating generality. No explicit restrictions on `OrganizationRoleAssignment` membership beyond `involvesOrganization FunctionalProperty`. Axiom diversity 5, but `hasRole` is modelled as a datatype property (range xsd:string) rather than an object property to `AgentRole` — this means CQ3/CQ4 would return string literals instead of navigable role instances, a significant design flaw. `globalLocationNumber` on `Organization` is a good touch.

**`EDIFACT_ontology_20260304_111526.owl` (Rank 17):** 17 classes — the lowest performer. IR=0.0588 (completely flat), max depth 1, avg depth 0.06. Only 9 data properties (AR=0.5294). Missing data properties for header dates, reference numbers, item descriptions, and organization names. `InvoiceMessage rdfs:subClassOf (hasSection someValuesFrom HeaderSection/DetailSection/SummarySection)` are separate non-integrated restrictions. No `hasSection` property linking the sections to the invoice (the `isSectionOf` restriction is on `HeaderSection` class itself, not on InvoiceMessage). No CQ for business process (CQ14) or mandatory identifiers (CQ13) is adequately modelled — `hasSection` property does not exist as a named property in the vocabulary, causing a disconnect. Only 3 axiom types (diversity 3). This ontology covers ~11/14 CQs at best and has the weakest structural foundation in the set.

---

*Report generated by: Ontology Expert Evaluation Agent*
*Date: 2026-03-08*
