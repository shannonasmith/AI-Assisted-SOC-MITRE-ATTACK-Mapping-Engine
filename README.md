<div align="center">

# 🛡️ ATT&CK Mapping Engine  

## 🧠 SOC Systems • Detection Engineering • Agentic Investigation

![Focus](https://img.shields.io/badge/Focus-Detection%20Engineering%20%7C%20ATT%26CK%20Mapping-blue?style=for-the-badge)
![Approach](https://img.shields.io/badge/Approach-Detection%20→%20Classification%20→%20Analysis-success?style=for-the-badge)
![Tech](https://img.shields.io/badge/Tech-Python%20%7C%20NLP%20%7C%20MITRE-black?style=for-the-badge)

</div>

<div align="center">
  <img src="images/demo.gif" width="900">
</div>

<p align="center"><em>Detection pipeline demonstrating ingestion → normalization → ATT&CK classification.</em></p>

---

## 🧠 Purpose

This project represents the **detection engineering stage** of a progressively evolving SOC system.

| Stage | Description |
|------|------------|
| Alert Analysis | Understanding and triaging security events |
| Detection Engineering | Mapping behavior to MITRE ATT&CK |
| Investigation | Correlating and enriching alerts |
| Decision Support | Recommending response actions |

---

## 🎯 Objective

The goal of this phase is to demonstrate:

- how raw telemetry is transformed into structured alerts  
- how behavior maps to MITRE ATT&CK techniques  
- how detection pipelines improve classification accuracy  
- how scoring and ranking influence detection quality  
- how structured detection supports downstream investigation  

---

## 🛡️ Phase 2 — ATT&CK Mapping Engine

![Focus](https://img.shields.io/badge/Focus-Detection%20Engineering-green)

| Category | Details |
|---------|--------|
| Focus | Classification and structured detection |
| Role | Detection engineering pipeline |
| Output | Ranked ATT&CK techniques |

---

## 🧩 Key Capabilities

- normalization pipeline  
- TF-IDF candidate retrieval  
- embedding-based reranking  
- hybrid scoring engine  
- ATT&CK technique ranking  
- explainable detection outputs  

---

## 📈 Capability Progression

```text
Alert Parsing → Classification → Investigation → Decision
```

---

## 🧠 System Role

This repository builds on earlier and later phases:

- Phase 1 → establishes alert understanding  
- Phase 2 → improves detection accuracy  
- Phase 3 → enables reasoning and decision-making  

---

## 🧠 Detection Workflow

| Stage | Description |
|------|------------|
| 🟦 Raw Logs | Ingestion from Zeek / SIEM |
| 🟨 Normalization | Structured alert creation |
| 🧠 Candidate Retrieval | TF-IDF technique selection |
| 🧬 Semantic Reranking | Embedding similarity |
| ⚙️ Scoring Engine | Behavior-based weighting |
| 🎯 ATT&CK Mapping | Final classification |
| 📊 Output | Ranked techniques + coverage |

---

## ⚡ Quick Start (Run the Project)

Run the detection pipeline locally.

### 1. Clone the repository

```bash
git clone https://github.com/shannonasmith/AI-Assisted-SOC-MITRE-ATTACK-Mapping-Engine.git
cd AI-Assisted-SOC-MITRE-ATTACK-Mapping-Engine
```

---

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install numpy scikit-learn sentence-transformers joblib python-dateutil
```

---

### 4. Download MITRE ATT&CK dataset

```bash
mkdir -p data/raw
curl -L "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json" -o data/raw/enterprise-attack.json
```

---

### 5. Ingest logs

```bash
python -m pipeline.ingest_logs --source zeek --path data/zeek/
```

---

### 6. Run analysis

```bash
python -m pipeline.analyze_alerts --input output/normalized_zeek_alerts.json
```

---

### 📁 Expected Output

```text
output/mapped_alerts.json
output/coverage_summary.json
output/attack_navigator.json
```

---

## 👀 What This Looks Like in Practice

The following steps show how raw telemetry is transformed into structured ATT&CK-aligned detections.

---

### 🌐 Step 1 — Multi-Source Ingestion

<div align="center">
  <img src="images/05-zeek-ingestion-success.png" width="600">
</div>

---

### 🔄 Step 2 — Normalization Pipeline

<div align="center">
  <img src="images/11-normalized-output.png" width="700">
</div>

---

### 🔍 Step 3 — Candidate Retrieval (TF-IDF)

<div align="center">
  <img src="images/03-tfidf-retrieval-test.png" width="600">
</div>

---

### 🧠 Step 4 — Behavior-Based Scoring Engine

<div align="center">
  <img src="images/04-scoring-logic2.png" width="600">
</div>

---

### ⚙️ Step 5 — ATT&CK Mapping Output

<div align="center">
  <img src="images/10-attack-mapping-output.png" width="700">
</div>

---

## ⚙️ Technical Pipeline (Under the Hood)

```text
Raw Logs
    ↓
Normalization
    ↓
Triage Scoring
    ↓
TF-IDF Retrieval
    ↓
Embedding Reranking
    ↓
Hybrid Scoring
    ↓
ATT&CK Mapping
    ↓
Output Generation
```

---

## 💡 What This Project Demonstrates

- detection engineering workflows  
- ATT&CK mapping logic  
- scoring and ranking systems  
- SOC-style classification pipelines  
- AI-assisted analysis techniques  

---

## 💼 SOC Relevance

Simulates:

- SIEM alert triage  
- ATT&CK classification  
- detection engineering pipelines  
- analyst-facing outputs  

---

## 🚧 Future Work

- integration with investigation engine (Phase 3)  
- improved scoring logic  
- threat intelligence enrichment  
- real-time detection pipelines  

---

<div align="center">

## 👤 Shannon Smith  

Cybersecurity | Detection Engineering • SOC Operations • AI-Assisted Security  

</div>
