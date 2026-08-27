# Incident Report — Storefront Unreachable

**When:** 2026-02-03, 02:00–04:00 local time

## Summary
Between 02:00 and 04:00 the platform was unreachable. Shoppers
could not open the storefront or complete checkout. Attempts to
load the catalogue timed out.

## Cause
A database connection pool was exhausted after a nightly batch
job failed to release connections.

## Resolution
The batch job was killed and the pool reset. Service recovered by
04:05. Orders queued during the window were processed once the
system was back.

## Follow-up
- Add an alert on pool saturation.
- Cap the batch job's connection usage.
