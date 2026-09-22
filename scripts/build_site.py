#!/usr/bin/env python3
"""Generate the static Orphan Well Intel site from checked public-scan facts."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://joshuaofisrael.github.io/orphan-well-intel"

SRC_ODNR = "https://dam.assets.ohio.gov/image/upload/ohiodnr.gov/documents/oil-gas/orphanwell/Annual%20Reports/2025_OWP_Annual_Report.pdf"
SRC_PA = "https://files.dep.state.pa.us/aboutdep/Office%20of%20Administration/ContractsPortalFiles/ConstructionContracts/BidResults.pdf"
SRC_KYBLOG = "https://landairwater.me/2023/01/12/orphan-well-capping-reclaims-closed-part-of-wildlife-management-area-in-pulaski-county/"
SRC_ORVI = "https://ohiorivervalleyinstitute.org/first-tranche-of-federal-orphan-well-funds-out-the-door/"
SRC_WV = "https://dep.wv.gov/bto/IHP/Pages/default.aspx"
SRC_CC = "https://projects.constructconnect.com/details/5925188-kastow-orphan-well-package-christian-001&find_loc=KY-42240"

LABEL_ODNR = "ODNR 2025 Orphan Well Program Annual Report"
LABEL_PA = "PA DEP Bid Opening Results"
LABEL_KYBLOG = "KY EEC Land, Air & Water blog"
LABEL_ORVI = "Ohio River Valley Institute Initial Grant analysis (secondary)"
LABEL_WV = "WV DEP In-House Purchasing"
LABEL_CC = "ConstructConnect notice, as indexed"


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def ext(url: str, label: str) -> str:
    return (
        f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}'
        f'<span class="sr-only"> (opens in a new tab)</span></a>'
    )


NAV = [
    ("index.html", "Home", "home"),
    ("how-it-works.html", "How it works", "how"),
    ("coverage.html", "Coverage", "coverage"),
    ("pricing.html", "Pricing", "pricing"),
    ("sample-digest.html", "Sample digest", "sample"),
    ("contact.html", "Request access", "contact"),
]

FOOTER_LINKS = NAV + [
    ("market-map.html", "Market map", "market"),
    ("disclaimer.html", "Disclaimer", "disclaimer"),
]


def nav_html(active: str) -> str:
    items = []
    for href, label, key in NAV:
        current = ' aria-current="page"' if key == active else ""
        klass = ' class="nav-cta"' if key == "contact" else ""
        items.append(f'<li><a href="{href}"{klass}{current}>{label}</a></li>')
    return "\n".join(items)


def footer_links() -> str:
    items = []
    for href, label, _key in FOOTER_LINKS:
        items.append(f'<li><a href="{href}">{label}</a></li>')
    return "\n".join(items)


DISCLAIMER_BLOCK = """
<div class="disclaimer-text">
  <p><strong>Service name:</strong> Abandoned Oil Wells Project (orphan-well procurement intelligence)<br>
  <strong>Operating entity:</strong> Joshua Israel Ventures LLC</p>
  <p>Joshua Israel Ventures LLC provides automated public-record and procurement-monitoring information through this service. This service is <strong>not affiliated with any government agency</strong> and does <strong>not</strong> provide legal, engineering, environmental, procurement, or bidding advice.</p>
  <p>Information may be incomplete, delayed, changed, or inaccurate. AI-generated summaries are provided for convenience and are <strong>not substitutes</strong> for official solicitation documents. Contractors are responsible for reviewing official procurement materials and independently determining eligibility, requirements, deadlines, pricing, and compliance before bidding.</p>
  <p><strong>Artificial intelligence is used</strong> to discover, extract, organize, and summarize publicly available materials. By using this service, you acknowledge that AI systems can make mistakes (including omissions, misreads, delayed updates, and incorrect summaries), and <strong>you accept full responsibility</strong> for verifying every material fact against the official government source before relying on it for any business, bidding, or compliance decision.</p>
  <p>This product sells <strong>information only</strong>. It does not submit bids, negotiate with agencies, determine legal eligibility, certify qualifications, recommend bid prices, or act as your authorized representative.</p>
</div>
""".strip()


def chrome(title, description, canonical, active, body, json_ld=""):
    ld = ""
    if json_ld:
        ld = f'<script type="application/ld+json">{json_ld}</script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="Joshua Israel Ventures LLC">
  <meta name="theme-color" content="#122333">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:locale" content="en_US">
  <meta property="og:site_name" content="Orphan Well Intel">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&amp;family=Public+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet">
  {ld}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <div class="trust-bar">Information only · Not affiliated with any government agency · AI is used — verify official sources · <a href="disclaimer.html">Read the disclaimer</a></div>
  <header class="site-header">
    <div class="wrap header-row">
      <a class="brand" href="index.html">
        <svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
          <rect x="1" y="1" width="30" height="30" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <circle cx="16" cy="16" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <circle cx="16" cy="16" r="1.6" fill="currentColor"/>
          <path d="M16 4.2v3.6M16 24.2V27.8M4.2 16h3.6M24.2 16H27.8" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span class="brand-text">
          <span class="brand-name">Orphan Well Intel</span>
          <span class="brand-sub">Joshua Israel Ventures LLC</span>
        </span>
      </a>
      <input id="nav-toggle" class="nav-toggle-input" type="checkbox">
      <label for="nav-toggle" class="nav-toggle"><span class="nav-open-label">Menu</span><span class="nav-close-label">Close</span></label>
      <nav id="site-nav" class="site-nav" aria-label="Primary">
        <ul>
          {nav_html(active)}
        </ul>
      </nav>
    </div>
  </header>
  <main id="main">
    {body}
  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <p class="footer-brand">Orphan Well Intel</p>
        <p>Abandoned Oil Wells Project<br>Joshua Israel Ventures LLC</p>
        <ul class="footer-trust">
          <li>Not affiliated with any government agency</li>
          <li>AI is used — verify official sources</li>
          <li>Information only. No bidding. No brokerage. No percentage of a contract.</li>
        </ul>
      </div>
      <nav aria-label="Footer">
        <ul class="footer-links">
          {footer_links()}
        </ul>
      </nav>
    </div>
    <div class="wrap">
      <p class="footer-disclaimer">Joshua Israel Ventures LLC provides automated public-record and procurement-monitoring information. This service is not affiliated with any government agency and does not provide legal, engineering, environmental, procurement, or bidding advice. AI is used — verify official sources. Artificial intelligence can omit, misread, or mis-summarize public records, and you accept full responsibility for checking every material fact against the official government source before any bidding or compliance decision. <a href="disclaimer.html">Full disclaimer and terms</a>.</p>
      <p class="footer-meta">© 2026 Joshua Israel Ventures LLC. Information only. Public site copy prepared 22 September 2026.</p>
    </div>
  </footer>
  <script src="js/main.js"></script>
</body>
</html>
"""


def page_hero(kicker, h1, lede):
    return f"""
    <header class="page-hero">
      <div class="wrap">
        <p class="kicker">{kicker}</p>
        <h1>{h1}</h1>
        <p class="lede">{lede}</p>
      </div>
    </header>
    """


FAQ = [
    (
        "Is this affiliated with a government agency?",
        "No. Joshua Israel Ventures LLC is a private company. The service is not affiliated with any government agency, including the Ohio Department of Natural Resources, the West Virginia Department of Environmental Protection, the Kentucky Energy and Environment Cabinet, the Pennsylvania Department of Environmental Protection, the Pennsylvania Department of Conservation and Natural Resources, the U.S. Department of the Interior, or the Bureau of Land Management.",
    ),
    (
        "Will you bid for me, or take a percentage of the contract?",
        "No. The product is information only. It does not submit bids, sign documents, negotiate with agencies, broker work, coordinate bids, or charge a percentage of a contract or a success fee.",
    ),
    (
        "Can I treat an alert as a substitute for the solicitation?",
        "No. Artificial intelligence is used to discover, extract, organize, and summarize publicly available materials. AI systems can make mistakes, including omissions, misreads, delayed updates, and incorrect summaries. You accept full responsibility for verifying every material fact against the official government source before relying on it for any business, bidding, or compliance decision.",
    ),
    (
        "Do you decide whether my company is eligible?",
        "No. The service does not determine legal eligibility, certify qualifications, or recommend a bid price. You review the official materials and make those decisions. A name on the market map is not a finding that the company may bid.",
    ),
    (
        "Which notices are in scope?",
        "Orphan, abandoned, idle, and legacy oil and gas well plugging and abandonment; site reclamation and restoration; methane mitigation tied to those wells; and associated excavation, access roads, and waste handling when they are part of those procurements. Also RFQs, RFIs, prequalification notices, amendments, cancellations, and awards for that work. Unrelated oilfield jobs that merely mention wells are out of scope.",
    ),
    (
        "Why do some deadlines have no time zone?",
        "If the public source did not state a time zone, the digest says the time zone was not stated. It does not invent one. Confirm the clock time with the agency before you rely on it.",
    ),
]


def faq_html():
    blocks = []
    for question, answer in FAQ:
        blocks.append(f"<h3>{esc(question)}</h3><p>{esc(answer)}</p>")
    return "\n".join(blocks)


def faq_ld():
    entities = []
    for question, answer in FAQ:
        entities.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        )
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": entities,
        },
        ensure_ascii=False,
    )


COMPANIES = [
    ("B&B Oilfield Service, Inc.", ["OH"], "Columbiana #11/#12/#13 LOTP; Columbiana-Knox #5A", LABEL_ODNR, SRC_ODNR, None),
    ("Bull Run Resources LLC", ["PA"], "OOGM FS25-3 (apparent low bid)", LABEL_PA, SRC_PA, None),
    ("Chavez Well Services, LLC", ["OH"], "Washington #25 / #32 LOTP", LABEL_ODNR, SRC_ODNR, None),
    ("Chipco, LLC", ["OH"], "Noble #19 - FY2025-31 (LOTP)", LABEL_ODNR, SRC_ODNR, None),
    ("Cline Oil Inc.", ["PA"], "OOGM 24-2 (apparent low bid); OOGM 25-1 (2nd); OOGM 26-1 (3rd)", LABEL_PA, SRC_PA, None),
    ("CMC Inc.", ["KY"], "Rockcastle River WMA (Pulaski County); multiple Initial Grant packages", LABEL_KYBLOG, SRC_KYBLOG, None),
    ("Coastal Drilling East, LLC", ["WV", "PA"], "Federal Initial Grant Regions 2 and 7; OOGM 23-1 / 23-3 / FS22 packages (bidder)", LABEL_ORVI, SRC_ORVI, None),
    ("CSR Services, LLC", ["OH", "PA"], "Construction Manager at Risk — Initial Grant; Phase I Formula Grant CMR", LABEL_ODNR, SRC_ODNR, "https://www.csrservicesllc.com/"),
    ("Dallas-Morris Drilling, Inc.", ["PA"], "OOGM FS25-8 (apparent low bid); OOGM 26-1 / 25-2 / 25-1 / FS24-2 / 24-1 / 23-3 / FS22-15", LABEL_PA, SRC_PA, "http://www.dallas-morris.com/"),
    ("Eagle Well Service Inc.", ["WV", "KY"], "Steerman Well Plugging Project; Rockcastle River WMA orphan wells (sub under CMC Inc.)", LABEL_KYBLOG, SRC_KYBLOG, None),
    ("FD Clean Energy, LLC", ["OH"], "Mercer #2", LABEL_ODNR, SRC_ODNR, None),
    ("HAD Inc.", ["OH"], "Ashland #6; Knox #8", LABEL_ODNR, SRC_ODNR, None),
    ("Hagen Well Service, LLC", ["OH"], "Coshocton #7; Holmes #3/#4; Medina #21", LABEL_ODNR, SRC_ODNR, None),
    ("Harley Oil Field Services LLC", ["OH"], "Ashland #5; Medina #16; Medina #F1 (T&M) Initial Grant sub-awards", LABEL_ODNR, SRC_ODNR, None),
    ("Howard Drilling, LLC", ["PA"], "OOGM 23-1 (apparent low bid); OOGM D25-1 / 25-1 / 24-1 (bidder)", LABEL_PA, SRC_PA, None),
    ("Huffman-Bowers, Inc.", ["OH"], "Meigs #5 - FY2026-4 (LOTP)", LABEL_ODNR, SRC_ODNR, None),
    ("Huwer Drilling LLC", ["OH"], "Logan #3; Warren #1 Emergency", LABEL_ODNR, SRC_ODNR, None),
    ("Hydrocarbon Well Services, Inc.", ["OH", "PA", "WV"], "Muskingum #8; Vinton #4/#5/#6; Pickaway #1; Richland #4; Law", LABEL_ODNR, SRC_ODNR, None),
    ("Indiana Petroleum Contractors", ["KY"], "Initial Grant orphan well packages", LABEL_ORVI, SRC_ORVI, None),
    ("J.T. Plus Well Services, LLC", ["OH"], "Meigs #2 - FY2025-24 (LOTP)", LABEL_ODNR, SRC_ODNR, None),
    ("Keystone Wireline, Inc. / Keystone Well Services", ["PA", "OH"], "OOGM FS26-1 (apparent low bid); OOGM FS25-4 / FS25-6 / FS24-5 / D25-1 (apparent low bids)", LABEL_PA, SRC_PA, "https://keystonewellservices.com/"),
    ("Knox Energy, Inc.", ["OH"], "Licking #13 / #15 LOTP", LABEL_ODNR, SRC_ODNR, None),
    ("M&A Energy Services, LLC", ["PA", "WV"], "Dinsmore Well Plugging Project; OOGM FS26-1 / FS25-4 / FS25-6 / FS25-2 / FS25-1 (bidder)", LABEL_WV, SRC_WV, None),
    ("MH Oilfield Service LLC", ["OH"], "Muskingum #7/#9/#11; Exploratory 2024 SE (change order)", LABEL_ODNR, SRC_ODNR, None),
    ("Moore Well Services, Inc.", ["OH"], "Cuyahoga #31 Emergency; Cuyahoga #27F / #28F; Wayne #3F", LABEL_ODNR, SRC_ODNR, None),
    ("Next LVL Energy, LLC", ["PA", "OH", "WV"], "Federal Plugging Contract - Burning Springs Group A; federal jumbo packages Regions 1, 3 and 6", LABEL_WV, SRC_WV, "https://www.div.energy/operations/next-lvl-energy-2/"),
    ("North Wind Response and Reclamation, LLC (also North Wind Site Services, LLC on older PA tabs)", ["WV", "PA"], "Tyler Co. Well Plugging Package - Group A; Tyler Co. Well Plugging Package - Group B", LABEL_WV, SRC_WV, None),
    ("NuPointe Energy, LLC", ["OH"], "Carroll #7; Columbiana #7/#9; Exploratory 2026 SE; Mercer/Ha", LABEL_ODNR, SRC_ODNR, None),
    ("Penn Mechanical Group", ["PA"], "OOGM FS25-1 (apparent low bid); multiple OOGM packages as 2nd/3rd bidder", LABEL_PA, SRC_PA, None),
    ("Plants & Goodwin, Inc.", ["PA", "OH", "WV", "NY"], "Ashtabula #12; Ashtabula #13", LABEL_ODNR, SRC_ODNR, "https://plantsgoodwin.com/"),
    ("PVR Well Service, LLC", ["OH"], "Knox #6", LABEL_ODNR, SRC_ODNR, None),
    ("R & J Well Service, Inc.", ["WV", "OH"], "Day #1 / Gideon #1 and other FY2024 OOG awards; S.R. Hill Well Plugging Project", LABEL_WV, SRC_WV, None),
    ("R & R Well Service, LLC", ["WV"], "Lewis Co. Group A - South Well Plugging Package; Lewis Co. Group B - South Well Plugging Package", LABEL_WV, SRC_WV, None),
    ("Rock Hard Energy LLC / Rock Hard Energy Services, Inc.", ["OH"], "Washington #24 / #28 LOTP", LABEL_ODNR, SRC_ODNR, None),
    ("Ronald A. Gibson & Associates, Inc.", ["OH"], "Multiple Cuyahoga/Lorain LOTP single-well packages", LABEL_ODNR, SRC_ODNR, None),
    ("Second Oil Ltd.", ["OH"], "Exploratory 2026 NW; Hancock #7 Emergency; Wood #9", LABEL_ODNR, SRC_ODNR, None),
    ("Unlimited Energy Services LLC", ["WV"], "Haught #1 Well Plugging Project API# 47-085-00273; Mcquain B-45-1 Well Plugging Project", LABEL_WV, SRC_WV, None),
    ("Womac Brothers, Inc. / Womack Brothers LLC", ["KY", "OH"], "Initial Grant packages; Wood #8F", LABEL_ORVI, SRC_ORVI, None),
    ("WPS Environmental", ["WV"], "Federal Initial Grant Regions 4 and 5", LABEL_ORVI, SRC_ORVI, None),
    ("Young's Well Service, LLC", ["KY"], "KASTOW - Orphan Well Package - Christian #001", LABEL_CC, SRC_CC, None),
]


def assert_counts():
    assert len(COMPANIES) == 40
    counts = {"OH": 0, "WV": 0, "KY": 0, "PA": 0}
    for _name, states, *_rest in COMPANIES:
        for state in states:
            if state in counts:
                counts[state] += 1
    assert counts == {"OH": 25, "WV": 11, "KY": 5, "PA": 13}, counts


def home():
    ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Orphan Well Intel",
            "url": ORIGIN + "/",
            "description": "Public-record procurement intelligence for orphan and abandoned well plugging.",
            "publisher": {
                "@type": "Organization",
                "name": "Joshua Israel Ventures LLC",
                "url": ORIGIN + "/",
            },
        },
        ensure_ascii=False,
    )
    body = """
    <section class="hero">
      <div class="wrap hero-grid">
        <div>
          <p class="kicker">Orphan well plugging bid alerts</p>
          <h1>Orphan well plugging bid alerts from public procurement records.</h1>
          <p class="hero-lead">Joshua Israel Ventures LLC watches official notices for orphan, abandoned, idle, and legacy oil and gas well plugging and site reclamation in Ohio, West Virginia, Kentucky, and Pennsylvania. Subscribers get a digest or an alert. They still open the official solicitation and decide whether to bid.</p>
          <div class="actions">
            <a class="btn" href="contact.html#request-access">Request access <span class="soon">Coming soon</span></a>
            <a class="btn btn-secondary" href="sample-digest.html">Read the 22 Sep 2026 sample</a>
          </div>
          <p class="fine">Orphan Well Intel is the public site for the Abandoned Oil Wells Project. Information only. No bidding, no brokerage, and no percentage of a contract.</p>
        </div>
        <aside class="bulletin" aria-label="Sample scan snapshot">
          <p class="bulletin-kicker">Frozen sample · not a live feed</p>
          <h2>First public scan</h2>
          <p class="bulletin-date">22 September 2026</p>
          <div class="stat-row cols-3">
            <div class="stat"><span class="stat-num">11</span><span class="stat-label">Open or apparently open</span></div>
            <div class="stat"><span class="stat-num">3</span><span class="stat-label">States with an item that day</span></div>
            <div class="stat"><span class="stat-num">0</span><span class="stat-label">Confirmed open KASTOW in KY</span></div>
          </div>
          <ol class="mini-list">
            <li><time datetime="2026-09-24">24 Sep</time><span class="st">OH</span><span>Washington 23F</span></li>
            <li><time datetime="2026-09-28">28 Sep</time><span class="st">WV</span><span>Lewis Group C</span></li>
            <li><time datetime="2026-09-28">28 Sep</time><span class="st">WV</span><span>Adkins #2</span></li>
            <li><time datetime="2026-10-01">1 Oct</time><span class="st">PA</span><span>Cornplanter SF</span></li>
          </ol>
          <p><a href="sample-digest.html">Open the sample digest</a></p>
        </aside>
      </div>
    </section>
    <nav class="state-index" aria-label="Launch states">
      <a href="coverage.html#ohio"><span class="state-code">OH</span><strong>Ohio</strong><span>ODNR orphan well program and OhioBuys</span></a>
      <a href="coverage.html#west-virginia"><span class="state-code">WV</span><strong>West Virginia</strong><span>DEP plugging pages and in-house purchasing</span></a>
      <a href="coverage.html#kentucky"><span class="state-code">KY</span><strong>Kentucky</strong><span>EEC program pages and VSS / KASTOW watch</span></a>
      <a href="coverage.html#pennsylvania"><span class="state-code">PA</span><strong>Pennsylvania</strong><span>DEP OOGM and DCNR listings on BidExpress</span></a>
    </nav>
    <section class="section">
      <div class="wrap">
        <p class="kicker">For plugging contractors</p>
        <h2>The notice is public. Finding it on time is the job.</h2>
        <div class="grid-3">
          <article class="card">
            <h3>Four portals, one trade</h3>
            <p>Solicitations sit on OhioBuys, West Virginia purchasing pages, Kentucky VSS, BidExpress, and the oil-and-gas program sites behind them. A weekly pass of each one is easy to miss when a package is re-offered.</p>
          </article>
          <article class="card">
            <h3>Deadlines that do not explain themselves</h3>
            <p>Some clocks state UTC. Others state a time and no time zone. When the source is silent or the sources disagree, the digest says so instead of guessing a zone.</p>
          </article>
          <article class="card">
            <h3>You still price the work</h3>
            <p>The service points at the public record. It does not tell you what to bid, whether you qualify, or how to engineer the plug. That judgment stays with the contractor.</p>
          </article>
        </div>
      </div>
    </section>
    <section class="section section-alt">
      <div class="wrap">
        <p class="kicker">How a notice moves</p>
        <h2>Public record, then a digest you can check.</h2>
        <ol class="steps">
          <li><span class="step-num">01</span><h3>Public data</h3><p>Official portals, program pages, bid calendars, award notices, and bid tabs.</p></li>
          <li><span class="step-num">02</span><h3>Extract</h3><p>Identifiers, agencies, places, stated well counts, deadlines, and document links. Missing fields stay missing.</p></li>
          <li><span class="step-num">03</span><h3>Organize</h3><p>Source facts kept apart from summary notes. Conflicts flagged for a human to verify.</p></li>
          <li><span class="step-num">04</span><h3>Match</h3><p>Compared with the states and project types you asked to watch.</p></li>
          <li><span class="step-num">05</span><h3>Alerts</h3><p>A digest or alert with the source link and the standing disclaimer.</p></li>
        </ol>
        <p style="margin-top:1rem"><a href="how-it-works.html">See the full path</a></p>
      </div>
    </section>
    <section class="section">
      <div class="wrap">
        <p class="kicker">Subscriptions</p>
        <h2>Three ways to read the same public record.</h2>
        <div class="grid-3">
          <article class="tier">
            <h3>Basic</h3>
            <p class="price">$49 <span>/ month</span></p>
            <p>Weekly multi-state digest for Ohio, West Virginia, Kentucky, and Pennsylvania.</p>
          </article>
          <article class="tier">
            <h3>Professional</h3>
            <p class="price">$149 <span>/ month</span></p>
            <p>Daily alerts, a weekly report, and a watch list limited to the states and project types you choose inside current coverage.</p>
          </article>
          <article class="tier">
            <h3>Premium</h3>
            <p class="price">$299 <span>/ month</span></p>
            <p>Immediate matching alerts, historical award intelligence from public records, and customized monitoring.</p>
          </article>
        </div>
        <p style="margin-top:1rem"><a class="btn btn-dark" href="pricing.html">Compare tiers</a></p>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <p class="kicker">Hard limits</p>
        <h2>Information on the table. Nothing else.</h2>
        <ul class="limit-list">
          <li>We do not submit bids, sign bid documents, or act as your authorized representative.</li>
          <li>We do not negotiate with agencies or broker plugging work.</li>
          <li>We do not charge a percentage of a contract or a success fee.</li>
          <li>We do not give legal, engineering, environmental, or procurement advice.</li>
          <li>We do not certify licensing, bonding, insurance, or eligibility.</li>
          <li>We do not recommend a bid price.</li>
          <li>We are not affiliated with any government agency.</li>
          <li>AI is used — verify official sources. Summaries are not the solicitation.</li>
        </ul>
      </div>
    </section>
    <section class="section">
      <div class="wrap prose">
        <p class="kicker">A worked example</p>
        <h2>The first scan is on the site so you can judge the format.</h2>
        <p>The <a href="sample-digest.html">22 September 2026 sample digest</a> lists 11 solicitations the scan treated as open or apparently open, each with the agency, the deadline as recorded, and a source URL. Kentucky had no confirmed open KASTOW solicitation that day. Several Ohio and West Virginia deadlines do not state a time zone. Contractors must verify every line. The sample is frozen; it is not updated when a package is amended or awarded.</p>
        <p>A separate <a href="market-map.html">market map</a> names 40 companies that appear in public award notices, bid tabs, or program write-ups. Appearance on that list is not eligibility to bid.</p>
        <p><a class="btn btn-dark" href="contact.html#request-access">Request access</a></p>
      </div>
    </section>
    """
    # drop the inline style by rewriting that one paragraph class — fix below in post? 
    # I'll leave a class instead. Replace style attributes.
    body = body.replace(
        '<p style="margin-top:1rem"><a href="how-it-works.html">See the full path</a></p>',
        '<p class="section-follow"><a href="how-it-works.html">See the full path</a></p>',
    ).replace(
        '<p style="margin-top:1rem"><a class="btn btn-dark" href="pricing.html">Compare tiers</a></p>',
        '<p class="section-follow"><a class="btn btn-dark" href="pricing.html">Compare tiers</a></p>',
    )
    return chrome(
        "Orphan Well Plugging Bid Alerts for OH, WV, KY, and PA | Joshua Israel Ventures LLC",
        "Public digests and alerts for orphan, abandoned, idle, and legacy well plugging and site reclamation in Ohio, West Virginia, Kentucky, and Pennsylvania. Information only. Not a government agency.",
        ORIGIN + "/",
        "home",
        body,
        ld,
    )


def how():
    body = page_hero(
        "Method",
        "How the monitoring works",
        "Five steps from a public page to a digest. The point of each step is to keep a source fact intact, including when the source is incomplete.",
    ) + f"""
    <section class="section">
      <div class="wrap">
        <div class="grid-2">
          <article class="card"><p class="kicker">01</p><h2>Public data</h2><p>Official state procurement portals, environmental and oil-and-gas agencies, orphan-well program pages, vendor portals, bid calendars, award notices, and bid tabs. Government sources come first. Login walls, CAPTCHAs, paywalls, and robots.txt exclusions are not bypassed.</p></article>
          <article class="card"><p class="kicker">02</p><h2>Extract</h2><p>Pull the solicitation identifier, agency, location, well count when the source states one, deadline, and document link. If a value is absent, the record says it is not stated. Numbers are not filled in to make a row look finished.</p></article>
          <article class="card"><p class="kicker">03</p><h2>Organize</h2><p>Keep what the source said separate from any summary. If two public surfaces disagree — a deadline is the usual case — the item is marked as a conflict that needs human verification.</p></article>
          <article class="card"><p class="kicker">04</p><h2>Match</h2><p>Compare the item with the states and work types on your watch list: plugging and abandonment, reclamation, methane work tied to abandoned wells, and the access, excavation, and waste handling those packages include.</p></article>
          <article class="card"><p class="kicker">05</p><h2>Alerts</h2><p>Send the digest or alert with the source link. The same disclaimer rides with every customer-facing report. You verify the official document before you act.</p></article>
        </div>
      </div>
    </section>
    <section class="section section-alt">
      <div class="wrap prose">
        <h2>What the products are</h2>
        <ul>
          <li><a href="pricing.html">Basic</a> — a weekly multi-state digest.</li>
          <li>Professional — daily alerts, a weekly report, and states or project types you select inside the geography we actually cover.</li>
          <li>Premium — immediate matching alerts, historical award intelligence drawn from public records, and customized monitoring.</li>
        </ul>
        <h2>What never happens</h2>
        <p>The service does not bid, does not broker, and does not take a percentage of a contract. It does not provide legal or engineering advice, and it does not claim a government affiliation. Coverage details are on the <a href="coverage.html">coverage page</a>. A frozen example of the output is the <a href="sample-digest.html">sample digest</a>.</p>
        <h2 id="faq">Questions contractors ask first</h2>
        {faq_html()}
      </div>
    </section>
    """
    return chrome(
        "How orphan well bid monitoring works | Joshua Israel Ventures LLC",
        "Public procurement records are extracted, organized, matched to states and project types, and sent as digests or alerts. Information only. AI summaries must be verified.",
        ORIGIN + "/how-it-works.html",
        "how",
        body,
        faq_ld(),
    )


def coverage():
    body = page_hero(
        "Geography",
        "Where the monitor looks, and what it looks for",
        "Launch coverage is Ohio, West Virginia, Kentucky, and Pennsylvania. Expansion, including later federal Interior and BLM context, is a plan. It is not a product you can buy today.",
    ) + f"""
    <section class="section">
      <div class="wrap prose">
        <h2 id="what-we-monitor">Work in scope</h2>
        <ul>
          <li>Orphan, abandoned, idle, and legacy oil and gas well plugging and abandonment.</li>
          <li>Site reclamation and restoration tied to those wells.</li>
          <li>Methane mitigation tied to abandoned wells.</li>
          <li>Excavation, access roads, and waste handling when they are part of those procurements.</li>
          <li>RFQs, RFIs, prequalification notices, amendments, cancellations, and awards for that work.</li>
        </ul>
        <p>Unrelated oilfield work that only mentions a well is out of scope. The 22 September 2026 scan checked a registry of public surfaces and recorded access limits honestly: where a portal disallows automated collection or hides the package behind a vendor login, the digest does not pretend the full file was read.</p>
        <h2 id="ohio">Ohio</h2>
        <p>Ohio Department of Natural Resources, Division of Oil and Gas Resources Management — the scan records the contracting office as ODNR DOGRM — plus OhioBuys and state procurement pages. On the scan date, OhioBuys <code>robots.txt</code> disallowed automated crawling, and public solicitations sat behind a security check. Full packages can require a login. Those walls were not bypassed. Some Ohio rows in the <a href="sample-digest.html">sample digest</a> therefore cite the OhioBuys home page because a stable public solicitation URL was not captured.</p>
        <ul class="source-list">
          <li>{ext("https://ohiobuys.ohio.gov/", "OhioBuys")}</li>
          <li>{ext("https://ohiodnr.gov/business-and-industry/energy-resources/oil-and-gas-wells/orphan-well-program", "ODNR orphan well program")}</li>
          <li>{ext("https://ohiodnr.gov/business-and-industry/business-opportunities/public-notice-orphan-well-plugging-contracts", "ODNR public notice: orphan well plugging contracts")}</li>
          <li>{ext("https://procure.ohio.gov/bidders-and-suppliers", "Ohio procurement — bidders and suppliers")}</li>
        </ul>
        <p>The scan also noted a historical class of Ohio prequalification add-on (MAC110 / CSP900922, described as the SRC0000027837 class). That is a type of notice worth watching. It is not an open solicitation on this site.</p>
        <h2 id="west-virginia">West Virginia</h2>
        <p>West Virginia Department of Environmental Protection, Office of Oil and Gas (WV DEP OOG on the scan), including abandoned-well plugging pages and the in-house purchasing summary. wvOASIS is the vendor-facing system. The scan found full solicitation PDFs behind a vendor account. The public summary used for the West Virginia rows is the in-house purchasing page.</p>
        <ul class="source-list">
          <li>{ext("https://dep.wv.gov/bto/IHP/Pages/default.aspx", "WV DEP in-house purchasing")}</li>
          <li>{ext("https://dep.wv.gov/oil-and-gas/abandoned-well-plugging/Pages/default.aspx", "WV DEP abandoned well plugging")}</li>
          <li>{ext("https://dep.wv.gov/oil-and-gas/abandoned-well-plugging/state-funded-plugging/Pages/default.aspx", "State-funded plugging")}</li>
          <li>{ext("https://dep.wv.gov/oil-and-gas/abandoned-well-plugging/infrastructure-investment-jobs-act/Pages/default.aspx", "Infrastructure Investment and Jobs Act plugging page")}</li>
          <li>{ext("https://dep.wv.gov/oil-and-gas/Pages/default.aspx", "WV DEP oil and gas")}</li>
          <li>{ext("https://www.wvoasis.gov/", "wvOASIS")}</li>
          <li>{ext("https://www.state.wv.us/admin/purchase/oasis.html", "West Virginia purchasing / OASIS overview")}</li>
        </ul>
        <h2 id="kentucky">Kentucky</h2>
        <p>Kentucky Energy and Environment Cabinet oil and gas pages, including the federal orphan-well plugging program page, and the Finance Cabinet’s Vendor Self Service. The scan’s keyword for these packages is KASTOW. As of 22 September 2026, zero currently open KASTOW solicitations were confirmed. County packages with a proposal due date of 18 September 2026 were treated as closed. VSS login is required for many attachments; that login was not bypassed.</p>
        <ul class="source-list">
          <li>{ext("https://eec.ky.gov/Natural-Resources/Oil-and-Gas/Pages/default.aspx", "KY EEC oil and gas")}</li>
          <li>{ext("https://eec.ky.gov/Natural-Resources/Oil-and-Gas/Pages/BIL-Federal-Orphan-Well-Plugging-Program.aspx", "KY EEC BIL federal orphan well plugging program")}</li>
          <li>{ext("https://finance.ky.gov/eProcurement/Pages/default.aspx", "Kentucky eProcurement")}</li>
          <li>{ext("https://vss.ky.gov/vssprod-ext/Advantage4", "Kentucky Vendor Self Service")}</li>
        </ul>
        <h2 id="pennsylvania">Pennsylvania</h2>
        <p>Pennsylvania Department of Environmental Protection, Office of Oil and Gas Management (PA DEP OOGM), legacy-well contractor pages, and Pennsylvania Department of Conservation and Natural Resources (PA DCNR) listings. BidExpress business pages for DEP and DCNR were the primary public find on the scan. Upcoming lists were readable. Drawings and specifications often need an account. The eMarketplace robots file disallowed automated crawling.</p>
        <ul class="source-list">
          <li>{ext("https://www.bidexpress.com/businesses/15106/home", "BidExpress — PA DEP")}</li>
          <li>{ext("https://www.bidexpress.com/businesses/65897/home?agency=true", "BidExpress — PA DCNR")}</li>
          <li>{ext("https://www.pa.gov/agencies/dep/programs-and-services/oil-and-gas/legacy-wells", "PA DEP legacy wells")}</li>
          <li>{ext("https://www.pa.gov/agencies/dep/programs-and-services/oil-and-gas/legacy-wells/contractors", "PA DEP legacy wells — contractors")}</li>
          <li>{ext("https://www.pa.gov/agencies/dep/programs-and-services/contracts-procurement-and-bonding/construction-contracts", "PA DEP construction contracts")}</li>
          <li>{ext("https://files.dep.state.pa.us/oilgas/BOGM/BOGMPortalFiles/AbandonedOrphanWells/Plugging_Contractor_Bidding_Information.pdf", "Plugging contractor bidding information (PDF)")}</li>
          <li>{ext("https://www.emarketplace.state.pa.us/", "Pennsylvania eMarketplace")}</li>
          <li>{ext("https://www.pasupplierportal.state.pa.us/", "PA Supplier Portal")}</li>
        </ul>
        <h2>Federal context, not a launch feed</h2>
        <p>Department of the Interior orphaned-wells pages, Bureau of Land Management oil and gas pages, SAM.gov, and Grants.gov are on the later watch list. Those surfaces often describe funding to states rather than a contractor solicitation. They are not part of the four-state product sold on the pricing page today.</p>
        <ul class="source-list">
          <li>{ext("https://www.doi.gov/orphanedwells", "DOI orphaned wells")}</li>
          <li>{ext("https://www.blm.gov/programs/energy-and-minerals/oil-and-gas", "BLM oil and gas")}</li>
          <li>{ext("https://sam.gov/", "SAM.gov")}</li>
          <li>{ext("https://www.grants.gov/", "Grants.gov")}</li>
        </ul>
        <h2>Secondary pages</h2>
        <p>When an official portal requires a login or presents a security check, a secondary bid board may be used only to discover a solicitation identifier or a deadline. The fact is then tied to an official URL when one is public. A secondary board is not the solicitation. The sample digest labels each row with the URL the scan recorded.</p>
      </div>
    </section>
    """
    return chrome(
        "Coverage: Ohio, West Virginia, Kentucky, and Pennsylvania | Orphan Well Intel",
        "What the orphan-well procurement monitor checks in OH, WV, KY, and PA: plugging, reclamation, amendments, and awards from public agency sources.",
        ORIGIN + "/coverage.html",
        "coverage",
        body,
    )


def pricing():
    body = page_hero(
        "Pricing",
        "Monthly information tiers",
        "Prices are for monitoring and reports. They are not a percentage of any contract, a success fee, or a brokerage charge. Stripe is not connected. Nothing on this page starts a subscription.",
    ) + """
    <section class="section">
      <div class="wrap">
        <div class="callout callout-warn">
          <p><strong>Coming soon.</strong> Request-access buttons open a form stub. The form does not send email, does not store what you type, and does not charge a card. Access requests will be collected after Stripe is wired.</p>
        </div>
        <div class="grid-3">
          <article class="tier">
            <h2>Basic</h2>
            <p class="price">$49 <span>USD / month</span></p>
            <ul>
              <li>Weekly multi-state digest</li>
              <li>Ohio, West Virginia, Kentucky, and Pennsylvania in one report</li>
              <li>Source links and the standing disclaimer on every issue</li>
            </ul>
            <div class="tier-actions">
              <a class="btn btn-dark" href="contact.html?tier=basic#request-access">Request access <span class="soon">Coming soon</span></a>
            </div>
          </article>
          <article class="tier">
            <h2>Professional</h2>
            <p class="price">$149 <span>USD / month</span></p>
            <ul>
              <li>Daily alerts</li>
              <li>Weekly report</li>
              <li>Customized states and project types inside the states we actually monitor</li>
            </ul>
            <div class="tier-actions">
              <a class="btn btn-dark" href="contact.html?tier=professional#request-access">Request access <span class="soon">Coming soon</span></a>
            </div>
          </article>
          <article class="tier">
            <h2>Premium</h2>
            <p class="price">$299 <span>USD / month</span></p>
            <ul>
              <li>Immediate matching alerts</li>
              <li>Historical award intelligence from public records</li>
              <li>Customized monitoring</li>
            </ul>
            <div class="tier-actions">
              <a class="btn btn-dark" href="contact.html?tier=premium#request-access">Request access <span class="soon">Coming soon</span></a>
            </div>
          </article>
        </div>
      </div>
    </section>
    <section class="section section-alt">
      <div class="wrap prose">
        <h2>What every tier includes</h2>
        <p>The same limits apply at $49, $149, and $299. You are buying information. Payment, when checkout exists, does not make Joshua Israel Ventures LLC your bidder, broker, engineer, or lawyer, and it does not create a government relationship.</p>
        <ul>
          <li>No bid submission and no authorized representation.</li>
          <li>No agency negotiation and no bid coordination.</li>
          <li>No percentage of a contract and no success fee.</li>
          <li>No eligibility certificate, license check, or bond opinion.</li>
          <li>No recommended bid price.</li>
          <li>No promise that the feed is complete or that an award will follow.</li>
        </ul>
        <h2>What “customized” means</h2>
        <p>Professional and Premium can narrow the watch list to states and project types inside current coverage. Launch coverage is Ohio, West Virginia, Kentucky, and Pennsylvania. Choosing a state does not add a state we do not monitor. Historical award intelligence is the Premium item; the public <a href="market-map.html">market map</a> is a single dated teaser, not that product.</p>
        <p>Read the <a href="sample-digest.html">sample digest</a> before you request access, and read the <a href="disclaimer.html">disclaimer</a> before you rely on any future issue.</p>
      </div>
    </section>
    """
    return chrome(
        "Pricing: $49, $149, and $299 monthly digests | Orphan Well Intel",
        "Basic $49/month weekly digest, Professional $149/month daily alerts, Premium $299/month matching and historical award intelligence. Information only. Checkout is not open.",
        ORIGIN + "/pricing.html",
        "pricing",
        body,
    )


OPPS = [
    {
        "state": "OH",
        "title": "OWP Federal — Washington 23F — 35 wells",
        "sid": "SRC0000041612",
        "agency": "ODNR DOGRM",
        "deadline": "2026-09-24 16:00",
        "tz": "Time zone not stated — verify with the agency.",
        "sources": [("OhioBuys", "https://ohiobuys.ohio.gov/")],
        "notes": "Scan note: imminent on 22 September 2026; 35 wells; MBE; federal. This page does not restate scope beyond that note. Confirm the set-aside, the package, and the clock on the official solicitation.",
        "hot": True,
    },
    {
        "state": "OH",
        "title": "OWP — Licking 12 — 1 well",
        "sid": "SRC0000041729",
        "agency": "ODNR DOGRM",
        "deadline": "2026-10-08 16:00",
        "tz": "Time zone not stated — verify with the agency.",
        "sources": [("OhioBuys solicitation page recorded by the scan", "https://ohiobuys.ohio.gov/page.aspx/en/bpm/process_manage_extranet/57682")],
        "notes": "Part of the Ohio cluster the scan grouped on 8 October 2026.",
        "hot": False,
    },
    {
        "state": "OH",
        "title": "OWP — Hardin 2 — 7 wells",
        "sid": "SRC0000041735",
        "agency": "ODNR DOGRM",
        "deadline": "2026-10-08 16:00",
        "tz": "Time zone not stated — verify with the agency.",
        "sources": [("OhioBuys", "https://ohiobuys.ohio.gov/")],
        "notes": "The scan did not capture a deeper public URL than the OhioBuys home page.",
        "hot": False,
    },
    {
        "state": "OH",
        "title": "OWP Federal — Cuyahoga 39F — 2 wells",
        "sid": "SRC0000041828",
        "agency": "ODNR DOGRM",
        "deadline": "2026-10-08 16:00",
        "tz": "Time zone conflict — verify with the agency. The scan flagged the time zone as conflicting across sources.",
        "sources": [("OhioBuys", "https://ohiobuys.ohio.gov/")],
        "notes": "Do not pick a time zone from this page. The scan’s instruction is to verify.",
        "hot": False,
    },
    {
        "state": "OH",
        "title": "OWP Federal — Allen 7F — 12 wells (re-offer)",
        "sid": "SRC for the re-offer was incomplete in the scan",
        "agency": "ODNR DOGRM",
        "deadline": "2026-10-08",
        "tz": "Time not stated. The scan recorded the re-offer SRC as incomplete.",
        "sources": [
            ("OhioBuys", "https://ohiobuys.ohio.gov/"),
            ("Scope-of-work PDF cited by the scan", "https://dam.assets.ohio.gov/image/upload/ohiodnr.gov/documents/oil-gas/contractor/SOW-Allen_7F.pdf"),
        ],
        "notes": "Described as a re-offer. Do not assume the PDF is the full current solicitation package.",
        "hot": False,
    },
    {
        "state": "WV",
        "title": "Lewis Co. Well Plugging Package — Group C",
        "sid": "ARFQ DEP2700000015",
        "agency": "WV DEP OOG",
        "deadline": "2026-09-28 14:30",
        "tz": "Time zone not stated — verify with the agency.",
        "sources": [("WV DEP in-house purchasing", "https://dep.wv.gov/bto/IHP/Pages/default.aspx")],
        "notes": "Scan note: 12 wells. The in-house purchasing page is a public summary. The scan found full solicitation PDFs behind a wvOASIS vendor account.",
        "hot": True,
    },
    {
        "state": "WV",
        "title": "Adkins #2 Well Plugging",
        "sid": "ARFQ DEP2700000016",
        "agency": "WV DEP OOG",
        "deadline": "2026-09-28",
        "tz": "Time not stated — verify with the agency.",
        "sources": [("WV DEP in-house purchasing", "https://dep.wv.gov/bto/IHP/Pages/default.aspx")],
        "notes": "Scan note: 1 well, Wayne County.",
        "hot": True,
    },
    {
        "state": "WV",
        "title": "Farmer #1 Well Plugging",
        "sid": "ARFQ DEP2700000019",
        "agency": "WV DEP OOG",
        "deadline": "2026-10-12",
        "tz": "Time not stated — verify with the agency.",
        "sources": [("WV DEP in-house purchasing", "https://dep.wv.gov/bto/IHP/Pages/default.aspx")],
        "notes": "API 47-045-00004. Scan note: Logan County.",
        "hot": False,
    },
    {
        "state": "PA",
        "title": "OOGM FS26-4 — 8 orphan gas wells, McKean County",
        "sid": "OOGM FS26-4",
        "agency": "PA DEP OOGM",
        "deadline": "2026-10-15 18:00 UTC",
        "tz": "The scan recorded this deadline as 18:00 UTC.",
        "sources": [("BidExpress — PA DEP", "https://www.bidexpress.com/businesses/15106/home")],
        "notes": "Inside the scan’s 30-day window (22 September through 22 October 2026).",
        "hot": False,
    },
    {
        "state": "PA",
        "title": "OOGM FS26-7 — 2 orphan gas wells, Greene County",
        "sid": "OOGM FS26-7",
        "agency": "PA DEP OOGM",
        "deadline": "2026-10-29 18:00 UTC",
        "tz": "The scan recorded this deadline as 18:00 UTC.",
        "sources": [("BidExpress — PA DEP", "https://www.bidexpress.com/businesses/15106/home")],
        "notes": "The scan listed this item as open or apparently open, and noted that 29 October 2026 falls just outside the 30-day window that ended 22 October 2026.",
        "hot": False,
    },
    {
        "state": "PA",
        "title": "FDC-014-104713.1 — 18 orphaned wells, Cornplanter SF (Forest County)",
        "sid": "FDC-014-104713.1",
        "agency": "PA DCNR",
        "deadline": "2026-10-01 17:00 UTC",
        "tz": "The scan recorded this deadline as 17:00 UTC.",
        "sources": [("BidExpress — PA DCNR", "https://www.bidexpress.com/businesses/65897/home?agency=true")],
        "notes": "Project identifier as recorded: FDC-014-104713.1.",
        "hot": True,
    },
]


def opp_card(opp):
    pills = [f'<span class="pill pill-{opp["state"].lower()}">{opp["state"]}</span>']
    if opp["hot"]:
        pills.append('<span class="pill pill-hot">Near-term on the scan date</span>')
    sources = "<br>".join(ext(url, label) for label, url in opp["sources"])
    return f"""
    <article class="opp">
      <div class="opp-head">{''.join(pills)}</div>
      <h2>{esc(opp["title"])}</h2>
      <dl>
        <div><dt>Solicitation ID</dt><dd class="id">{esc(opp["sid"])}</dd></div>
        <div><dt>Agency</dt><dd>{esc(opp["agency"])}</dd></div>
        <div><dt>Deadline recorded</dt><dd>{esc(opp["deadline"])}<br><em class="meta-note">{esc(opp["tz"])}</em></dd></div>
        <div><dt>Source</dt><dd>{sources}</dd></div>
      </dl>
      <p>{esc(opp["notes"])}</p>
    </article>
    """


def sample():
    cards = "\n".join(opp_card(opp) for opp in OPPS)
    body = page_hero(
        "Sample digest",
        "Sample digest from the 22 September 2026 scan",
        "A frozen example of how a weekly issue is organized. These are the solicitations that scan recorded. This page is not a live subscriber feed and it is not updated when an agency amends, cancels, or awards a package.",
    ) + f"""
    <section class="section">
      <div class="wrap">
        <div class="callout callout-warn">
          <p><strong>Contractors must verify.</strong> Every fact below is limited to the first live scan dated 22 September 2026. A deadline may already have passed by the time you read this. Confirm status, time zone, amendments, and requirements on the official source before you rely on a line for any bidding decision.</p>
        </div>
        {DISCLAIMER_BLOCK}
        <h2>Open or apparently open on the scan date</h2>
        <p>The scan saved 11 solicitations under that label. Kentucky is not in the list. Zero currently open KASTOW solicitations were confirmed that day.</p>
        {cards}
        <h2>Near-term deadlines the scan highlighted</h2>
        <p>Window used by the scan: 22 September 2026 through 22 October 2026.</p>
        <div class="table-wrap">
          <table>
            <caption>Deadlines inside 30 days of the scan, as recorded</caption>
            <thead>
              <tr><th>Deadline</th><th>State</th><th>ID</th><th>Scan note</th></tr>
            </thead>
            <tbody>
              <tr><td>2026-09-24</td><td>OH</td><td class="id">SRC0000041612 Washington 23F</td><td>Imminent on the scan date — 35 wells, MBE, federal</td></tr>
              <tr><td>2026-09-28</td><td>WV</td><td class="id">DEP2700000015 Lewis Group C</td><td>12 wells</td></tr>
              <tr><td>2026-09-28</td><td>WV</td><td class="id">DEP2700000016 Adkins #2</td><td>1 well, Wayne County</td></tr>
              <tr><td>2026-10-01</td><td>PA</td><td class="id">FDC-014-104713.1</td><td>DCNR, 18 wells; 17:00 UTC</td></tr>
              <tr><td>2026-10-08</td><td>OH</td><td class="id">SRC0000041729 / SRC0000041735 / SRC0000041828 / Allen 7F</td><td>Cluster of Ohio OWP due dates</td></tr>
              <tr><td>2026-10-12</td><td>WV</td><td class="id">DEP2700000019 Farmer #1</td><td>Logan County</td></tr>
              <tr><td>2026-10-15</td><td>PA</td><td class="id">OOGM FS26-4</td><td>McKean County, 8 wells; 18:00 UTC</td></tr>
            </tbody>
          </table>
        </div>
        <h2>Kentucky — none confirmed open</h2>
        <p>Zero currently open KASTOW solicitations were confirmed as of 22 September 2026 after portal and open-web checks. Multiple county packages (for example Ohio #005 / RFP-58-27 and Green #003 / RFP-56-27, plus Webster, Logan, and others) showed a proposal due date of 2026-09-18 and were treated as closed because that date had passed. They are not listed above as open work. The scan’s ongoing keyword is KASTOW on Kentucky VSS.</p>
        <h2>What the scan could not see</h2>
        <p>These limits are part of the record. They are not an invitation to get around them.</p>
        <ul>
          <li>OhioBuys disallowed automated crawling and presented a security check on public solicitations. Full packages can require login.</li>
          <li>Some Ohio agency pages responded to one fetch path and returned an error on another. A link in this digest is not a promise that the file is still posted.</li>
          <li>West Virginia full solicitation PDFs sat behind a vendor account. The in-house purchasing page is a public summary.</li>
          <li>Kentucky VSS attachments generally require login.</li>
          <li>Pennsylvania eMarketplace disallowed automated crawling. BidExpress upcoming lists were public; many drawings need an account.</li>
        </ul>
        <p>No bids were submitted to produce this sample. Joshua Israel Ventures LLC is not affiliated with the agencies named above. <a href="coverage.html">Coverage and source list</a> · <a href="disclaimer.html">Full disclaimer</a></p>
      </div>
    </section>
    """
    return chrome(
        "Sample digest: 22 September 2026 public scan | Orphan Well Intel",
        "Eleven open or apparently open orphan-well solicitations recorded on 22 September 2026 in Ohio, West Virginia, and Pennsylvania, with source URLs. Verify each item. Kentucky had none confirmed open.",
        ORIGIN + "/sample-digest.html",
        "sample",
        body,
    )


def market_rows():
    rows = []
    for name, states, appearance, label, url, site in COMPANIES:
        state_txt = ", ".join(states)
        site_cell = ext(site, "Public site") if site else "Not recorded"
        rows.append(
            f"""<tr data-states="{esc(" ".join(states))}" data-name="{esc(name)}">
              <td data-label="Company">{esc(name)}</td>
              <td data-label="States">{esc(state_txt)}</td>
              <td data-label="Public appearance">{esc(appearance)}</td>
              <td data-label="Primary source">{ext(url, label)}</td>
              <td data-label="Company site">{site_cell}</td>
            </tr>"""
        )
    return "\n".join(rows)


def market():
    body = page_hero(
        "Market map",
        "Companies named in the public plugging record",
        "Forty companies from a 22 September 2026 index of public award notices, bid tabs, and program documents in Ohio, West Virginia, Kentucky, and Pennsylvania. This list is not a bidder’s list.",
    ) + f"""
    <section class="section">
      <div class="wrap">
        <div class="callout callout-warn">
          <p><strong>Appearance on this list does not mean eligibility to bid.</strong> It does not mean a company is licensed, bonded, insured, prequalified, or authorized to plug wells for any agency. Pennsylvania entries drawn from bid-opening results are apparent low bids or competing bids, not always confirmed awards. Contact fields that were not on a public page were left blank. This teaser is not the Premium historical-award product.</p>
        </div>
        {DISCLAIMER_BLOCK}
        <h2>Counts</h2>
        <p>A company can appear in more than one state. Distinct companies: 40.</p>
        <div class="stat-row">
          <div class="stat"><span class="stat-num">25</span><span class="stat-label">Ohio</span></div>
          <div class="stat"><span class="stat-num">13</span><span class="stat-label">Pennsylvania</span></div>
          <div class="stat"><span class="stat-num">11</span><span class="stat-label">West Virginia</span></div>
          <div class="stat"><span class="stat-num">5</span><span class="stat-label">Kentucky</span></div>
        </div>
        <p class="fine">Plants &amp; Goodwin is also indexed with a New York association. Launch coverage for the service remains Ohio, West Virginia, Kentucky, and Pennsylvania.</p>
        <div class="filters" role="group" aria-label="Filter by state">
          <button type="button" class="filter-btn" data-filter="all" aria-pressed="true">All</button>
          <button type="button" class="filter-btn" data-filter="OH" aria-pressed="false">Ohio</button>
          <button type="button" class="filter-btn" data-filter="WV" aria-pressed="false">West Virginia</button>
          <button type="button" class="filter-btn" data-filter="KY" aria-pressed="false">Kentucky</button>
          <button type="button" class="filter-btn" data-filter="PA" aria-pressed="false">Pennsylvania</button>
        </div>
        <div class="search-row">
          <label for="company-search">Filter by company name</label>
          <input id="company-search" type="search" placeholder="Filter the list below" autocomplete="off">
        </div>
        <p id="filter-count" aria-live="polite">40 companies shown</p>
        <p id="filter-empty" hidden>No company in this index matches that filter.</p>
        <div class="table-wrap">
          <table class="market-table">
            <caption>Public-record index dated 22 September 2026. Descriptions are abbreviated from that index and are not a complete award history. Two lines stop where the index stops (Hydrocarbon Well Services; NuPointe Energy) and were not completed by guesswork.</caption>
            <thead>
              <tr>
                <th>Company</th>
                <th>States</th>
                <th>Key awards or bid appearances</th>
                <th>Primary source</th>
                <th>Company site</th>
              </tr>
            </thead>
            <tbody>
              {market_rows()}
            </tbody>
          </table>
        </div>
        <h2>How to read a row</h2>
        <ul>
          <li>The primary source is the one the index cited for that company. A firm working in two states may have other public records that are not repeated here.</li>
          <li>Ohio River Valley Institute rows are a published secondary summary of grant awards, not an agency bid tab.</li>
          <li>Dollar amounts are omitted on purpose. This page does not estimate contract value.</li>
          <li>A linked company website was already on the public index. The link is not an endorsement and not a finding that the site’s claims are current.</li>
        </ul>
      </div>
    </section>
    """
    return chrome(
        "Public market map of plugging contractors | Orphan Well Intel",
        "Forty companies named in public orphan-well award notices and bid tabs for Ohio, West Virginia, Kentucky, and Pennsylvania. Listing is not eligibility, licensing, or prequalification.",
        ORIGIN + "/market-map.html",
        "market",
        body,
    )


def disclaimer():
    body = page_hero(
        "Legal",
        "Disclaimer and terms",
        "The notice below is the customer-facing disclaimer for the Abandoned Oil Wells Project, operated by Joshua Israel Ventures LLC. It applies to this website, to digests, and to alerts.",
    ) + f"""
    <section class="section">
      <div class="wrap prose">
        {DISCLAIMER_BLOCK}
        <h2>Artificial intelligence and your responsibility</h2>
        <p><strong>Artificial intelligence is used</strong> to discover, extract, organize, and summarize publicly available materials. AI systems can make mistakes, including omissions, misreads, delayed updates, and incorrect summaries. <strong>You accept full responsibility</strong> for verifying every material fact against the official government source before relying on it for any business, bidding, or compliance decision. An alert is not a substitute for the solicitation, the amendment, the bid tab, or the award notice.</p>
        <h2>Information only</h2>
        <p>This product sells <strong>information only</strong>. Joshua Israel Ventures LLC does not submit bids, negotiate with agencies, determine legal eligibility, certify qualifications, recommend bid prices, coordinate bidding, or act as your authorized representative. The service does not broker plugging work and does not charge a percentage of a contract or a success fee.</p>
        <p>The service does <strong>not</strong> provide legal, engineering, environmental, procurement, or bidding advice. Nothing on this site is a professional opinion about how a well should be plugged or what a compliant bid looks like.</p>
        <h2>No government affiliation</h2>
        <p>This service is <strong>not affiliated with any government agency</strong>. Names of agencies, portals, and programs appear because those offices publish the records being monitored. Publication of a link is not sponsorship, partnership, or endorsement by that office, and it is not a claim that Joshua Israel Ventures LLC speaks for that office.</p>
        <h2>This website</h2>
        <ul>
          <li>The <a href="sample-digest.html">sample digest</a> freezes the 22 September 2026 scan. It can go stale the same day an agency posts an addendum.</li>
          <li>The <a href="market-map.html">market map</a> is a public-record index. A row is not an eligibility determination.</li>
          <li><a href="pricing.html">Prices</a> describe intended monthly information subscriptions. Stripe is not connected. This site does not take payment.</li>
          <li>The <a href="contact.html">request-access form</a> is a stub. It does not transmit or store a message. No contact email is published here.</li>
        </ul>
        <h2>Reports, alerts, and digests</h2>
        <p>Substantially this notice is included on every customer-facing report, alert, and digest. If a shorter footer is all you can see on a given screen, the short version does not replace this page.</p>
        <h2>No warranty of completeness</h2>
        <p>Information may be incomplete, delayed, changed, or inaccurate. Portals block automated access, hide files behind vendor accounts, and revise deadlines without notice to this service. Joshua Israel Ventures LLC does not guarantee that every relevant solicitation will be found, that a found solicitation is still open, or that any user will receive an award.</p>
      </div>
    </section>
    """
    return chrome(
        "Disclaimer and terms | Joshua Israel Ventures LLC",
        "Joshua Israel Ventures LLC provides information only. Not a government agency. AI is used and can be wrong. Users accept full responsibility for verifying official procurement sources.",
        ORIGIN + "/disclaimer.html",
        "disclaimer",
        body,
    )


def contact():
    body = page_hero(
        "Access",
        "Request access",
        "Checkout is not open. This form is a preview of the questions a later signup will ask. It does not send email and it does not store what you type.",
    ) + """
    <section class="section">
      <div class="wrap">
        <div class="grid-2">
          <div class="prose">
            <h2>No payment on this site</h2>
            <p>Stripe is not connected. Access requests will be collected after Stripe is wired. Until then there is no mailing list, no inbox behind this form, and no published contact email address.</p>
            <p>Tiers, when they are for sale, will be the information subscriptions on the <a href="pricing.html">pricing page</a>: Basic at $49/month, Professional at $149/month, and Premium at $299/month. None of them include bidding, brokerage, or a percentage of a contract.</p>
            <p>Read the <a href="disclaimer.html">disclaimer</a> before you use a future issue. AI is used — verify official sources.</p>
          </div>
          <form id="access-form" class="form-card" action="contact.html" method="post" autocomplete="off" onsubmit="return false;">
            <div id="request-access" class="form-row">
              <label for="person-name">Name</label>
              <input id="person-name" type="text" autocomplete="off">
            </div>
            <div class="form-row">
              <label for="company">Company</label>
              <input id="company" type="text" autocomplete="off">
            </div>
            <div class="form-row">
              <label for="work-email">Work email</label>
              <input id="work-email" type="text" inputmode="email" autocomplete="off" aria-describedby="email-note">
              <p id="email-note" class="fine">Typed here only as a preview. It is not transmitted.</p>
            </div>
            <fieldset class="form-row">
              <legend>States you would want covered</legend>
              <div class="checks">
                <label><input type="checkbox" value="OH"> Ohio</label>
                <label><input type="checkbox" value="WV"> West Virginia</label>
                <label><input type="checkbox" value="KY"> Kentucky</label>
                <label><input type="checkbox" value="PA"> Pennsylvania</label>
              </div>
            </fieldset>
            <fieldset class="form-row">
              <legend>Tier</legend>
              <div class="radios">
                <label><input type="radio" name="tier-preview" value="basic"> Basic — $49/month weekly digest</label>
                <label><input type="radio" name="tier-preview" value="professional"> Professional — $149/month</label>
                <label><input type="radio" name="tier-preview" value="premium"> Premium — $299/month</label>
              </div>
            </fieldset>
            <div class="form-row">
              <label for="types">Project types you care about</label>
              <textarea id="types" placeholder="For example: orphan well plugging, site reclamation"></textarea>
            </div>
            <div class="form-row ack">
              <label for="ack"><input id="ack" type="checkbox"> I understand this service is information only, is not a government agency, uses AI, and that I must verify official sources. I also understand this preview does not send my request.</label>
            </div>
            <button type="button" class="btn btn-dark" id="access-submit">Request access</button>
            <p id="form-result" class="form-result" role="status" hidden></p>
            <noscript>
              <p>JavaScript is off, so this preview button cannot run. There is still no email address on this site. Access requests will be collected after Stripe is connected.</p>
            </noscript>
          </form>
        </div>
      </div>
    </section>
    """
    return chrome(
        "Request access | Orphan Well Intel",
        "Request access to orphan well procurement digests. The form is a stub: Stripe is not connected, and no message is sent or stored.",
        ORIGIN + "/contact.html",
        "contact",
        body,
    )


def not_found():
    body = page_hero(
        "404",
        "This page is not on the site",
        "The address does not match a published page. The sample digest and the disclaimer are linked below.",
    ) + """
    <section class="section">
      <div class="wrap prose">
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="sample-digest.html">Sample digest</a></li>
          <li><a href="pricing.html">Pricing</a></li>
          <li><a href="disclaimer.html">Disclaimer</a></li>
          <li><a href="contact.html">Request access</a></li>
        </ul>
      </div>
    </section>
    """
    return chrome(
        "Page not found | Orphan Well Intel",
        "That address is not a page on the Orphan Well Intel site from Joshua Israel Ventures LLC.",
        ORIGIN + "/404.html",
        "",
        body,
    )


def sitemap():
    pages = [
        ("", "2026-09-22", "1.0"),
        ("how-it-works.html", "2026-09-22", "0.8"),
        ("coverage.html", "2026-09-22", "0.8"),
        ("pricing.html", "2026-09-22", "0.9"),
        ("sample-digest.html", "2026-09-22", "0.9"),
        ("market-map.html", "2026-09-22", "0.6"),
        ("disclaimer.html", "2026-09-22", "0.5"),
        ("contact.html", "2026-09-22", "0.7"),
    ]
    urls = []
    for path, lastmod, priority in pages:
        loc = ORIGIN + "/" + path
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <priority>{priority}</priority>
  </url>"""
        )
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""" + "\n".join(urls) + "\n</urlset>\n"


def main():
    assert_counts()
    assert len(OPPS) == 11
    pages = {
        "index.html": home(),
        "how-it-works.html": how(),
        "coverage.html": coverage(),
        "pricing.html": pricing(),
        "sample-digest.html": sample(),
        "market-map.html": market(),
        "disclaimer.html": disclaimer(),
        "contact.html": contact(),
        "404.html": not_found(),
    }
    for name, html in pages.items():
        path = ROOT / name
        path.write_text(html, encoding="utf-8")
        print(f"wrote {path.name} ({len(html)} bytes)")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
