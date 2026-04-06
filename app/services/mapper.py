from typing import Dict, List, Tuple


class AttackMapper:
    def __init__(self, tfidf_index, embedder):
        self.tfidf_index = tfidf_index
        self.embedder = embedder

    def _safe_lower(self, value):
        return str(value or "").lower()

    def _build_alert_text(self, alert: Dict) -> str:
        parts = []

        for key in ["title", "summary", "description", "service", "src_ip", "dst_ip", "dst_port"]:
            if alert.get(key):
                parts.append(str(alert.get(key)))

        http = alert.get("http", {}) or {}
        for key in ["method", "uri", "user_agent"]:
            if http.get(key):
                parts.append(str(http.get(key)))

        return " ".join(parts).lower()

    def _extract_http_features(self, alert: Dict):
        http = alert.get("http", {}) or {}

        method = self._safe_lower(http.get("method"))
        uri = self._safe_lower(http.get("uri"))
        ua = self._safe_lower(http.get("user_agent"))

        return {
            "method": method,
            "uri": uri,
            "ua": ua,
            "login_like": "login" in uri,
            "upload_like": method == "post" and "upload" in uri,
            "payload_like": method == "get" and (".zip" in uri or "payload" in uri),
            "scripted_http": any(x in ua for x in ["curl", "python", "wget"])
        }

    def _rule_score(self, alert: Dict, technique_name: str, corpus_text: str):
        technique_text = f"{technique_name.lower()} {corpus_text.lower()}"

        score = 0.0
        reasons = []

        service = self._safe_lower(alert.get("service"))
        dst_port = str(alert.get("dst_port", ""))

        http = self._extract_http_features(alert)

        if service == "smb" or dst_port == "445":
            if "smb" in technique_text:
                score += 1.0
                reasons.append("SMB activity")

        if service == "rdp" or dst_port == "3389":
            if "rdp" in technique_text:
                score += 1.0
                reasons.append("RDP activity")

        if http["upload_like"]:
            if "web shell" in technique_text:
                score += 2.0
                reasons.append("Web shell upload")

        if http["payload_like"]:
            if "ingress tool transfer" in technique_text:
                score += 2.0
                reasons.append("Payload download")

        return score, reasons

    def _normalize(self, scores):
        max_score = max(scores.values()) if scores else 1.0
        return {k: v / max_score for k, v in scores.items()} if max_score else scores

    def map_alert(self, alert: Dict, top_k_tfidf=15, top_k_final=5):
        query = self._build_alert_text(alert)

        tfidf_results = self.tfidf_index.query(query, top_k=top_k_tfidf)
        candidate_techniques = [t for t, _ in tfidf_results]

        # 🔥 FORCE ADD TECHNIQUES VIA QUERY (NO corpus needed)
        http = self._extract_http_features(alert)

        if http["payload_like"]:
            extra = self.tfidf_index.query("ingress tool transfer", top_k=5)
            for t, _ in extra:
                if t not in candidate_techniques:
                    candidate_techniques.append(t)

        if http["upload_like"]:
            extra = self.tfidf_index.query("web shell exploit upload", top_k=5)
            for t, _ in extra:
                if t not in candidate_techniques:
                    candidate_techniques.append(t)

        embed_results = self.embedder.query(query, candidate_techniques)

        tfidf_scores = self._normalize({t.technique_id: s for t, s in tfidf_results})
        embed_scores = self._normalize({t.technique_id: s for t, s in embed_results})

        results = []

        for t in candidate_techniques:
            tid = t.technique_id

            rule_score, reasons = self._rule_score(alert, t.name, t.corpus_text)

            final = (
                0.3 * tfidf_scores.get(tid, 0) +
                0.2 * embed_scores.get(tid, 0) +
                0.5 * rule_score
            )

            results.append({
                "technique_id": tid,
                "name": t.name,
                "tactics": getattr(t, "tactics", []),
                "final_score": round(final, 4),
                "confidence": 0.0,
                "explanation": reasons
            })

        results.sort(key=lambda x: x["final_score"], reverse=True)

        top = results[:top_k_final]
        max_score = top[0]["final_score"] if top else 1.0

        for r in top:
            r["confidence"] = round((r["final_score"] / max_score) * 100, 2)

        return {
            "query_used": query,
            "matches": top
        }
