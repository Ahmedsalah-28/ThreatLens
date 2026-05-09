from graph import graph
from IPython.display import Image


if __name__ == "__main__":
    # ── Optional: visualise the graph ──────────────────────
    Image(graph.get_graph().draw_mermaid_png())

    # ── Run ────────────────────────────────────────────────
    result = graph.invoke({
        "file_path": "Lab09-02.exe"
    })

    print(result.keys())
