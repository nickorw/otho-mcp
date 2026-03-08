# Ontology Quality Report

> Generated automatically from `generate_ontology_report.py`  
> Date: 2026-03-08

---

## 1. Reference Ontologies (TUMedifact)

These two ontologies serve as the baseline for comparison.

| Metric | TUMedifact (full) | TUMedifact (trimmed) |
|--------|:-----------------:|:--------------------:|
| Syntax valid | ✅ | ✅ |
| Triples (axioms) | 2670 | 2267 |
| Classes | 31 | 31 |
| Object properties | 10 | 10 |
| Data properties | 261 | 261 |
| Annotation properties | 22 | 9 |
| Max inheritance depth | 1 | 1 |
| Avg inheritance depth | 0.8 | 0.8 |
| Max branching factor | 21 | 21 |
| Avg branching factor | 5.2 | 5.2 |
| Leaf classes | 26 | 26 |
| RR (Relationship Richness) | 0.2778 | 0.2778 |
| AR (Attribute Richness) | 8.4194 | 8.4194 |
| IR (Inheritance Richness) | 0.8387 | 0.8387 |
| Axiom Diversity Score | 2 | 2 |
| Naming: Strict CamelCase | 0.9844 | 0.9870 |
| Naming: Underscore Style | 0.0031 | 0.0000 |
| Naming: Non-conformant | 0.0125 | 0.0130 |
| Label Coverage | 0.9564 | 0.9870 |
| Comment Coverage | 0.9408 | 0.9805 |

---

## 2. Generated Ontologies — Summary by Agent Type

Each folder contains 20 generated ontologies for the EDIFACT domain story.

### 2.1 High-level Validation Summary

| Agent Type | N | Syntax Valid | HermiT Consistent | Pellet Consistent | OOPS Passed | No Critical Pitfalls |
|------------|:-:|:------------:|:-----------------:|:-----------------:|:-----------:|:--------------------:|
| **workflow** | 15 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| **singleAgent** | 17 | 100.0% | 85.0% | 85.0% | 100.0% | 100.0% |
| **dualAgent** | 20 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| **triAgent** | 11 | 100.0% | 85.0% | 70.0% | 65.0% | 95.0% |

### 2.2 Structural Metrics (avg / median)

| Agent Type | Triples avg | Triples med | Classes avg | Classes med | Obj Props avg | Data Props avg | Ann Props avg |
|------------|:-----------:|:-----------:|:-----------:|:-----------:|:-------------:|:--------------:|:-------------:|
| **workflow** | 856 | 845 | 65.2 | 65 | 64.3 | 48.3 | 0 |
| **singleAgent** | 325.6 | 339 | 18.9 | 19 | 28.8 | 11.4 | 0.1 |
| **dualAgent** | 316.1 | 323.5 | 18.6 | 18.5 | 29.5 | 9.6 | 0 |
| **triAgent** | 387.9 | 405 | 27.3 | 27 | 35.6 | 6.5 | 0 |

### 2.3 Structural Range (min–max)

| Agent Type | Triples min | Triples max | Classes min | Classes max |
|------------|:-----------:|:-----------:|:-----------:|:-----------:|
| **workflow** | 696 | 1045 | 56 | 74 |
| **singleAgent** | 267 | 386 | 16 | 21 |
| **dualAgent** | 227 | 373 | 13 | 22 |
| **triAgent** | 270 | 444 | 22 | 37 |

### 2.4 OOPS Pitfall Summary

| Agent Type | Total Pitfall Occurrences | Unique Pitfalls | Most Common |
|------------|:-------------------------:|:---------------:|-------------|
| **workflow** | 0 | 0 | None |
| **singleAgent** | 0 | 0 | None |
| **dualAgent** | 0 | 0 | None |
| **triAgent** | 10 | 5 | P04 (×4), P20 (×2), P22 (×2), P12 (×1), P13 (×1) |

### 2.5 Hierarchy Complexity (avg across ontologies in folder)

| Agent Type | Max Depth (max) | Max Depth (avg) | Avg Depth (avg) | Max Branching (max) | Avg Branching (avg) | Leaf Classes (avg) |
|------------|:---------------:|:---------------:|:---------------:|:-------------------:|:-------------------:|:------------------:|
| **workflow** | 4 | 2.5 | 0.6 | 39 | 2.5 | 50.7 |
| **singleAgent** | 5 | 1.7 | 0.4 | 4 | 1.6 | 15.8 |
| **dualAgent** | 4 | 1.2 | 0.3 | 4 | 1.6 | 15.7 |
| **triAgent** | 3 | 1.5 | 0.4 | 8 | 2.1 | 23 |

### 2.6 OntoQA Structural Ratios

| Agent Type | RR avg | AR avg | IR avg |
|------------|:------:|:------:|:------:|
| **workflow** | 0.6000 | 0.7000 | 0.5000 |
| **singleAgent** | 0.9000 | 0.6000 | 0.3000 |
| **dualAgent** | 0.9000 | 0.5000 | 0.3000 |
| **triAgent** | 0.8000 | 0.2000 | 0.3000 |

### 2.7 Axiom Complexity & Lexical Quality

| Agent Type | Axiom Diversity avg | Axiom Diversity max | Naming Strict avg | Naming Underscore avg | Naming Bad avg | Label Coverage avg | Comment Coverage avg |
|------------|:-------------------:|:-------------------:|:-----------------:|:---------------------:|:--------------:|:------------------:|:--------------------:|
| **workflow** | 7.1 | 8 | 0.6000 | 0.4000 | 0.0000 | 0.3000 | 0.1000 |
| **singleAgent** | 4.5 | 7 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 |
| **dualAgent** | 3.4 | 6 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 |
| **triAgent** | 5.2 | 7 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 |

### 2.8 Generator Performance

| Agent Type | Gen Success Rate | Avg Duration (s) | Avg Iterations | Pitfalls During Gen |
|------------|:----------------:|:----------------:|:--------------:|:-------------------:|
| **workflow** | 100.0% | 332.1 | N/A | 0 |
| **singleAgent** | 0.0% | 0 | N/A | 0 |
| **dualAgent** | 100.0% | 180.1 | 2.2 | 9 |
| **triAgent** | 100.0% | 1037.9 | 3.0 | 0 |

---

## 3. Per-Folder Detail

### 3.1 workflow

**HermiT inconsistent classes (16):** `xml_combined_owl.xml.Cl_Information`, `owl.Nothing`, `xml_combined_owl.xml.Cl_ItemSoldDate`, `xml_combined_owl.xml.Cl_Invoice`, `xml_combined_owl.xml.Cl_ItemSKU`, `xml_combined_owl.xml.Cl_ItemName`, `xml_combined_owl.xml.Cl_ItemPrice`, `xml_combined_owl.xml.Cl_InvoiceOrganizationRole`, `xml_combined_owl.xml.Cl_InvoiceLine`, `xml_combined_owl.xml.Cl_ItemImage` ...

**Pellet inconsistent classes (70):** `xml_combined_owl.xml.Cl_Service`, `xml_combined_owl.xml.Cl_InvoiceLine`, `xml_combined_owl.xml.Cl_OrganizationInvolvementDisplay`, `xml_combined_owl.xml.Cl_ProvidedInformation`, `xml_combined_owl.xml.Cl_RequiredInformation`, `xml_combined_owl.xml.Cl_InvoiceAssignment`, `xml_combined_owl.xml.Cl_SellerRole`, `xml_combined_owl.xml.Cl_DisplayAttribute`, `xml_combined_owl.xml.Cl_InvoiceDetail`, `xml_combined_owl.xml.Cl_OrganizationInformationDisplay` ...

**Validation Results**

| File (15) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_combined_turtle_20260301_223728.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_235347.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_223204.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_222612.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_221951.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_215419.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_220409.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_232958.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_231410.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_230354.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_221415.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_233503.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_220919.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_234726.owl` | ✅ | ❌ | ❌ | ✅ |
| `EDIFACT_combined_turtle_20260301_231957.owl` | ✅ | ❌ | ❌ | ✅ |

**Extracted Details**

| File (15) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_combined_turtle_20260301_223728.owl` | 74 | 75 | 48 | 0 | 899 | 2 | 0.51 | 6 | 58 | 0.6696 | 0.6486 | 0.5 | 8 | 0.6244 | 0.3756 | 0.0 | 0.1421 | 0.0305 |
| `EDIFACT_combined_turtle_20260301_235347.owl` | 74 | 69 | 46 | 0 | 1045 | 4 | 0.77 | 8 | 55 | 0.6509 | 0.6216 | 0.5 | 6 | 0.6085 | 0.3915 | 0.0 | 0.5291 | 0.3862 |
| `EDIFACT_combined_turtle_20260301_223204.owl` | 72 | 62 | 46 | 0 | 911 | 2 | 0.56 | 7 | 54 | 0.62 | 0.6389 | 0.5278 | 8 | 0.6 | 0.4 | 0.0 | 0.5111 | 0.2444 |
| `EDIFACT_combined_turtle_20260301_222612.owl` | 69 | 65 | 47 | 0 | 803 | 2 | 0.55 | 6 | 53 | 0.6311 | 0.6812 | 0.5507 | 7 | 0.5746 | 0.4254 | 0.0 | 0.2044 | 0.1271 |
| `EDIFACT_combined_turtle_20260301_221951.owl` | 68 | 58 | 61 | 0 | 882 | 3 | 0.71 | 8 | 53 | 0.6105 | 0.8971 | 0.5441 | 7 | 0.6364 | 0.3636 | 0.0 | 0.262 | 0.0749 |
| `EDIFACT_combined_turtle_20260301_215419.owl` | 66 | 53 | 43 | 0 | 713 | 2 | 0.62 | 6 | 52 | 0.6235 | 0.6515 | 0.4848 | 6 | 0.6149 | 0.3851 | 0.0 | 0.087 | 0.1118 |
| `EDIFACT_combined_turtle_20260301_220409.owl` | 65 | 67 | 44 | 0 | 845 | 3 | 1.06 | 39 | 52 | 0.5194 | 0.6769 | 0.9538 | 7 | 0.5966 | 0.4034 | 0.0 | 0.125 | 0.0966 |
| `EDIFACT_combined_turtle_20260301_232958.owl` | 65 | 62 | 51 | 0 | 816 | 2 | 0.43 | 5 | 52 | 0.6813 | 0.7846 | 0.4462 | 6 | 0.6236 | 0.3764 | 0.0 | 0.2135 | 0.0281 |
| `EDIFACT_combined_turtle_20260301_231410.owl` | 64 | 63 | 52 | 0 | 784 | 2 | 0.3 | 3 | 52 | 0.7683 | 0.8125 | 0.2969 | 8 | 0.5866 | 0.4134 | 0.0 | 0.3408 | 0.1732 |
| `EDIFACT_combined_turtle_20260301_230354.owl` | 63 | 72 | 53 | 0 | 965 | 3 | 0.89 | 16 | 48 | 0.6102 | 0.8413 | 0.7302 | 8 | 0.633 | 0.367 | 0.0 | 0.4628 | 0.0106 |
| `EDIFACT_combined_turtle_20260301_221415.owl` | 62 | 65 | 47 | 0 | 877 | 2 | 0.48 | 7 | 49 | 0.6842 | 0.7581 | 0.4839 | 6 | 0.6416 | 0.3584 | 0.0 | 0.3295 | 0.0173 |
| `EDIFACT_combined_turtle_20260301_233503.owl` | 62 | 71 | 53 | 0 | 773 | 2 | 0.53 | 7 | 52 | 0.6961 | 0.8548 | 0.5 | 6 | 0.6667 | 0.3333 | 0.0 | 0.2204 | 0.0215 |
| `EDIFACT_combined_turtle_20260301_220919.owl` | 59 | 60 | 45 | 0 | 829 | 3 | 0.78 | 7 | 42 | 0.625 | 0.7627 | 0.6102 | 8 | 0.6402 | 0.3598 | 0.0 | 0.3963 | 0.0061 |
| `EDIFACT_combined_turtle_20260301_234726.owl` | 59 | 70 | 47 | 0 | 1002 | 3 | 0.97 | 5 | 44 | 0.6667 | 0.7966 | 0.5932 | 8 | 0.6648 | 0.3352 | 0.0 | 0.6136 | 0.3352 |
| `EDIFACT_combined_turtle_20260301_231957.owl` | 56 | 53 | 41 | 0 | 696 | 2 | 0.5 | 10 | 45 | 0.6709 | 0.7321 | 0.4643 | 7 | 0.6267 | 0.3733 | 0.0 | 0.02 | 0.02 |

### 3.2 singleAgent

**HermiT inconsistent classes (8):** `ontology.Buyer`, `ontology.Organization`, `ontology.Price`, `ontology.DeliveryParty`, `ontology.AgentRole`, `ontology.OrganizationRoleAssignment`, `ontology.RoleAssignment`, `owl.Nothing`

**Pellet inconsistent classes (8):** `ontology.Buyer`, `ontology.Organization`, `ontology.Price`, `ontology.DeliveryParty`, `ontology.AgentRole`, `ontology.OrganizationRoleAssignment`, `ontology.RoleAssignment`, `owl.Nothing`

**Validation Results**

| File (17) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_ontology_20260304_070119.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_075831.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_062606.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_063345.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_071919.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_072404.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_112519.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_085410.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_090528.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_093001.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_094903.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_071618.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_075320.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_072939.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_092221.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_111526.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260304_073706.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File (17) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260304_070119.owl` | 21 | 32 | 13 | 0 | 345 | 4 | 1.29 | 3 | 14 | 0.7442 | 0.619 | 0.5238 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_075831.owl` | 21 | 28 | 13 | 1 | 349 | 1 | 0.33 | 3 | 17 | 0.8 | 0.619 | 0.3333 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_062606.owl` | 20 | 28 | 13 | 0 | 348 | 2 | 0.5 | 3 | 16 | 0.8235 | 0.65 | 0.3 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_063345.owl` | 20 | 32 | 15 | 0 | 362 | 1 | 0.2 | 3 | 18 | 0.8889 | 0.75 | 0.2 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_071919.owl` | 20 | 22 | 14 | 0 | 285 | 1 | 0.3 | 3 | 17 | 0.7857 | 0.7 | 0.3 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_072404.owl` | 20 | 34 | 13 | 0 | 342 | 1 | 0.35 | 3 | 16 | 0.8293 | 0.65 | 0.35 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_112519.owl` | 20 | 28 | 12 | 0 | 302 | 1 | 0.3 | 3 | 16 | 0.8235 | 0.6 | 0.3 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_085410.owl` | 19 | 30 | 9 | 0 | 305 | 1 | 0.05 | 1 | 18 | 0.9677 | 0.4737 | 0.0526 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_090528.owl` | 19 | 30 | 11 | 0 | 341 | 1 | 0.21 | 3 | 17 | 0.8824 | 0.5789 | 0.2105 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_093001.owl` | 19 | 36 | 14 | 0 | 386 | 5 | 1.74 | 4 | 12 | 0.7826 | 0.7368 | 0.5263 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_094903.owl` | 19 | 28 | 15 | 0 | 340 | 2 | 0.37 | 4 | 16 | 0.8235 | 0.7895 | 0.3158 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_071618.owl` | 18 | 28 | 7 | 0 | 317 | 3 | 0.72 | 3 | 14 | 0.8 | 0.3889 | 0.3889 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_075320.owl` | 18 | 34 | 6 | 0 | 310 | 1 | 0.06 | 1 | 17 | 0.9714 | 0.3333 | 0.0556 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_072939.owl` | 17 | 24 | 8 | 0 | 267 | 1 | 0.24 | 3 | 15 | 0.8571 | 0.4706 | 0.2353 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_092221.owl` | 17 | 28 | 14 | 0 | 339 | 2 | 0.35 | 3 | 14 | 0.8485 | 0.8235 | 0.2941 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_111526.owl` | 17 | 24 | 9 | 0 | 296 | 1 | 0.06 | 1 | 16 | 0.96 | 0.5294 | 0.0588 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260304_073706.owl` | 16 | 24 | 8 | 0 | 302 | 1 | 0.06 | 1 | 15 | 0.96 | 0.5 | 0.0625 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

### 3.3 dualAgent

**Validation Results**

| File (20) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_ontology_20260301_222236.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_220437.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221940.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_223501.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_220832.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_224527.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_215924.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_224922.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_225145.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_225409.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221113.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221332.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_222534.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_223750.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_225732.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_230018.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_230338.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_215700.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_224212.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260301_221725.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File (20) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260301_222236.owl` | 22 | 30 | 12 | 0 | 340 | 1 | 0.41 | 4 | 18 | 0.7692 | 0.5455 | 0.4091 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_220437.owl` | 21 | 40 | 3 | 0 | 369 | 2 | 0.43 | 3 | 17 | 0.8333 | 0.1429 | 0.381 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221940.owl` | 21 | 28 | 5 | 0 | 308 | 1 | 0.33 | 3 | 17 | 0.8 | 0.2381 | 0.3333 | 3 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_223501.owl` | 21 | 32 | 7 | 0 | 316 | 1 | 0.38 | 3 | 17 | 0.8 | 0.3333 | 0.381 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_220832.owl` | 20 | 38 | 8 | 0 | 352 | 1 | 0.3 | 3 | 16 | 0.8636 | 0.4 | 0.3 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_224527.owl` | 20 | 32 | 13 | 0 | 373 | 1 | 0.2 | 3 | 18 | 0.8889 | 0.65 | 0.2 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_215924.owl` | 19 | 34 | 8 | 0 | 322 | 1 | 0.11 | 1 | 17 | 0.9444 | 0.4211 | 0.1053 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_224922.owl` | 19 | 34 | 7 | 0 | 304 | 1 | 0.32 | 3 | 15 | 0.85 | 0.3684 | 0.3158 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_225145.owl` | 19 | 30 | 9 | 0 | 308 | 2 | 0.47 | 4 | 16 | 0.8108 | 0.4737 | 0.3684 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_225409.owl` | 19 | 30 | 12 | 0 | 315 | 1 | 0.11 | 1 | 17 | 0.9375 | 0.6316 | 0.1053 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221113.owl` | 18 | 28 | 5 | 0 | 261 | 1 | 0.28 | 3 | 15 | 0.8485 | 0.2778 | 0.2778 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221332.owl` | 18 | 32 | 12 | 0 | 327 | 1 | 0.06 | 1 | 17 | 0.9697 | 0.6667 | 0.0556 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_222534.owl` | 18 | 30 | 7 | 0 | 348 | 4 | 1.06 | 3 | 12 | 0.7895 | 0.3889 | 0.4444 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_223750.owl` | 18 | 26 | 15 | 0 | 325 | 1 | 0.22 | 3 | 16 | 0.8667 | 0.8333 | 0.2222 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_225732.owl` | 18 | 26 | 16 | 0 | 338 | 1 | 0.28 | 3 | 15 | 0.8387 | 0.8889 | 0.2778 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_230018.owl` | 18 | 26 | 14 | 0 | 327 | 1 | 0.28 | 3 | 15 | 0.8387 | 0.7778 | 0.2778 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_230338.owl` | 17 | 26 | 14 | 0 | 335 | 1 | 0.06 | 1 | 16 | 0.963 | 0.8235 | 0.0588 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_215700.owl` | 16 | 22 | 9 | 0 | 235 | 1 | 0.25 | 3 | 14 | 0.8462 | 0.5625 | 0.25 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_224212.owl` | 16 | 24 | 8 | 0 | 292 | 1 | 0.25 | 3 | 14 | 0.8571 | 0.5 | 0.25 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260301_221725.owl` | 13 | 22 | 8 | 0 | 227 | 1 | 0.08 | 1 | 12 | 0.9565 | 0.6154 | 0.0769 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

### 3.4 triAgent

**HermiT inconsistent classes (5):** `ontology.BuyerRole`, `ontology.GLNIdentifier`, `ontology.InvoiceMessage`, `owl.Nothing`, `ontology.SimpleDataElement`

**Pellet inconsistent classes (5):** `ontology.BuyerRole`, `ontology.GLNIdentifier`, `ontology.InvoiceMessage`, `owl.Nothing`, `ontology.SimpleDataElement`

**Validation Results**

| File (11) | Syntax | HermiT | Pellet | OOPS |
|------|:------:|:------:|:------:|:----:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |
| `EDIFACT_ontology_20260302_081000.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260302_124024.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260303_094621.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260302_140235.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260302_133553.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260302_073654.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_085821.owl` | ✅ | ✅ | ✅ | ❌ |
| `EDIFACT_ontology_20260303_061520.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_070100.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260302_082612.owl` | ✅ | ✅ | ✅ | ✅ |
| `EDIFACT_ontology_20260303_091850.owl` | ✅ | ✅ | ✅ | ✅ |

**Extracted Details**

| File (11) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |
|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|
| **TUMedifact (trimmed)** _(baseline)_ | **31** | **10** | **261** | **9** | **2267** | **1** | **0.81** | **21** | **26** | **0.2778** | **8.4194** | **0.8387** | **2** | **0.987** | **0.0** | **0.013** | **0.987** | **0.9805** |
| `EDIFACT_ontology_20260302_081000.owl` | 37 | 30 | 8 | 0 | 367 | 2 | 0.81 | 8 | 29 | 0.5769 | 0.2162 | 0.5946 | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_124024.owl` | 30 | 27 | 2 | 0 | 314 | 1 | 0.3 | 3 | 25 | 0.75 | 0.0667 | 0.3 | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_094621.owl` | 30 | 42 | 7 | 0 | 440 | 1 | 0.37 | 3 | 24 | 0.7925 | 0.2333 | 0.3667 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_140235.owl` | 29 | 40 | 14 | 0 | 426 | 2 | 0.38 | 3 | 24 | 0.7843 | 0.4828 | 0.3793 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_133553.owl` | 28 | 23 | 3 | 0 | 270 | 1 | 0.25 | 5 | 25 | 0.7667 | 0.1071 | 0.25 | 5 | 0.9444 | 0.0556 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_073654.owl` | 27 | 38 | 2 | 0 | 396 | 3 | 0.74 | 3 | 20 | 0.76 | 0.0741 | 0.4444 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_085821.owl` | 27 | 34 | 3 | 0 | 365 | 1 | 0.3 | 5 | 24 | 0.8095 | 0.1111 | 0.2963 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_061520.owl` | 24 | 38 | 11 | 0 | 444 | 1 | 0.17 | 2 | 21 | 0.9048 | 0.4583 | 0.1667 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_070100.owl` | 24 | 34 | 12 | 0 | 411 | 1 | 0.21 | 2 | 21 | 0.8718 | 0.5 | 0.2083 | 7 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260302_082612.owl` | 22 | 42 | 5 | 0 | 405 | 2 | 0.32 | 3 | 20 | 0.913 | 0.2273 | 0.1818 | 6 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| `EDIFACT_ontology_20260303_091850.owl` | 22 | 44 | 4 | 0 | 429 | 1 | 0.27 | 5 | 20 | 0.88 | 0.1818 | 0.2727 | 5 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |

---

## 4. Comparison with Reference Ontologies

Values compared against **TUMedifact (full)** and **TUMedifact (trimmed)**.

| Agent Type | Triples avg | vs Full | vs Trimmed | Classes avg | vs Full | vs Trimmed |
|------------|:-----------:|:-------:|:----------:|:-----------:|:-------:|:----------:|
| **workflow** | 856 | -1814 | -1411 | 65.2 | +34 | +34 |
| **singleAgent** | 325.6 | -2344 | -1941 | 18.9 | -12 | -12 |
| **dualAgent** | 316.1 | -2354 | -1951 | 18.6 | -12 | -12 |
| **triAgent** | 387.9 | -2282 | -1879 | 27.3 | -4 | -4 |

_Reference — TUMedifact (full): 2670 triples, 31 classes_  
_Reference — TUMedifact (trimmed): 2267 triples, 31 classes_

---

## 5. Key Observations

- **workflow**: HermiT consistency rate is 0.0% — 15 ontologies are inconsistent.
- **workflow**: Average class count is 65.2 (210.3% of reference full ontology's 31 classes).
- **singleAgent**: HermiT consistency rate is 85.0% — 3 ontologies are inconsistent.
- **singleAgent**: Average class count is 18.9 (61.0% of reference full ontology's 31 classes).
- **dualAgent**: Average class count is 18.6 (60.0% of reference full ontology's 31 classes).
- **triAgent**: HermiT consistency rate is 85.0% — 2 ontologies are inconsistent.
- **triAgent**: 10 OOPS pitfall occurrence(s) detected across runs (most common: P04, P20, P22, P12, P13).
- **triAgent**: Average class count is 27.3 (88.1% of reference full ontology's 31 classes).

---

## 6. Metric Definitions

### Structural Ratios (OntoQA Framework)
- **RR (Relationship Richness)** = `|ObjectProperties| / (|subClassOf axioms| + |ObjectProperties|)`. Ratio of non-taxonomic to all relations. Higher values indicate a more interconnected graph rather than a flat taxonomy.
- **AR (Attribute Richness)** = `|DatatypeProperties| / |Classes|`. Average number of data properties per class. Higher values indicate richer per-instance data modelling.
- **IR (Inheritance Richness)** = `|subClassOf triples| / |all named classes|`. Average number of inheritance edges per class (including leaf classes). Distinct from Avg Branching which only considers parent classes.

### Axiom Complexity
- **Axiom Diversity Score** (0–10): Count of distinct advanced OWL constructs present in the ontology, out of: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, `owl:equivalentClass`, `owl:unionOf`, `owl:intersectionOf`, `owl:hasValue`, and cardinality restrictions (`owl:cardinality`, `owl:minCardinality`, `owl:maxCardinality`, counted as one). A score of 0 means the ontology uses only declarations and `rdfs:subClassOf`; a score of 10 means all construct types are present.

### Lexical & Annotation Quality
- **Naming: Strict CamelCase** (0.0–1.0): Fraction of named entities matching strict Semantic Web conventions — UpperCamelCase for classes (`^[A-Z][A-Za-z0-9]*$`), lowerCamelCase for properties (`^[a-z][A-Za-z0-9]*$`). No underscores.
- **Naming: Underscore Style** (0.0–1.0): Fraction that follow camelCase with underscores (e.g. `Cl_Invoice`), a common prefix-based variation that would pass if underscores are allowed but failed the strict check.
- **Naming: Non-conformant** (0.0–1.0): Fraction that match neither pattern. The three fractions sum to 1.0.
- **Label Coverage** (0.0–1.0): Fraction of named entities (classes + all property types) that have at least one `rdfs:label` triple. 1.0 = fully labelled.
- **Comment Coverage** (0.0–1.0): Fraction of named entities that have at least one `rdfs:comment` triple. 1.0 = fully documented.

### Hierarchy Metrics
- **Max Depth**: Length of the longest `rdfs:subClassOf` chain from a root class (no parent) to a leaf class. Computed via BFS.
- **Avg Depth**: Mean depth across all named classes.
- **Max Branching**: Highest number of direct subclasses any single class has.
- **Avg Branching**: Mean number of direct subclasses per class, computed only over classes that have at least one child (excludes leaf classes).
- **Leaf Classes**: Count of classes with no direct subclasses.
