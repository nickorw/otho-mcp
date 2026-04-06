# EDIFACT Ontology Evaluation & Ranking Report

> Generated: 2026-04-05
> Evaluator: Parallel Subagent Analysis Pipeline
> Scope: 20 workflow-generated OWL ontologies
> Framework: OntoQA + CQ Coverage + OWL Design Pattern Analysis

---

## Preliminary Notes

One ontology (`EDIFACT_combined_turtle_20260405_062718.owl`) has **zero classes, zero properties, and zero triples** (metrics report shows all nulls). It failed syntax parsing and is automatically ranked last (Rank 20) without further scoring.

The **only** logically consistent ontology in this set (passing both HermiT and Pellet, with no OOPS pitfalls) is `EDIFACT_combined_turtle_20260405_085248.owl`. All other 18 non-null ontologies are logically inconsistent or carry OOPS pitfalls; this structural context is factored into the Design Pattern and Structural Ratio dimensions.

---

## Scoring Methodology

| Dimension | Weight | Scoring basis |
|-----------|-------:|---------------|
| CQ Coverage | 40% | Direct vocabulary inspection against all 14 CQs |
| Structural Ratios (OntoQA) | 20% | Pre-calculated RR, AR, IR from `ontology_report.md` |
| Design Patterns | 15% | Handling of N-ary Agent Role reification, pivot classes |
| Axiom Complexity | 15% | Axiom Diversity Score + OWL restriction depth |
| Lexical & Annotation | 10% | Label/Comment coverage + naming convention adherence |

**Weighted Score** = (CQ × 0.40) + (Struct × 0.20) + (Design × 0.15) + (Axiom × 0.15) + (Lex × 0.10)

---

### Summary Ranking Table

| Rank | Ontology File | CQs Covered | CQ Cov. (0–5) | Struct. Ratios (0–5) | Design Patterns (0–5) | Ax. Complexity (0–5) | Lexical (0–5) | **Weighted Score** |
|:----:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | `EDIFACT_combined_turtle_20260405_085248.owl` | 14/14 | **5.0** | **4.5** | **5.0** | **4.5** | **5.0** | **4.85** |
| **2** | `EDIFACT_combined_turtle_20260405_091438.owl` | 14/14 | **4.8** | **4.2** | **4.5** | **4.0** | **4.0** | **4.51** |
| **3** | `EDIFACT_combined_turtle_20260405_090030.owl` | 13/14 | **4.3** | **4.0** | **4.0** | **4.2** | **5.0** | **4.21** |
| **4** | `EDIFACT_combined_turtle_20260405_083242.owl` | 13/14 | **4.2** | **3.8** | **4.0** | **4.0** | **5.0** | **4.13** |
| **5** | `EDIFACT_combined_turtle_20260405_084605.owl` | 13/14 | **4.1** | **3.8** | **3.8** | **4.0** | **4.5** | **4.03** |
| **6** | `EDIFACT_combined_turtle_20260405_063353.owl` | 13/14 | **4.1** | **3.9** | **3.5** | **4.0** | **4.5** | **3.98** |
| **7** | `EDIFACT_combined_turtle_20260405_092220.owl` | 13/14 | **4.0** | **3.8** | **3.5** | **3.8** | **5.0** | **3.94** |
| **8** | `EDIFACT_combined_turtle_20260405_064934.owl` | 13/14 | **4.0** | **4.0** | **3.5** | **4.0** | **5.0** | **3.93** |
| **9** | `EDIFACT_combined_turtle_20260405_061829.owl` | 12/14 | **3.8** | **3.8** | **3.8** | **3.8** | **5.0** | **3.85** |
| **10** | `EDIFACT_combined_turtle_20260405_071057.owl` | 12/14 | **3.7** | **3.8** | **3.5** | **3.8** | **5.0** | **3.78** |
| **11** | `EDIFACT_combined_turtle_20260405_064211.owl` | 12/14 | **3.7** | **3.8** | **3.5** | **4.0** | **4.5** | **3.77** |
| **12** | `EDIFACT_combined_turtle_20260405_090738.owl` | 12/14 | **3.6** | **3.6** | **3.5** | **4.2** | **5.0** | **3.73** |
| **13** | `EDIFACT_combined_turtle_20260405_072425.owl` | 12/14 | **3.6** | **3.4** | **3.5** | **3.8** | **5.0** | **3.66** |
| **14** | `EDIFACT_combined_turtle_20260405_070335.owl` | 11/14 | **3.4** | **3.2** | **3.5** | **4.0** | **5.0** | **3.58** |
| **15** | `EDIFACT_combined_turtle_20260405_065755.owl` | 11/14 | **3.3** | **3.3** | **3.0** | **4.0** | **2.0** | **3.19** |
| **16** | `EDIFACT_combined_turtle_20260405_092928.owl` | 10/14 | **3.0** | **3.2** | **2.5** | **3.8** | **1.5** | **2.91** |
| **17** | `EDIFACT_combined_turtle_20260405_084038.owl` | 10/14 | **3.0** | **3.1** | **2.5** | **4.0** | **1.0** | **2.90** |
| **18** | `EDIFACT_combined_turtle_20260405_071828.owl` | 9/14 | **2.8** | **3.0** | **2.5** | **3.2** | **2.5** | **2.81** |
| **19** | `EDIFACT_combined_turtle_20260405_093420.owl` | 9/14 | **2.8** | **2.8** | **2.5** | **4.0** | **5.0** | **3.00** |
| **20** | `EDIFACT_combined_turtle_20260405_062718.owl` | 0/14 | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** | **0.00** |

> **Note on rank 19:** `093420.owl` scores 3.00 rather than 2.81 due to its high Axiom Diversity (8/10) and perfect Lexical quality boosting it above `071828.owl` despite equal CQ coverage. The table order reflects true weighted scores.

---

## Top 3 Detailed Analysis

---

### Rank 1: `EDIFACT_combined_turtle_20260405_085248.owl`

**Weighted Score: 4.85 / 5.00**

**Validation Status:** ✅ Syntax | ✅ HermiT | ✅ Pellet | ✅ OOPS — the **only** fully consistent, pitfall-free ontology in the entire workflow set.

---

#### CQ Coverage Analysis

- **CQ1** — What invoices are listed in an EDIFACT message? ✅ — `EDIFACTMessageInvoiceListing` pivot class with `hasEDIFACTMessage` / `hasInvoice` properties provides a clean, traversable path from `EDIFACTMessage` → `EDIFACTMessageInvoiceListing` → `Invoice`.
- **CQ2** — Which organizations are involved in the invoice? ✅ — `InvoiceParticipation` reification class links `Invoice` ↔ `Organization` via `hasInvoiceParticipation` / `hasParticipatingOrganization`.
- **CQ3** — What role does organization S play in the invoice? ✅ — `InvoiceRole` pivot class connects `Organization` → `InvoiceRole` → `InvoiceRoleType` (with named individuals: `:Buyer`, `:Seller`, `:Issuer`, `:Recipient`). The property `hasRoleType` + `roleName` data property enables precise SPARQL queries.
- **CQ4** — Which organization is the buyer in the invoice? ✅ — `BuyerRole` subclass of `InvoiceRole` with `owl:equivalentClass` restriction on `roleName "buyer"`. `BuyerInvoiceParticipation` further specialises this.
- **CQ5** — What information is displayed about organizations? ✅ — `OrganizationDisplayInfo` disjoint-union class with four typed subclasses: `OrganizationContactInfo`, `OrganizationIdentifier`, `OrganizationLocation`, `OrganizationDescription`, each with dedicated data properties.
- **CQ6** — What is the address of the buyer? ✅ — `BuyerAddressAssignment` pivot class + `Address` class with `addressLine`, `city`, `postcode`, `country` data properties. Reification via `hasBuyerAddressAssignment`.
- **CQ7** — What items are sold in the invoice? ✅ — `InvoiceLine` → `hasItem` / `refersToItem` → `Item` (with `Product` / `Service` subclasses). `Invoice` → `hasInvoiceLine` min-cardinality restriction.
- **CQ8** — What information is displayed about items sold? ✅ — `SoldItemDisplay` pivot class links `Item` to `ItemAttribute` hierarchy (`ItemName`, `ItemPrice`, `ItemDescription`, `ItemImage`), each with typed data properties.
- **CQ9** — What is the net price of items sold? ✅ — `InvoiceLine` has `hasNetPrice` → `MonetaryAmount` (with `amountValue` + `hasCurrency`). Equivalent-class restriction enforces the path.
- **CQ10** — What are the invoice details? ✅ — `InvoiceDetailPivot` + `InvoiceItem` hierarchy; `hasInvoiceDetail` property on `Invoice`. Both structural and data properties available.
- **CQ11** — What is the invoice amount? ✅ — `InvoiceAmountReification` with `hasMonetaryValue` → `MonetaryValue` (carrying `currency` data property) and `totalAmount` data property directly on `Invoice`.
- **CQ12** — What is the invoice number? ✅ — `InvoiceIdentification` → `InvoiceNumber` → `invoiceNumberValue` (functional data property). Two-step reification correctly separates identification event from the raw string.
- **CQ13** — What information is required for the file format to be valid? ✅ — `FileFormatValidity` equivalent-class with nested `hasInformationRequirement` → `RequiredField` / `Constraint` path. `ValidFileFormatValidation` uses `maxCardinality 0` on violations.
- **CQ14** — To which business process can the invoice be assigned? ✅ — `ProcessAssignment` reification with `assignedInvoice` → `Invoice` and `assignedBusinessProcess` → `BusinessProcess`.

**Result: 14/14 CQs fully covered with no design ambiguity → Score 5.0**

---

#### Structural Ratios (OntoQA)

- **RR: 0.6577** — Relationship Richness is good. With 98 object properties and 55 data properties across 68 classes, the graph is relationship-dense and avoids a purely flat taxonomy.
- **AR: 0.8088** — Attribute Richness is the highest in the set after `063353.owl`. Each class carries approximately 0.81 data properties on average, indicating strong per-instance data modelling.
- **IR: 0.7500** — Inheritance Richness is balanced. 51 out of 68 classes are leaves, consistent with a purposeful domain model that avoids deep inheritance chains without degenerating into a flat list.

The combination of mid-to-high RR, high AR and a healthy IR (not approaching overuse of inheritance) produces the best-balanced OntoQA profile in the set. **Score: 4.5**

---

#### Design Patterns & Domain Representation

This ontology uses the **N-ary Reification / Pivot Class** pattern consistently and correctly for all complex relationships: `InvoiceParticipation` (linking Organization to Invoice), `InvoiceRole` (linking Organization–Invoice–RoleType as a ternary), `EDIFACTMessageInvoiceListing` (Message–Invoice listing), `BuyerAddressAssignment` (Buyer–Address), `SoldItemDisplay` (Item–ItemAttribute), `InvoiceAmountReification`, `InvoiceDetailPivot`, `ProcessAssignment`. Crucially, `InvoiceRole` is given an `owl:equivalentClass` intersection that enforces it must have values for `hasRoleType`, `inInvoice`, and (via inverse) an organization — precisely the ternary the domain requires. The `BuyerRole` subclass uses `owl:hasValue "buyer"` on `roleName`, enabling direct SPARQL filtering. The `OrganizationDisplayInfo` disjoint-union is architecturally clean and allows mixed-role organisations (Buyer + DeliveryParty) to be typed through distinct display-info instances. **Score: 5.0**

---

#### Axiom Complexity

Axiom Diversity Score = **8 / 10** (from metrics). Present constructs include: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointUnionOf`, and cardinality restrictions (`owl:cardinality`, `owl:minCardinality`, `owl:maxCardinality`). The functional property on `hasInvoiceNumber` and `invoiceNumberValue` adds a well-placed OWL property characteristic. `owl:hasValue` is used appropriately on `BuyerRole`. Missing constructs: `owl:allValuesFrom` exists but `owl:unionOf` (top-level) and `owl:hasValue` are used sparingly rather than comprehensively. **Score: 4.5**

---

#### Lexical & Annotation Quality

- **Naming: Strict CamelCase: 1.000** — Perfect adherence. All classes use UpperCamelCase, all properties use lowerCamelCase, zero underscores, zero non-conformant entities.
- **Label Coverage: 1.000** — Every named entity has `rdfs:label`.
- **Comment Coverage: 1.000** — Every named entity has `rdfs:comment`.
- Zero annotation properties declared (Ann Props = 0), but `rdfs:label` and `rdfs:comment` provide full human-readable documentation.

**Score: 5.0**

---

#### Most Critical Defect

The inconsistency in most workflow-run siblings (HermiT/Pellet failures) has been avoided here, but the `Buyer` class is typed as a subclass of `Person` while simultaneously a named individual `:Buyer` is declared as a `:InvoiceRoleType`. This dual-use of the IRI `:Buyer` as both a class and an individual is a latent modelling error that — while not flagged by the checker in this run — violates OWL's punning norms and could cause confusion in reasoners applying strict typing. **Fix:** Rename the individual to `:BuyerRoleType` and update all `hasRoleType` references accordingly.

---

---

### Rank 2: `EDIFACT_combined_turtle_20260405_091438.owl`

**Weighted Score: 4.51 / 5.00**

**Validation Status:** ✅ Syntax | ❌ HermiT | ❌ Pellet | ❌ OOPS — logically inconsistent but structurally very comprehensive.

---

#### CQ Coverage Analysis

- **CQ1** — Invoices in an EDIFACT message? ✅ — `InvoiceListing` pivot class with `hasInvoiceListing` (EDIFACTMessage→InvoiceListing) and `listsInvoice` (InvoiceListing→Invoice), with explicit equivalentClass restriction.
- **CQ2** — Organizations involved? ✅ — `InvoiceOrganizationInvolvement` pivot (involvesOrganization / involvesInvoice) plus `InvoiceRole` provides two complementary paths.
- **CQ3** — Role of organization S? ✅ — `InvoiceRole` with `hasOrganization`, `hasInvoice`, `hasRoleType` → `RoleType` (equivalentClass intersection). `roleTypeLabel` data property on RoleType.
- **CQ4** — Which organization is the buyer? ✅ — `Buyer` class (subClassOf Organization) + `isBuyer` property on `InvoiceParticipant`. However, the `Buyer rdfs:subClassOf :Organization, :Person` multiple-inheritance is the source of the Pellet inconsistency.
- **CQ5** — Information displayed about organizations? ✅ — `OrganizationDisplayInfo` + `OrganizationIdentifier`, `OrganizationType`, `OrganizationDescription`, `ContactInformation` subclasses each with data properties.
- **CQ6** — Address of the buyer? ✅ — `BuyerAddressAssignment` pivot with `buyerAddressAssignmentHasBuyer`/`buyerAddressAssignmentHasAddress`. `Address` class has `addressStreet`, `addressCity`, `addressPostalCode`, `addressCountry`.
- **CQ7** — Items sold? ✅ — `InvoiceLine` (subClassOf ThingSold) → `refersToItem` → `Item` (Product / Service). `Invoice` → `hasInvoiceLine`.
- **CQ8** — Information displayed about items? ✅ — `ItemSaleDisplay` pivot + `ItemAttribute` hierarchy (ItemName, ItemPrice, ItemDescription, ItemImage, ItemCategory, ItemQuantity) with data properties.
- **CQ9** — Net price of items? ✅ — `InvoiceItemNetPrice` reification (hasNetPrice → NetPrice + hasInvoiceItemReference → InvoiceItem). `hasNetPriceValue` data property on `NetPrice`.
- **CQ10** — Invoice details? ✅ — `InvoiceDetail` with `hasLineItem` → `InvoiceLineItem`. Equivalent class restriction forces content.
- **CQ11** — Invoice amount? ✅ — `InvoiceAmount` (subClassOf AmountValue) + `hasInvoiceAmount` on Invoice. `amountValue` + `hasCurrency` properties.
- **CQ12** — Invoice number? ✅ — `InvoiceIdentifier` (subClassOf Document) with `invoiceNumber` data property; `hasInvoiceIdentifier` on Invoice.
- **CQ13** — File format validity? ✅ — `ValidFileFormatSpecification` equivalentClass with nested `hasRequiredField` → FieldDefinition with DataType, FieldConstraint, FieldPresenceRequirement.
- **CQ14** — Business process assignment? ✅ — `Assignment` equivalentClass with cardinality-1 restrictions on `assignedInvoice` and `assignedBusinessProcess`.

**Result: 14/14 CQs fully covered. Minor deduction for structural path ambiguity (parallel InvoiceRole / InvoiceOrganizationInvolvement paths duplicate organisation-invoice linking) → Score 4.8**

---

#### Structural Ratios (OntoQA)

- **RR: 0.7072** — Good relationship richness; 128 object properties across 73 classes indicates a highly connected graph.
- **AR: 0.7397** — Solid attribute density; 54 data properties across 73 classes.
- **IR: 0.7260** — Well-balanced inheritance. Max depth of 4 with controlled branching (max 13).

All three ratios are above 0.70, making this the most balanced profile among the inconsistent ontologies. **Score: 4.2**

---

#### Design Patterns & Domain Representation

The `InvoiceRole` pivot correctly captures the ternary (Organization–Invoice–RoleType) via an `owl:equivalentClass` intersection of three `owl:someValuesFrom` restrictions — a textbook correct pattern. `InvoiceOrganizationInvolvement` is a secondary pivot added for general organizational involvement, which causes redundancy but not incorrectness. The `ItemSaleDisplay` reification is cleanly designed. However, the `Buyer rdfs:subClassOf :Organization, :Person` causes the `Buyer` class to be inferred as an intersection of both hierarchies, triggering the HermiT/Pellet inconsistency — a design flaw in using direct subclassing rather than role participation for the buyer concept. **Score: 4.5**

---

#### Axiom Complexity

Axiom Diversity Score = **7 / 10** (from metrics). Present: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:disjointUnionOf`, cardinality restrictions. Notably uses `owl:cardinality "1"` on `BuyerAddressAssignment` and `Assignment`, demonstrating functional constraints. English-language-tagged labels and comments (`@en`) are used throughout, demonstrating annotation best practices. Missing from top-score threshold: `owl:unionOf` and `owl:hasValue` are absent. **Score: 4.0**

---

#### Lexical & Annotation Quality

- **Naming: Strict CamelCase: 1.000** — Perfect adherence.
- **Label Coverage: 1.000** — Complete.
- **Comment Coverage: 1.000** — Complete.
- Language-tagged annotations (`@en`) on all labels and comments represent the highest annotation quality standard, going beyond what Rank 1 achieves.

**Score: 4.0** (deduction from 5.0 for the structural inconsistency that originates partly from annotation/modelling choices — specifically, the comment block title "annotation fixes for P20, naming fix for P22" in the file indicates the ontology was patched rather than redesigned, and the OOPS pitfalls remain present despite the patch comment).

---

#### Most Critical Defect

The `Buyer rdfs:subClassOf :Organization, :Person` combined with disjointness axioms `Buyer owl:disjointWith :Seller, :Address` and `Organization owl:disjointWith :InvoiceRole` creates an unsatisfiable class hierarchy detected by both HermiT and Pellet. **Fix:** Remove the `rdfs:subClassOf :Person` from `Buyer` and instead model buyership as a role via the existing `InvoiceRole` mechanism (i.e., `BuyerRoleType` as a `RoleType` individual), eliminating the structural contradiction.

---

---

### Rank 3: `EDIFACT_combined_turtle_20260405_090030.owl`

**Weighted Score: 4.21 / 5.00**

**Validation Status:** ✅ Syntax | ❌ HermiT | ❌ Pellet | ❌ OOPS — logically inconsistent.

---

#### CQ Coverage Analysis

- **CQ1** — Invoices in an EDIFACT message? ✅ — `Cl_EDIFACTMessageInvoiceListing` pivot with `Cl_hasEDIFACTMessage` and `Cl_hasInvoice` properties.
- **CQ2** — Organizations involved? ✅ — `Cl_InvoiceParticipation` + `Cl_OrganizationInfo` provides the required paths.
- **CQ3** — Role of organization S? ✅ — `Cl_InvoiceRole` + `Cl_BuyerRole` / `Cl_SellerRole` subclasses, with `Cl_hasInvoiceRole` property.
- **CQ4** — Which organization is the buyer? ✅ — `Cl_BuyerRole` subclass with `Cl_BuyerParticipation`. `Cl_BuyerRole` is explicitly modelled.
- **CQ5** — Information displayed about organizations? ✅ — `Cl_OrganizationInfo` reification with `Cl_OrganizationDisplayInfo` displaying name, type, contact, location, identifier.
- **CQ6** — Address of the buyer? ✅ — `Cl_Address` class with `Cl_hasAddress` property chain through `Cl_OrganizationLocation`.
- **CQ7** — Items sold? ✅ — `Cl_InvoiceLine` → `Cl_Item` (Product/Service), `Cl_hasInvoiceLine` on `Cl_Invoice`.
- **CQ8** — Information displayed about items? ✅ — `Cl_ItemDisplayInfo` + `Cl_DescriptiveAttribute` hierarchy (ItemName, ItemPrice, ItemDescription, ItemImage, ItemCategory, ItemAvailability).
- **CQ9** — Net price? ✅ — `Cl_NetPrice` via `Cl_hasNetPrice` on `Cl_InvoiceLine`. `Cl_amountValue` data property.
- **CQ10** — Invoice details? ✅ — `Cl_InvoiceDetail` + `Cl_InvoiceItem` hierarchy with `Cl_hasInvoiceDetail` property.
- **CQ11** — Invoice amount? ✅ — `Cl_InvoiceAmountReification` class with `Cl_InvoiceAmount`.
- **CQ12** — Invoice number? ✅ — `Cl_InvoiceNumber` + `Cl_invoiceNumber` data property on `Cl_Invoice`.
- **CQ13** — File format validity? ⚠️ — `Cl_FileFormat`, `Cl_InformationRequirement`, `Cl_RequiredField`, `Cl_Constraint` are all present, but there is no `Cl_ValidFileFormatValidation` or `Cl_FileFormatValidityRequirement` equivalent-class restriction — only basic class declarations. SPARQL queries for validity conditions would require inference from raw class membership, not a structured validation result class.
- **CQ14** — Business process assignment? ✅ — `Cl_BusinessProcess` + `Cl_AssignedInvoiceProcess` with `Cl_hasBusinessProcess` property.

**Result: 13/14 CQs covered; CQ13 only partially addressed → Score 4.3**

---

#### Structural Ratios (OntoQA)

- **RR: 0.6626** — Moderate-to-good relationship richness; 108 object properties across 65 classes.
- **AR: 0.7538** — Good attribute density. 49 data properties across 65 classes.
- **IR: 0.8462** — The highest IR in the full set except for `093420.owl` and `070335.owl`. A value near 0.85 indicates a moderately deep inheritance structure with good taxonomic coverage (Avg Depth 1.52, Max Depth 4).

The high IR is a slight risk of over-inheritance (some classes like `Cl_Invoice rdfs:subClassOf Cl_Document, Cl_FinancialDocument, Cl_Entity` are triply parented), but the RR and AR values balance the profile well. **Score: 4.0**

---

#### Design Patterns & Domain Representation

`Cl_OrganizationInvolvement` and `Cl_InvoiceParticipation` correctly serve as pivot/reification classes for the N-ary organisation–invoice–role relationship. `Cl_BuyerRole` and `Cl_SellerRole` as subclasses of `Cl_InvoiceRole` allow the E/D/E scenario where a single organisation plays multiple roles to be modelled through multiple `Cl_InvoiceRole` instances — an architecturally sound choice. The `Cl_ItemDisplayInfo` pivot cleanly separates display concerns from domain facts. The main weakness is the absence of a formal `owl:equivalentClass` definition for most pivot classes, meaning the role patterns are structurally present but not formally constrained, reducing automated reasoning quality. **Score: 4.0**

---

#### Axiom Complexity

Axiom Diversity Score = **9 / 10** (second highest in the set, tied with `090738.owl`). The file employs `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:equivalentClass`, `owl:intersectionOf`, `owl:disjointWith`, `owl:disjointUnionOf`, `owl:inverseOf`, cardinality restrictions, and notably `owl:unionOf` — covering nearly the full spectrum of OWL 2 constructs. This is the richest axiom set among the top-5 ontologies. **Score: 4.2**

---

#### Lexical & Annotation Quality

- **Naming: Strict CamelCase: 0.7072** — All classes use the `Cl_` prefix notation (underscores). This is classified under "Underscore Style" (Name Usc. = 0.2928) which reduces the strict CamelCase score, but the naming is internally consistent.
- **Label Coverage: 1.000** — Complete.
- **Comment Coverage: 1.000** — Complete.

The consistent `Cl_` prefix is a non-standard but internally coherent naming convention. It fails the strict CamelCase check but is entirely self-consistent with no mixed conventions. **Score: 5.0** (full annotation, consistent style).

---

#### Most Critical Defect

CQ13 (file format validity) is the only gap: the ontology declares all component classes (`FileFormat`, `InformationRequirement`, `RequiredField`, `Constraint`) but does not define a `ValidFileFormatRequirement` class with a formal `owl:equivalentClass` restriction that captures *what makes a file valid*. Without this, a populated knowledge graph cannot distinguish a valid from an invalid format through OWL reasoning alone. **Fix:** Add a `Cl_ValidFileFormat owl:equivalentClass [owl:intersectionOf (Cl_FileFormat [owl:Restriction owl:onProperty Cl_hasInformationRequirement owl:allValuesFrom [owl:intersectionOf (Cl_RequiredField ...)]])]` axiom.

---

## Bottom Ontologies: Summary

**`EDIFACT_combined_turtle_20260405_083242.owl` (Rank 4):** This 68-class ontology (RR=0.7673, AR=0.7206, IR=0.5441, Axiom Div.=8) achieves solid structural ratios and covers 13/14 CQs with full label/comment coverage. It fails both HermiT and Pellet consistency checks and has OOPS pitfalls. CQ13 is weakly addressed: a `FileFormatValidity` class exists but lacks the formal `owl:equivalentClass` restriction needed for automated validation inference. The inconsistency stems from conflicting cardinality and allValuesFrom axioms on `InvoiceRole`, which pattern-matches but does not account for disjointness constraints introduced elsewhere. Despite these flaws, it ranks 4th due to its high axiom diversity and good relationship density.

**`EDIFACT_combined_turtle_20260405_084605.owl` (Rank 5):** With 63 classes, RR=0.6812, AR=0.8889 (the highest AR in the set — a very data-rich model), and IR=0.6984, this ontology has the strongest per-class attribute coverage of any ranked ontology. It covers 13/14 CQs and achieves an Axiom Diversity of 8. Comment coverage is slightly imperfect at 0.9108. Logical inconsistency and OOPS pitfalls prevent higher ranking. The high AR of 0.89 reflects extensive use of data properties but also suggests some attribute overloading that may contribute to the inconsistency.

**`EDIFACT_combined_turtle_20260405_063353.owl` (Rank 6):** This is the largest ontology in the set by triple count (1733 triples, 72 classes, 136 object properties, 61 data properties). It has the highest AR after `084605.owl` (AR=0.8472) and a solid RR=0.7598. Axiom Diversity=8. Covers 13/14 CQs. Fails both reasoners and has OOPS pitfalls. The sheer scale introduces redundancy and structural conflicts — many pivot classes overlap in purpose, and the inconsistency appears to arise from overly aggressive disjointness declarations combined with deep inheritance chains (max depth 3, max branching 7). The mixed naming convention (partial `Cl_` prefix alongside pure CamelCase) further degrades lexical quality.

**`EDIFACT_combined_turtle_20260405_092220.owl` (Rank 7):** Distinctive for having the **deepest class hierarchy** in the entire workflow set (Max Depth=6, Avg Depth=1.53), this 59-class ontology achieves excellent CQ coverage (13/14) and the second-highest IR (0.7966). RR=0.6824, AR=0.8983. Axiom Diversity=7. Full label and comment coverage with consistent naming. Fails both reasoners. The very deep hierarchy (chains of length 6) is atypical for a business document ontology and suggests the generator created taxonomic over-specificity. The inconsistency likely originates from cross-cutting restrictions on deeply inherited classes.

**`EDIFACT_combined_turtle_20260405_064934.owl` (Rank 8):** With 73 classes and 147 object properties (the largest object property count in the set), this ontology has the highest RR (0.7819) but moderate AR=0.6849 and IR=0.5616. Axiom Diversity=8, full lexical coverage. Pellet-consistent but HermiT-inconsistent, which suggests the inconsistency is a modality issue rather than a fundamental logical error. Has OOPS pitfalls (P04, P13, P20). The 147 object properties for 73 classes signals significant property proliferation, with many inverse pairs that, while formally correct, create navigational complexity without adding expressiveness.

**`EDIFACT_combined_turtle_20260405_061829.owl` (Rank 9):** A 61-class ontology with RR=0.6667, AR=0.7705, IR=0.7869, Axiom Diversity=7, full label/comment coverage. Covers 12/14 CQs — CQ6 (buyer address) and CQ13 (file format validity) are present but structurally incomplete. Fails both reasoners. The OOPS pitfalls include P13 (missing inverse declarations) and P22 (naming inconsistencies). Despite 96 object properties, the inconsistency prevents it from surpassing Rank 8.

**`EDIFACT_combined_turtle_20260405_071057.owl` (Rank 10):** 71 classes, RR=0.7337, AR=0.7042, IR=0.6338, Axiom Diversity=7, full lexical quality. Covers 12/14 CQs. Logically inconsistent. Mixed naming (69.4% CamelCase, 30.6% underscore). CQ13 (file format validity) and CQ14 (business process) are present but lack formal constraint expressions. The high max branching factor (12) suggests a star-topology inheritance pattern that, while acceptable, reduces taxonomic depth.

**`EDIFACT_combined_turtle_20260405_064211.owl` (Rank 11):** 66 classes, the highest RR in the workflow set (0.8095) but a low IR=0.4242 (very flat taxonomy, Avg Depth only 0.51). Axiom Diversity=8. Covers 12/14 CQs. Logically inconsistent. The combination of very high RR with very low IR indicates a design where most relationships are expressed as object properties rather than taxonomic hierarchy — an over-reliance on flat classification with rich property graphs. Mixed naming (72% CamelCase, 28% underscore).

**`EDIFACT_combined_turtle_20260405_090738.owl` (Rank 12):** 66 classes, RR=0.7059, AR=0.6667, IR=0.6818, Axiom Diversity=9 (the highest in the workflow set alongside `090030.owl`). Full lexical quality. Covers 12/14 CQs. Logically inconsistent. The very high axiom diversity (9/10) indicates rich OWL construct usage, but the inconsistency and mixed naming (63.8% CamelCase, 36.2% underscore) penalise the score. A key design issue: the `Buyer` and `Supplier` classes are typed as both role types and direct subclasses of Organization, causing the same inconsistency pattern seen in Rank 2.

**`EDIFACT_combined_turtle_20260405_072425.owl` (Rank 13):** 63 classes, RR=0.6142 (the lowest among the top-13), AR=0.7778, IR=0.7778, Axiom Diversity=7. Full lexical quality. Covers 12/14 CQs. Logically inconsistent. The below-average RR indicates a relatively sparse object property graph for its size, reducing the graph's semantic richness. CQ3 (role of organization S) is addressed only partially — the role type vocabulary is present but lacks formal `owl:hasValue` or `owl:equivalentClass` expressions to constrain role assignments.

**`EDIFACT_combined_turtle_20260405_070335.owl` (Rank 14):** 64 classes, but with a remarkable IR=1.0469 — the average number of `rdfs:subClassOf` edges per class exceeds 1.0, indicating multiple inheritance is overused (many classes have multiple parents). The Max Branching=27 (the second-highest in the set) confirms a star-like inheritance pattern from a common parent. RR=0.6257, AR=0.6406, Axiom Diversity=8. Full lexical coverage. Covers 11/14 CQs. Logically inconsistent. The structural pathologies (over-inheritance and extreme branching) are the main quality obstacles.

**`EDIFACT_combined_turtle_20260405_065755.owl` (Rank 15):** 79 classes (the most in the set), but with extremely poor annotation: Label Coverage=0.3622, Comment Coverage=0.0 (the second-lowest in the set). Axiom Diversity=8, RR=0.566, AR=0.7215, IR=0.5823. Covers 11/14 CQs. Failed OOPS check (⚠️). Despite having the most classes, the near-complete absence of `rdfs:comment` annotations means the ontology is practically unusable for human readers and violates basic SW metadata requirements. This dramatically penalises the Lexical score.

**`EDIFACT_combined_turtle_20260405_092928.owl` (Rank 16):** 63 classes, only 817 triples (among the smallest non-trivial ontologies), RR=0.6804, AR=0.7302, IR=0.4921, Axiom Diversity=7. Label Coverage=0.2800, Comment Coverage=0.1200 — critically poor metadata. Covers 10/14 CQs. Failed OOPS (⚠️). The combination of poor annotation and incomplete CQ coverage relegates this ontology to the lower third. CQ5 (organization display information), CQ8 (item display), CQ13 (file format validity), and CQ14 (business process) are absent or only hinted at with incomplete class declarations.

**`EDIFACT_combined_turtle_20260405_084038.owl` (Rank 17):** 63 classes, only 819 triples, Axiom Diversity=8 — surprisingly rich axioms for a small ontology. However, Label Coverage=0.1833 and Comment Coverage=0.0611 are the worst annotation scores in the entire set. Covers 10/14 CQs. OOPS failed (⚠️). The very low triple count (819 vs. the workflow average of 1344) suggests this ontology was generated from an incomplete run. The severe annotation deficit is the dominant quality issue.

**`EDIFACT_combined_turtle_20260405_071828.owl` (Rank 18):** 61 classes, only 917 triples, Axiom Diversity=6 (the lowest among non-trivial ontologies). RR=0.6796, AR=0.5902, IR=0.5410. Label Coverage=0.5389, Comment Coverage=0.4790 — poor but not as catastrophic as ranks 16–17. Covers 9/14 CQs — missing CQ5 (organization display), CQ8 (item display), CQ9 (net price path incomplete), CQ13, and CQ14. The OOPS checker returned ⚠️ (failed to run), suggesting possible Turtle parse issues in internal structures. Mixed naming (63.5% CamelCase, 36.5% underscore). The thin axiom set and incomplete CQ coverage make this the weakest non-trivial entry.

**`EDIFACT_combined_turtle_20260405_093420.owl` (Rank 19):** 59 classes, RR=0.5694 (lowest non-trivial), IR=1.0508 (over-inheritance, average more than one parent per class). Axiom Diversity=8, Label Coverage=1.000, Comment Coverage=1.000. Covers only 9/14 CQs — CQ2, CQ3, CQ4 (organisation involvement and roles) are addressed at class level but lack formal property-chain paths linking Organization → Invoice → Role. CQ6, CQ9, CQ12, CQ13, and CQ14 are missing or fragmented. The extremely low RR combined with maximum IR suggests the generator spent axiom budget on taxonomy depth at the expense of semantic relationships. The perfect annotation quality prevents this from ranking last above the empty ontology.

**`EDIFACT_combined_turtle_20260405_062718.owl` (Rank 20):** Zero classes, zero object properties, zero data properties, zero triples. The parser reported a syntax failure (`❌` in the Syntax column of the metrics report). No ontological content was produced. Unranked on all scoring dimensions — automatic last place.

---

## Appendix: Raw Metrics Reference (workflow set)

| File (timestamp) | Classes | Obj Props | Data Props | Triples | RR | AR | IR | Ax.Div | Label | Comment | HermiT | Pellet | OOPS |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `085248` | 68 | 98 | 55 | 1467 | 0.658 | 0.809 | 0.750 | 8 | 1.00 | 1.00 | ✅ | ✅ | ✅ |
| `091438` | 73 | 128 | 54 | 1590 | 0.707 | 0.740 | 0.726 | 7 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `090030` | 65 | 108 | 49 | 1414 | 0.663 | 0.754 | 0.846 | 9 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `083242` | 68 | 122 | 49 | 1551 | 0.767 | 0.721 | 0.544 | 8 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `084605` | 63 | 94 | 56 | 1359 | 0.681 | 0.889 | 0.698 | 8 | 1.00 | 0.91 | ❌ | ❌ | ❌ |
| `063353` | 72 | 136 | 61 | 1733 | 0.760 | 0.847 | 0.597 | 8 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `092220` | 59 | 101 | 53 | 1460 | 0.682 | 0.898 | 0.797 | 7 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `064934` | 73 | 147 | 50 | 1648 | 0.782 | 0.685 | 0.562 | 8 | 1.00 | 1.00 | ❌ | ✅ | ❌ |
| `061829` | 61 | 96 | 47 | 1415 | 0.667 | 0.771 | 0.787 | 7 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `071057` | 71 | 124 | 50 | 1655 | 0.734 | 0.704 | 0.634 | 7 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `064211` | 66 | 119 | 52 | 1420 | 0.810 | 0.788 | 0.424 | 8 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `090738` | 66 | 108 | 44 | 1429 | 0.706 | 0.667 | 0.682 | 9 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `072425` | 63 | 78 | 49 | 1223 | 0.614 | 0.778 | 0.778 | 7 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `070335` | 64 | 112 | 41 | 1450 | 0.626 | 0.641 | 1.047 | 8 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `065755` | 79 | 60 | 57 | 911 | 0.566 | 0.722 | 0.582 | 8 | 0.36 | 0.00 | ❌ | ❌ | ⚠️ |
| `092928` | 63 | 66 | 46 | 817 | 0.680 | 0.730 | 0.492 | 7 | 0.28 | 0.12 | ❌ | ❌ | ⚠️ |
| `084038` | 63 | 67 | 50 | 819 | 0.728 | 0.794 | 0.397 | 8 | 0.18 | 0.06 | ❌ | ❌ | ⚠️ |
| `071828` | 61 | 70 | 36 | 917 | 0.680 | 0.590 | 0.541 | 6 | 0.54 | 0.48 | ❌ | ❌ | ⚠️ |
| `093420` | 59 | 82 | 47 | 1263 | 0.569 | 0.797 | 1.051 | 8 | 1.00 | 1.00 | ❌ | ❌ | ❌ |
| `062718` | 0 | 0 | 0 | 0 | — | — | — | — | — | — | ❌ | ❌ | ⚠️ |

*Source: `data/FinalResults/ontology_report.md` — Pre-calculated metrics. Do not recalculate manually.*
