# Editorial review queue

Files in this folder are **draft candidates only**. They are not served by the app and must not be copied into `content/current-affairs.json` until a human editor has approved every article and each MCQ answer.

## Current draft

- `2026-11-08.json` — seven selected SSC + RRB candidates covering 4–7 November 2026.
- It contains 20 draft MCQs, primary-source URLs, cross-check URLs, verification notes and one held item with conflicting dates.
- The status is `pending-human-approval`. The listed proposed answer keys have been checked against the cited source text by the research assistant but have **not** received human sign-off.

## Approval steps

1. Open each primary source and cross-check source.
2. Verify all names, dates, designations, figures, units, scheme periods and context.
3. Solve each MCQ independently; verify that exactly one option is correct and the explanation supports it.
4. If any conflict remains, leave the item in this queue or reject it. Do not guess.
5. Only after review, convert approved items to the live feed format in `content/current-affairs.json`, set `editorialReview.status` to `approved`, identify the human reviewer and set each approved question's `reviewed` to `true`.
6. Run `python scripts/validate_feed.py` and confirm the GitHub Actions workflow succeeds.

The validator checks data structure and editorial sign-off metadata. It does not prove that claims or answer keys are true.
