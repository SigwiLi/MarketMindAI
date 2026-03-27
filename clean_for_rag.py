"""
RAG Dataset Cleaner
Converts three financial-fraud sources into clean, chunked, metadata-rich JSONL.

Sources:
  1. FTC Consumer Sentinel Network Data Book 2024 (page content + CSV notes)
  2. FTC Explore Data landing page
  3. CSI Iowa Financial Fraud Report (August 2025)
"""

import json
import re
import textwrap
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Remove excess whitespace, nav artefacts, and markdown noise."""
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)          # strip markdown links
    text = re.sub(r"#{1,6} ", "", text)                  # strip heading hashes
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)  # strip bold/italic
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)          # strip images
    text = re.sub(r"-{2,}", "", text)                    # strip hr lines
    text = re.sub(r"[ \t]+", " ", text)                  # collapse spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text)               # collapse blank lines
    return text.strip()


def make_chunk(chunk_id: str, source_name: str, source_url: str,
               pub_date: str, section: str, topic_tags: list,
               text: str) -> dict:
    """Return a single RAG chunk as a dict."""
    return {
        "id": chunk_id,
        "source_name": source_name,
        "source_url": source_url,
        "publication_date": pub_date,
        "section": section,
        "topic_tags": topic_tags,
        "word_count": len(text.split()),
        "text": text.strip()
    }


def write_jsonl(records: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  ✓  Wrote {len(records)} chunks → {path}")


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 1 — FTC Consumer Sentinel Network Data Book 2024
# ─────────────────────────────────────────────────────────────────────────────

FTC_URL   = "https://www.ftc.gov/reports/consumer-sentinel-network-data-book-2024"
FTC_NAME  = "FTC Consumer Sentinel Network Data Book 2024"
FTC_DATE  = "2025-03-01"   # release announced March 2025

ftc_raw_chunks = [
    {
        "section": "Overview",
        "tags": ["consumer fraud", "identity theft", "sentinel network", "2024 statistics"],
        "text": """
The FTC Consumer Sentinel Network Data Book 2024 compiles unverified consumer reports
about fraud, identity theft, and other consumer-protection topics submitted to the Federal
Trade Commission. During 2024, Sentinel received 6.5 million consumer reports, sorted
into 29 top categories. New FTC data show a significant jump in reported losses to fraud,
reaching $12.5 billion in 2024. The Consumer Sentinel Network (Sentinel) is a secure
online database available exclusively to law enforcement partners across local, national,
and international jurisdictions. Since its launch in 1997, Sentinel has collected tens of
millions of consumer reports. Sentinel maintains a five-year data retention policy, with
reports older than five years purged biannually. The data is not based on a consumer
survey; all figures reflect unverified self-reported consumer submissions.
"""
    },
    {
        "section": "Data Sources and Access",
        "tags": ["data contributors", "law enforcement", "Better Business Bureau", "data access"],
        "text": """
In addition to direct consumer reports submitted via the FTC's call center or online portal,
Sentinel aggregates reports from other federal, state, local, and international law enforcement
agencies, as well as non-government organizations including the Better Business Bureau.
A full listing of data contributors is available in Appendices A3 and A4 of the annual data book.
Non-government organizations that contribute reports do not receive access to Sentinel data;
access is restricted to verified law enforcement agencies only. Interactive data dashboards with
charts, maps, and filtered views are available through Tableau Public at the FTC's profile.
Quarterly updates to the data are provided online at ftc.gov/exploredata. Raw data files are
published annually as a ZIP archive containing CSV files covering all 29 report categories.
"""
    },
    {
        "section": "Fraud Loss Trends",
        "tags": ["fraud losses", "financial loss", "2024", "consumer reports"],
        "text": """
Total reported losses to fraud reached $12.5 billion in 2024, representing a substantial
year-over-year increase compared to 2023 figures. Of the 6.5 million consumer reports
received by the Sentinel network in 2024, a significant share involved fraudulent activity
with a financial component. The 29 report categories tracked by the FTC span a wide range
of fraud and consumer-protection topics, enabling law enforcement to identify trends,
spot questionable business practices, and build enforcement targets. Law enforcement
personnel may join Sentinel and access the underlying database through a registration
process at Register.ConsumerSentinel.gov.
"""
    },
    {
        "section": "Interactive Data and Downloads",
        "tags": ["Tableau", "CSV data", "interactive dashboard", "data visualization"],
        "text": """
The FTC publishes Consumer Sentinel data in multiple formats to support research and
law-enforcement use. An interactive Tableau Public dashboard (The Big View: All Sentinel
Reports) provides top-report summaries, geographic maps, and trend charts filterable
by year, state, category, and age group. Quarterly data refreshes are available at
ftc.gov/exploredata. The full annual data book is downloadable as a PDF (4.3 MB).
Raw tabular data are provided as a ZIP archive of CSV files (approximately 121 KB),
covering aggregated statistics for each of the 29 report categories. These files are
suitable for downstream data processing, visualization, and machine-learning pipelines.
"""
    },
]

ftc_chunks = []
for i, c in enumerate(ftc_raw_chunks, 1):
    ftc_chunks.append(make_chunk(
        chunk_id   = f"ftc_csn_2024_{i:03d}",
        source_name= FTC_NAME,
        source_url = FTC_URL,
        pub_date   = FTC_DATE,
        section    = c["section"],
        topic_tags = c["tags"],
        text       = clean_text(c["text"])
    ))


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 2 — FTC Explore Data (Tableau interactive hub)
# ─────────────────────────────────────────────────────────────────────────────

EXP_URL  = "https://www.ftc.gov/news-events/data-visualizations/explore-data"
EXP_NAME = "FTC Explore Data — Interactive Sentinel Dashboards"
EXP_DATE = "2025-01-01"   # ongoing/quarterly updated resource

explore_raw_chunks = [
    {
        "section": "Overview of Explore Data Hub",
        "tags": ["data visualization", "Tableau", "consumer sentinel", "interactive"],
        "text": """
The FTC Explore Data hub at ftc.gov/news-events/data-visualizations/explore-data is the
central portal for interactive visualizations derived from the Consumer Sentinel Network.
It links to Tableau Public dashboards that allow users to filter, explore, and download
Sentinel data by fraud category, year, U.S. state, and consumer age group. The hub is
updated quarterly as new consumer reports are processed. Key dashboards include:
(1) The Big View: All Sentinel Reports — top-level summary of all 6.5 million 2024 reports
across 29 categories; (2) FTC Refunds to Consumers — refund statistics by case and
dollar amount; (3) Top Fraud Reports — a focused view of the ten most-reported fraud types.
All visualizations are publicly accessible without login through Tableau Public.
"""
    },
    {
        "section": "Available Dashboard Categories",
        "tags": ["dashboard", "fraud categories", "identity theft", "imposter scams", "data spotlight"],
        "text": """
The Explore Data hub surfaces Sentinel data across several thematic dashboard groups.
Fraud dashboards cover imposter scams, online shopping fraud, telephone and mobile
services fraud, prizes and sweepstakes, business and job opportunities, and travel and
vacation scams, among others. Identity theft dashboards break down government documents
and benefits fraud, credit card fraud, bank fraud, and employment or tax-related fraud.
The Data Spotlight section publishes periodic narrative analyses of emerging trends,
such as the sharp rise in crypto investment fraud and social media impersonation scams.
These spotlights are intended to inform consumers, researchers, and policymakers about
evolving fraud patterns observed in real-time Sentinel data.
"""
    },
    {
        "section": "Data Currency and Methodology",
        "tags": ["data currency", "methodology", "quarterly updates", "unverified reports"],
        "text": """
All data presented through the Explore Data hub derives from the Consumer Sentinel
Network, which is populated by unverified consumer self-reports. Reports are contributed
by the FTC's own consumer reporting channels as well as hundreds of partner organizations
including the Better Business Bureau, federal agencies, and state consumer-protection
offices. Quarterly updates ensure the dashboards reflect recent trends within months
of their occurrence. Users should note that the underlying reports are unverified;
figures represent reported incidents and losses, not confirmed fraud amounts. The
five-year data-retention policy means the hub covers rolling five-year windows.
Year-over-year comparisons are best drawn using the annual Data Book rather than
live dashboard snapshots, which may shift as new reports are added retroactively.
"""
    },
]

exp_chunks = []
for i, c in enumerate(explore_raw_chunks, 1):
    exp_chunks.append(make_chunk(
        chunk_id   = f"ftc_explore_{i:03d}",
        source_name= EXP_NAME,
        source_url = EXP_URL,
        pub_date   = EXP_DATE,
        section    = c["section"],
        topic_tags = c["tags"],
        text       = clean_text(c["text"])
    ))


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 3 — CSI Iowa Financial Fraud Report (August 2025)
# ─────────────────────────────────────────────────────────────────────────────

CSI_URL  = "https://www.commonsenseinstituteus.org/ResearchUploads/CSI%20Report%20-%20IA%20Financial%20Fraud%20FINAL.pdf"
CSI_NAME = "CSI Iowa: The Impact of Financial Fraud in Iowa (August 2025)"
CSI_DATE = "2025-08-01"

csi_raw_chunks = [
    {
        "section": "Introduction and National Context",
        "tags": ["financial fraud", "national trends", "FBI", "FTC", "Iowa", "2024"],
        "text": """
Financial fraud is rising nationally. The FBI's Internet Crime report tracked 859,532 fraud
claims in 2024, resulting in $16.6 billion in financial loss — up 33 percent from 2023. The
FTC Consumer Sentinel Network reported 2.6 million fraud cases in 2024, of which 38 percent
involved losing money; citizens reported losing $12 billion to fraud, up $2 billion over 2023.
Despite the national rise, Iowa has a comparatively strong record on fraud mitigation. Based
on FBI cyber-enabled crime statistics, Iowa ranks 16th best on total losses, 10th best in
cyber-enabled crime per 100,000 residents, 15th best for complaints filed by individuals
aged 60 and over, and 10th best for cryptocurrency losses by state. Using FTC Consumer
Sentinel metrics, Iowa holds the third-lowest rate of fraud and the sixth-lowest rate of
identity theft nationally. Iowa's banking industry, law enforcement, and state agencies
have worked to raise awareness of fraud risk, likely contributing to the state's favorable
national ranking.
"""
    },
    {
        "section": "Key Findings Summary",
        "tags": ["key findings", "economic impact", "Iowa", "GDP", "jobs", "2025 projections"],
        "text": """
CSI projects the following losses from financial fraud in Iowa in 2025:
- An estimated $93 million in direct, reported losses.
- Between $93 million and $573 million in direct, unreported losses.
- Combined reported and unreported losses of up to $666 million — equivalent to $57 to
  $205 per Iowan.
The economic impact of reported fraud alone is projected to include a $225 million reduction
in state GDP, a $200 million reduction in statewide personal income, and the loss of
approximately 1,500 jobs. If all financial fraud — reported and unreported — is accounted for,
the projected impact rises to up to a $1.5 billion reduction in state GDP, up to a $1 billion
reduction in statewide personal income, and the loss of up to approximately 5,000 jobs.
The state General Fund is estimated to lose $46 million in tax revenue due to reported and
unreported fraud. Iowa's fraud incidence rate is 715 reported incidents per 100,000 residents,
the third lowest in the country, surpassed only by North Dakota (696) and South Dakota (676).
"""
    },
    {
        "section": "Types of Financial Fraud",
        "tags": ["fraud types", "imposter scams", "romance scams", "investment fraud", "elder fraud"],
        "text": """
Financial fraud transactions take two main forms: verified (customer-initiated or approved)
and unverified (not initiated or confirmed by the customer). Verified fraud typically involves
deception or coercion leading the customer to authorize a transaction, as in scams or social
engineering. Unverified fraud involves unauthorized access, such as stolen card credentials
used without the customer's knowledge. Key fraud types discussed in this report include:

Grandparent Scam — thieves create a false emergency compelling grandparents to send money.
Romance Scams — fraudsters build fake relationships to manipulate victims into sending money.
Wire Transfer Fraud — scammers impersonate trusted contacts to divert wire transfers.
Investment Fraud — fake or misleading investment opportunities (crypto scams, Ponzi schemes,
  pump-and-dump stocks, real estate fraud, high-yield investment programs).
Gift Card Scams — victims are tricked into purchasing gift cards for scammers posing as
  authority figures.
Imposter Scams — scammers pose as IRS, Social Security Administration, or other officials.
Elder Financial Fraud — targeted scams against older adults through deception or coercion.
Check Fraud, Credit and Debit Card Fraud, Account Takeover, Phishing, Social Media Fraud,
  Payment App Fraud (Zelle, Venmo, Cash App), ATM Fraud, Skimming, Money Laundering,
  Loan Fraud, and Identity Fraud are also documented categories.
"""
    },
    {
        "section": "Iowa Fraud Trends 2020–2024",
        "tags": ["Iowa", "fraud trend", "FTC data", "FBI data", "reported losses", "2020-2024"],
        "text": """
Based on both FBI and FTC data, financial fraud in Iowa increased every year from 2020 to 2024.
Direct losses tracked in the FTC's Consumer Sentinel Network rose from $17.1 million in 2020
to $52 million in 2024 — a 204 percent increase over the period. FBI-reported losses from
cyber-enabled crime in Iowa grew 241 percent over the same period, reaching $72 million in 2024.
The Iowa Department of Public Safety reported a 6 percent increase in fraud cases from 2022
through 2024. These figures encompass only reported fraud; a substantial share of financial
fraud goes unreported, meaning actual totals are considerably higher. The most common type
of fraud in Iowa is imposter scams, which include grandparent scams, fake distress calls,
and other forms of illegal financial misrepresentation.
"""
    },
    {
        "section": "Demographic Profile — Age and Loss Patterns",
        "tags": ["demographics", "age groups", "elder fraud", "Iowa", "FTC age data"],
        "text": """
In Iowa, 31 percent of reported fraud cases involved a financial loss greater than zero,
with an average loss of $3,128 per incident. Average loss amounts vary significantly by age.
Fraud victims aged 60 to 69 experience the highest average loss at $4,880 per incident,
compared to $1,890 for 20- to 29-year-olds. After peaking in the 60–69 age group, average
losses decline, reaching $1,703 for individuals aged 80 and older.

Younger Iowans aged 20 to 29, though less likely to report fraud, report a financial loss
at a higher rate (46 percent of their fraud reports involve money lost) than older age groups.
The 80-and-over group reports a financial loss in only 15 percent of cases.

FBI Internet Crime data shows that individuals aged 60 and over account for more than 70
percent of reported financial loss from internet-based fraud in Iowa in 2024, up from 50
percent in 2023 and 34 percent in 2020. The two age groups under 30 consistently represent
a small fraction of total loss — just 2.1 percent in 2024.
"""
    },
    {
        "section": "Case Study — Cryptocurrency ATM Fraud",
        "tags": ["case study", "cryptocurrency ATM", "Iowa", "elder fraud", "economic impact"],
        "text": """
Iowa Attorney General Brenna Bird filed lawsuits against the two largest cryptocurrency ATM
operators in Iowa, alleging the companies allowed citizens to transfer more than $20 million
to scammers through their kiosks. The two companies reportedly charged fees of 23 and 21
percent respectively. The suits allege violations of Iowa's Consumer Fraud Act, including
failing to inform Iowans of their refund policies. Most alleged victims were over the age of 60.

Using REMI's Tax PI+ economic model, CSI estimated the economy-wide impact if this case had
occurred in 2025. The removal of $20 million from consumer wealth would result in:
- A $14 million reduction in state GDP.
- An $8 million reduction in personal income.
- A $25 million reduction in business sales (output).
- A loss of 122 jobs statewide.
This case illustrates how fraud losses do not stay isolated — the money that would have
otherwise circulated through Iowa's economy disappears, creating a multiplier contraction.
"""
    },
    {
        "section": "Unreported Fraud Estimates",
        "tags": ["unreported fraud", "FINRA", "reporting rate", "dark figure", "Iowa"],
        "text": """
A significant portion of financial fraud goes unreported for a variety of reasons, including:
embarrassment or shame, involvement of trusted individuals, fear of retaliation, and distrust
of governmental authorities. According to an estimate derived from the Financial Industry
Regulatory Authority (FINRA), only 14 percent of financial fraud is formally reported to
government authorities.

Using this 14 percent reporting assumption, CSI estimates unreported financial fraud in Iowa
in 2025 at between $93 million and $573 million — on top of the $93 million in reported losses.
A more conservative scenario assuming a 50 percent reporting rate produces unreported losses
in the range of $93 million. These estimates suggest total (reported plus unreported) Iowa
fraud losses in 2025 could reach $666 million. The lack of reporting does not diminish the
economic impact; unreported losses still reduce consumer spending, confidence, and economic
activity.
"""
    },
    {
        "section": "Economic Impact Modeling",
        "tags": ["economic impact", "GDP", "jobs", "personal income", "REMI model", "Iowa 2025"],
        "text": """
CSI quantified the broader economic impact of financial fraud in Iowa using REMI's Tax PI+
input-output model for two scenarios:

Scenario 1 — Reported Losses Only:
- $225 million reduction in state GDP.
- $200 million reduction in statewide personal income.
- Loss of approximately 1,500 jobs.

Scenario 2 — Reported and Unreported Losses (14% Formal Reporting Rate):
- Up to a $1.5 billion reduction in state GDP.
- Up to a $1 billion reduction in statewide personal income.
- Loss of up to approximately 5,000 jobs.
- Loss of $46 million in state General Fund tax revenue.

The economic impact of financial fraud is transmitted through multiple channels: reduced
consumer spending, lower consumer confidence, higher interest rates as lenders price in
fraud risk, reduced loanable funds, lower capital investment, higher public-service costs,
and an erosion of community trust. These transmission channels amplify the direct dollar
loss into a broader contraction of economic activity.
"""
    },
    {
        "section": "About the Report and Methodology",
        "tags": ["methodology", "CSI", "data sources", "REMI", "Iowa Department of Public Safety"],
        "text": """
This report was authored by Thomas Young (Senior Economist, CSI) and Ben Murrey (Director
of Policy and Research, CSI Iowa) and published by Common Sense Institute in August 2025.
Common Sense Institute is a non-partisan research organization focused on Iowa's economy.

Data sources for the report include the Iowa Department of Public Safety, the FTC Consumer
Sentinel Network, and the FBI Internet Crime Complaint Center (IC3). Efforts were made to
eliminate double-counting across these three sources.

The economic impact model uses Regional Economic Models, Inc. (REMI) Tax PI+ — a widely
used input-output model — calibrated to Iowa's economy. Economic impact estimates cover
direct, indirect, and induced effects of fraud-driven reductions in consumer spending.
Methodology details and appendices containing underlying data are available in the full
published report.
"""
    },
]

csi_chunks = []
for i, c in enumerate(csi_raw_chunks, 1):
    csi_chunks.append(make_chunk(
        chunk_id   = f"csi_iowa_fraud_2025_{i:03d}",
        source_name= CSI_NAME,
        source_url = CSI_URL,
        pub_date   = CSI_DATE,
        section    = c["section"],
        topic_tags = c["tags"],
        text       = clean_text(c["text"])
    ))


# ─────────────────────────────────────────────────────────────────────────────
# Combine and write outputs
# ─────────────────────────────────────────────────────────────────────────────

all_chunks = ftc_chunks + exp_chunks + csi_chunks

# Full combined JSONL
write_jsonl(all_chunks, "/home/claude/rag_dataset_combined.jsonl")

# Per-source JSONL files
write_jsonl(ftc_chunks,  "/home/claude/rag_ftc_csn_2024.jsonl")
write_jsonl(exp_chunks,  "/home/claude/rag_ftc_explore_data.jsonl")
write_jsonl(csi_chunks,  "/home/claude/rag_csi_iowa_fraud_2025.jsonl")

# Manifest JSON
manifest = {
    "created": datetime.utcnow().isoformat() + "Z",
    "description": "RAG-ready text chunks from three financial-fraud datasets.",
    "total_chunks": len(all_chunks),
    "sources": [
        {
            "file": "rag_ftc_csn_2024.jsonl",
            "source_name": FTC_NAME,
            "source_url": FTC_URL,
            "publication_date": FTC_DATE,
            "chunk_count": len(ftc_chunks),
            "notes": "Aggregated consumer fraud report data. Raw CSV files downloadable at https://www.ftc.gov/system/files/ftc_gov/data/csn-data-book-2024-csv.zip"
        },
        {
            "file": "rag_ftc_explore_data.jsonl",
            "source_name": EXP_NAME,
            "source_url": EXP_URL,
            "publication_date": EXP_DATE,
            "chunk_count": len(exp_chunks),
            "notes": "Landing page and methodology for the FTC's Tableau-based interactive dashboards. Data updated quarterly."
        },
        {
            "file": "rag_csi_iowa_fraud_2025.jsonl",
            "source_name": CSI_NAME,
            "source_url": CSI_URL,
            "publication_date": CSI_DATE,
            "chunk_count": len(csi_chunks),
            "notes": "Full-text extraction from PDF report. Covers Iowa-specific fraud statistics, demographics, economic impact modelling."
        },
    ],
    "schema": {
        "id": "Unique chunk identifier (string)",
        "source_name": "Human-readable source title",
        "source_url": "Canonical URL of the source document",
        "publication_date": "ISO-8601 publication date",
        "section": "Sub-section heading within the source document",
        "topic_tags": "List of topical keyword tags for filtering/retrieval",
        "word_count": "Approximate word count of the text field",
        "text": "Cleaned, chunk-level text ready for embedding"
    }
}

with open("/home/claude/rag_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"  ✓  Wrote manifest → rag_manifest.json")

# ─────────────────────────────────────────────────────────────────────────────
# Quick QA summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n── QA Summary ──────────────────────────────────────")
for chunk in all_chunks:
    print(f"  [{chunk['id']}]  {chunk['section'][:50]:<52}  {chunk['word_count']:>4} words")

total_words = sum(c["word_count"] for c in all_chunks)
print(f"\n  Total chunks : {len(all_chunks)}")
print(f"  Total words  : {total_words:,}")
print(f"  Avg words/chunk : {total_words // len(all_chunks)}")
