# week5-semantic-search

Embedded Qdrant + FastEmbed semantic search over a small anonymised business-ops
corpus (invoices, support tickets, HR memos, contracts, and Bahasa documents).
Built for Week 5 — Embeddings & Vector Search.

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install "qdrant-client[fastembed]"
python3 index.py          # embeds corpus/ into the 'docs' collection
```

## Corpus

22 anonymised documents in `corpus/` (15 `.txt`, 7 `.md`), covering finance,
support tickets, HR, IT/ops, procurement, and three Bahasa Indonesia documents
for the cross-language probe. `corpus/real/` holds a separate 20-document set
of real Wikipedia extracts on matching topics, used only for the optional
generated-vs-real benchmark below — it is not part of the main index.

## Search

```bash
python3 search.py <query words>
```

Returns the top 5 matches with cosine similarity score and source filename.

**Keyword-style query** (words appear literally in the target document):

```
$ python3 search.py purchase order packaging materials
0.885  vendor_purchase_order.txt
```

![keyword search, no filter](images/Screenshot%202026-08-27%20at%2017.01.52.png)

**Paraphrase-style query** (shares no words with the target document):

```
$ python3 search.py customer still has not sent the money
0.873  payment_overdue_notice.txt
```

![paraphrase search, no filter](images/Screenshot%202026-08-27%20at%2017.03.29.png)

## Metadata filter

```bash
python3 search.py --type <txt|md> <query words>
```

`--type` restricts results to one file extension via a Qdrant `FieldCondition`
on `metadata.type`.

**Exclusion proof** — same paraphrase query as above, filtered both ways:

`--type md` excludes the correct `.txt` answer entirely, surfacing only
`.md` files:

![--type md filter](images/Screenshot%202026-08-27%20at%2017.25.25.png)

`--type txt` restores it to rank 1, and every result is now `.txt`:

![--type txt filter](images/Screenshot%202026-08-27%20at%2017.25.45.png)

## Paraphrase wins

Three queries that share **no words** with their target document, yet the
target still ranks first:

| Query | Target doc | Score |
|---|---|---|
| `customer still has not sent the money` | `payment_overdue_notice.txt` | 0.873 |
| `supplier increasing prices` | `rate_adjustment_notice.md` | 0.851 |
| `employee resignation handover` | `staff_departure_memo.txt` | 0.875 |

(Full 10-query set — 5 keyword, 5 paraphrase — is in `queries.md`.)

## Threshold observation

Probing the index with queries about topics **absent from the corpus**
(volcanic eruptions, cake recipes, ancient Rome, dog training) still returns
a top hit — but the score caps out around **0.78–0.79**, versus 0.81–0.89 for
genuinely relevant matches:

```
volcanic eruption geology report    -> 0.789  team_outing_plan.md
recipe for chocolate cake           -> 0.781  team_outing_plan.md
history of ancient rome             -> 0.781  pengumuman_libur.md
how to train a dog                  -> 0.776  onboarding_checklist.md
```

For this corpus and model (`BAAI/bge-small-en`), **scores below ~0.79 are
noise, not relevance** — the model's cosine similarity floor for unrelated
text on a small corpus. This number is specific to this corpus/model pair and
would need to be re-calibrated for a different one.

## Optional: generated vs. real corpus benchmark

```bash
python3 index_real.py               # embeds corpus/real/ into 'docs_real'
python3 compare_real_vs_generated.py
```

Runs the same 10 queries against both collections side by side. The generated
corpus (short, deliberately planted paraphrase targets) produces crisper
top-1 hits and wider score gaps; the real corpus (longer, topically
overlapping Wikipedia extracts) compresses scores and produces muddier
rankings — illustrating why score thresholds must be calibrated per corpus,
not assumed from a demo dataset.
