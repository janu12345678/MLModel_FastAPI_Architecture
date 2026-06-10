# Loan Underwriting & Credit Risk Service (Group 84)

This repository contains the implementation of the **Loan Approval Risk Assessment Service**, designed for automated consumer lending credit risk evaluation.

The project applies **Software Engineering for ML (SE4ML)** best practices, integrating **GR4ML requirements modeling** and **Sculley's "Hidden Technical Debt" architectural framework** using a **Pipe-and-Filter design pattern**.

---

## Project Structure

```
├── README.md
├── requirements.txt
├── configs/
│   └── config.yaml               # Externalized system and model thresholds
├── data/
│   ├── Loan.csv                  # Kaggle dataset (20,000 records, 36 features)
│   ├── prepare_data.py           # Feature engineering & preprocessing script
│   └── loan_data_processed.csv   # Processed dataset (20,000 records, 22 features + target)
├── app/
│   ├── __init__.py
│   ├── config.py                 # PyYAML-based configuration management
│   ├── schemas.py                # Pydantic input/output schemas (robustness boundary)
│   ├── pipeline.py               # Pipe-and-Filter execution engine
│   ├── logger.py                 # Structured JSON logger & runtime timers
│   ├── main.py                   # FastAPI serving microservice
│   └── model.pkl                 # Serialized trained RandomForest model
├── training/
│   ├── __init__.py
│   └── step1_notebook.py         # RandomForest training pipeline
├── diagrams/
│   ├── generate_diagrams.py      # GR4ML diagram generator
│   ├── generate_architecture.py  # System architecture diagram generator
│   ├── gr4ml_business_view.png
│   ├── gr4ml_analytics_design_view.png
│   ├── gr4ml_data_prep_view.png
│   └── system_architecture.png
└── Group_84.ipynb                # Jupyter Notebook report
```

---

## Architecture Design & Patterns

### 1. Pipe-and-Filter Pattern
The runtime prediction sequence is structured as a series of decoupled Filters connected by Pipes:
* **Filter 1 (validate_input):** Validates business constraints (e.g., loan amount <= 500% of annual income).
* **Filter 2 (extract_features):** Computes derived features (LoanToIncomeRatio, SavingsToLoanRatio) and prepares feature DataFrame.
* **Filter 3 (run_model):** Invokes model inference and applies classification thresholds.
* **Filter 4 (format_response):** Maps probability to risk tiers (LOW/MEDIUM/HIGH) and packages output.

### 2. Microservices Serving & Event-Driven Monitoring
* The pipeline is wrapped in a **FastAPI** service.
* Application metrics (latency, credit score, approval status) are logged in **structured JSON format**.
* Exposes a `/health` endpoint for liveness/readiness checks.

---

## Dataset

**Source:** Kaggle - Financial Risk for Loan Approval (lorenzozoppelletto/financial-risk-for-loan-approval)
- 20,000 records, 36 original features
- After feature engineering: 22 features + 1 target

### Feature Engineering Pipeline (`data/prepare_data.py`):
1. Drop non-predictive columns (ApplicationDate, LoanApproved) → 36 → 30 features
2. Drop redundant features via correlation analysis (r > 0.95) → 30 → 27 features
3. Drop low-importance features (importance < 0.005) → 27 → 21 features
4. Encode categorical variables (EmploymentStatus, EducationLevel, LoanPurpose)
5. Engineer derived features: LoanToIncomeRatio, SavingsToLoanRatio

---

## Quick Start

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Data Preparation
Run feature engineering on the raw Kaggle dataset:
```bash
python data/prepare_data.py
```

### 3. Model Training
Train the Random Forest classifier (150 trees, max_depth=10):
```bash
python training/step1_notebook.py
```

### 4. Run FastAPI Service
```bash
uvicorn app.main:app --reload --port 8000
```
Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger documentation.

---

## Quality Attributes

| Attribute | Implementation |
|-----------|---------------|
| **Robustness** | Pydantic schema validation + business rule checks in Filter 1 |
| **Reliability** | Risk tiering logic with deterministic categorization in Filter 4 |
| **Performance** | Latency tracking with <150ms SLA target |
