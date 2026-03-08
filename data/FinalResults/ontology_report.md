# Ontology Quality Report

> Generated automatically from `generate_ontology_report.py`  
> Date: /Users/i833032/DevResearch/Otho

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

---

## 2. Generated Ontologies — Summary by Agent Type

Each folder contains 20 generated ontologies for the EDIFACT domain story.

### 2.1 High-level Validation Summary

| Agent Type | N | Syntax Valid | HermiT Consistent | Pellet Consistent | OOPS Passed | No Critical Pitfalls |
|------------|:-:|:------------:|:-----------------:|:-----------------:|:-----------:|:--------------------:|
| **workflow** | 20 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| **singleAgent** | 20 | 100.0% | 85.0% | 85.0% | 100.0% | 100.0% |
| **dualAgent** | 20 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| **triAgent** | 20 | 100.0% | 85.0% | 70.0% | 65.0% | 95.0% |

### 2.2 Structural Metrics (avg / median / min / max)

| Agent Type | Triples avg | Triples med | Classes avg | Classes med | Obj Props avg | Data Props avg | Ann Props avg |
|------------|:-----------:|:-----------:|:-----------:|:-----------:|:-------------:|:--------------:|:-------------:|
| **workflow** | 846.1 | 834.0 | 77.2 | 75.0 | 64.2 | 48.5 | 0 |
| **singleAgent** | 319.9 | 328.0 | 19.8 | 20.0 | 28.1 | 11.2 | 0.1 |
| **dualAgent** | 316.1 | 323.5 | 19 | 19.0 | 29.5 | 9.6 | 0 |
| **triAgent** | 359.4 | 400.5 | 28.4 | 29.0 | 31.8 | 6.3 | 0 |

### 2.3 Structural Range (min–max)

| Agent Type | Triples min | Triples max | Classes min | Classes max |
|------------|:-----------:|:-----------:|:-----------:|:-----------:|
| **workflow** | 696 | 1045 | 68 | 91 |
| **singleAgent** | 224 | 386 | 17 | 22 |
| **dualAgent** | 227 | 373 | 13 | 23 |
| **triAgent** | 3 | 623 | 0 | 39 |

### 2.4 OOPS Pitfall Summary

| Agent Type | Total Pitfall Occurrences | Unique Pitfalls | Most Common |
|------------|:-------------------------:|:---------------:|-------------|
| **workflow** | 0 | 0 | None |
| **singleAgent** | 0 | 0 | None |
| **dualAgent** | 0 | 0 | None |
| **triAgent** | 10 | 5 | P04 (×4), P20 (×2), P22 (×2), P12 (×1), P13 (×1) |

### 2.5 Generator Performance

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

| File | Syntax | HermiT | Pellet | OOPS | Classes | Obj Props | Data Props | Ann Props | Triples |
|------|:------:|:------:|:------:|:----:|:-------:|:---------:|:----------:|:---------:|:-------:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — | **31** | **10** | **261** | **9** | **2267** |
| `EDIFACT_combined_turtle_20260301_223204.owl` | ✅ | ❌ | ❌ | ✅ | 91 | 62 | 46 | 0 | 911 |
| `EDIFACT_combined_turtle_20260301_223728.owl` | ✅ | ❌ | ❌ | ✅ | 89 | 75 | 48 | 0 | 899 |
| `EDIFACT_combined_turtle_20260301_235347.owl` | ✅ | ❌ | ❌ | ✅ | 89 | 69 | 46 | 0 | 1045 |
| `EDIFACT_combined_turtle_20260301_214840.owl` | ✅ | ❌ | ❌ | ✅ | 88 | 72 | 50 | 0 | 914 |
| `EDIFACT_combined_turtle_20260301_221951.owl` | ✅ | ❌ | ❌ | ✅ | 82 | 58 | 61 | 0 | 882 |
| `EDIFACT_combined_turtle_20260301_220409.owl` | ✅ | ❌ | ❌ | ✅ | 81 | 67 | 44 | 0 | 845 |
| `EDIFACT_combined_turtle_20260301_222612.owl` | ✅ | ❌ | ❌ | ✅ | 79 | 65 | 47 | 0 | 803 |
| `EDIFACT_combined_turtle_20260301_230354.owl` | ✅ | ❌ | ❌ | ✅ | 78 | 72 | 53 | 0 | 965 |
| `EDIFACT_combined_turtle_20260301_233503.owl` | ✅ | ❌ | ❌ | ✅ | 77 | 71 | 53 | 0 | 773 |
| `EDIFACT_combined_turtle_20260301_232450.owl` | ✅ | ❌ | ❌ | ✅ | 75 | 54 | 49 | 0 | 798 |
| `EDIFACT_combined_turtle_20260301_232958.owl` | ✅ | ❌ | ❌ | ✅ | 75 | 62 | 51 | 0 | 816 |
| `EDIFACT_combined_turtle_20260301_221415.owl` | ✅ | ❌ | ❌ | ✅ | 74 | 65 | 47 | 0 | 877 |
| `EDIFACT_combined_turtle_20260301_215907.owl` | ✅ | ❌ | ❌ | ✅ | 73 | 57 | 50 | 0 | 808 |
| `EDIFACT_combined_turtle_20260301_220919.owl` | ✅ | ❌ | ❌ | ✅ | 73 | 60 | 45 | 0 | 829 |
| `EDIFACT_combined_turtle_20260301_215419.owl` | ✅ | ❌ | ❌ | ✅ | 71 | 53 | 43 | 0 | 713 |
| `EDIFACT_combined_turtle_20260301_230929.owl` | ✅ | ❌ | ❌ | ✅ | 71 | 64 | 47 | 0 | 723 |
| `EDIFACT_combined_turtle_20260301_234726.owl` | ✅ | ❌ | ❌ | ✅ | 71 | 70 | 47 | 0 | 1002 |
| `EDIFACT_combined_turtle_20260301_231410.owl` | ✅ | ❌ | ❌ | ✅ | 70 | 63 | 52 | 0 | 784 |
| `EDIFACT_combined_turtle_20260301_234116.owl` | ✅ | ❌ | ❌ | ✅ | 70 | 73 | 51 | 0 | 839 |
| `EDIFACT_combined_turtle_20260301_231957.owl` | ✅ | ❌ | ❌ | ✅ | 68 | 53 | 41 | 0 | 696 |

### 3.2 singleAgent

**HermiT inconsistent classes (8):** `ontology.Buyer`, `ontology.Organization`, `ontology.Price`, `ontology.DeliveryParty`, `ontology.AgentRole`, `ontology.OrganizationRoleAssignment`, `ontology.RoleAssignment`, `owl.Nothing`

**Pellet inconsistent classes (8):** `ontology.Buyer`, `ontology.Organization`, `ontology.Price`, `ontology.DeliveryParty`, `ontology.AgentRole`, `ontology.OrganizationRoleAssignment`, `ontology.RoleAssignment`, `owl.Nothing`

| File | Syntax | HermiT | Pellet | OOPS | Classes | Obj Props | Data Props | Ann Props | Triples |
|------|:------:|:------:|:------:|:----:|:-------:|:---------:|:----------:|:---------:|:-------:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — | **31** | **10** | **261** | **9** | **2267** |
| `EDIFACT_ontology_20260304_075831.owl` | ✅ | ✅ | ✅ | ✅ | 22 | 28 | 13 | 1 | 349 |
| `EDIFACT_ontology_20260304_070119.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 32 | 13 | 0 | 345 |
| `EDIFACT_ontology_20260304_071618.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 28 | 7 | 0 | 317 |
| `EDIFACT_ontology_20260304_073706.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 24 | 8 | 0 | 302 |
| `EDIFACT_ontology_20260304_074731.owl` | ✅ | ❌ | ❌ | ✅ | 21 | 36 | 12 | 0 | 363 |
| `EDIFACT_ontology_20260304_090528.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 30 | 11 | 0 | 341 |
| `EDIFACT_ontology_20260304_094903.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 28 | 15 | 0 | 340 |
| `EDIFACT_ontology_20260304_062606.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 28 | 13 | 0 | 348 |
| `EDIFACT_ontology_20260304_063345.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 32 | 15 | 0 | 362 |
| `EDIFACT_ontology_20260304_063821.owl` | ✅ | ❌ | ❌ | ✅ | 20 | 13 | 12 | 0 | 224 |
| `EDIFACT_ontology_20260304_071919.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 22 | 14 | 0 | 285 |
| `EDIFACT_ontology_20260304_072404.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 34 | 13 | 0 | 342 |
| `EDIFACT_ontology_20260304_085410.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 30 | 9 | 0 | 305 |
| `EDIFACT_ontology_20260304_093001.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 36 | 14 | 0 | 386 |
| `EDIFACT_ontology_20260304_112519.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 28 | 12 | 0 | 302 |
| `EDIFACT_ontology_20260304_110544.owl` | ✅ | ❌ | ❌ | ✅ | 19 | 22 | 7 | 0 | 275 |
| `EDIFACT_ontology_20260304_075320.owl` | ✅ | ✅ | ✅ | ✅ | 18 | 34 | 6 | 0 | 310 |
| `EDIFACT_ontology_20260304_072939.owl` | ✅ | ✅ | ✅ | ✅ | 17 | 24 | 8 | 0 | 267 |
| `EDIFACT_ontology_20260304_092221.owl` | ✅ | ✅ | ✅ | ✅ | 17 | 28 | 14 | 0 | 339 |
| `EDIFACT_ontology_20260304_111526.owl` | ✅ | ✅ | ✅ | ✅ | 17 | 24 | 9 | 0 | 296 |

### 3.3 dualAgent

| File | Syntax | HermiT | Pellet | OOPS | Classes | Obj Props | Data Props | Ann Props | Triples |
|------|:------:|:------:|:------:|:----:|:-------:|:---------:|:----------:|:---------:|:-------:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — | **31** | **10** | **261** | **9** | **2267** |
| `EDIFACT_ontology_20260301_222236.owl` | ✅ | ✅ | ✅ | ✅ | 23 | 30 | 12 | 0 | 340 |
| `EDIFACT_ontology_20260301_224527.owl` | ✅ | ✅ | ✅ | ✅ | 22 | 32 | 13 | 0 | 373 |
| `EDIFACT_ontology_20260301_220437.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 40 | 3 | 0 | 369 |
| `EDIFACT_ontology_20260301_221940.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 28 | 5 | 0 | 308 |
| `EDIFACT_ontology_20260301_222534.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 30 | 7 | 0 | 348 |
| `EDIFACT_ontology_20260301_223501.owl` | ✅ | ✅ | ✅ | ✅ | 21 | 32 | 7 | 0 | 316 |
| `EDIFACT_ontology_20260301_215924.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 34 | 8 | 0 | 322 |
| `EDIFACT_ontology_20260301_220832.owl` | ✅ | ✅ | ✅ | ✅ | 20 | 38 | 8 | 0 | 352 |
| `EDIFACT_ontology_20260301_224922.owl` | ✅ | ✅ | ✅ | ✅ | 19 | 34 | 7 | 0 | 304 |
| `EDIFACT_ontology_20260301_225145.owl` | ✅ | ✅ | ✅ | ✅ | 19 | 30 | 9 | 0 | 308 |
| `EDIFACT_ontology_20260301_225409.owl` | ✅ | ✅ | ✅ | ✅ | 19 | 30 | 12 | 0 | 315 |
| `EDIFACT_ontology_20260301_230338.owl` | ✅ | ✅ | ✅ | ✅ | 19 | 26 | 14 | 0 | 335 |
| `EDIFACT_ontology_20260301_221113.owl` | ✅ | ✅ | ✅ | ✅ | 18 | 28 | 5 | 0 | 261 |
| `EDIFACT_ontology_20260301_221332.owl` | ✅ | ✅ | ✅ | ✅ | 18 | 32 | 12 | 0 | 327 |
| `EDIFACT_ontology_20260301_223750.owl` | ✅ | ✅ | ✅ | ✅ | 18 | 26 | 15 | 0 | 325 |
| `EDIFACT_ontology_20260301_225732.owl` | ✅ | ✅ | ✅ | ✅ | 18 | 26 | 16 | 0 | 338 |
| `EDIFACT_ontology_20260301_230018.owl` | ✅ | ✅ | ✅ | ✅ | 18 | 26 | 14 | 0 | 327 |
| `EDIFACT_ontology_20260301_215700.owl` | ✅ | ✅ | ✅ | ✅ | 16 | 22 | 9 | 0 | 235 |
| `EDIFACT_ontology_20260301_224212.owl` | ✅ | ✅ | ✅ | ✅ | 16 | 24 | 8 | 0 | 292 |
| `EDIFACT_ontology_20260301_221725.owl` | ✅ | ✅ | ✅ | ✅ | 13 | 22 | 8 | 0 | 227 |

### 3.4 triAgent

**HermiT inconsistent classes (5):** `ontology.BuyerRole`, `ontology.GLNIdentifier`, `ontology.InvoiceMessage`, `owl.Nothing`, `ontology.SimpleDataElement`

**Pellet inconsistent classes (5):** `ontology.BuyerRole`, `ontology.GLNIdentifier`, `ontology.InvoiceMessage`, `owl.Nothing`, `ontology.SimpleDataElement`

| File | Syntax | HermiT | Pellet | OOPS | Classes | Obj Props | Data Props | Ann Props | Triples |
|------|:------:|:------:|:------:|:----:|:-------:|:---------:|:----------:|:---------:|:-------:|
| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — | **31** | **10** | **261** | **9** | **2267** |
| `EDIFACT_ontology_20260302_075401.owl` | ✅ | ✅ | ✅ | ❌ | 39 | 68 | 2 | 0 | 623 |
| `EDIFACT_ontology_20260302_081000.owl` | ✅ | ✅ | ✅ | ✅ | 37 | 30 | 8 | 0 | 367 |
| `EDIFACT_ontology_20260302_142221.owl` | ✅ | ❌ | ❌ | ❌ | 35 | 0 | 0 | 0 | 165 |
| `EDIFACT_ontology_20260302_071802.owl` | ✅ | ✅ | ❌ | ✅ | 33 | 17 | 13 | 0 | 296 |
| `EDIFACT_ontology_20260302_124024.owl` | ✅ | ✅ | ✅ | ❌ | 33 | 27 | 2 | 0 | 314 |
| `EDIFACT_ontology_20260303_063400.owl` | ✅ | ❌ | ❌ | ❌ | 32 | 40 | 5 | 0 | 427 |
| `EDIFACT_ontology_20260302_133553.owl` | ✅ | ✅ | ✅ | ✅ | 30 | 23 | 3 | 0 | 270 |
| `EDIFACT_ontology_20260303_094621.owl` | ✅ | ✅ | ✅ | ❌ | 30 | 42 | 7 | 0 | 440 |
| `EDIFACT_ontology_20260302_073654.owl` | ✅ | ✅ | ✅ | ✅ | 29 | 38 | 2 | 0 | 396 |
| `EDIFACT_ontology_20260302_140235.owl` | ✅ | ✅ | ✅ | ✅ | 29 | 40 | 14 | 0 | 426 |
| `EDIFACT_ontology_20260303_072631.owl` | ✅ | ✅ | ✅ | ❌ | 29 | 2 | 9 | 0 | 173 |
| `EDIFACT_ontology_20260303_085821.owl` | ✅ | ✅ | ✅ | ❌ | 29 | 34 | 3 | 0 | 365 |
| `EDIFACT_ontology_20260302_130930.owl` | ✅ | ✅ | ❌ | ✅ | 28 | 44 | 13 | 0 | 460 |
| `EDIFACT_ontology_20260303_061520.owl` | ✅ | ✅ | ✅ | ✅ | 28 | 38 | 11 | 0 | 444 |
| `EDIFACT_ontology_20260303_070100.owl` | ✅ | ✅ | ✅ | ✅ | 28 | 34 | 12 | 0 | 411 |
| `EDIFACT_ontology_20260303_093322.owl` | ✅ | ✅ | ❌ | ✅ | 27 | 36 | 3 | 0 | 360 |
| `EDIFACT_ontology_20260302_082612.owl` | ✅ | ✅ | ✅ | ✅ | 25 | 42 | 5 | 0 | 405 |
| `EDIFACT_ontology_20260303_064029.owl` | ✅ | ❌ | ❌ | ✅ | 24 | 36 | 11 | 0 | 414 |
| `EDIFACT_ontology_20260303_091850.owl` | ✅ | ✅ | ✅ | ✅ | 24 | 44 | 4 | 0 | 429 |
| `EDIFACT_ontology_20260303_093956.owl` | ✅ | ✅ | ✅ | ✅ | 0 | 0 | 0 | 0 | 3 |

---

## 4. Comparison with Reference Ontologies

Values compared against **TUMedifact (full)** and **TUMedifact (trimmed)**.

| Agent Type | Triples avg | vs Full | vs Trimmed | Classes avg | vs Full | vs Trimmed |
|------------|:-----------:|:-------:|:----------:|:-----------:|:-------:|:----------:|
| **workflow** | 846.1 | -1824 | -1421 | 77.2 | +46 | +46 |
| **singleAgent** | 319.9 | -2350 | -1947 | 19.8 | -11 | -11 |
| **dualAgent** | 316.1 | -2354 | -1951 | 19 | -12 | -12 |
| **triAgent** | 359.4 | -2311 | -1908 | 28.4 | -3 | -3 |

_Reference — TUMedifact (full): 2670 triples, 31 classes_  
_Reference — TUMedifact (trimmed): 2267 triples, 31 classes_

---

## 5. Key Observations

- **workflow**: HermiT consistency rate is 0.0% — 20 ontologies are inconsistent.
- **workflow**: Average class count is 77.2 (249.0% of reference full ontology's 31 classes).
- **singleAgent**: HermiT consistency rate is 85.0% — 3 ontologies are inconsistent.
- **singleAgent**: Average class count is 19.8 (63.9% of reference full ontology's 31 classes).
- **dualAgent**: Average class count is 19.0 (61.3% of reference full ontology's 31 classes).
- **triAgent**: HermiT consistency rate is 85.0% — 3 ontologies are inconsistent.
- **triAgent**: 10 OOPS pitfall occurrence(s) detected across runs (most common: P04, P20, P22, P12, P13).
- **triAgent**: Average class count is 28.4 (91.6% of reference full ontology's 31 classes).
