import json
from state import GraphState
from utils.llm import call_llm


def format_dynamic(data: dict) -> str:
    prompt = f"""You are a malware analyst. The following data is the result of dynamic analysis (VirusTotal + sandbox) on a suspicious file.

Display this data in a clean, readable format:
- Do NOT remove any value
- Do NOT change any string or number
- Only organize and present clearly (headings, sections, clear formatting)
- Do NOT write any analysis or commentary of your own

Data:
{json.dumps(data, indent=2, default=str)}"""
    return call_llm(prompt)


def dynamic_node(state: GraphState):
    vt = state.get("vt_data", {})

    try:
        attrs = vt["data"]["attributes"]

        stats           = attrs.get("last_analysis_stats", {})
        total           = sum(v for k, v in stats.items() if k != "type-unsupported")
        malicious_count = stats.get("malicious", 0)
        detection_ratio = round(malicious_count / total * 100, 1) if total else 0

        dynamic_analysis = {
            "sandbox_verdicts": attrs.get("sandbox_verdicts", {}),
            "av_stats":         stats,
            "detection_ratio":  f"{malicious_count}/{total} ({detection_ratio}%)",
            "crowdsourced_ai":  attrs.get("crowdsourced_ai_results", []),
            "crowdsourced_ids": attrs.get("crowdsourced_ids_results", []),
            "sigma":            attrs.get("sigma_analysis_results", []),
            "threat_label": (
                attrs
                .get("popular_threat_classification", {})
                .get("suggested_threat_label", "unknown")
            ),
            "threat_category": (
                attrs
                .get("popular_threat_classification", {})
                .get("popular_threat_category", [])
            ),
            "reputation":    attrs.get("reputation"),
            "total_votes":   attrs.get("total_votes", {}),
            "behavior_tags": attrs.get("tags", []),
            "network":       attrs.get("network_infrastructure", {}),
        }

    except KeyError as e:
        print(f"[dynamic_node] KeyError: {e}")
        dynamic_analysis = {}
    except Exception as e:
        print(f"[dynamic_node] Error: {e}")
        dynamic_analysis = {}

    dynamic_analysis = {
        **dynamic_analysis,
        "llm_formatted": format_dynamic(dynamic_analysis)
    }
    print("dynamic")
    return {"dynamic_analysis": dynamic_analysis}
