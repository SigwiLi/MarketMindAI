# Financial Fraud RAG Dataset

Cleaned, chunked, and metadata-tagged text dataset prepared for
Retrieval-Augmented Generation (RAG) pipelines.

---

## Sources

| File | Source | Date | Chunks |
|------|--------|------|--------|
| `rag_ftc_csn_2024.jsonl` | FTC Consumer Sentinel Network Data Book 2024 | Mar 2025 | 4 |
| `rag_ftc_explore_data.jsonl` | FTC Explore Data — Interactive Dashboards | Quarterly | 3 |
| `rag_csi_iowa_fraud_2025.jsonl` | CSI Iowa: Impact of Financial Fraud in Iowa | Aug 2025 | 9 |
| `rag_dataset_combined.jsonl` | **All sources combined** | — | **16** |

---

## Chunk Schema

Every line in each `.jsonl` file is a self-contained JSON object:

```json
{
  "id":               "csi_iowa_fraud_2025_002",
  "source_name":      "CSI Iowa: The Impact of Financial Fraud in Iowa (August 2025)",
  "source_url":       "https://...",
  "publication_date": "2025-08-01",
  "section":          "Key Findings Summary",
  "topic_tags":       ["key findings", "economic impact", "Iowa", "GDP", "jobs"],
  "word_count":       175,
  "text":             "Cleaned chunk text ready for embedding..."
}
```

---

## Cleaning Steps Applied

1. **Navigation/boilerplate removal** — all HTML nav menus, headers, footers,
   breadcrumbs, and repeated site chrome stripped.
2. **Markdown normalisation** — heading hashes, bold/italic markers, link syntax,
   and image tags removed; plain prose retained.
3. **Whitespace normalisation** — multiple consecutive spaces collapsed to one;
   three or more blank lines collapsed to two.
4. **Semantic chunking** — text split at natural section boundaries (report headings,
   topic shifts) rather than by fixed token count, preserving coherent arguments in
   each chunk. Target range: 90–200 words per chunk.
5. **Metadata enrichment** — each chunk carries a stable `id`, canonical `source_url`,
   ISO-8601 `publication_date`, human-readable `section`, topical `topic_tags`, and
   `word_count`.
6. **No PII** — the underlying public reports contain no personal consumer data;
   all figures are aggregated statistics.

---

## Quick Usage (Python)

```python
import json

chunks = []
with open("rag_dataset_combined.jsonl") as f:
    for line in f:
        chunks.append(json.loads(line))

# Filter to Iowa-specific chunks
iowa = [c for c in chunks if "Iowa" in c["topic_tags"]]

# Pass text to your embedding model
texts = [c["text"] for c in chunks]
```

---

## Recommended Next Steps

- **Embed** each `text` field with your chosen encoder
  (e.g., `text-embedding-3-small`, `all-MiniLM-L6-v2`, etc.).
- **Index** into a vector store (Pinecone, Weaviate, pgvector, Chroma, etc.)
  storing all metadata fields as filterable attributes.
- **Augment** with the raw FTC CSV files
  (`https://www.ftc.gov/system/files/ftc_gov/data/csn-data-book-2024-csv.zip`)
  for tabular/statistical queries — unzip and ingest each CSV as structured data
  alongside these narrative chunks.
- **Re-chunk** if your embedding model has a smaller token budget — split at
  double-newlines and re-run the cleaning function in `clean_for_rag.py`.

---

## Manifest

See `rag_manifest.json` for a machine-readable index of all source files,
chunk counts, and schema definitions.
