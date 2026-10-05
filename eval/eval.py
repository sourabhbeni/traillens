"""Quick accuracy check: run identify() over sample photos in eval/samples/.

Usage:
    python eval/eval.py            # needs Ollama + model pulled
    python eval/eval.py --stub     # offline: exercises JSON extraction/validation only
"""

import argparse
import glob
import json
import sys

sys.path.insert(0, ".")

from traillens.identify import extract_json, validate

STUB_OUTPUT = """{
  "common_name": "coast live oak",
  "scientific_name": "Quercus agrifolia",
  "confidence": 0.82,
  "identifying_features": ["holly-like spiny leaves", "dark furrowed bark"],
  "habitat_note": "Common along California coastal trails and canyons.",
  "safety_note": "Do not eat or use wild plants without expert verification."
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stub", action="store_true")
    args = ap.parse_args()

    if args.stub:
        data = validate(extract_json("chatter before " + STUB_OUTPUT + " chatter after"))
        print("stub validation OK:")
        print(json.dumps(data, indent=2))
        return

    from traillens.identify import identify

    files = sorted(glob.glob("eval/samples/*"))
    if not files:
        print("no samples in eval/samples/ — add a few trail photos and re-run")
        return
    for f in files:
        with open(f, "rb") as fh:
            try:
                d = identify(fh.read())
                print(f"{f}: {d['common_name']} ({d['scientific_name']}) conf={d['confidence']:.2f}")
            except Exception as exc:
                print(f"{f}: FAILED — {exc}")


if __name__ == "__main__":
    main()
