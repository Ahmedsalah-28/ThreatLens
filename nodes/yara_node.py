import json
from state import GraphState
from utils.llm import call_llm
from utils.yara_loader import load_clean_rules

YARA_RULES = load_clean_rules()


def format_yara(data: dict) -> str:
    prompt = f"""You are a malware analyst. The following data is the result of a YARA scan on a suspicious file.

Display this data in a clean, readable format:
- Do NOT remove any value
- Do NOT change any string
- Only organize and present clearly (headings, bullets, clear formatting)
- Do NOT write any analysis or commentary of your own

Data:
{json.dumps(data, indent=2, default=str)}"""
    return call_llm(prompt)


def yara_node(state: GraphState):
    file_path = state["file_path"]

    try:
        matches    = YARA_RULES.match(file_path)
        results    = []
        namespaces = set()

        for m in matches:
            namespaces.add(m.namespace.split("_")[0])
            results.append({
                "rule":      m.rule,
                "namespace": m.namespace.split("_")[0],
                "tags":      m.tags,
                "meta":      dict(m.meta)
            })

        if "malware" in namespaces:
            severity = "high"
        elif "packers" in namespaces:
            severity = "medium"
        elif "webshells" in namespaces:
            severity = "medium"
        elif len(results) > 0:
            severity = "low"
        else:
            severity = "none"

        yara_result = {
            "match_count":        len(results),
            "severity":           severity,
            "matched_categories": list(namespaces),
            "matched_rules":      results
        }

    except Exception as e:
        yara_result = {"error": str(e)}

    yara_result = {
        **yara_result,
        "llm_formatted": format_yara(yara_result)
    }
    print("yara")
    return {"yara_result": yara_result}
