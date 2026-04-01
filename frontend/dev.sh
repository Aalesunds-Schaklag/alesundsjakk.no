#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Install dependencies if needed
if [ ! -d node_modules ]; then
  echo "Installing dependencies..."
  npm install
fi

# Start Vite dev server
echo "Starting Vite on :5173..."
exec npm run dev
