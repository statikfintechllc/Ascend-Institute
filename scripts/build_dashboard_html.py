# scripts/build_dashboard_html.py

with open("docs/graph/dashboard_template.html", "r") as f:
    template = f.read()

with open("docs/graph/traffic_totals.json", "r") as f:
    totals = f.read()

filled = template.replace("{{TRAFFIC_TOTALS}}", totals.strip())

with open("docs/graph/dashboard.html", "w") as f:
    f.write(filled)
