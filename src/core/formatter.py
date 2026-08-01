"""Markdown summary formatters for each tool result type."""


def format_syntax_result(data: dict) -> str:
    if data["valid"]:
        return f"## Syntax Validation\n\n✅ **Valid** — {data['triple_count']} triples parsed successfully."
    return f"## Syntax Validation\n\n❌ **Invalid**\n\n```\n{data['error']}\n```"


def format_oops_result(data: dict) -> str:
    if not data["has_pitfalls"]:
        return "## OOPs Pitfall Scan\n\n✅ **No pitfalls detected.**"

    lines = [f"## OOPs Pitfall Scan\n\n⚠️ **{data['pitfall_count']} pitfall(s) detected:**\n"]
    lines.append("| Severity | Code | Name | Affected |")
    lines.append("|----------|------|------|----------|")
    for p in data["pitfalls"]:
        icon = {"Critical": "\U0001f534", "Important": "\U0001f7e0", "Minor": "\U0001f7e1"}.get(p["importance"], "⚪")
        lines.append(f"| {icon} {p['importance']} | {p['code']} | {p['name']} | {p['affected_elements']} |")
    return "\n".join(lines)


def format_reasoning_result(data: dict) -> str:
    lines = ["## Reasoning Validation\n"]
    for r in data.get("results", [data]):
        name = r.get("reasoner", "Unknown")
        if r.get("error"):
            lines.append(f"- **{name}:** ❌ Error — {r['error']}")
        elif r["is_consistent"]:
            lines.append(f"- **{name}:** ✅ Consistent ({r['execution_time_seconds']}s)")
        else:
            classes = ", ".join(r["inconsistent_classes"][:5])
            lines.append(f"- **{name}:** ❌ Inconsistent — {classes}")
    return "\n".join(lines)


def format_metrics_result(data: dict) -> str:
    lines = ["## Ontology Metrics\n"]
    ac = data["axiom_counts"]
    lines.append(f"**Axiom Counts:** {ac['triples']} triples, {ac['classes']} classes, "
                 f"{ac['object_properties']} obj props, {ac['data_properties']} data props\n")

    h = data["hierarchy"]
    lines.append(f"**Hierarchy:** depth {h['max_depth']} (avg {h['avg_depth']}), "
                 f"branching {h['max_branching']} (avg {h['avg_branching']}), {h['leaf_count']} leaves\n")

    q = data["ontoqa_ratios"]
    lines.append(f"**OntoQA:** RR={q['RR']}, AR={q['AR']}, IR={q['IR']}\n")

    cx = data["axiom_complexity"]
    lines.append(f"**Axiom Diversity:** {cx['axiom_diversity_score']}/10\n")

    lx = data["lexical_quality"]
    lines.append(f"**Lexical:** {lx['naming_strict_pct']*100:.0f}% strict naming, "
                 f"{lx['label_coverage']*100:.0f}% labels, {lx['comment_coverage']*100:.0f}% comments")
    return "\n".join(lines)


def format_conversion_result(content: str, target_format: str) -> str:
    preview = content[:500] + ("..." if len(content) > 500 else "")
    return f"## Format Conversion\n\n✅ Converted to **{target_format}** ({len(content)} chars)\n\n```\n{preview}\n```"
