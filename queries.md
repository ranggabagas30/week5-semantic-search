# 10-Query Test File

Per Step 5 of the trainee guide: 5 keyword-style queries (words that
literally appear in the target document) and 5 paraphrase-style queries
(same meaning, different words). Run each with `search.py`, then fill in
the rank-1 document and score.

## Keyword-style (words appear literally in the target)

| # | Query | Expected top doc | Rank-1 doc (fill in) | Score (fill in) |
|---|---|---|---|---|
| 1 | `purchase order packaging materials` | vendor_purchase_order.txt | | |
| 2 | `warehouse rent courier fees` | expense_report_q1.txt | | |
| 3 | `wrong colour blue black exchange` | support_ticket_wrong_item.txt | | |
| 4 | `database connection pool exhausted` | system_outage_report.md | | |
| 5 | `annual leave request family trip` | leave_request_annual.txt | | |

## Paraphrase-style (same meaning, no shared words with the target)

| # | Query | Expected top doc | Rank-1 doc (fill in) | Score (fill in) |
|---|---|---|---|---|
| 6 | `customer still has not sent the money` | payment_overdue_notice.txt | | |
| 7 | `website down customers cannot access` | system_outage_report.md | | |
| 8 | `supplier increasing prices` | rate_adjustment_notice.md | | |
| 9 | `money reimbursed to buyer` | refund_confirmation.txt | | |
| 10 | `employee resignation handover` | staff_departure_memo.txt | | |

## Notes for the README

- Pick **3 of the 5 paraphrase queries** above (#6–10) and write them up as
  your "paraphrase wins" — target doc ranked #1 despite sharing no words
  with the query.
- Record the **score threshold** below which results stop being relevant
  for your corpus (Sunday lab: threshold hunt).
- Same 10 queries can be re-run against the `corpus/real/` set (see
  `compare_real_vs_generated.py`) to compare generated vs. real-document
  search quality — scores will likely compress and ranking get muddier on
  the longer, more overlapping real documents.
