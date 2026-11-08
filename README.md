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

Each article requires an explicit `editorialReview` record. It must include at least one authoritative cross-check source on a different host from the primary source, or a specific `singleSourceJustification` explaining why the issuing authority is the only suitable verifier. The reviewer must be identified truthfully: human review must name the human reviewer; owner-authorised AI review must identify the AI reviewer and state that it is not a human second-person check. Each MCQ requires `reviewed: true` only after its answer key and explanation have been checked individually.

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

The workflow validates the feed's data structure and required review metadata, then deploys it. **It does not independently verify whether a news claim is true, whether sources are genuinely authoritative, or whether the keyed MCQ answer is correct.** Those checks must be performed by the named reviewer. A review may be human or explicitly owner-authorised AI review, but AI approval must be labelled as AI review and never presented as human sign-off. GitHub Actions passing is not a guarantee of factual correctness.

This first version deliberately has no autonomous scraping or automatic fact publication. A trustworthy curated feed is better than a fast feed containing errors. A future collection assistant can propose candidate stories, but nothing should enter the live feed until it passes the editorial checks above.

## Offline behaviour

After a successful sync, the module caches the latest feed in IndexedDB and can display it offline. Initial sync and updates require internet. Bookmarks are local to the device. For Android WebView packaging, separately test network access and offline caching in the native build.

## Local validation

```bash
python scripts/validate_feed.py
```

## Current editorial review queue

The starter edition for **8 November 2026** is in [`review-queue/2026-11-08.json`](review-queue/2026-11-08.json), with its source trail and review history. Seven items and 20 MCQs have been published in the live feed following an AI-assisted source audit explicitly authorised by the repository owner. This is labelled as AI review, not human review. One conflicting-date story remains held. See [`review-queue/README.md`](review-queue/README.md).

## App sync behaviour

The importable HTML module uses this repository's live JSON feed by default. On first use it attempts an immediate sync. After that, it checks for updates once per India calendar day after **8:30 AM IST** when the module is open or reopened, with an additional 15-minute check while it remains open. It also checks when the app returns to the foreground or network connectivity returns. A manual **Sync** button remains available. The last successful feed is cached in IndexedDB for offline reading.

**Background limitation:** an imported HTML topic cannot reliably run JavaScript after Tomato Math is fully closed. If the user does not open/resume the module after the daily feed is published, the new content will download on the next open/resume (or manual Sync). This is not a guaranteed Android background job.
