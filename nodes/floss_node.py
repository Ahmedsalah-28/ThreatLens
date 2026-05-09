import subprocess
import re
import json
from state import GraphState
from utils.llm import call_llm


def format_floss(data: dict) -> str:
    prompt = f"""You are a malware analyst. The following data was extracted by FLOSS from a suspicious file.

Display this data in a clean, readable format:
- Do NOT remove any value
- Do NOT change any string
- Only organize and present clearly (headings, bullets, logical sections)
- Do NOT write any analysis or commentary of your own

Data:
{json.dumps(data, indent=2, default=str)}"""
    return call_llm(prompt)


def floss_node(state: GraphState):
    file_path = state["file_path"]

    try:
        result = subprocess.run(
            ["floss64.exe", file_path],
            capture_output=True,
            text=True
        )

        lines = result.stdout.splitlines()

        urls = list(set([l for l in lines if "http" in l.lower()]))
        ips  = list(set([l for l in lines if re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b", l)]))

        command_patterns = [r"\bcmd\b", r"\bpowershell\b", r"\bexec\b", r"\bsystem\b"]
        commands = list(set([
            l for l in lines
            if any(re.search(p, l, re.IGNORECASE) for p in command_patterns)
        ]))

        categorized  = set(urls + ips + commands)
        other_strings = list(set([l for l in lines if l not in categorized]))

        floss_result = {
            "total_strings": len(lines),
            "urls":          urls[:10],
            "ips":           ips[:10],
            "commands":      commands[:10],
            "other_strings": other_strings[:10]
        }
    except Exception as e:
        floss_result = {"error": str(e)}

    floss_result = {
        **floss_result,
        "llm_formatted": format_floss(floss_result)
    }
    print("floss")
    return {"floss_result": floss_result}
