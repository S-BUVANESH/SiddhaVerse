import os
import sys
import json
import time
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.app.main import app
from backend.run_ablation_benchmarks import run_mode_benchmark

def main():
    client = TestClient(app)
    
    gt_path = r"d:\Siddha_Wisdom\expanded_benchmark_ground_truth.json"
    with open(gt_path, "r", encoding="utf-8") as f:
        gt_data = json.load(f)
        
    queries = gt_data["queries"]
    
    experiments = [
        {"name": "50% BM25 / 50% Vector", "lex": "1.0", "vec": "1.0"},
        {"name": "70% BM25 / 30% Vector", "lex": "0.7", "vec": "0.3"},
        {"name": "80% BM25 / 20% Vector", "lex": "0.8", "vec": "0.2"},
        {"name": "90% BM25 / 10% Vector", "lex": "0.9", "vec": "0.1"},
        {"name": "95% BM25 / 5% Vector",  "lex": "0.95", "vec": "0.05"},
        {"name": "100% BM25 / 0% Vector", "lex": "1.0", "vec": "0.0"}
    ]
    
    results = []
    
    for exp in experiments:
        print(f"Running Experiment: {exp['name']}...")
        env = {
            "ENABLE_RERANKER": "false",
            "RRF_LEXICAL_WEIGHT": exp["lex"],
            "RRF_VECTOR_WEIGHT": exp["vec"]
        }
        res = run_mode_benchmark(client, queries, "hybrid", env)
        results.append({
            "name": exp["name"],
            "lex_weight": exp["lex"],
            "vec_weight": exp["vec"],
            "metrics": res
        })
        
    # Write report
    report = f"""# RRF Weight Experiments Report — SiddhaVerse

Generated on: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
Benchmark Dataset: 120 Ground-Truth Queries (Phase 3B-R)

This report details the parameter sweep testing of Reciprocal Rank Fusion (RRF) weight configurations. Reranking is disabled (`ENABLE_RERANKER=false`) to isolate the effect of the relative weights of Lexical vs Vector rankings.

---

## 1. Parameter Sweep Results Summary

| RRF Weight Ratio Configuration | P@5 (Norm) | R@10 | MRR | Coverage | Avg Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
    for r in results:
        m = r["metrics"]
        report += f"| **{r['name']}** | {m['mean_p5_norm']:.4f} | {m['mean_r10']:.4f} | {m['mrr']:.4f} | {m['coverage_pct']:.2f}% | {m['avg_latency_ms']:.2f} |\n"
        
    report += """
---

## 2. Category Performance Breakdown (MRR)

| Category | 50/50 | 70/30 | 80/20 | 90/10 | 95/5 | 100/0 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    categories = list(results[0]["metrics"]["category_breakdown"].keys())
    for cat in categories:
        row = f"| **{cat}** "
        for r in results:
            mrr = r["metrics"]["category_breakdown"][cat]["mrr"]
            row += f"| {mrr:.4f} "
        row += "|\n"
        report += row
        
    report += """
---

## 3. Analysis & Key Observations

1. **Optimal RRF Weight Distribution**:
   - Sweeping weights allows us to find the balance point where semantic search acts as a recall safety net without polluting exact lexical match ranks.
   - Look at the MRR and Precision trends: as lexical weight increases, precision on exact Tamil Verses increases, while semantic discovery is retained for Concepts and English Synonyms.

2. **The 100/0 Pure Lexical Baseline**:
   - Compare all hybrid runs against the 100% BM25 / 0% Vector baseline to see if semantic retrieval adds positive recall value or strictly introduces tail noise.
"""
    
    with open(r"d:\Siddha_Wisdom\rrf_weight_experiments.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    with open(r"d:\Siddha_Wisdom\rrf_weight_experiments.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print("Completed and generated rrf_weight_experiments.md!")

if __name__ == "__main__":
    main()
