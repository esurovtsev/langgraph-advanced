import base64
import nest_asyncio
from IPython.display import HTML, display
from langchain_core.runnables.graph_mermaid import MermaidDrawMethod


def draw_mermaid_png(agent, max_height="70vh", max_width="min(90vw, 720px)"):
    """
    Render a Mermaid graph locally while auto-scaling it for notebook display.

    The diagram keeps its aspect ratio, shrinks if it would exceed the viewport
    height, and otherwise stays readable without manual tuning.
    """
    nest_asyncio.apply()
    png_bytes = agent.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.PYPPETEER
    )

    style = ";".join([
        "display:block",
        "margin:0 auto",
        "width:100%",
        f"max-width:{max_width}",
        f"max-height:{max_height}",
        "height:auto",
    ])

    encoded = base64.b64encode(png_bytes).decode("utf-8")
    html = f'<img src="data:image/png;base64,{encoded}" style="{style}"/>'
    display(HTML(html))