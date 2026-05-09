import json
from state import GraphState
from utils.llm import call_llm


def format_static(data: dict) -> str:
    prompt = f"""You are a malware analyst. The following data is the result of static PE analysis on a suspicious file.

Display this data in a clean, readable format:
- Do NOT remove any value
- Do NOT change any string or number
- Only organize and present clearly (headings, sections, clear formatting)
- Do NOT write any analysis or commentary of your own

Data:
{json.dumps(data, indent=2, default=str)}"""
    return call_llm(prompt)


def static_node(state: GraphState):
    vt = state.get("vt_data", {})

    try:
        attrs = vt["data"]["attributes"]
        pe    = attrs.get("pe_info", {})

        sections = pe.get("sections", [])
        imports  = pe.get("import_list", [])
        exports  = pe.get("exports", {}).get("exported_functions", [])

        entropy_values = [
            {
                "section": s.get("name"),
                "entropy": s.get("entropy"),
                "flagged": (s.get("entropy") or 0) >= 7.0
            }
            for s in sections
        ]

        detectiteasy = attrs.get("detectiteasy", {})
        packers      = attrs.get("packers", {})

        static_analysis = {
            "sections":       sections,
            "imports":        imports,
            "exports":        exports,
            "entropy_values": entropy_values,
            "timestamp":      pe.get("timestamp"),
            "entry_point":    pe.get("entry_point"),
            "machine_type":   pe.get("machine_type"),
            "imphash":        pe.get("imphash"),
            "rich_pe_hash":   pe.get("rich_pe_header_hash"),
            "resources":      pe.get("resource_details", []),
            "file_type":      attrs.get("type_description"),
            "magic":          attrs.get("magic"),
            "trid":           attrs.get("trid", []),
            "detectiteasy":   detectiteasy.get("values", []),
            "packers":        packers,
            "tags":           attrs.get("tags", []),
            "known_names":    attrs.get("names", []),
            "md5":            attrs.get("md5"),
            "sha1":           attrs.get("sha1"),
            "sha256":         attrs.get("sha256"),
            "ssdeep":         attrs.get("ssdeep"),
            "authentihash":   attrs.get("authentihash"),
            "size":           attrs.get("size"),
        }

    except KeyError as e:
        print(f"[static_node] KeyError — missing key: {e}")
        static_analysis = {}
    except Exception as e:
        print(f"[static_node] Unexpected error: {e}")
        static_analysis = {}

    static_analysis = {
        **static_analysis,
        "llm_formatted": format_static(static_analysis)
    }
    print("static")
    return {"static_analysis": static_analysis}
