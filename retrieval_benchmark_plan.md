# Retrieval Evaluation & Benchmark Plan — SiddhaVerse

## Document Information
- **Role**: Lead Systems Architect  
- **System Version**: v3.1-RC2  
- **Scope**: Retrieval Accuracy, Rank Evaluation, and Search Performance Benchmarks  

---

## 1. Objectives

Before integrating any large language model (LLM) or generating context-based responses, the underlying retrieval engine must meet strict accuracy and recall performance gates. This benchmark plan defines the ground-truth datasets, testing harness, and target metrics to measure the quality of both the **Lexical (FTS5)** and **Semantic (Qdrant)** search pipelines.

---

## 2. Evaluation Metrics

The system will measure search quality using five standard retrieval metrics:

### A. Precision@5
Measures the proportion of retrieved documents in the top 5 results that are relevant to the query.

$$Precision@5 = \frac{\text{Number of relevant documents in top 5}}{5}$$

- **Target Threshold**: $\ge 0.80$ (meaning at least 4 out of the top 5 results must be relevant).

### B. Recall@10
Measures the proportion of all relevant documents in the corpus that are successfully retrieved in the top 10 results.

$$Recall@10 = \frac{\text{Number of relevant documents retrieved in top 10}}{\text{Total number of relevant documents in corpus}}$$

- **Target Threshold**: $\ge 0.95$ (ensures primary source documents are rarely missed).

### C. Mean Reciprocal Rank (MRR)
Evaluates where the first relevant document appears in the search results. If the first relevant document is at rank $r$, the reciprocal rank is $1/r$. MRR is the average across all queries $Q$:

$$MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{r_i}$$

- **Target Threshold**: $\ge 0.90$ (indicates the most relevant document is consistently the 1st or 2nd result).

### D. Search Latency
Measures the response time of the search endpoint in milliseconds under simulated concurrent loads.
- **Target Thresholds**:
  - p50 (median) latency: $< 50\text{ ms}$
  - p95 latency: $< 150\text{ ms}$
  - p99 latency: $< 300\text{ ms}$

### E. Retrieval Coverage
The percentage of queries that return at least one relevant document in the top 5 results.
- **Target Threshold**: $100\%$ (no search queries should result in an empty set if matching evidence exists in the corpus).

---

## 3. Benchmark Dataset Structure

We will define a ground-truth dataset in `benchmark_ground_truth.json`. It will map test queries across five categories to their expected document identifiers:

```json
{
  "version": "2B-4",
  "queries": [
    {
      "query_id": "q001",
      "category": "Tamil Verse Lookup",
      "query_text": "நினைப்பதொன்று கண்டேன்",
      "expected_documents": ["sivavakkiyar_pm_0609"],
      "relevance_scores": {"sivavakkiyar_pm_0609": 1.0}
    },
    {
      "query_id": "q002",
      "category": "Romanized Suffix",
      "query_text": "pranayamam",
      "expected_documents": ["text_thirumandiram_pm_0127", "text_thirumandiram_pm_0240"],
      "relevance_scores": {"text_thirumandiram_pm_0127": 1.0, "text_thirumandiram_pm_0240": 0.8}
    },
    {
      "query_id": "q003",
      "category": "English Synonym",
      "query_text": "breath retention",
      "expected_documents": ["text_thirumandiram_pm_0127"],
      "relevance_scores": {"text_thirumandiram_pm_0127": 1.0}
    },
    {
      "query_id": "q004",
      "category": "Entity Search",
      "query_text": "holy basil",
      "expected_documents": ["plant_tulsi", "text_thirumandiram_pm_0255"],
      "relevance_scores": {"plant_tulsi": 1.0, "text_thirumandiram_pm_0255": 0.9}
    },
    {
      "query_id": "q005",
      "category": "Concept Query",
      "query_text": "Kaya Kalpa rejuvenation",
      "expected_documents": ["siddhar_korakkar_bio", "formulation_brahma_rasayanam"],
      "relevance_scores": {"siddhar_korakkar_bio": 1.0, "formulation_brahma_rasayanam": 0.9}
    }
  ]
}
```

---

## 4. Benchmark Execution Harness

The test runner script (`search_benchmark_runner.py`) will automatically execute the evaluation.

```python
# Conceptual Test Harness Script
import json
import time

def load_ground_truth(path):
    with open(path) as f:
        return json.load(f)["queries"]

def execute_search_api(query_text):
    # Simulated HTTP request to FastAPI search endpoint
    # returns list of document_ids
    pass

def run_evaluation():
    queries = load_ground_truth("benchmark_ground_truth.json")
    latencies = []
    mrr_sum = 0.0
    recalls = []
    precisions = []
    
    for q in queries:
        t0 = time.time()
        results = execute_search_api(q["query_text"])
        latencies.append((time.time() - t0) * 1000)
        
        # Calculate Precision@5
        top_5 = results[:5]
        relevant_in_top_5 = sum(1 for d in top_5 if d in q["expected_documents"])
        precisions.append(relevant_in_top_5 / 5.0)
        
        # Calculate Recall@10
        top_10 = results[:10]
        retrieved_relevant = sum(1 for d in top_10 if d in q["expected_documents"])
        recalls.append(retrieved_relevant / len(q["expected_documents"]))
        
        # Calculate MRR
        for rank, doc_id in enumerate(results, 1):
            if doc_id in q["expected_documents"]:
                mrr_sum += 1.0 / rank
                break
                
    print("--- BENCHMARK RESULTS ---")
    print(f"Mean P@5:   {sum(precisions)/len(queries):.4f} (Target: >=0.80)")
    print(f"Mean R@10:  {sum(recalls)/len(queries):.4f}  (Target: >=0.95)")
    print(f"MRR:        {mrr_sum/len(queries):.4f}        (Target: >=0.90)")
    print(f"p50 Latency: {percentile(latencies, 50):.2f} ms")
    print(f"p95 Latency: {percentile(latencies, 95):.2f} ms")

if __name__ == "__main__":
    run_evaluation()
```

---

## 5. Phase Transitions & Gates

The project cannot proceed to RAG or LLM integration (Phase 3C) unless all benchmarks pass the targets:

| Gate Check | Target Metric | Metric Goal | Action on Failure |
| :--- | :--- | :--- | :--- |
| **Recall Gate** | Recall@10 | $\ge 0.95$ | Expand synonym maps or adjust vector retrieval parameters in Qdrant. |
| **Precision Gate** | Precision@5 | $\ge 0.80$ | Adjust Cross-Encoder reranking rules or tune RRF stabilizer $k$. |
| **Latency Gate** | p95 latency | $< 150\text{ ms}$ | Implement database connection pooling or cache query keys. |

---

*Report generated by SiddhaVerse Systems Architecture Board, 2026-06-25*
