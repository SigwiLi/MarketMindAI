# Iowa City Housing Prices — RAG Dataset
**Geography:** Iowa City, IA | Area Code 319 | Johnson County | Iowa City MSA

Cleaned, chunked, and metadata-tagged housing price dataset for
Retrieval-Augmented Generation (RAG) pipelines.

---

## Sources

| File | Source | Credibility | Date | Chunks |
|------|--------|-------------|------|--------|
| `housing_rag_fred_fhfa.jsonl` | FRED / FHFA House Price Index (Iowa City MSA) | U.S. Federal Government | Updated Feb 2026 | 3 |
| `housing_rag_zillow.jsonl` | Zillow ZHVI + ZORI | Industry standard index | Feb 2026 | 3 |
| `housing_rag_iarealtors.jsonl` | Iowa REALTORS® Annual Report | State MLS association | Jan 2025 | 2 |
| `housing_rag_redfin.jsonl` | Redfin Market Data | National MLS brokerage | Nov 2025 | 3 |
| `housing_rag_johnsoncounty.jsonl` | Johnson County / Rocket Homes | Cedar Rapids Area REALTORS® MLS | Apr 2025 | 3 |
| `housing_rag_combined.jsonl` | **All sources combined** | — | — | **14** |

---

## Chunk Schema

```json
{
  "id":               "housing_zillow_002",
  "source_name":      "Zillow: Iowa City, IA Housing Market — ZHVI & ZORI",
  "source_url":       "https://www.zillow.com/home-values/5291/iowa-city-ia/",
  "publication_date": "2026-02-28",
  "section":          "Zillow Neighborhood Breakdown — Iowa City",
  "topic_tags":       ["neighborhoods", "Iowa City", "ZHVI", "home values by area"],
  "word_count":       99,
  "text":             "Cleaned chunk text ready for embedding..."
}
```

---

## What's Covered

- **FHFA quarterly price index** — Q2 1986 through Q4 2025 (index values + methodology)
- **Zillow ZHVI** — citywide value, 9 neighborhoods, sale-to-list ratio, inventory, days to pending
- **Zillow ZORI** — rental market index, Iowa City vs. national comparison
- **Iowa REALTORS®** — full-year 2024 statewide stats + Iowa City December 2024 local data
- **Redfin** — November 2025 snapshot, Downtown Iowa City submarket, affordability comparison
- **Johnson County** — April 2025 county summary, breakdown by bedroom count, University of Iowa context

---

## Cleaning Steps Applied

1. HTML navigation, footers, and site chrome stripped
2. Markdown syntax normalised to plain prose
3. Whitespace collapsed; blank lines normalised
4. Chunked at natural section/topic boundaries (~100–175 words each)
5. All chunks enriched with stable ID, canonical URL, ISO-8601 date, section heading, and keyword tags

---

## Quick Usage

```python
import json

chunks = []
with open("housing_rag_combined.jsonl") as f:
    for line in f:
        chunks.append(json.loads(line))

# Filter to rental-related chunks
rental = [c for c in chunks if "rental market" in c["topic_tags"]]

# Get all texts for embedding
texts = [c["text"] for c in chunks]
```

---

## Recommended Next Steps

- **Raw FHFA CSV** (full quarterly history, Q2 1986–present):
  `https://fred.stlouisfed.org/data/ATNHPIUS26980Q.txt`
  Download and ingest as structured time-series data alongside these narrative chunks.
- **Zillow Research Data Downloads** (bulk ZHVI/ZORI CSVs by ZIP, city, metro):
  `https://www.zillow.com/research/data/`
- **Embed** each `text` field with your chosen encoder and index into a vector store,
  storing all metadata as filterable attributes.

---

## Manifest

See `housing_rag_manifest.json` for a machine-readable index of all sources, chunk counts,
credibility notes, and schema definitions.
