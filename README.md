# GenAI Assisted Insurance Document Extraction and Risk Classification

This project demonstrates an end to end workflow that mirrors real insurtech pipelines used for document intake, risk extraction, and downstream modelling. It combines GenAI driven structured extraction with classical machine learning to create a transparent and explainable risk classifier over synthetic insurance related documents.

---

## 1. Project Overview

This repository implements a complete pipeline for transforming unstructured insurance style documents into structured, validated JSON outputs and a final high risk vs low risk classifier. The workflow is designed to reflect production style patterns used in marine, motor, and specialty insurance analytics.

The project includes:

* Chunking and preprocessing of raw documents
* LLM driven extraction with strict JSON schema and controlled vocabularies
* MapReduce style consolidation
* EDA and normalisation of extracted records
* Feature engineering for modelling
* Risk classification using Logistic Regression and Random Forest
* Interpretation of model behaviour for underwriter style communication

All data in the repository is fully synthetic and safe for public use.

---

## 2. Folder Structure

```
project/
├── data/
│   ├── raw/
│   │   ├── policy/
│   │   ├── esg/
│   │   └── incident/
│   └── processed/
│       ├── docs_extracted.csv
│       ├── docs_extracted.json
│       └── docs_clean.csv
│
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_eda_and_normalisation.ipynb
│   └── 03_feature_engineering_and_classification.ipynb
│
├── src/
│   ├── chunking.py
│   ├── extraction.py
│   ├── validation.py
│   ├── prompt_template.py
│   ├── reducer.py
│   └── utils.py
│
└── README.md

```

---

## 3. Data Description

The dataset consists of fourteen synthetic documents across three categories:

* **Insurance policies** (coverage wording, exclusions, operational risks)
* **ESG reports** (climate, governance, and transition risk narratives)
* **Incident reports** (operational loss events, collisions, and failures)

The documents are intentionally messy and unstructured to reflect realistic insurance text. They range from 700 to 1000 words each.

---

## 4. Pipeline Summary

The full workflow is split across three notebooks.

### Notebook 01: LLM Extraction and MapReduce

* Load raw text files
* Apply sliding window chunking
* Build a strict JSON extraction prompt
* Call a Groq hosted LLaMA model for structured extraction
* Validate each output using a schema and controlled vocabularies
* Apply MapReduce logic to merge chunk level extractions into one record per document
* Save document level extracted data

**Outputs:**

* `docs_extracted.csv`
* `docs_extracted.json`

### Notebook 02: EDA and Normalisation

* Inspect distributions of categorical fields
* Check missingness and consistency
* Convert key risk factors into a list format using a robust regex method
* Create numeric features (risk factor count, summary lengths)
* Apply minimal normalisation (lowercasing, trimming) while protecting list columns
* Produce a clean modelling ready dataset

**Output:**

* `docs_clean.csv`

### Notebook 03: Feature Engineering and Classification

* Define a realistic high risk target
* Perform a split before any preprocessing to prevent leakage
* Build a ColumnTransformer for numeric and categorical encoding
* Train Logistic Regression and Random Forest classifiers
* Evaluate models using metrics suited for imbalanced data
* Interpret model behaviour using feature importances
* Provide an underwriter friendly explanation of risk drivers

---

## 5. Modelling Approach

The classifier predicts whether a document should be considered high risk based on extracted features.

### Models Used

* **Logistic Regression** with balanced class weights
* **Random Forest** for non linear patterns

### Preprocessing

* Numeric: median imputation and standard scaling
* Categorical: most frequent imputation and one hot encoding

### Evaluation

* Accuracy
* Precision
* Recall
* F1 score
* ROC AUC
* Confusion matrix

The approach prioritises explainability and stability, which is essential in insurance settings.

---

## 6. Explainability

Feature importance methods are applied to understand which factors drive risk predictions. These include:

* Coefficients from Logistic Regression
* Feature importances from Random Forest

Key risk indicators captured by the models include:

* Document category
* Risk type
* Summary length
* Number of extracted risk factors
* Region and sector indicators

These patterns align with expectations from underwriting, confirming the extraction and modelling pipeline behaves as intended.

---

## 7. Why This Project Matters

This project demonstrates:

* Understanding of GenAI driven extraction workflows
* Ability to design and validate a schema and prompt
* Clean, modular engineering practices
* Strong EDA and feature engineering skills
* Correct handling of class imbalance and leakage
* Clear communication of model behaviour to stakeholders
* Practical alignment with real insurtech document processing tasks

The workflow reflects how GenAI and classical ML can work together to support decision making in insurance environments.

---

## 8. Future Improvements

Potential enhancements include:

* Using retrieval augmented generation for extraction
* Adding SHAP or ALE plots for deeper interpretability
* Improving sector and region normalisation
* Experimenting with gradient boosted trees
* Adding evaluation on new unseen synthetic documents

---

## 9. How to Reproduce

1. Clone the repository
2. Install dependencies from requirements file
3. Set up a `.env` file with Groq API credentials
4. Run the notebooks in order: 01, 02, then 03

---

## 10. Author

**Mishara Sapukotanage**
MSc Data Science, University of Bristol

This project was built to strengthen GenAI understanding, EDA intuition, and feature engineering skills, while exploring realistic insurance analytics workflows.

