# Malware Analysis Pipeline

Automated malware threat intelligence pipeline built with LangGraph + Groq.

## Project Structure

```
malware_pipeline/
│
├── config.py                      # API keys & shared constants
├── state.py                       # GraphState TypedDict
├── graph.py                       # Graph builder & compiler
├── main.py                        # Entry point
├── requirements.txt
│
├── nodes/
│   ├── hash_node.py               # SHA256 hashing
│   ├── upx_node.py                # UPX packer detection
│   ├── floss_node.py              # FLOSS string extraction
│   ├── vt_node.py                 # VirusTotal API lookup
│   ├── static_node.py             # Static PE analysis
│   ├── dynamic_node.py            # Dynamic / sandbox analysis
│   ├── yara_node.py               # YARA rule matching
│   ├── aggregation_node.py        # Fan-in aggregator
│   ├── insight_node.py            # LLM threat intelligence report
│   ├── summary_report_node.py     # LLM → premium HTML summary
│   └── render_report_html_node.py # Markdown → full HTML report
│
├── utils/
│   ├── llm.py                     # Groq client + call_llm()
│   └── yara_loader.py             # YARA rules loader
│
├── rules/                         # YARA rule files
│   ├── malware/
│   ├── packers/
│   └── webshells/
│
└── outputs/                       # Generated reports (auto-created)
    ├── analysis.json
    ├── insights_report.md
    ├── summary_report.html
    └── full_report.html
```

## Pipeline Flow

```
input ──┬──► hash ──► vt ──┬──► static ──┐
        │                  └──► dynamic ──┤
        ├──► upx ──► floss ──────────────┤
        │                                ├──► agg ──► insight ──► summary_report
        └──► yara ───────────────────────┘         └──────────► render_report_html
```

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Config

Edit `config.py` to update API keys:
- `GROQ_API_KEY` — Groq API key
- `VT_API_KEY`   — VirusTotal API key
- `YARA_RULES_PATH` — path to YARA rules folder
