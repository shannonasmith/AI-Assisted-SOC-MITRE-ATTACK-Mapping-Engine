# 🛡️ AI-Assisted SOC + MITRE ATT&CK Mapping Engine

## 🚀 Overview

This project is a **production-style cybersecurity pipeline** that ingests security telemetry, normalizes events, and maps them to **MITRE ATT&CK techniques** using a hybrid AI-driven scoring system.

It simulates how a modern SOC can leverage **AI-assisted analysis, behavioral logic, and explainable scoring** to accelerate detection and triage.

---

## 🎯 Key Capabilities

* 🔍 **Multi-source ingestion**

  * Zeek (network telemetry)
  * Splunk-style alerts

* 🔄 **Normalized alert pipeline**

  * Converts raw logs into a unified schema
  * Ensures consistent downstream analysis

* 🧠 **Hybrid ATT&CK mapping engine**

  * TF-IDF retrieval
  * Embedding-based semantic similarity (Sentence Transformers)
  * Rule-based scoring
  * Field-aware enrichment
  * Behavior-based overrides

* 📊 **Explainable detection results**

  * Ranked ATT&CK techniques
  * Confidence scoring
  * Human-readable reasoning

* 🧪 **Evaluation framework**

  * Top-1 / Top-3 / Top-5 accuracy tracking

* 🗺️ **ATT&CK Navigator export**

  * Visualize detection coverage

---

## 🧠 Why This Project Exists

Traditional detection pipelines often struggle with:

* False positives (e.g., login pages misclassified as web shells)
* Weak context awareness
* Lack of explainability
* Static rule-based logic

This system addresses those gaps by combining:

> **Retrieval + Semantic Understanding + Behavioral Context**

---

## 🏗️ Architecture

```text
Logs (Zeek / Splunk)
        ↓
Ingestion Pipeline
        ↓
Normalization Layer
        ↓
AI Mapping Engine
  ├── TF-IDF Retrieval
  ├── Embedding Reranking
  ├── Rule-Based Scoring
  ├── Behavior Overrides
        ↓
Ranked ATT&CK Techniques
        ↓
Explainable Output + Navigator Export
```

---

## ⚙️ How It Works

### 1. Ingestion

```bash
python -m pipeline.ingest_logs --source zeek --path data/sample/
```

* Parses Zeek logs (`conn.log`, `http.log`)
* Normalizes into a unified alert schema

---

### 2. Analysis & Mapping

```bash
python -m pipeline.analyze_alerts --input output/normalized_zeek_alerts.json
```

* Maps alerts to ATT&CK techniques
* Produces ranked results with explanations

---

### 3. Output Example

```json
{
  "technique_id": "T1505.003",
  "name": "Web Shell",
  "confidence": 100.0,
  "explanation": [
    "Upload behavior aligned with web shell placement",
    "Server-side script indicator",
    "Scripted upload activity"
  ]
}
```

---

## 🧠 Core Design Decisions

### 1. Hybrid Scoring Model

Rather than relying on a single method:

* TF-IDF → keyword relevance
* Embeddings → semantic similarity
* Rules → domain knowledge
* Behavior overrides → real-world context

---

### 2. Behavior-Aware Overrides

Key insight:

> If retrieval misses the correct technique, scoring cannot fix it.

Solution:

* Inject behavior-driven candidates
* Prioritize critical techniques like:

  * `T1505.003` (Web Shell)
  * `T1105` (Ingress Tool Transfer)

---

### 3. False Positive Reduction

Example:

* Login page traffic is **not** classified as web shell
* Generic HTTP traffic does not dominate mappings

---

## 🧪 Sample Scenarios Covered

* SMB lateral movement → `T1021.002`
* RDP activity → `T1021.001`
* Web shell upload → `T1505.003`
* Exploitation of public-facing app → `T1190`
* Payload download → `T1105`

---

## 📂 Project Structure

```text
app/
  services/
    mapper.py

pipeline/
  ingest_logs.py
  analyze_alerts.py

data/
  sample/

output/
  sample/

requirements.txt
```

---

## 🔐 Security & Hardening Considerations

This project incorporates:

* Input normalization and schema consistency
* Behavior-based detection to reduce false positives
* Controlled scoring to prevent dominance from noisy signals
* Separation of ingestion, processing, and output layers

Future improvements include:

* Schema validation (Pydantic)
* Config-driven scoring
* CI/CD + regression testing
* API-based SIEM/SOAR integration

---

## 🚧 Future Enhancements

* 🔗 SOAR integration (automated response playbooks)
* 🤖 AI-assisted incident response engine
* 📡 Threat intelligence enrichment
* 🧪 Detection quality benchmarking
* 🐳 Dockerized deployment

---

## 💼 Relevance to Security Operations

This project demonstrates:

* SOC pipeline design
* MITRE ATT&CK mapping
* Detection engineering
* AI-assisted analysis
* Python-based security automation
* Troubleshooting and system debugging under real constraints

---

## 🧠 Key Takeaway

This is not a static script — it is a **modular detection system** designed to simulate how modern SOCs can:

* Reduce analyst workload
* Improve detection accuracy
* Provide explainable security insights

---

## 👤 Author

**Shannon Smith**
Cybersecurity | Threat Detection | AI-Assisted Security

GitHub: https://github.com/shannonasmith

---
