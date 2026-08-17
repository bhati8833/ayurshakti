#!/bin/bash
# AyurShakti local cache & temp cleaner
# Usage: npm run clean

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[CLEAN] Clearing build artifacts & caches..."

# Build outputs (regenerated on next build)
rm -rf .next out

# Incremental build metadata
rm -f tsconfig.tsbuildinfo

# Throwaway temp / draft scratch files
rm -rf temp
mkdir -p temp

# Python / node caches
rm -rf .ruff_cache node_modules/.cache

echo "[CLEAN] Done. Run 'npm run build' to rebuild fresh."