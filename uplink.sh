#!/bin/bash
echo "📡 [TITAN] Syncing Maryland Lab to Kaida Vault..."

cd ~/titan_system
git add .
git commit -m "🚀 Titan Update: $(date)"

# Only show success if the push actually works
if git push origin main; then
    echo "✅ [STATUS] Forever Memory: SECURED."
else
    echo "❌ [ERROR] Uplink Failed. Check your connection or token."
fi
