# TUMedifact Ontology Diff: Original vs. Trimmed

**Files compared**
- Original: `data/TUMedifact/TUMedifact.owl` (5028 lines)
- Trimmed: `data/TUMedifact/TUMedifact_trimmed.owl` (2907 lines)
- Line reduction: 2121 lines (−42.2 %)

**Method:** Both files were parsed with Python's `xml.etree.ElementTree`. Every element (class, property, annotation) in both files was catalogued and compared directly from the parsed trees. No inference was applied; every finding below is a direct observation of what is or is not present in each file.

---

## 1. Summary of Differences

| Element category | Original count | Trimmed count | Difference |
|---|:-:|:-:|:-:|
| `owl:Ontology` header triples | 13 | 6 | −7 |
| Namespace declarations (`xmlns:*`) | 12 | 10 | −2 |
| `owl:AnnotationProperty` declarations | 22 | 9 | −13 |
| `owl:ObjectProperty` declarations | 10 | 10 | 0 |
| `owl:DatatypeProperty` declarations | 261 | 261 | 0 |
| `owl:Class` declarations | 31 | 31 | 0 |
| `rdf:Description` blocks | 3 | 3 | 0 |
| `rdfs:Datatype` declarations | 1 | 0 | −1 |
| Properties losing `ns1:term_status` | — | — | 261 DPs + 10 OPs + 31 Classes + 3 rdf:Descriptions = **305** |
| Data properties losing `rdfs:subPropertyOf owl:topDataProperty` | — | — | **65** |

---

## 2. Ontology Header (`owl:Ontology` block)

### 2.1 Triples present in original, absent in trimmed

| Triple predicate | Value in original |
|---|---|
| `ns:license` | `https://creativecommons.org/licenses/by-nc/4.0/` |
| `terms:contributor` | `EDIFACT experts from Einkaufsbüro Deutscher Eisenhändler GmbH` |
| `terms:contributor` | `Johannes Mäkelburg` |
| `terms:contributor` | `Maribel Acosta` |
| `terms:created` | `2023-12-06` |
| `terms:creator` | `Johannes Mäkelburg` |
| `terms:creator` | `Maribel Acosta` |
| `terms:issued` | `2023-12-06` (typed as `xsd:date`) |
| `terms:modified` | `2023-12-06` |
| `terms:publisher` | `Johannes Mäkelburg` |
| `terms:rights` | `Copyright © 2024 Johannes Mäkelburg, Maribel Acosta Deibe` |

### 2.2 Triples present in both files (unchanged)

`terms:description`, `terms:title`, `vann:preferredNamespacePrefix`, `vann:preferredNamespaceUri`, `rdfs:comment`, `rdfs:label`, `owl:versionInfo`.

---

## 3. Namespace Declarations (root `rdf:RDF` element)

### 3.1 Namespaces present in original, absent in trimmed

| Prefix | URI |
|---|---|
| `xmlns:ns` | `http://creativecommons.org/ns#` |
| `xmlns:ns1` | `http://www.w3.og/2003/06/sw-vocab-status/ns#` *(note: contains typo "w3.og" — this is the URI as written in the original)* |

### 3.2 Namespaces present in both files (unchanged)

`xmlns` (default), `xml:base`, `xmlns:owl`, `xmlns:rdf`, `xmlns:xml`, `xmlns:xsd`, `xmlns:rdfs`, `xmlns:vann`, `xmlns:terms`, `xmlns:ontology`.

---

## 4. Annotation Property Declarations

### 4.1 Declared in original only (13 removed)

| Local name | Full URI | Notes in original |
|---|---|---|
| `license` | `http://creativecommons.org/ns#license` | No child triples |
| `contributor` | `http://purl.org/dc/terms/contributor` | No child triples |
| `created` | `http://purl.org/dc/terms/created` | No child triples |
| `creator` | `http://purl.org/dc/terms/creator` | No child triples |
| `issued` | `http://purl.org/dc/terms/issued` | No child triples |
| `modified` | `http://purl.org/dc/terms/modified` | No child triples |
| `publisher` | `http://purl.org/dc/terms/publisher` | No child triples |
| `rights` | `http://purl.org/dc/terms/rights` | No child triples |
| `term_status` | `http://www.w3.og/2003/06/sw-vocab-status/ns#term_status` | No child triples |
| `subClassOf` | `http://www.w3.org/2000/01/rdf-schema#subClassOf` | No child triples |
| `subPropertyOf` | `http://www.w3.org/2000/01/rdf-schema#subPropertyOf` | Has `rdfs:label "subPropertyOf"@en` |
| `disjointWith` | `http://www.w3.org/2002/07/owl#disjointWith` | Has `rdfs:label "disjointWith"@en` |
| `inverseOf` | `http://www.w3.org/2002/07/owl#inverseOf` | Has `rdfs:label "inverseOf"@en` |

### 4.2 Declared in both files (9 retained)

`terms:description`, `terms:title`, `vann:preferredNamespacePrefix`, `vann:preferredNamespaceUri`, `edifact-o:E-Invoice`, `edifact-o:EDIFACT-Structure`, `edifact-o:InvoiceContent`, `edifact-o:seeEDIFACT`, `edifact-o:seeXML`.

The `EDIFACT-Structure` and `InvoiceContent` declarations retain their `rdfs:subPropertyOf edifact-o:E-Invoice` child triple in both files. The `seeEDIFACT` and `seeXML` declarations retain their `rdfs:label` child triple in both files.

### 4.3 Declared in trimmed only

None.

---

## 5. Datatype Declarations

The original declares `rdfs:Datatype rdf:about="http://www.w3.org/2001/XMLSchema#date"`. This declaration is absent in the trimmed file. The `xsd:date` datatype is still referenced within property definitions in both files; only its explicit `rdfs:Datatype` declaration has been removed.

---

## 6. Object Properties (10 in both files)

All 10 object properties are present in both files with identical URIs. The differences are purely in the set of child triples on each property element.

### 6.1 Axioms removed from all 10 object properties

Every object property in the original has both of the following child triples. Neither is present in the trimmed file for any object property.

| Removed triple | Value |
|---|---|
| `rdfs:subPropertyOf` | `owl:topObjectProperty` |
| `ns1:term_status` | `stable` |

### 6.2 Object properties affected (all 10)

1. `agentrole:isPerformedBy`
2. `agentrole:isProvidedBy`
3. `agentrole:performsAgentRole`
4. `agentrole:providesAgentRole`
5. `edifact-o:followsStandard`
6. `edifact-o:hasInvoiceDetails`
7. `edifact-o:hasItem`
8. `edifact-o:isInvoiceDetailsOf`
9. `edifact-o:isItemOf`
10. `edifact-o:isStandardOf`

### 6.3 Axioms retained in both files for all object properties

`owl:inverseOf`, `rdfs:domain`, `rdfs:range`, `rdfs:comment`, `rdfs:label`, `rdfs:isDefinedBy` — all present and identical in both versions.

---

## 7. Data Properties (261 in both files)

All 261 data properties are present in both files with identical URIs. Every data property shows a difference. The differences fall into exactly two patterns.

### 7.1 Pattern A — `ns1:term_status` removed (261 of 261)

Every data property in the original has the child triple:

```xml
<ns1:term_status>stable</ns1:term_status>
```

This triple is absent from every data property in the trimmed file.

### 7.2 Pattern B — `rdfs:subPropertyOf owl:topDataProperty` removed (65 of 261)

65 data properties in the original carry an explicit `rdfs:subPropertyOf owl:topDataProperty` triple that is not present in the trimmed file. The 196 remaining data properties do not have this triple in either file.

The 65 affected properties are listed below, grouped by namespace.

**External namespaces (9 properties)**

| Property | Namespace |
|---|---|
| `hasCountryCode` | `http://purl.org/cerif/frapo/` |
| `date` | `http://purl.org/dc/elements/1.1/` |
| `identifier` | `http://purl.org/dc/elements/1.1/` |
| `amount` | `http://schema.org/` |
| `currency` | `http://schema.org/` |
| `hasMeasurement` | `http://schema.org/` |
| `hasStreetAddress` | `http://www.w3.org/2006/vcard/ns#` |
| `invoicedQuantityUnitOfMeasure` | `https://purl.org/p2p-o/documentline#` |
| `itemName` | `https://purl.org/p2p-o/item#` |
| `countrySubdivision` | `https://purl.org/p2p-o/organization#` |
| `formalName` | `https://purl.org/p2p-o/organization#` |
| `globalLocationNumber` | `https://purl.org/p2p-o/organization#` |

**`edifact-o` namespace (53 properties)**

`belongsToProcess`, `bilateralAgreed`, `changeInformation`, `consumerUnitsInTradingUnitQuantityWithUnit`, `contactPerson`, `creationTime`, `dataExchangeCounter`, `dataExchangeReference`, `deliveryCondition`, `descriptionOfGoods`, `hasAdditionalProductIdentification`, `hasAllowanceReason`, `hasChargeReason`, `hasCity`, `hasDiscreteQuantityWithUnit`, `hasDocumentFunction`, `hasDocumentType`, `hasFunctionInInvoice`, `hasGeneralInformation`, `hasHeightDimension`, `hasLengthMeasurements`, `hasNetWeight`, `hasNetWeightPerUnit`, `hasPhysicalDimension`, `hasPriceSource`, `hasPriceType`, `hasProductIdentification`, `hasStockRestriction`, `hasTAXrate`, `hasTransportRestriction`, `hasUnit`, `informationCustomsDeclaration`, `instructionForInvoicingParty`, `managingOrganisations`, `messageReferenceNumber`, `messageTypeIdentifier`, `otherServiceInformation`, `percentage`, `priceAndDeliveryCondition`, `priceCondition`, `purchasingInformation`, `quantity`, `recipientIndicator`, `releaseNumberMessageType`, `reportingInformation`, `supplierNote`, `synatxIdentifier`, `synatxVersion`, `timePeriod`, `totalNumberOfSegments`, `unitPriceBasis`, `versionNumberMessageType`, `widthDimension`.

### 7.3 What is preserved in both files for all 261 data properties

For every data property, the following are identical in both files:
- `rdfs:subPropertyOf` pointing to any URI **other than** `owl:topDataProperty` (196 properties retain their domain-specific property hierarchy)
- `rdfs:domain`
- `rdfs:range`
- `rdfs:comment`
- `rdfs:label`
- `rdfs:isDefinedBy`
- `edifact-o:seeEDIFACT` annotation values (where present)
- `edifact-o:seeXML` annotation values (where present)

---

## 8. Classes (31 in both files)

All 31 classes are present in both files. The only difference per class is the removal of `ns1:term_status`.

### 8.1 Axiom removed from all 31 classes

Every class in the original has:

```xml
<ns1:term_status>stable</ns1:term_status>
```

This is absent from every class in the trimmed file.

### 8.2 Classes affected (all 31)

`org:FormalOrganization`, `agentrole:AgentRole`, and the 29 classes in the `edifact-o` namespace: `BrokerSalesOfficeRole`, `BuyerRole`, `CalculateDeliverToRole`, `CentralRegulatorRole`, `DeliveryPartyRole`, `DespatchPartyRole`, `E-Invoice`, `FinalConsigneeRole`, `FormalOrganization`, `InvoiceDetails`, `InvoiceeRole`, `InvoicingPartyRole`, `Item`, `PayeeRole`, `RecipientOfInvoiceRegulationRole`, `RecipientRole`, `RegulatorRole`, `RepresentativeOfSupplierRole`, `SalesAgentRole`, `SellerRole`, `SendToRole`, `SupplierRole`, `SuppliersCompanyHeadquarterRole`, `WarehouseNumberRole`, `WholesalerRole`, and the three classes defined by reuse pointers `InvoiceContent` (via `rdf:Description`), `EDIFACT-Structure` (via `rdf:Description`), and one external `E-Invoice` (via `rdf:Description`).

### 8.3 Axioms preserved in both files for all 31 classes

`rdfs:subClassOf`, `owl:disjointWith` (where declared), `rdfs:comment`, `rdfs:label`, `rdfs:isDefinedBy` — all present and identical in both versions.

---

## 9. `rdf:Description` Blocks (3 in both files)

Three named resources are described outside the main class/property declarations via `rdf:Description` elements: `edifact-o:E-Invoice`, `edifact-o:EDIFACT-Structure`, and `edifact-o:InvoiceContent`. All three blocks are present in both files, but each loses `ns1:term_status` in the trimmed version.

| URI | Removed triple |
|---|---|
| `edifact-o:E-Invoice` | `ns1:term_status = stable` |
| `edifact-o:EDIFACT-Structure` | `ns1:term_status = stable` |
| `edifact-o:InvoiceContent` | `ns1:term_status = stable` |

All other triples in these three blocks (`rdfs:comment`, `rdfs:isDefinedBy`, `rdfs:label`) are present and identical in both files.

---

## 10. Elements present in trimmed but absent in original

None. The trimmed file is a strict subset of the original at the triple level.

---

## 11. Consolidated Taxonomy of Changes

The differences between the original and trimmed ontology reduce to exactly four change types, all involving removal from the original:

| # | Change type | Scope | Count |
|---|---|---|---|
| T1 | Ontology-level provenance metadata removed | `owl:Ontology` header | 11 triples removed |
| T2 | `ns1:term_status "stable"` removed | All classes, object properties, data properties, and `rdf:Description` blocks | 305 triples removed |
| T3 | `rdfs:subPropertyOf owl:topDataProperty` removed | 65 of 261 data properties | 65 triples removed |
| T4 | Annotation property declarations removed | 13 of 22 `owl:AnnotationProperty` entries | 13 declarations removed (plus 3 child triples for the three that had labels) |
| T5 | `rdfs:subPropertyOf owl:topObjectProperty` removed | All 10 object properties | 10 triples removed |
| T6 | `rdfs:Datatype` declaration for `xsd:date` removed | 1 explicit datatype declaration | 1 element removed |
| T7 | Namespace declarations removed | 2 namespace prefixes (`xmlns:ns`, `xmlns:ns1`) | 2 declarations removed |

---

## 12. LLM-Readable Summary

The following is a plain-language summary intended to be consumed by a language model evaluating LLM-generated ontologies against the trimmed reference.

---

**What the trimmed ontology is:**
`TUMedifact_trimmed.owl` is a version of the TUMedifact EDIFACT invoice ontology with authorship, provenance, and stability metadata removed. All structural and semantic content is preserved.

**What was removed and why it is not recoverable by an LLM from formal specifications:**

1. **Provenance metadata (T1, T7):** The `owl:Ontology` block in the original contains the names and affiliations of the human authors (`terms:creator`, `terms:contributor`), the publication and modification dates, a copyright statement, a license URI (CC BY-NC 4.0), and a publisher name. The two removed namespace prefixes (`xmlns:ns` for Creative Commons, `xmlns:ns1` for the W3C vocabulary status vocabulary) supported these annotations. None of this information is derivable from any EDIFACT standard specification; it is project-specific authorship information.

2. **Vocabulary status annotations (T2):** The original marks every class, object property, data property, and named resource description with `ns1:term_status "stable"`, using the W3C SemWeb Vocab Status vocabulary (`http://www.w3.og/2003/06/sw-vocab-status/ns#` — note the typo in the URI as published). This annotation signals that each term is in a stable, published state. It is a housekeeping annotation applied uniformly across all 305 annotatable elements; it conveys no domain knowledge about EDIFACT. An LLM would have no basis to generate this specific vocabulary status annotation, and the misspelled URI makes it additionally opaque.

3. **Explicit rooting to `owl:topDataProperty` and `owl:topObjectProperty` (T3, T5):** In OWL, every data property is implicitly a sub-property of `owl:topDataProperty` and every object property of `owl:topObjectProperty`. Making this implicit subsumption explicit is a stylistic authoring choice. The original makes it explicit for 65 of 261 data properties and all 10 object properties. This is not derivable from any EDIFACT specification because it is an ontology-engineering convention, not a domain fact. Which 65 data properties were selected for explicit rooting appears to follow no externally documented rule.

4. **Annotation property declarations for built-in and external vocabularies (T4):** The original explicitly re-declares 13 annotation properties from external vocabularies (`terms:contributor`, `terms:creator`, etc., and the three OWL/RDFS built-in predicates `owl:disjointWith`, `owl:inverseOf`, `rdfs:subPropertyOf` as annotation properties with `rdfs:label` child triples). These declarations serve as documentation hooks within the ontology file itself. They are project-specific in the sense that the choice of which external annotation properties to document inside the ontology is a local authoring decision.

5. **`rdfs:Datatype` declaration for `xsd:date` (T6):** The original contains an explicit `rdfs:Datatype rdf:about="http://www.w3.org/2001/XMLSchema#date"` element. This is redundant with the XSD built-in type and is an optional ontology-authoring annotation. It is not required by any EDIFACT standard.

**What was NOT removed:**

- All 31 classes with their full `rdfs:subClassOf`, `owl:disjointWith`, `rdfs:comment`, `rdfs:label`, and `rdfs:isDefinedBy` axioms.
- All 10 object properties with their `owl:inverseOf`, `rdfs:domain`, `rdfs:range`, `rdfs:comment`, `rdfs:label`, and `rdfs:isDefinedBy` axioms.
- All 261 data properties with their `rdfs:subPropertyOf` (to domain-specific properties, not `topDataProperty`), `rdfs:domain`, `rdfs:range`, `rdfs:comment`, `rdfs:label`, `rdfs:isDefinedBy`, `edifact-o:seeEDIFACT`, and `edifact-o:seeXML` axioms.
- The domain-specific property hierarchy (e.g. all `dateX` properties sub-classing `referenceDate`, all quantity properties sub-classing `quantity`, all amount properties sub-classing `schema:amount`).
- The custom annotation properties `seeEDIFACT` and `seeXML` with their `rdfs:label` declarations.
- The annotation property hierarchy `EDIFACT-Structure rdfs:subPropertyOf E-Invoice` and `InvoiceContent rdfs:subPropertyOf E-Invoice`.
- The three `rdf:Description` blocks for `E-Invoice`, `EDIFACT-Structure`, and `InvoiceContent` with their comments, labels, and `isDefinedBy` triples.
- The `vann:preferredNamespacePrefix` and `vann:preferredNamespaceUri` metadata in the ontology header.

**Implication for LLM ontology evaluation:**
When comparing an LLM-generated ontology against `TUMedifact_trimmed.owl`, differences in T1–T7 content should not be penalised, as this content either (a) cannot be derived from the EDIFACT formal specification, (b) is implicit in OWL semantics, or (c) is project-specific authorship data. Structural and semantic evaluation should focus on: class hierarchy, class disjointness axioms, object property domain/range/inverse declarations, data property domain/range/subPropertyOf-to-domain-properties declarations, and the custom `seeEDIFACT`/`seeXML` cross-reference annotations.
