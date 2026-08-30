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

## Model

Embeddings use **`intfloat/multilingual-e5-large`** (1024 dims, ~100
languages), chosen for the SEA/multilingual requirement — `BAAI/bge-m3` was
evaluated first but isn't in `fastembed`'s supported model catalogue (checked
against `fastembed==0.8.0`, the latest release; not in the dense, sparse, or
late-interaction model lists). E5 models require a `"query: "` / `"passage: "`
prefix on text at embedding time (handled in `index.py`/`index_real.py` for
documents and `search.py`/`compare_real_vs_generated.py` for queries) — the
prefix is embedding-only and never stored or displayed.

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
0.870  vendor_purchase_order.txt
```

**Paraphrase-style query** (shares no words with the target document):

```
$ python3 search.py customer still has not sent the money
0.876  payment_overdue_notice.txt
```

> Screenshots below are from the earlier `BAAI/bge-small-en` run (scores
> 0.885 / 0.873) — kept as evidence the CLI output format works, but the
> exact numbers shown in the images predate the model switch above and
> won't match a fresh run. Re-screenshot if you need images that match the
> current model exactly.

![keyword search, no filter](images/Screenshot%202026-08-27%20at%2017.01.52.png)
![paraphrase search, no filter](images/Screenshot%202026-08-27%20at%2017.03.29.png)

## Metadata filter

```bash
python3 search.py --type <txt|md> <query words>
```

`--type` restricts results to one file extension via a Qdrant `FieldCondition`
on `metadata.type`.

**Exclusion proof** — same paraphrase query as above, filtered both ways:

```
$ python3 search.py --type md customer still has not sent the money
0.787  maintenance_window_notice.md   # correct .txt answer excluded entirely

$ python3 search.py --type txt customer still has not sent the money
0.876  payment_overdue_notice.txt     # back to rank 1, all results now .txt
```

(Screenshots below predate the model switch — same staleness note as above.)

![--type md filter](images/Screenshot%202026-08-27%20at%2017.25.25.png)
![--type txt filter](images/Screenshot%202026-08-27%20at%2017.25.45.png)

## Paraphrase wins

Three queries that share **no words** with their target document, yet the
target still ranks first:

| Query | Target doc | Score |
|---|---|---|
| `customer still has not sent the money` | `payment_overdue_notice.txt` | 0.876 |
| `supplier increasing prices` | `rate_adjustment_notice.md` | 0.849 |
| `employee resignation handover` | `staff_departure_memo.txt` | 0.855 |

(Full 10-query set — 5 keyword, 5 paraphrase — is in `queries.md`.)

## Threshold observation

Probing the index with queries about topics **absent from the corpus**
(volcanic eruptions, cake recipes, ancient Rome, dog training) still returns
a top hit — but the score caps out around **0.75–0.78**, versus 0.82–0.89 for
genuinely relevant matches:

```
volcanic eruption geology report    -> 0.783  system_outage_report.md
recipe for chocolate cake           -> 0.765  office_lunch_menu.txt
history of ancient rome             -> 0.753  customer_thankyou_note.txt
how to train a dog                  -> 0.779  onboarding_checklist.md
```

For this corpus and model (`intfloat/multilingual-e5-large`), **scores below
~0.78 are noise, not relevance** — the model's cosine similarity floor for
unrelated text on a small corpus. This number is specific to this
corpus/model pair and would need to be re-calibrated for a different one; it
shifted from the ~0.79 floor measured under `BAAI/bge-small-en` since the
embedding space itself changed with the model.

## Cross-language probe (Bahasa query vs. English/Bahasa corpus)

The point of switching to a multilingual model: querying in Bahasa Indonesia
against a corpus that's mostly English.

```
$ query: "harga akan naik" (price will increase)
0.862  pemberitahuan_kenaikan_harga.txt   (Bahasa doc, same topic)
0.830  rate_adjustment_notice.md          (English doc, same topic — cross-lingual match)
0.803  keluhan_pengiriman.txt

$ query: "pengiriman terlambat" (shipping delay)
0.853  keluhan_pengiriman.txt             (Bahasa doc, same topic)
0.813  pengumuman_libur.md
0.812  pemberitahuan_kenaikan_harga.txt
0.810  support_ticket_shipping_delay.txt  (English doc, same topic — rank 4, above noise floor)
```

Result: the model genuinely bridges languages — the English equivalent
document scores meaningfully above the ~0.78 noise floor for both Bahasa
queries — but it isn't perfect. A same-language document on an unrelated
topic can still outrank the correct cross-lingual match (e.g. `pengumuman_libur.md`,
a holiday notice, outranked the shipping-delay ticket for `pengiriman terlambat`).
For production use on Bahasa/English mixed content, this would need
calibration per language pair rather than a single global threshold.

## Optional: generated vs. real corpus benchmark

```bash
python3 index_real.py               # embeds corpus/real/ into 'docs_real'
python3 compare_real_vs_generated.py
```

Runs the same 10 queries against both collections side by side:

```
query                                    generated (docs)                  real (docs_real)
purchase order packaging materials       0.870  vendor_purchase_order.txt  0.858  purchase_order.txt
warehouse rent courier fees              0.888  expense_report_q1.txt     0.780  bill_of_lading.txt
wrong colour blue black exchange         0.856  support_ticket_wrong_item 0.770  return_merchandise_auth...
database connection pool exhausted       0.848  system_outage_report.md  0.784  downtime.txt
annual leave request family trip         0.887  leave_request_annual.txt 0.850  annual_leave.txt
customer still has not sent the money    0.876  payment_overdue_notice   0.792  accounts_receivable.txt
website down customers cannot access     0.841  system_outage_report.md  0.793  downtime.txt
supplier increasing prices               0.849  rate_adjustment_notice   0.777  invoice.md
money reimbursed to buyer                0.822  refund_confirmation.txt  0.834  return_merchandise_auth...
employee resignation handover            0.855  staff_departure_memo.txt 0.815  letter_of_resignation.txt
```

The generated corpus (short, deliberately planted paraphrase targets)
produces crisper top-1 hits; the real corpus (longer, topically overlapping
Wikipedia extracts) generally scores lower and picks a *different but still
topically correct* document (e.g. `bill_of_lading.txt` and `downtime.txt`
instead of the generated set's exact matches) — illustrating why score
thresholds and even "correct" top-1 expectations must be calibrated per
corpus, not assumed from a demo dataset.
