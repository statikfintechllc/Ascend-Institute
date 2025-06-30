# docs/build_dashboard_html.py

with open("docs/dashboard_template.html", "r") as f:
    template = f.read()

with open("docs/graph/traffic_totals.json", "r") as f:
    totals = f.read()

filled = template.replace("{{TRAFFIC_TOTALS}}", totals.strip())

with open("docs/dashboard.html", "w") as f:
    f.write(filled)
