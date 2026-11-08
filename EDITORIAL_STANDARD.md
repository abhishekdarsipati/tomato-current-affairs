# Editorial accuracy standard — Tomato Current Affairs

**Scope:** SSC and RRB examinations only.

**Core rule:** accuracy outranks speed, coverage and daily volume. If a fact or answer cannot be verified confidently, do not publish it.

## 1. Source hierarchy

1. Primary issuer / official source: PIB, Union or State ministry/department, RBI, SEBI, ISRO, DRDO, Election Commission, statutory/regulatory body, official sports federation or tournament organiser, or organisation that issued the award/report/appointment.
2. Independent or secondary authoritative publication: another government body, public broadcaster, recognised international organisation, or established news organisation with direct reporting and clear attribution.
3. Secondary explainers may help discover context but must not replace the primary source for exam-critical facts.

Never use an aggregator, coaching site, social-media post, anonymous claim or AI-generated summary as the only evidence for a factual claim.

## 2. Mandatory checks for every article

- Open the exact source URL and confirm that it supports the stated claim.
- Confirm the correct person/organisation, designation, spelling, location, date, number, unit, ranking, edition and category.
- Distinguish announcement date, publication date, event date and effective/implementation date.
- Distinguish a proposal, cabinet approval, notification, launch, commencement and actual implementation.
- For schemes, verify the exact ministry, beneficiaries, objective, amount/coverage and launch or effective date as relevant.
- For appointments, verify the exact post, person, appointing authority and tenure/effective date.
- For awards, verify recipient, award name, category, year/edition and awarding body.
- For reports/indexes, verify publisher, edition/year, subject, rank/score and comparison base. Never mix rank, score, position and percentage.
- For sports, verify event, edition, venue, winner/runner-up, record and date from the official organiser/federation where possible.
- Cross-check exam-critical facts with a second authoritative publication wherever one is available. If only the primary issuer can verify a detail, explain why in `editorialReview.notes`.
- Check whether the item is genuinely useful for SSC, RRB or both. Do not invent a claim about likely exam appearance.
- Search the existing feed for duplicate events and repeated facts before adding the item.

## 3. Mandatory checks for every MCQ

- The question tests one precise fact and contains enough context to avoid ambiguity.
- Exactly one option is correct in the stated context.
- Exactly three distractors are plausible but clearly incorrect; avoid overlapping, synonymous or time-dependent alternatives.
- The answer index is checked against the final option order: A=0, B=1, C=2, D=3.
- The explanation explicitly supports the keyed answer and adds no unsourced claims.
- Names, spelling, year, date, unit and wording match the cited source.
- Every question is checked separately; article-level review does not automatically approve all MCQs.

## 4. Publication and review labels

A delegated review may be performed by a human editor or, when explicitly authorised by the repository owner, by an AI research assistant.

- Human review must identify the human reviewer.
- AI review must identify the AI reviewer and say that it is AI-assisted; it must never be described as human-reviewed or as a guarantee of zero errors.
- AI-reviewed content must be based on opened/retrieved source material, not the source title alone. The reviewer should compare the primary source with a second authoritative publication where available and check each MCQ answer against the source text.
- If a source cannot be accessed, a claim is contradicted, the evidence is insufficient, or an answer remains ambiguous, hold or reject that item. Do not guess.
- Passing the automated validator is a structural pass only, not proof of factual correctness.

For the first edition, the repository owner explicitly delegated the review to ChatGPT. The edition's `editorialReview.reviewer` and `reviewMode` fields transparently record this as AI source review, not a human second-person check.

## 5. Corrections

When an error is found, remove or correct the item immediately, preserve an editor note describing the correction, re-check affected MCQs, and rerun validation. Do not silently leave a known incorrect answer in the live feed.

## 6. What code validation means

`scripts/validate_feed.py` checks the data contract and that editorial sign-off metadata is present. It cannot inspect the truth of claims, establish source authority, or prove the answer key correct. CI success is not a factual accuracy certificate.
