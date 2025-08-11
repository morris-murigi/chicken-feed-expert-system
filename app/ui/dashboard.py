from pathlib import Path

def get_dashboard_html():
    html_path = Path(__file__).parent / "templates" / "dashboard.html"
    return html_path.read_text(encoding="utf-8")
