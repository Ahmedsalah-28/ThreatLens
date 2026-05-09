import subprocess
import json
from state import GraphState
from utils.llm import call_llm


def format_upx(data: dict) -> str:
    prompt = f"""You are a malware analyst. Based on the UPX scan result below, write one or two sentences that clearly state:
- Whether the file is packed or not
- What that implies

Do not add any information beyond what is in the data below:
{json.dumps(data, indent=2, default=str)}"""
    return call_llm(prompt)


def upx_check_node(state: GraphState):
    file_path = state["file_path"]

    try:
        result = subprocess.run(
            ["upx", "-t", file_path],
            capture_output=True,
            text=True
        )
        packed = "packed" in result.stdout.lower()
        upx_result = {
            "packed": packed,
            "raw_output": result.stdout
        }
    except Exception as e:
        upx_result = {"error": str(e)}

    upx_result = {
        **upx_result,
        "llm_summary": format_upx(upx_result)
    }
    print("upx")
    return {"upx_result": upx_result}
