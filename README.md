# Tomato Current Affairs — SSC + RRB

A source-led Current Affairs feed and offline-capable HTML module for the Tomato learning app. The initial exam scope is **SSC and RRB only**.

## Accuracy comes before quantity

A wrong fact or answer key can cost exam marks. This project therefore uses an editorial publication gate, not a daily article quota:

- Prefer the issuing authority or another primary source (PIB, the relevant ministry/department, RBI, SEBI, ISRO, DRDO, statutory bodies, official sports federations/tournament organisers, and the organisation that issued an award or report).
- Cross-check key details against a second independent authoritative source wherever one is available. If only the issuing authority can confirm a fact, the editor must record a specific single-source justification.
- Check names, designations, dates, event dates, figures, units, rankings, award categories, report editions and the exact status of policies/schemes. A proposal, approval, launch and implementation are not interchangeable.
- Verify every MCQ's answer index and explanation separately. Each question must have exactly one defensible answer; distractors must be unambiguously wrong in the question's context.
- Reject rumours, opinion, ambiguous claims, contradictory reporting, weak sources and duplicate items. **Do not publish an item just to meet a target.**
- If something cannot be verified confidently, leave it out and record the uncertainty for editorial follow-up.

See [`EDITORIAL_STANDARD.md`](EDITORIAL_STANDARD.md) for the mandatory article and MCQ checks.

## Repository contents

- `app-module/current-affairs.html` — category and exam filters (SSC/RRB), search, bookmarks, MCQ practice, manual feed sync and offline cache.
- `content/current-affairs.json` — curated feed. It starts empty intentionally; no unverified or fabricated news is preloaded.
- `content/schema.json` — feed schema, including editorial approval metadata.
- `scripts/validate_feed.py` — publication gate for structure, dates, exam tags, source URLs, independent corroboration metadata, and per-question editorial sign-off.
- `.github/workflows/publish.yml` — validates the feed and publishes it to GitHub Pages on pushes to `main` or manual runs.
- `EDITORIAL_STANDARD.md` — detailed accuracy and MCQ checklist.

## Publish with GitHub Pages

1. Open repository **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Open **Actions** and enable workflows if GitHub asks.
4. Run **Validate and publish Current Affairs feed** once, or push a commit to `main`.
5. After the Pages workflow succeeds, the feed URL is:

   `https://abhishekdarsipati.github.io/tomato-current-affairs/content/current-affairs.json`

6. In Tomato, use **＋ Import HTML** to import `app-module/current-affairs.html`.
7. Open the Current Affairs topic, expand **Feed connection settings**, paste the feed URL, and save.

## Add a reviewed article

Edit `content/current-affairs.json` and commit the change. The GitHub Actions workflow runs the validator before deploying.

Each article requires an explicit `editorialReview` record. It must either include at least one independent, authoritative cross-check source on a different host from the primary source, or a specific `singleSourceJustification` explaining why the issuing authority is the only suitable verifier. Each MCQ also requires `reviewed: true` after its answer key and explanation have been checked.

Illustrative structure only — the example contains placeholders and is **not** a publishable news item:

```json
{
  "id": "sample-2026-11-08-001",
  "date": "2026-11-08",
  "eventDate": "2026-11-07",
  "category": "Science & Technology",
  "title": "Replace with a verified announcement headline",
  "summary": "Write an original, concise summary supported by the cited sources.",
  "sourceName": "Official issuing organisation",
  "sourceUrl": "https://official.example.gov/release",
  "examTags": ["SSC", "RRB"],
  "editorialReview": {
    "status": "approved",
    "reviewer": "editor",
    "checkedAt": "2026-11-08T10:00:00+05:30",
    "crossCheckSources": [
      {"sourceName": "Independent authoritative source", "sourceUrl": "https://independent.example.org/report"}
    ]
  },
  "questions": [
    {
      "question": "Replace with a fact-based question whose answer is explicit in the source.",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": 0,
      "explanation": "Explain why A is correct, using only facts supported by the source.",
      "reviewed": true
    }
  ]
}
```

`date` is the item's publication/coverage date; use `eventDate` when the event date differs and is relevant. MCQ `answer` is zero-based: A=0, B=1, C=2, D=3. Tag each item with `SSC`, `RRB`, or both by listing the applicable tags. Do not use a generic `Both` tag.

## What the automation does — and does not do

The workflow validates the feed's data structure and required review metadata, then deploys it. **It does not independently verify whether a news claim is true, whether sources are genuinely authoritative, or whether the keyed MCQ answer is correct.** Those are editorial responsibilities. Setting `status: "approved"` or `reviewed: true` is a human sign-off, not an AI or CI fact-check. GitHub Actions passing is not a guarantee of factual correctness.

This first version deliberately has no autonomous scraping or automatic fact publication. A trustworthy curated feed is better than a fast feed containing errors. A future collection assistant can propose candidate stories, but nothing should enter the live feed until it passes the editorial checks above.

## Offline behaviour

After a successful sync, the module caches the latest feed in IndexedDB and can display it offline. Initial sync and updates require internet. Bookmarks are local to the device. For Android WebView packaging, separately test network access and offline caching in the native build.

## Local validation

```bash
python scripts/validate_feed.py
```
