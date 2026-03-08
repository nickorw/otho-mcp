Use subagents where it makes sense to keep context under control, here is your prompt:

You are an expert ontology engineer and evaluator. Your task is to review a set of pre-triaged OWL ontologies (which have already passed syntactic and basic logical consistency checks) and rank them. You will evaluate them based on their structural depth using the OntoQA framework, their architectural design patterns, and how perfectly they satisfy a list of domain-specific Competency Questions (CQs).

---

## Domain Context

The UN/EDIFACT standard defines a rigid hierarchy for digital business documents, beginning with an Interchange envelope that contains specific Messages like the INVOIC for global trade transactions. Each message is composed of Segments, such as the Beginning of Message (BGM) for document identification and the Name and Address (NAD) for participant details. These segments are further broken down into Composite and Simple Data Elements, separated by specific delimiters like plus signs and colons. Within a single invoice message, data is organized into three distinct sections: a header, a detail section, and a summary section.

In industrial procurement scenarios, such as those at the Einkaufsbüro Deutscher Eisenhändler (E/D/E), an organization often performs multiple roles within a single transaction, acting as the Buyer in one context and the Delivery Party in another. Each role may involve different attributes, which are linked to the organization through specific Agent Role patterns and identifiers like Global Location Numbers. To ensure semantic interoperability, these documents are aligned with the European Standard EN 16931-1 and the Purchase-to-Pay Ontology (P2P-O). The resulting knowledge graphs allow for automated validation using SHACL constraints.

---

## Competency Questions

The ontology must be capable of answering the following questions when populated with instance data:
1. What invoices are all listed in an EDIFACT message?
2. Which organizations are involved in the invoice?
3. What role does organization S play in the invoice?
4. Which organization is the buyer in the invoice?
5. What information is displayed about the involved organizations?
6. What is the address of the buyer?
7. What items are sold in the invoice?
8. What information is displayed about the items sold?
9. What is the net price of the items sold in the invoice?
10. What are the invoice details of the invoice?
11. What is the invoice amount of the invoice?
12. What is the invoice number?
13. What information must be provided so that the file format is valid?
14. To which business process can the invoice be assigned?

---
## Input Files

You will need to analyze two sets of inputs to complete your evaluation: the raw ontology files and a pre-calculated metrics report.

### 1. Pre-Calculated Metrics Data
Do not attempt to manually count classes, triples, or structural ratios. You are provided with a markdown file containing the exact, pre-calculated structural metrics (OntoQA ratios, axiom counts, etc.) for every ontology. Use these exact values for your quantitative scoring.

**Metrics File Path:** `data/FinalResults/ontology_report.md`

### 2. Ontologies to Evaluate
Read and analyze the following ontology files to evaluate CQ coverage, design patterns, and lexical quality.

You will evaluate the ontologies located at the following file paths. Please read and analyze each file directly.

**Ontology Paths:**
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_215700.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_215924.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_220437.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_220832.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_221113.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_221332.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_221725.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_221940.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_222236.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_222534.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_223501.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_223750.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_224212.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_224527.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_224922.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_225145.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_225409.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_225732.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_230018.owl`
`data/FinalResults/Ontologies/dualAgent/EDIFACT_ontology_20260301_230338.owl`

---

## Evaluation Criteria & Scoring Anchors

Evaluate each ontology across the following five dimensions, scoring each from 0.0 to 5.0. Base your scoring strictly on the anchors provided below.

| Dimension | Description & Scoring Anchors | Weight |
|-----------|-------------------------------|--------|
| **1. CQ Coverage** | Does the vocabulary directly enable precise, elegant SPARQL queries for every CQ?<br>**5.0:** All 14 CQs covered with no design ambiguities.<br>**4.5–4.9:** All 14 covered with minor deductions (redundancy, conceptual overlap).<br>**4.0–4.4:** 13/14 covered, or 14/14 with structurally incomplete paths.<br>**< 4.0:** 12 or fewer CQs addressed. | 40% |
| **2. Structural Ratios** | Check the provided metrics file. $RR=\frac{|P|}{|H|+|P|}$; $AR=\frac{|dp|}{|C|}$; $IR=\frac{|H|}{|C|}$.<br>**5.0:** Perfectly balanced graph (rich RR, detailed AR, healthy DAG IR).<br>**4.0–4.9:** Good structure, minor metric imbalances (e.g., slightly high IR).<br>**3.0–3.9:** Noticeable flaws (flat taxonomy, overused multiple inheritance).<br>**< 3.0:** Severe issues (totally disconnected graph, massive linear chains). | 20% |
| **3. Design Patterns** | How well does the ontology handle complex n-ary relationships (e.g., Agent Roles)?<br>**5.0:** Flawless use of reification/pivot classes for roles.<br>**4.0–4.9:** Correct patterns used but with minor structural bloat.<br>**3.0–3.9:** Clumsy workarounds or partially collapsed roles.<br>**< 3.0:** Complete failure to model complex N-ary relationships accurately. | 15% |
| **4. Axiom Complexity** | Does the ontology utilize advanced OWL constructs (`owl:someValuesFrom`, `owl:InverseOf`, etc.)?<br>**5.0:** Deep, appropriate use of logical restrictions and property characteristics.<br>**4.0–4.9:** Good use of basic restrictions, missing some advanced logical depth.<br>**3.0–3.9:** Mostly `owl:Declaration` and `rdfs:subClassOf`; very few restrictions.<br>**< 3.0:** Extremely shallow; zero advanced OWL constructs used. | 15% |
| **5. Lexical & Annotation**| Adherence to naming conventions and metadata presence (`rdfs:label`, `rdfs:comment`).<br>**5.0:** 100% adherence to naming (CamelCase/camelBack) and robust metadata.<br>**4.0–4.9:** Minor naming inconsistencies or occasionally sparse comments.<br>**3.0–3.9:** Noticeable lack of metadata or mixed naming conventions.<br>**< 3.0:** Barely any human-readable annotations; highly inconsistent URIs. | 10% |

---

## Your Task

1. **Read the inputs:** Parse the pre-calculated metrics `.md` file and the individual `.owl` ontology files.
2. **Apply Metrics:** Extract the exact $RR$, $AR$, and $IR$ ratios for each ontology from the provided metrics report. Do not estimate them.
3. **Evaluate & Score:** Assess each ontology against all five dimensions using the scoring anchors above.
4. **Compute a weighted score** for each ontology out of 5.00.
5. **Produce a ranked list** from best to worst.
6. **Write a detailed justification** for the top three ranked ontologies.
7. **Identify the most critical defect** for the top three ontologies.

---

## Output Format

Respond EXACTLY with the following structure:

### Summary Ranking Table

| Rank | Ontology File | CQs Covered (Count) | CQ Cov. Score (0-5) | Struct. Ratios (0-5) | Design Patterns (0-5) | Ax. Complexity (0-5) | Lexical (0-5) | Weighted Score |
|---|---|---|---|---|---|---|---|---|
| 1 | ... | .../14 | ... | ... | ... | ... | ... | ... |
| 2 | ... | .../14 | ... | ... | ... | ... | ... | ... |
| ... | ... | .../14 | ... | ... | ... | ... | ... | ... |

---

### Top 3 Detailed Analysis

#### Rank 1: <ontology filename>
**Weighted score:** X.XX / 5.00

**CQ Coverage Analysis:**
- CQ1 — [Covered ✅ / Partially covered ⚠️ / Not covered ❌] — [brief reason]
- *(List all 14 CQs...)*

**Structural Ratios (OntoQA):**
- **RR:** [Value from metrics file] - [Brief analysis: Is it a rich graph or flat taxonomy?]
- **AR:** [Value from metrics file] - [Brief analysis of attribute density]
- **IR:** [Value from metrics file] - [Brief analysis of hierarchy balance]

**Design Patterns & Domain Representation:**
- [2-3 sentences evaluating the handling of EDIFACT structures and N-ary roles (Buyer/Delivery Party).]

**Axiom Complexity:**
- [1-2 sentences detailing the presence/absence of advanced OWL restrictions.]

**Lexical & Annotation Quality:**
- [1-2 sentences on naming conventions and metadata coverage.]

**Most Critical Defect:**
- [1 sentence identifying the single highest-impact fix to improve the ontology.]

---

#### Rank 2: <ontology filename>
[same structure as Rank 1]

#### Rank 3: <ontology filename>
[same structure as Rank 1]

---

### Bottom Ontologies: Summary

**<ontology filename> (Rank 4):** [One paragraph for each file summarizing why it failed to score higher, referencing specific metrics or coverage gaps.]

Publish this report as an `agent_ontology_ranking.md` file in the folder of the ontologies.