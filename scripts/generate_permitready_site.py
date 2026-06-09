#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_DATA_PATH = ROOT / "permitready" / "data" / "states.json"
STATE_PAGES_DIR = ROOT / "permitready" / "states"
LLMS_PATH = ROOT / "llms.txt"
SITEMAP_PATH = ROOT / "sitemap.xml"
VERIFY_SCRIPT_PATH = ROOT / "verify_permitready_sitemap.sh"
BASE_URL = "https://techsmog.com"
APP_STORE_URL = "https://apps.apple.com/us/app/permitready-dmv-practice/id6763930311"
UPDATE_DATE = date.today().isoformat()


def load_states() -> list[dict]:
    return json.loads(STATE_DATA_PATH.read_text())


def percent_text(state: dict) -> str:
    question_count = state["questionCount"]
    passing_score = state["passingScore"]
    passing_percentage = state["passingPercentage"]
    prefix = "~" if (passing_score * 100) % question_count else ""
    return f"{prefix}{passing_percentage}%"


def format_age(age: float) -> str:
    if int(age) == age:
        return str(int(age))
    return str(age).rstrip("0").rstrip(".")


def seo_name(state: dict) -> str:
    return state.get("seoName", state["name"])


def state_label(state: dict) -> str:
    return f"{seo_name(state)} {state['agencyShort']}"


def state_page_url(state: dict) -> str:
    return f"{BASE_URL}/permitready/states/{state['slug']}/"


def render_faq_answer(state: dict) -> str:
    answer = (
        f"The {state_label(state)} permit test has {state['questionCount']} questions. "
        f"You typically need at least {state['passingScore']} correct ({percent_text(state)}) to pass."
    )
    if state["timeLimitMinutes"]:
        answer += f" The official test is timed at {state['timeLimitMinutes']} minutes."
    if state["hasSplitTest"]:
        answer += " The official test also includes separate scored sections, so be ready for both sign and rule questions."
    answer += f" Always verify current requirements with the official {state['agencyLong']}."
    return answer


def render_overview_paragraphs(state: dict) -> tuple[str, str]:
    first = (
        f"PermitReady is a free iOS app that helps teens prepare for the {state_label(state)} permit test. "
        f"The exam has {state['questionCount']} questions; you need at least {state['passingScore']} correct "
        f"({percent_text(state)}) to pass."
    )
    if state["timeLimitMinutes"]:
        first += f" The official test is timed at {state['timeLimitMinutes']} minutes."
    if state["hasSplitTest"]:
        first += " The official test includes separate scored sections, so make sure you practice both sign recognition and road-rule questions."
    first += (
        f" The app covers {seo_name(state)} handbook topics like road signs, traffic laws, safe driving, and state-specific rules with practice quizzes, "
        "timed test simulations, and progress tracking."
    )

    second = (
        f"Minimum permit age in {seo_name(state)} is {format_age(state['minimumPermitAge'])}. "
        f"PermitReady also highlights important {seo_name(state)} licensing rules so you can study the test format and the steps that come after you pass."
    )
    return first, second


def render_requirements_list(state: dict) -> str:
    items = []
    for requirement in state["uniqueRequirements"]:
        items.append(f"<li>{escape(requirement)}</li>")
    return "\n".join(items)


def render_state_page(state: dict) -> str:
    state_title = f"{state_label(state)} Permit Test Practice"
    page_title = f"PermitReady - {state_title} 2026"
    meta_description = (
        f"Practice for the {state_label(state)} permit test with PermitReady. "
        f"Free iOS app with {state['questionCount']}-question practice quizzes, timed tests, progress tracking, and offline study."
    )
    og_description = (
        f"Free iOS app for {seo_name(state)} permit test prep. "
        f"{state['questionCount']}-question practice with state-specific content from official 2026 handbooks."
    )
    software_description = (
        f"Practice for the {state_label(state)} permit test with state-specific questions based on the 2026 official handbook. "
        f"The exam has {state['questionCount']} questions; you need at least {state['passingScore']} correct ({percent_text(state)}) to pass."
    )
    faq_answer = render_faq_answer(state)
    intro, secondary = render_overview_paragraphs(state)
    requirements_html = render_requirements_list(state)
    question_label = f"How many questions is the {seo_name(state)} permit test?"
    coverage_label = f"Does PermitReady cover the {state_label(state)} permit test?"
    offline_label = f"Can I study for the {seo_name(state)} permit test offline with PermitReady?"
    overview_title = f"{seo_name(state)} Permit Test Overview"
    current_page_url = state_page_url(state)

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TechSmog Apps", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "PermitReady", "item": f"{BASE_URL}/permitready/"},
            {"@type": "ListItem", "position": 3, "name": state_title, "item": current_page_url},
        ],
    }
    software_schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "PermitReady",
        "description": software_description,
        "applicationCategory": "EducationalApplication",
        "applicationSubCategory": "Driver Education",
        "operatingSystem": "iOS",
        "inLanguage": "en-US",
        "downloadUrl": APP_STORE_URL,
        "offers": [
            {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free version with ads"},
            {"@type": "Offer", "price": "4.99", "priceCurrency": "USD", "description": "Ad-free one-time purchase"},
        ],
        "author": {"@type": "Organization", "name": "TechSmog", "url": BASE_URL},
        "url": f"{BASE_URL}/permitready/",
        "image": f"{BASE_URL}/permitready/images/appstore.png",
    }
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question_label, "acceptedAnswer": {"@type": "Answer", "text": faq_answer}},
            {
                "@type": "Question",
                "name": coverage_label,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Yes. PermitReady includes state-specific practice questions for the {state_label(state)} permit test, "
                        f"based on the latest 2026 official driver handbook. It covers road signs, traffic laws, safe driving, parking, right of way, and state-specific rules."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": offline_label,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Yes. All {seo_name(state)} question banks are bundled in the PermitReady app, so you can study anywhere without an internet connection.",
                },
            },
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(page_title)}</title>
    <meta name="description" content="{escape(meta_description)}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="TechSmog">
    <meta name="application-name" content="PermitReady">
    <link rel="canonical" href="{escape(current_page_url)}">

    <!-- Open Graph -->
    <meta property="og:title" content="{escape(page_title)}">
    <meta property="og:description" content="{escape(og_description)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{escape(current_page_url)}">
    <meta property="og:image" content="{BASE_URL}/permitready/images/appstore.png">
    <meta property="og:image:width" content="1024">
    <meta property="og:image:height" content="1024">
    <meta property="og:site_name" content="TechSmog">
    <meta property="og:locale" content="en_US">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{escape(page_title)}">
    <meta name="twitter:description" content="{escape(og_description)}">
    <meta name="twitter:image" content="{BASE_URL}/permitready/images/appstore.png">

    <!-- Structured Data -->
    <script type="application/ld+json">
{json.dumps(breadcrumb_schema, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(software_schema, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
    </script>

    <link rel="stylesheet" href="/permitready/styles.css">
</head>
<body>
<!-- Generated by scripts/generate_permitready_site.py. -->
<header class="nav-header">
    <div class="container">
        <nav class="nav">
            <div class="logo"><a href="/permitready/">PermitReady</a></div>
            <ul class="nav-links">
                <li><a href="/permitready/">Home</a></li>
                <li><a href="/permitready/privacy.html">Privacy</a></li>
                <li><a href="/permitready/terms.html">Terms</a></li>
            </ul>
        </nav>
    </div>
</header>
<main>
    <section class="hero state-hero">
        <div class="container">
            <h1>{escape(state_title)}</h1>
            <p>{escape(intro)}</p>
            <a href="{APP_STORE_URL}" class="cta-button">Download PermitReady Free</a>
        </div>
    </section>

    <section class="features">
        <div class="container">
            <h2>{escape(overview_title)}</h2>
            <p>{escape(secondary)}</p>
            <ul>
                <li><strong>Question count:</strong> {state['questionCount']}</li>
                <li><strong>Passing score:</strong> {state['passingScore']} correct ({escape(percent_text(state))})</li>
                <li><strong>Minimum permit age:</strong> {escape(format_age(state['minimumPermitAge']))}</li>
                <li><strong>Time limit:</strong> {escape(str(state['timeLimitMinutes'])) + ' minutes' if state['timeLimitMinutes'] else 'No official time limit listed'}</li>
                <li><strong>Split test:</strong> {'Yes, separate scored sections apply' if state['hasSplitTest'] else 'No separate scored sections listed'}</li>
            </ul>

            <h2>Study Modes</h2>
            <ul>
                <li><strong>Practice Quiz:</strong> Untimed questions with explanations after every answer.</li>
                <li><strong>Practice Test:</strong> A state-sized simulation with {state['questionCount']} questions{f" and a {state['timeLimitMinutes']}-minute timer" if state['timeLimitMinutes'] else ''}.</li>
                <li><strong>Study by Category:</strong> Focus on road signs, traffic laws, safe driving, parking, right of way, and more.</li>
                <li><strong>Review Missed Questions:</strong> Revisit mistakes quickly and learn why the correct answer is right.</li>
                <li><strong>Progress Tracking:</strong> Monitor mastery, streaks, recent scores, and study history.</li>
                <li><strong>Offline-First:</strong> Study without a constant internet connection.</li>
            </ul>

            <h2>State-Specific Requirements</h2>
            <ul>
{requirements_html}
            </ul>

            <h2>Who This Is For</h2>
            <p>Great for teens preparing for a first learner's permit, parents helping a new driver study, and anyone retaking the knowledge test in {escape(seo_name(state))}.</p>
            <p><a href="/permitready/">Back to PermitReady main page</a> &middot; <a href="/permitready/#states-covered">View all supported states</a></p>
        </div>
    </section>

    <section class="features">
        <div class="container">
            <h2>Frequently Asked Questions</h2>
            <h3>{escape(question_label)}</h3>
            <p>{escape(faq_answer)}</p>
            <h3>{escape(coverage_label)}</h3>
            <p>Yes. PermitReady includes state-specific practice questions for the {escape(state_label(state))} permit test, based on the latest 2026 official driver handbook. It covers road signs, traffic laws, safe driving, parking, right of way, and state-specific rules.</p>
            <h3>Can I study for the {escape(seo_name(state))} permit test offline?</h3>
            <p>Yes. All {escape(seo_name(state))} question banks are bundled in the PermitReady app, so you can study anywhere without an internet connection.</p>
        </div>
    </section>

    <section class="disclaimer">
        <div class="container">
            <h2>Important Disclaimer</h2>
            <ul>
                <li>PermitReady is not affiliated with or endorsed by the {escape(state['agencyLong'])} or any government agency.</li>
                <li>Content is educational and based on publicly available handbook sources.</li>
                <li>Using this app does not guarantee passing the official permit exam.</li>
                <li>Verify current requirements with your state licensing agency before testing.</li>
            </ul>
        </div>
    </section>
</main>
<footer class="footer">
    <div class="container">
        <div class="footer-links">
            <a href="/permitready/">PermitReady Home</a>
            <a href="/permitready/privacy.html">Privacy Policy</a>
            <a href="/permitready/terms.html">Terms of Service</a>
        </div>
    </div>
</footer>
</body>
</html>
"""


def render_llms(states: list[dict]) -> str:
    lines = [
        "# TechSmog",
        "",
        "> iOS app developer building educational and productivity apps for iPhone and iPad. Primary product: PermitReady — a free driver's permit practice test app for teens across all 50 U.S. states plus Washington, DC.",
        "",
        "## PermitReady",
        "",
        "PermitReady is a free iOS app that helps teens study for their driver's permit (learner's permit) exam. It covers all 50 U.S. states plus Washington, DC with state-specific practice questions based on official 2026 driver handbooks. The app includes practice quiz mode, timed test simulation, study-by-category, progress tracking, and offline access.",
        "",
        "- Free with ads; optional $4.99 one-time purchase to remove ads",
        "- No subscriptions",
        "- Available on iPhone and iPad",
        f"- App Store: {APP_STORE_URL}",
        "",
        "## Key Pages",
        "",
        f"- [PermitReady — Features, Pricing & FAQ]({BASE_URL}/permitready/)",
    ]

    for state in states:
        lines.append(f"- [{state_label(state)} Permit Test Practice]({state_page_url(state)})")

    lines.extend(
        [
            f"- [Privacy Policy]({BASE_URL}/permitready/privacy.html)",
            f"- [Terms of Service]({BASE_URL}/permitready/terms.html)",
            "",
            "## Contact",
            "",
            "- Email: permitready@techsmog.com",
            f"- Website: {BASE_URL}",
            "",
        ]
    )
    return "\n".join(lines)


def sitemap_entry(url: str, lastmod: str, changefreq: str, priority: str) -> str:
    return f"""  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""


def render_sitemap(states: list[dict]) -> str:
    entries = [
        sitemap_entry(f"{BASE_URL}/", UPDATE_DATE, "monthly", "0.8"),
        sitemap_entry(f"{BASE_URL}/permitready/", UPDATE_DATE, "weekly", "1.0"),
        sitemap_entry(f"{BASE_URL}/permitready/privacy.html", "2025-01-01", "yearly", "0.3"),
        sitemap_entry(f"{BASE_URL}/permitready/terms.html", UPDATE_DATE, "yearly", "0.3"),
    ]
    for state in states:
        entries.append(sitemap_entry(state_page_url(state), UPDATE_DATE, "monthly", "0.9"))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"


def render_verify_script() -> str:
    return """#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python3 - <<'PY'
import json
import xml.etree.ElementTree as ET
from pathlib import Path

base = "https://techsmog.com"
states = json.loads(Path("permitready/data/states.json").read_text())
required = [
    f"{base}/permitready/",
    f"{base}/permitready/privacy.html",
    f"{base}/permitready/terms.html",
]
required.extend(f"{base}/permitready/states/{state['slug']}/" for state in states)

tree = ET.parse("sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = {elem.text for elem in tree.findall(".//sm:loc", ns)}

missing = [url for url in required if url not in locs]
if missing:
    for url in missing:
        print(f"MISSING: {url}")
    raise SystemExit("Verification failed.")

robots = Path("robots.txt").read_text()
for expected in (
    "Sitemap: https://techsmog.com/sitemap.xml",
    "Sitemap: https://techsmog.com/llms.txt",
):
    if expected not in robots:
        raise SystemExit(f"Verification failed: missing robots.txt reference: {expected}")

print("XML parse: OK")
print("Verification passed: all required PermitReady URLs and robots sitemap declarations are present.")
PY
"""


def main() -> None:
    states = load_states()

    for state in states:
        state_dir = STATE_PAGES_DIR / state["slug"]
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "index.html").write_text(render_state_page(state))

    LLMS_PATH.write_text(render_llms(states) + "\n")
    SITEMAP_PATH.write_text(render_sitemap(states))
    VERIFY_SCRIPT_PATH.write_text(render_verify_script())
    VERIFY_SCRIPT_PATH.chmod(0o755)

    print(f"Generated {len(states)} state pages.")
    print(f"Updated {LLMS_PATH.relative_to(ROOT)}")
    print(f"Updated {SITEMAP_PATH.relative_to(ROOT)}")
    print(f"Updated {VERIFY_SCRIPT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
