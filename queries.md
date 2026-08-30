# 10-Query Test File

Per Step 5 of the trainee guide: 5 keyword-style queries (words that
literally appear in the target document) and 5 paraphrase-style queries
(same meaning, different words). Run each with `search.py`, then fill in
the rank-1 document and score.

## Keyword-style (words appear literally in the target)

| # | Query | Expected top doc | Rank-1 doc (fill in) | Score (fill in) |
|---|---|---|---|---|
| 1 | `purchase order packaging materials` | vendor_purchase_order.txt | vendor_purchase_order.txt | 0.870 |
| 2 | `warehouse rent courier fees` | expense_report_q1.txt | expense_report_q1.txt | 0.888 |
| 3 | `wrong colour blue black exchange` | support_ticket_wrong_item.txt | support_ticket_wrong_item.txt | 0.856 |
| 4 | `database connection pool exhausted` | system_outage_report.md | system_outage_report.md | 0.848 |
| 5 | `annual leave request family trip` | leave_request_annual.txt | leave_request_annual.txt | 0.887 |

## Paraphrase-style (same meaning, no shared words with the target)

| # | Query | Expected top doc | Rank-1 doc (fill in) | Score (fill in) |
|---|---|---|---|---|
| 6 | `customer still has not sent the money` | payment_overdue_notice.txt | payment_overdue_notice.txt | 0.876 |
| 7 | `website down customers cannot access` | system_outage_report.md | system_outage_report.md | 0.841 |
| 8 | `supplier increasing prices` | rate_adjustment_notice.md | rate_adjustment_notice.md | 0.849 |
| 9 | `money reimbursed to buyer` | refund_confirmation.txt | refund_confirmation.txt | 0.822 |
| 10 | `employee resignation handover` | staff_departure_memo.txt | staff_departure_memo.txt | 0.855 |

## Screenshots

CLI output for each of the 10 queries, run against `intfloat/multilingual-e5-large`.

**#1 — `purchase order packaging materials`**
![query 1](images/Screenshot%202026-08-30%20at%2012.01.14.png)

**#2 — `warehouse rent courier fees`**
![query 2](images/Screenshot%202026-08-30%20at%2012.01.52.png)

**#3 — `wrong colour blue black exchange`**
![query 3](images/Screenshot%202026-08-30%20at%2012.02.22.png)

**#4 — `database connection pool exhausted`**
![query 4](images/Screenshot%202026-08-30%20at%2012.03.01.png)

**#5 — `annual leave request family trip`**
![query 5](images/Screenshot%202026-08-30%20at%2012.03.23.png)

**#6 — `customer still has not sent the money`**
![query 6](images/Screenshot%202026-08-30%20at%2012.03.53.png)

**#7 — `website down customers cannot access`**
![query 7](images/Screenshot%202026-08-30%20at%2012.04.56.png)

**#8 — `supplier increasing prices`**
![query 8](images/Screenshot%202026-08-30%20at%2012.05.15.png)

**#9 — `money reimbursed to buyer`**
![query 9](images/Screenshot%202026-08-30%20at%2012.05.34.png)

**#10 — `employee resignation handover`**
![query 10](images/Screenshot%202026-08-30%20at%2012.05.48.png)

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
