#!/bin/sh

# Define the Markdown badge block with centering (using HTML)
MD_BADGE="<div align=\"center\">
  <img src=\"https://img.shields.io/badge/Fair%20Use-GremlinGPT%20v1.0-black?style=for-the-badge&labelColor=black&color=red&logo=ghost&logoColor=red\" alt=\"GremlinGPT Fair Use\">
</div>"

# Traverse and inject headers
for file in $(find . -type f \( -name "*.py" -o -name "*.md" \)); do
  # Skip files already tagged
  if grep -q "GremlinGPT Fair Use" "$file"; then
    echo "[SKIP] $file already contains license header."
    continue
  fi

  # Temp file so we don’t mutate mid-read
  tmpfile=$(mktemp)

  if echo "$file" | grep -q "\.py$"; then
    echo "$PY_HEADER" > "$tmpfile"
    echo "" >> "$tmpfile"
    cat "$file" >> "$tmpfile"
  else
    echo "$MD_BADGE" > "$tmpfile"
    echo "" >> "$tmpfile"
    cat "$file" >> "$tmpfile"
  fi

  mv "$tmpfile" "$file"
  echo "[INJECTED] $file"
done
