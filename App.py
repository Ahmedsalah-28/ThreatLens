import streamlit as st
import os
import tempfile
import base64
from pathlib import Path

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="ThreatLens",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;800&display=swap');

:root {
    --bg:         #060810;
    --surface:    #0b0d16;
    --card:       #0f1120;
    --border:     #1a1d2e;
    --border2:    #252840;
    --accent:     #00d4ff;
    --accent2:    #7b5ea7;
    --danger:     #ff3b6b;
    --success:    #00e5a0;
    --warning:    #ffb340;
    --text:       #dde4f0;
    --muted:      #5a6380;
    --mono:       #00d4ff;
}

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Exo 2', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(123,94,167,0.05) 0%, transparent 55%),
        var(--bg) !important;
}

.main .block-container {
    padding: 0 2.5rem 3rem !important;
    max-width: 1100px !important;
}

            

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 1px; height: 3rem;
    background: linear-gradient(to bottom, transparent, var(--accent));
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.2);
    color: var(--accent);
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 18px;
    border-radius: 2px;
    margin-bottom: 1.5rem;
}
.hero-tag::before { content: '▶'; font-size: 8px; }
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 700;
    line-height: 0.95;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #fff 0%, var(--accent) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .8rem;
}
.hero-sub {
    font-size: 14px;
    color: var(--muted);
    font-weight: 300;
    letter-spacing: .5px;
    max-width: 480px;
    margin: 0 auto 2.5rem;
    line-height: 1.8;
}
.hero-line {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--border2) 30%, var(--border2) 70%, transparent 100%);
    margin-bottom: 2.5rem;
    position: relative;
}
.hero-line::after {
    content: '◈';
    position: absolute;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    color: var(--border2);
    font-size: 14px;
    background: var(--bg);
    padding: 0 8px;
}

/* ── Upload card ── */
.upload-card {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 4px;
    padding: 2rem 2.5rem 1.8rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.upload-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.card-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-label::before {
    content: '';
    width: 16px; height: 1px;
    background: var(--accent);
}

/* ── File uploader override ── */
[data-testid="stFileUploader"] > div {
    background: rgba(0,212,255,0.02) !important;
    border: 1px dashed var(--border2) !important;
    border-radius: 4px !important;
    transition: all 0.3s !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--accent) !important;
    background: rgba(0,212,255,0.04) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--muted) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
    color: var(--muted) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    border-radius: 2px !important;
    transition: all 0.25s !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: rgba(0,212,255,0.08) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2), inset 0 0 20px rgba(0,212,255,0.03) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* reset btn */
div[data-testid="column"]:nth-child(2) .stButton > button {
    border-color: var(--border2) !important;
    color: var(--muted) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    border-color: var(--danger) !important;
    color: var(--danger) !important;
    background: rgba(255,59,107,0.05) !important;
    box-shadow: 0 0 15px rgba(255,59,107,0.1) !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div {
    background: rgba(0,212,255,0.1) !important;
    border-radius: 0 !important;
    height: 2px !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 0 !important;
    box-shadow: 0 0 10px var(--accent) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 2px !important;
    padding: 5px !important;
    gap: 3px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    border-radius: 2px !important;
    padding: 8px 24px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: rgba(0,212,255,0.08) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(0,212,255,0.25) !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.1) !important;
}
[data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {
    color: var(--text) !important;
    background: rgba(255,255,255,0.03) !important;
}
[data-testid="stTabs"] [role="tabpanel"] {
    padding-top: 1.5rem !important;
}

/* ── Pipeline tracker ── */
.pipeline-wrap {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.pipeline-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.pipeline-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.steps-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
}
.step-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 12px 10px;
    text-align: center;
    transition: all 0.3s ease;
}
.step-item.done {
    border-color: rgba(0,229,160,0.4);
    background: rgba(0,229,160,0.04);
    box-shadow: 0 0 10px rgba(0,229,160,0.06);
}
.step-item.running {
    border-color: rgba(0,212,255,0.5);
    background: rgba(0,212,255,0.05);
    box-shadow: 0 0 14px rgba(0,212,255,0.12);
    animation: pulse-border 1.5s infinite;
}
.step-item.pending { opacity: 0.35; }

@keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 8px rgba(0,212,255,0.1); }
    50%       { box-shadow: 0 0 20px rgba(0,212,255,0.25); }
}

.step-icon  { font-size: 20px; margin-bottom: 5px; line-height: 1; }
.step-name  {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 4px;
}
.step-state {
    font-size: 9px;
    font-family: 'Share Tech Mono', monospace;
}
.step-state.s-done    { color: var(--success); }
.step-state.s-running { color: var(--accent); }
.step-state.s-pending { color: var(--muted); }

/* ── Status line ── */
.status-line {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: var(--accent);
    letter-spacing: 1px;
    padding: 6px 0;
}

/* ── Hash display ── */
.hash-block {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 3px;
    padding: 14px 20px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 16px;
    font-family: 'Share Tech Mono', monospace;
}
.hash-lbl {
    font-size: 9px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    white-space: nowrap;
    border-right: 1px solid var(--border2);
    padding-right: 16px;
}
.hash-val {
    font-size: 11px;
    color: var(--accent);
    word-break: break-all;
    line-height: 1.5;
}

/* ── Report toolbar ── */
.report-bar {
    background: var(--card);
    border: 1px solid var(--border2);
    border-bottom: none;
    border-radius: 3px 3px 0 0;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.report-bar-left {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 1px;
}
.report-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
.report-frame-wrap {
    border: 1px solid var(--border2);
    border-top: none;
    border-radius: 0 0 3px 3px;
    overflow: hidden;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(0,229,160,0.05) !important;
    border: 1px solid rgba(0,229,160,0.3) !important;
    color: var(--success) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,229,160,0.1) !important;
    box-shadow: 0 0 16px rgba(0,229,160,0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── Alert ── */
[data-testid="stAlert"] {
    background: rgba(255,59,107,0.06) !important;
    border: 1px solid rgba(255,59,107,0.25) !important;
    border-radius: 3px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Open-in-new-tab link ── */
.open-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(123,94,167,0.08);
    border: 1px solid rgba(123,94,167,0.3);
    color: #b48bff;
    font-family: 'Rajdhani', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    text-decoration: none;
    padding: 8px 18px;
    border-radius: 2px;
    transition: all 0.2s;
    white-space: nowrap;
}
.open-link:hover {
    background: rgba(123,94,167,0.15);
    box-shadow: 0 0 16px rgba(123,94,167,0.2);
    color: #c9aaff;
    text-decoration: none;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 2rem 0 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Session state init
# ─────────────────────────────────────────────────────────────
defaults = {
    "done":        False,
    "summary_html": None,
    "full_html":   None,
    "file_hash":   None,
    "error":       None,
    "running":     False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# Pipeline steps
# ─────────────────────────────────────────────────────────────
STEPS = [
    ("hash",    "🔑", "Hash"),
    ("upx",     "📦", "UPX"),
    ("floss",   "🔍", "Floss"),
    ("vt",      "🌐", "VT"),
    ("static",  "📄", "Static"),
    ("dynamic", "⚡", "Dynamic"),
    ("yara",    "🎯", "Yara"),
    ("agg",     "🧩", "Agg"),
    ("insight", "🧠", "Insight"),
    ("summary", "📊", "Report"),
]

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap" >
    <div class="hero-tag">Threat Intelligence Platform</div>
    <div class="hero-title">MALWARE<br>SCOPE</div>
    <p class="hero-sub" style="margin-left: 525px;">
        Drop a binary. Get full static, dynamic, YARA, and AI-synthesized<br>
        threat intelligence — automated end-to-end.
    </p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Upload section
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Upload Sample</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "drop binary",
    type=None,
    label_visibility="collapsed",
)

c1, c2, c3 = st.columns([3, 1.2, 5])
with c1:
    run_btn = st.button(
        "⬡  RUN ANALYSIS",
        use_container_width=True,
        disabled=(uploaded is None or st.session_state.running),
    )
with c2:
    reset_btn = st.button("↺  RESET", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Reset
# ─────────────────────────────────────────────────────────────
if reset_btn:
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────
if run_btn and uploaded and not st.session_state.done:
    st.session_state.running = True

    # Save to temp file
    suffix = Path(uploaded.name).suffix or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    # ── Pipeline tracker UI ──────────────────────────────
    st.markdown('<div class="pipeline-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="pipeline-title">◈ pipeline execution</div>', unsafe_allow_html=True)
    steps_ph  = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

    progress_ph = st.empty()
    status_ph   = st.empty()

    def render_steps(completed: set, running_key: str | None):
        cards = ""
        for key, icon, label in STEPS:
            if key in completed:
                cls, sc, st_txt = "done",    "s-done",    "✓ done"
            elif key == running_key:
                cls, sc, st_txt = "running",  "s-running", "⟳ running"
            else:
                cls, sc, st_txt = "pending",  "s-pending", "· queued"
            cards += f"""
            <div class="step-item {cls}">
                <div class="step-icon">{icon}</div>
                <div class="step-name">{label}</div>
                <div class="step-state {sc}">{st_txt}</div>
            </div>"""
        steps_ph.markdown(
            f'<div class="steps-grid">{cards}</div>',
            unsafe_allow_html=True,
        )

    render_steps(set(), "hash")
    progress_ph.progress(0.0)

    # ── Intercept prints to track steps ─────────────────
    import builtins, queue, threading

    print_q = queue.Queue()
    _orig_print = builtins.print

    def _patched_print(*args, **kwargs):
        _orig_print(*args, **kwargs)
        print_q.put(" ".join(str(a) for a in args))

    builtins.print = _patched_print

    result_q = queue.Queue()

    def _run(path):
        try:
            from graph import graph
            out = graph.invoke({"file_path": path})
            result_q.put(("ok", out))
        except Exception as e:
            result_q.put(("err", str(e)))

    t = threading.Thread(target=_run, args=(tmp_path,), daemon=True)
    t.start()

    step_order = [s[0] for s in STEPS]
    completed  = set()

    while t.is_alive() or not print_q.empty():
        try:
            msg = print_q.get_nowait()
            matched = next(
                (k for k in step_order if msg.strip().lower().startswith(k)),
                None,
            )
            if matched:
                completed.add(matched)
                idx      = step_order.index(matched)
                nxt      = step_order[idx + 1] if idx + 1 < len(step_order) else None
                pct      = len(completed) / len(STEPS)
                render_steps(completed, nxt)
                progress_ph.progress(min(pct, 1.0))
                status_ph.markdown(
                    f'<div class="status-line">▶ {matched.upper()} complete '
                    f'({int(pct*100)}%)</div>',
                    unsafe_allow_html=True,
                )
        except queue.Empty:
            import time; time.sleep(0.12)

    builtins.print = _orig_print

    render_steps(completed, None)
    progress_ph.progress(1.0)
    status_ph.markdown(
        '<div class="status-line" style="color:var(--success);">'
        '✓ PIPELINE COMPLETE — all modules finished</div>',
        unsafe_allow_html=True,
    )

    os.unlink(tmp_path)

    status, payload = result_q.get()

    if status == "err":
        st.session_state.error   = payload
        st.session_state.running = False
    else:
        def _read(path):
            return open(path, encoding="utf-8").read() if os.path.exists(path) else None

        st.session_state.done         = True
        st.session_state.running      = False
        st.session_state.file_hash    = payload.get("file_hash", "N/A")
        st.session_state.summary_html = (
            payload.get("summary_html") or _read("outputs/summary_report.html")
        )
        st.session_state.full_html    = (
            payload.get("full_report_html") or _read("outputs/full_report.html")
        )

    st.rerun()

# ─────────────────────────────────────────────────────────────
# Error
# ─────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"Pipeline error: {st.session_state.error}")

# ─────────────────────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────────────────────
if st.session_state.done:

    st.markdown("<hr>", unsafe_allow_html=True)

    # Hash row
    st.markdown(
        f'<div class="hash-block">'
        f'<span class="hash-lbl">SHA-256</span>'
        f'<span class="hash-val">{st.session_state.file_hash}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Tabs
    tab_sum, tab_full = st.tabs([
        "  📊  SUMMARY REPORT  ",
        "  📄  FULL TECHNICAL REPORT  ",
    ])

    def _render_tab(html: str | None, label: str, fname: str):
        if not html:
            st.warning(f"{label} not available.")
            return

        b64 = base64.b64encode(html.encode("utf-8")).decode()

        # Action row
        ca, cb, cc = st.columns([2.2, 2, 6])
        with ca:
            st.download_button(
                label="⬇  DOWNLOAD",
                data=html.encode("utf-8"),
                file_name=fname,
                mime="text/html",
                use_container_width=True,
            )
        with cb:
            st.markdown(
                f'<a class="open-link" '
                f'href="data:text/html;base64,{b64}" target="_blank">'
                f'↗&nbsp; OPEN</a>',
                unsafe_allow_html=True,
            )

        # Report preview
        st.markdown(
            '<div class="report-bar">'
            '  <div class="report-bar-left"><div class="report-dot"></div>LIVE PREVIEW</div>'
            '  <span style="font-family:\'Share Tech Mono\',monospace;font-size:9px;'
            '  color:var(--muted);letter-spacing:2px;">HTML REPORT</span>'
            '</div>'
            '<div class="report-frame-wrap">',
            unsafe_allow_html=True,
        )
        st.components.v1.html(html, height=800, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_sum:
        _render_tab(
            st.session_state.summary_html,
            "Summary Report",
            "summary_report.html",
        )

    with tab_full:
        _render_tab(
            st.session_state.full_html,
            "Full Technical Report",
            "full_report.html",
        )

# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    margin-top: 5rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid #1a1d2e;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: #2a2e45;
    text-transform: uppercase;
">
    MalwareScope · LangGraph + Groq · Automated Threat Intelligence
</div>
""", unsafe_allow_html=True)
