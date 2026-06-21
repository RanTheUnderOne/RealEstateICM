#!/usr/bin/env sh
# Golden test: proves the matcher is deterministic and correct.
# Exit 0 = output matches the committed expected result.
DIR="$(dirname "$0")"
py "$DIR/../scripts/match.py" "$DIR/sample-leads.json" "$DIR/sample-properties.json" "$DIR/actual.json" "$DIR/../shared/match-config.json" >/dev/null
if diff -q "$DIR/expected-matches.json" "$DIR/actual.json" >/dev/null; then
  echo "PASS: output matches expected"; rm -f "$DIR/actual.json"; exit 0
else
  echo "FAIL: output differs"; diff "$DIR/expected-matches.json" "$DIR/actual.json"; exit 1
fi
