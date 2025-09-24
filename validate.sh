#!/bin/bash
# Simple validation script for LaTeX document and bibliography

echo "=== LaTeX Document Validation ==="
echo

# Check if required files exist
echo "Checking required files..."
files=("document.tex" "references.bib")
for file in "${files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        exit 1
    fi
done
echo

# Extract citations from LaTeX document
echo "Extracting citations from document.tex..."
citations=$(grep -o '\\cite{[^}]*}' document.tex | sed 's/\\cite{//; s/}//' | sort -u)
echo "Citations found: $(echo "$citations" | wc -l)"
echo "$citations"
echo

# Extract bibliography entries
echo "Extracting entries from references.bib..."
bibentries=$(grep -o '^@[^{]*{[^,]*' references.bib | sed 's/^@[^{]*{//' | sort)
echo "Bibliography entries found: $(echo "$bibentries" | wc -l)"
echo "$bibentries"
echo

# Check if all citations have corresponding bibliography entries
echo "Checking citation-bibliography consistency..."
missing_refs=()
for citation in $citations; do
    if ! echo "$bibentries" | grep -q "^$citation$"; then
        missing_refs+=("$citation")
    fi
done

if [[ ${#missing_refs[@]} -eq 0 ]]; then
    echo "✓ All citations have corresponding bibliography entries"
else
    echo "✗ Missing bibliography entries for:"
    printf '  %s\n' "${missing_refs[@]}"
    exit 1
fi

echo
echo "✓ Validation completed successfully!"