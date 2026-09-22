#!/usr/bin/env python3
"""Static checks for the GitHub Pages site. Stdlib only."""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://joshuaofisrael.github.io/orphan-well-intel"

PAGES = [
    "index.html",
    "how-it-works.html",
    "coverage.html",
    "pricing.html",
    "sample-digest.html",
    "market-map.html",
    "disclaimer.html",
    "contact.html",
    "404.html",
]

REQUIRED_IDS = [
    "SRC0000041612",
    "SRC0000041729",
    "SRC0000041735",
    "SRC0000041828",
    "Allen 7F",
    "DEP2700000015",
    "DEP2700000016",
    "DEP2700000019",
    "OOGM FS26-4",
    "OOGM FS26-7",
    "FDC-014-104713.1",
    "47-045-00004",
]

SOURCE_URLS = [
    "https://ohiobuys.ohio.gov/",
    "https://ohiobuys.ohio.gov/page.aspx/en/bpm/process_manage_extranet/57682",
    "https://dam.assets.ohio.gov/image/upload/ohiodnr.gov/documents/oil-gas/contractor/SOW-Allen_7F.pdf",
    "https://dep.wv.gov/bto/IHP/Pages/default.aspx",
    "https://www.bidexpress.com/businesses/15106/home",
    "https://www.bidexpress.com/businesses/65897/home?agency=true",
]

DISCLAIMER_PHRASES = [
    "not affiliated with any government agency",
    "does <strong>not</strong> provide legal, engineering, environmental, procurement, or bidding advice",
    "not substitutes",
    "Artificial intelligence is used",
    "you accept full responsibility",
    "information only",
    "does not submit bids",
    "Joshua Israel Ventures LLC",
]

BANNED = [
    "mailto:",
    "checkout.stripe.com",
    "buy.stripe.com",
    "official partner",
    "government-approved",
    "guaranteed award",
    "we will bid",
]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.hrefs = []
        self.styles = []
        self.scripts = []
        self.canonical = ""
        self.description = ""
        self.title_parts = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and "href" in ad:
            self.hrefs.append(ad["href"])
        if tag == "link":
            rel = ad.get("rel", "")
            if "stylesheet" in rel:
                self.styles.append(ad.get("href", ""))
            if rel == "canonical":
                self.canonical = ad.get("href", "")
        if tag == "script" and ad.get("src"):
            self.scripts.append(ad["src"])
        if tag == "meta" and ad.get("name") == "description":
            self.description = ad.get("content", "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)


def fail(errors, message):
    errors.append(message)


def main():
    errors = []
    titles = {}
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            fail(errors, f"missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(text)
        title = "".join(parser.title_parts).strip()
        if parser.h1 != 1:
            fail(errors, f"{name} has {parser.h1} h1 elements")
        if not title:
            fail(errors, f"{name} missing title")
        elif title in titles:
            fail(errors, f"duplicate title {title!r} on {name} and {titles[title]}")
        else:
            titles[title] = name
        if not parser.description:
            fail(errors, f"{name} missing meta description")
        if not parser.canonical.startswith(ORIGIN):
            fail(errors, f"{name} canonical {parser.canonical!r}")
        if "css/styles.css" not in parser.styles:
            fail(errors, f"{name} missing css/styles.css ({parser.styles})")
        for href in parser.styles:
            if href != "css/styles.css" and not href.startswith("https://fonts.googleapis.com/"):
                fail(errors, f"{name} unexpected stylesheet {href}")
        if "js/main.js" not in parser.scripts:
            fail(errors, f"{name} missing js/main.js")
        for phrase in (
            "Not affiliated with any government agency",
            "AI is used — verify official sources",
            "you accept full responsibility",
            "Joshua Israel Ventures LLC",
        ):
            if phrase not in text:
                fail(errors, f"{name} missing footer phrase: {phrase}")
        lower = text.lower()
        for banned in BANNED:
            if banned in lower:
                fail(errors, f"{name} contains banned token {banned}")
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
            fail(errors, f"{name} contains an email address")
        for href in parser.hrefs:
            if href.startswith("#") or href.startswith("mailto:"):
                continue
            if href.startswith("/") and not href.startswith("//"):
                fail(errors, f"{name} root-absolute link {href} breaks project Pages")
            if "://" in href:
                continue
            target = href.split("#", 1)[0].split("?", 1)[0]
            if target and not (ROOT / target).exists():
                fail(errors, f"{name} broken internal link {href}")

    pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
    for price in ("$49", "$149", "$299", "Coming soon", "Request access"):
        if price not in pricing:
            fail(errors, f"pricing.html missing {price}")

    sample = (ROOT / "sample-digest.html").read_text(encoding="utf-8")
    for token in REQUIRED_IDS + SOURCE_URLS:
        if token not in sample:
            fail(errors, f"sample digest missing {token}")
    if "Zero currently open KASTOW" not in sample:
        fail(errors, "sample digest missing Kentucky zero-open finding")
    if "Contractors must verify" not in sample:
        fail(errors, "sample digest missing verify notice")

    disclaimer = (ROOT / "disclaimer.html").read_text(encoding="utf-8")
    for phrase in DISCLAIMER_PHRASES:
        if phrase not in disclaimer:
            fail(errors, f"disclaimer missing {phrase!r}")

    contact = (ROOT / "contact.html").read_text(encoding="utf-8")
    if "Stripe is not connected" not in contact:
        fail(errors, "contact page does not say Stripe is disconnected")
    if 'type="email"' in contact:
        fail(errors, "contact page uses an email input that browsers may treat as a real address field")

    market = (ROOT / "market-map.html").read_text(encoding="utf-8")
    if market.count("<tr data-states=") != 40:
        fail(errors, "market map does not list 40 companies")
    if "does not mean eligibility" not in market:
        fail(errors, "market map missing eligibility warning")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for name in PAGES:
        if name == "404.html":
            continue
        loc = ORIGIN + "/" if name == "index.html" else f"{ORIGIN}/{name}"
        if loc not in sitemap:
            fail(errors, f"sitemap missing {loc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
        fail(errors, "robots.txt missing sitemap")
    if not (ROOT / ".nojekyll").exists():
        fail(errors, "missing .nojekyll")
    if not (ROOT / ".github/workflows/pages.yml").exists():
        fail(errors, "missing Pages workflow")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"ok — {len(PAGES)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
