#!/usr/bin/env bash
# Verify ddgs CLI is installed and working
# Run: bash scripts/verify-ddgs.sh

echo "=== ddgs availability check ==="

# Check CLI
if command -v ddgs &>/dev/null; then
    echo "✅ CLI: ddgs found"
    ddgs_version=$(pip show ddgs 2>/dev/null | grep Version | awk '{print $2}')
    echo "   Version: $ddgs_version"
else
    echo "❌ CLI: ddgs not found"
    echo "   Install: pip install ddgs"
    exit 1
fi

# Quick query test
echo ""
echo "=== Quick query test ==="
python -c "
from ddgs import DDGS
import warnings
warnings.filterwarnings('ignore')
with DDGS() as ddgs:
    results = list(ddgs.text('test query', max_results=2))
    print(f'✅ Search returned {len(results)} results')
    for r in results:
        print(f'   - {r.get(\"title\",\"\")[:50]}')
"

if [ $? -eq 0 ]; then
    echo "✅ DDGS Python API works"
else
    echo "❌ DDGS Python API failed"
    exit 1
fi

echo ""
echo "=== All checks passed ==="
