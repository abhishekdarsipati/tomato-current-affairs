# Editorial review queue

Files in this folder preserve source research and the review history for candidate editions. This folder is not consumed by the Tomato app; the live app reads only `content/current-affairs.json`.

## Edition: 8 November 2026

- `2026-11-08.json` contains seven SSC + RRB articles and 20 MCQs for the 4–7 November coverage window.
- The repository owner explicitly asked ChatGPT to perform the review and complete publication.
- The source audit was performed against primary releases and other authoritative publications. Each answer was checked against the cited source text and final option order.
- Review status is transparently recorded as AI review, not human second-person review. It is not a guarantee of zero errors.
- The seven approved-by-AI items and all 20 MCQs were published to `content/current-affairs.json`.
- One India–Myanmar exercise item remains held because the PIB and Myanmar International TV reports show different end dates. It must not be published until the issuing authorities clarify the duration.

## Corrections and escalation

If any discrepancy is found, correct or withdraw the live item promptly, update the queue with the correction note, re-check related MCQs and run the validator again. The validator checks structure and required review metadata only; it does not fact-check truth.
