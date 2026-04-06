import argparse
import json
import os

from app.services.retrieval_index import TfidfAttackIndex
from app.services.embedder import AttackEmbedder
from app.services.mapper import AttackMapper
from app.services.triage import triage_alert
from app.services.response_engine import recommend_actions
from app.services.reporter import build_coverage_summary, build_attack_navigator_layer
from app.config import (
    INPUT_ALERTS_FILE,
    MAPPED_OUTPUT_FILE,
    COVERAGE_OUTPUT_FILE,
    NAVIGATOR_OUTPUT_FILE,
    TFIDF_VECTORIZER_FILE,
    TFIDF_MATRIX_FILE,
    TFIDF_TECHNIQUES_FILE,
    EMBEDDINGS_FILE,
)


def load_alerts(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_alerts(alerts):
    tfidf_index = TfidfAttackIndex()
    tfidf_index.load(
        TFIDF_VECTORIZER_FILE,
        TFIDF_MATRIX_FILE,
        TFIDF_TECHNIQUES_FILE,
    )

    embedder = AttackEmbedder(model_name="all-MiniLM-L6-v2")
    embedder.load(tfidf_index.techniques, EMBEDDINGS_FILE)

    mapper = AttackMapper(tfidf_index, embedder)

    all_results = []

    for i, alert in enumerate(alerts, start=1):
        triage = triage_alert(alert)
        mapping = mapper.map_alert(alert)
        actions = recommend_actions(mapping["matches"])

        result = {
            "alert_id": alert.get("alert_id", f"alert-{i}"),
            "alert": alert,
            "triage": triage,
            "query_used": mapping["query_used"],
            "matches": mapping["matches"],
            "recommended_actions": actions,
        }

        all_results.append(result)

        print("\n" + "=" * 70)
        print(f"ALERT ID: {result['alert_id']}")
        print(f"SEVERITY: {triage['severity']}")
        print(f"TRIAGE SCORE: {triage['triage_score']}")
        print(f"QUERY USED: {result['query_used']}")

        print("\nTOP MATCHES:")
        for m in result["matches"]:
            print(f"  {m['technique_id']} - {m['name']}")
            print(f"    TF-IDF Score: {m.get('tfidf_score', 0):.4f}")
            print(f"    Embedding Score: {m.get('embedding_score', 0):.4f}")
            print(f"    Rule Score: {m.get('rule_score', 0):.4f}")
            print(f"    Field Match Score: {m.get('field_match_score', 0):.4f}")
            print(f"    Final Score: {m.get('final_score', 0):.4f}")
            print(f"    Confidence: {m['confidence']}%")
            print(f"    Tactics: {m['tactics']}")
            print(f"    Explanation: {' | '.join(m['explanation'])}")

        print("\nRECOMMENDED ACTIONS:")
        for action in actions:
            print(f"  - {action}")

    os.makedirs("output", exist_ok=True)

    with open(MAPPED_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    coverage = build_coverage_summary(all_results)
    with open(COVERAGE_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2)

    navigator = build_attack_navigator_layer(all_results)
    with open(NAVIGATOR_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(navigator, f, indent=2)

    print("\n" + "=" * 70)
    print(f"[+] Results written to: {MAPPED_OUTPUT_FILE}")
    print(f"[+] Coverage summary written to: {COVERAGE_OUTPUT_FILE}")
    print(f"[+] ATT&CK Navigator layer written to: {NAVIGATOR_OUTPUT_FILE}")

    return all_results


def main():
    parser = argparse.ArgumentParser(description="Analyze normalized alerts and map them to MITRE ATT&CK techniques.")
    parser.add_argument(
        "--input",
        default=INPUT_ALERTS_FILE,
        help=f"Path to normalized alerts JSON file (default: {INPUT_ALERTS_FILE})",
    )
    args = parser.parse_args()

    alerts = load_alerts(args.input)

    print(f"[DEBUG] Loaded {len(alerts)} alerts from {args.input}")
    if alerts:
        print(f"[DEBUG] First alert ID: {alerts[0].get('alert_id', 'missing-alert-id')}")

    analyze_alerts(alerts)


if __name__ == "__main__":
    main()
