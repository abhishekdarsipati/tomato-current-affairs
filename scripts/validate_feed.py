#!/usr/bin/env python3
"""Strict structural/editorial-metadata gate for Tomato Current Affairs.

This script DOES NOT fact-check claims or verify that sources are authoritative.
Human review recorded in editorialReview and each question's reviewed flag is mandatory.
"""
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

FEED = Path(__file__).resolve().parents[1] / "content" / "current-affairs.json"
ALLOWED_CATEGORIES = {
    "National Affairs", "International Affairs", "Economy",
    "Science & Technology", "Defence", "Environment", "Sports",
    "Awards & Appointments"
}
ALLOWED_EXAMS = {"SSC", "RRB"}


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_iso_datetime(value, path):
    if not isinstance(value, str):
        fail(f"{path} must be an ISO-8601 datetime string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{path} must be a valid ISO-8601 datetime")
    if parsed.tzinfo is None:
        fail(f"{path} must include a timezone (for example +05:30 or Z)")
    return parsed


def parse_https_url(value, path):
    if not isinstance(value, str):
        fail(f"{path} must be a URL string")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname or " " in value:
        fail(f"{path} must be a valid HTTPS URL")
    if parsed.hostname.lower() in {"example.com", "example.org", "example.net"}:
        fail(f"{path} contains a placeholder domain; replace it with the real source")
    return parsed


try:
    data = json.loads(FEED.read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"Cannot parse {FEED}: {exc}")

if not isinstance(data, dict):
    fail("feed root must be an object")
if data.get("schemaVersion") != 1:
    fail("schemaVersion must be 1")
generated_at = parse_iso_datetime(data.get("generatedAt"), "generatedAt")
if generated_at > datetime.now(timezone.utc).replace(microsecond=0):
    fail("generatedAt cannot be in the future")

articles = data.get("articles")
if not isinstance(articles, list):
    fail("articles must be an array")

seen_ids, seen_titles = set(), set()
question_count = 0
for i, article in enumerate(articles):
    p = f"articles[{i}]"
    if not isinstance(article, dict):
        fail(f"{p} must be an object")
    required = ("id", "date", "category", "title", "summary", "sourceName", "sourceUrl", "examTags", "editorialReview", "questions")
    for key in required:
        if key not in article:
            fail(f"{p} missing required field: {key}")

    article_id = article["id"]
    if not isinstance(article_id, str) or not article_id.strip():
        fail(f"{p}.id must be non-empty text")
    if article_id in seen_ids:
        fail(f"duplicate article id: {article_id}")
    seen_ids.add(article_id)

    try:
        date.fromisoformat(article["date"])
    except (TypeError, ValueError):
        fail(f"{p}.date must be YYYY-MM-DD")
    if article.get("eventDate") is not None:
        try:
            date.fromisoformat(article["eventDate"])
        except (TypeError, ValueError):
            fail(f"{p}.eventDate must be YYYY-MM-DD when supplied")

    if article["category"] not in ALLOWED_CATEGORIES:
        fail(f"{p}.category is not an allowed category")
    for key in ("title", "summary", "sourceName"):
        if not isinstance(article[key], str) or not article[key].strip():
            fail(f"{p}.{key} must be non-empty text")
    title_key = re.sub(r"\W+", " ", article["title"].casefold()).strip()
    if title_key in seen_titles:
        fail(f"duplicate/near-identical article title: {article['title']}")
    seen_titles.add(title_key)

    primary = parse_https_url(article["sourceUrl"], f"{p}.sourceUrl")
    tags = article["examTags"]
    if not isinstance(tags, list) or not tags or not all(isinstance(x, str) and x in ALLOWED_EXAMS for x in tags):
        fail(f"{p}.examTags must be a non-empty list containing only SSC and/or RRB")
    if len(set(tags)) != len(tags):
        fail(f"{p}.examTags contains duplicates")

    review = article["editorialReview"]
    if not isinstance(review, dict):
        fail(f"{p}.editorialReview must be an object")
    if review.get("status") != "approved":
        fail(f"{p}.editorialReview.status must be 'approved' after human editorial review")
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        fail(f"{p}.editorialReview.reviewer must identify the human reviewer")
    parse_iso_datetime(review.get("checkedAt"), f"{p}.editorialReview.checkedAt")

    cross_checks = review.get("crossCheckSources", [])
    if not isinstance(cross_checks, list):
        fail(f"{p}.editorialReview.crossCheckSources must be an array")
    independent_hosts = set()
    for j, source in enumerate(cross_checks):
        sp = f"{p}.editorialReview.crossCheckSources[{j}]"
        if not isinstance(source, dict) or not isinstance(source.get("sourceName"), str) or not source["sourceName"].strip():
            fail(f"{sp}.sourceName must be non-empty text")
        secondary = parse_https_url(source.get("sourceUrl"), f"{sp}.sourceUrl")
        if secondary.hostname.lower() == primary.hostname.lower():
            fail(f"{sp} must be hosted on a different domain from the primary source")
        independent_hosts.add(secondary.hostname.lower())
    single_source_reason = review.get("singleSourceJustification")
    if not independent_hosts and (not isinstance(single_source_reason, str) or len(single_source_reason.strip()) < 20):
        fail(f"{p}.editorialReview needs an independent cross-check source or a specific singleSourceJustification (at least 20 characters)")

    questions = article["questions"]
    if not isinstance(questions, list):
        fail(f"{p}.questions must be an array")
    seen_questions = set()
    for j, q in enumerate(questions):
        qp = f"{p}.questions[{j}]"
        if not isinstance(q, dict):
            fail(f"{qp} must be an object")
        for key in ("question", "options", "answer", "explanation", "reviewed"):
            if key not in q:
                fail(f"{qp} missing required field: {key}")
        if not isinstance(q["question"], str) or not q["question"].strip():
            fail(f"{qp}.question must be non-empty text")
        qkey = re.sub(r"\W+", " ", q["question"].casefold()).strip()
        if qkey in seen_questions:
            fail(f"{qp} duplicates another question in the same article")
        seen_questions.add(qkey)
        options = q["options"]
        if not isinstance(options, list) or len(options) != 4 or not all(isinstance(x, str) and x.strip() for x in options):
            fail(f"{qp}.options must contain exactly four non-empty strings")
        normalized_options = [re.sub(r"\W+", " ", x.casefold()).strip() for x in options]
        if len(set(normalized_options)) != 4:
            fail(f"{qp}.options must be unique")
        if isinstance(q["answer"], bool) or not isinstance(q["answer"], int) or q["answer"] not in range(4):
            fail(f"{qp}.answer must be an integer from 0 to 3 (A=0, B=1, C=2, D=3)")
        if not isinstance(q["explanation"], str) or len(q["explanation"].strip()) < 8:
            fail(f"{qp}.explanation must be meaningful non-empty text")
        if q["reviewed"] is not True:
            fail(f"{qp}.reviewed must be true only after the answer and explanation are checked by a human")
        question_count += 1

print(f"Feed structurally valid: {len(articles)} article(s), {question_count} individually reviewed MCQ(s).")
print("Reminder: this script does not fact-check claims, source authority, or answer-key truth.")
