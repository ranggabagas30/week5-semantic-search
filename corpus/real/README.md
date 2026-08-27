# Real corpus — generated-vs-real benchmark

20 **real** documents pulled from the public internet, kept separate from the
hand-authored `../` (generated) corpus so you can compare embedding-search
behaviour on clean planted data vs. messy real-world text.

## Source & licence
All files are plain-text extracts of Wikipedia articles (English, plus two
Indonesian: `faktur_id`, `logistik_id`), fetched via the MediaWiki
`extracts` API. Each file ends with a `Source:` line. Content is
**CC BY-SA**. Extracts are capped at ~8k chars.

Topics deliberately mirror the generated clusters so the comparison is fair:

| Generated (planted)            | Real (this folder)                          |
|--------------------------------|---------------------------------------------|
| invoice / payment overdue      | `invoice.md`, `accounts_receivable.txt`     |
| refund / damaged goods         | `product_return.txt`, `chargeback.txt`, `return_merchandise_authorization.txt` |
| support tickets                | `customer_service.md`                       |
| contract renewal               | `service_level_agreement.md`, `force_majeure.txt` |
| system outage                  | `downtime.txt`                              |
| staff departure                | `layoff.txt`, `letter_of_resignation.txt`   |
| shipping / PO                  | `third_party_logistics.txt`, `bill_of_lading.txt`, `purchase_order.txt`, `procurement.md`, `supply_chain.txt` |
| leave / onboarding             | `annual_leave.txt`, `onboarding.txt`        |
| Bahasa docs                    | `faktur_id.txt`, `logistik_id.txt`          |

## Why results will differ (the point of the exercise)
- **Generated** docs are short and each planted to *win* one paraphrase query
  with no shared words → crisp #1 hits, clean score gaps.
- **Real** docs are long, encyclopedic, and overlapping (invoice ⇄ accounts
  receivable ⇄ purchase order all discuss each other) → top-5 gets muddier,
  scores compress, and your relevance **threshold sits differently**. That gap
  is exactly what you write up.

## How to run the comparison
`index.py`'s `Path("corpus").glob("*.*")` is non-recursive, so it indexes the
generated set only and ignores this subfolder. To index the real set instead,
point the glob here and use a separate collection + db path, e.g.:

```python
# index_real.py — same as index.py but:
for n, p in enumerate(sorted(Path("corpus/real").glob("*.*"))):
    ...
client.add(collection_name="docs_real", documents=docs, metadata=meta, ids=ids)
```

Then run your 10 queries (`queries.md`) against both collections and compare
rank-1 doc + score side by side. Record: which set finds paraphrases more
reliably, and how the "relevance dies" threshold shifts between them.
