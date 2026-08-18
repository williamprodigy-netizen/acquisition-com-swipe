#!/usr/bin/env python3
"""Build the Acquisition.com swipe site.

One repo per competitor. Reads data/ and the optimised JPEGs in media/,
writes a static hub plus one page per asset class. Images are real files,
never base64 — the board is the only place base64 is correct.

Run: python3 build_site.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(ROOT, "data")

SITE = "Acquisition.com — Scaling Workshop swipe"
CAPTURED = "11 August 2026"
FID = "F133"

PAGES = [
    ("index.html", "Overview"),
    ("funnel.html", "The pages"),
    ("vsl.html", "The VSL"),
    ("emails.html", "The emails"),
    ("application.html", "The application"),
    ("steal.html", "What to steal"),
    ("board.html", "Wired board"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--panel:#fff;--bg:#eef0f3;
 --accent:#4f46e5;--good:#059669;--warn:#ea580c;--bad:#9f1239}
@media(prefers-color-scheme:dark){:root{--ink:#e8eaed;--muted:#9aa3b2;--line:#2a3140;
 --panel:#151a23;--bg:#0d1117;--accent:#818cf8;--good:#34d399;--warn:#fb923c;--bad:#fb7185}}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;
 -webkit-font-smoothing:antialiased;line-height:1.55}
h1,h2,h3,h4{font-weight:600;letter-spacing:-.02em}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:0 28px}
header.top{background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.topin{max-width:1120px;margin:0 auto;padding:0 28px;display:flex;align-items:center;gap:26px;height:60px}
.brand{font-size:15px;font-weight:600;white-space:nowrap}
.brand span{color:var(--muted);font-weight:400}
nav.main{display:flex;gap:20px;overflow-x:auto;scrollbar-width:none}
nav.main::-webkit-scrollbar{display:none}
nav.main a{font-size:14px;color:var(--muted);text-decoration:none;white-space:nowrap;
 padding:6px 0;border-bottom:2px solid transparent}
nav.main a:hover{color:var(--ink)}
nav.main a.on{color:var(--ink);border-bottom-color:var(--accent)}
.hero{padding:48px 0 22px}
.kick{font-size:12px;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.hero h1{font-size:40px;margin-bottom:14px;line-height:1.15}
.hero p{font-size:17px;color:var(--muted);max-width:840px}
.hero p+p{margin-top:12px}
section{padding:26px 0}
h2.sec{font-size:22px;margin-bottom:8px;padding-bottom:9px;border-bottom:1px solid var(--line)}
h2.sec+p.lede{font-size:15px;color:var(--muted);margin-bottom:16px;max-width:840px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(215px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px}
.card h3{font-size:15px;margin-bottom:7px}
.card p{font-size:14px;color:var(--muted)}
.card p+p{margin-top:9px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px}
.stat .n{font-size:25px;font-weight:600;letter-spacing:-.03em}
.stat .l{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin-top:3px}
table{width:100%;border-collapse:collapse;font-size:14px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
th,td{text-align:left;padding:9px 13px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600}
tr:last-child td{border-bottom:none}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--muted)}
.tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:99px;
 border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.tag.good{color:var(--good);border-color:var(--good)}
.tag.warn{color:var(--warn);border-color:var(--warn)}
.tag.bad{color:var(--bad);border-color:var(--bad)}
.tag.a{color:var(--accent);border-color:var(--accent)}
figure{background:var(--panel);border:1px solid var(--line);border-radius:9px;overflow:hidden}
figure .shot{max-height:420px;overflow:hidden;display:block}
figure img{width:100%;display:block;background:#000;cursor:zoom-in}
figcaption{padding:9px 11px;font-size:12.5px;color:var(--muted);border-top:1px solid var(--line)}
figcaption b{color:var(--ink);font-weight:600;display:block;margin-bottom:2px;font-size:13.5px}
figcaption a{color:var(--accent);text-decoration:none;word-break:break-all}
details{background:var(--panel);border:1px solid var(--line);border-radius:9px;margin-bottom:9px}
summary{padding:12px 15px;cursor:pointer;font-size:14px;font-weight:500;list-style:none;
 display:flex;justify-content:space-between;gap:14px;align-items:baseline}
summary::-webkit-details-marker{display:none}
summary .meta{font-size:12px;color:var(--muted);font-weight:400;white-space:nowrap}
details .body{padding:0 15px 15px;font-size:14.5px;line-height:1.75}
details .body p{margin-bottom:11px;white-space:pre-wrap}
details .note{padding:0 15px 12px;font-size:13px;color:var(--warn);font-style:italic}
.q{background:var(--panel);border-left:3px solid var(--accent);padding:14px 17px;border-radius:0 8px 8px 0;
 font-size:15.5px;line-height:1.65;margin-bottom:12px}
.q .src{display:block;margin-top:8px;font-size:12px;color:var(--muted);font-style:normal}
.ev{font-size:11px;letter-spacing:.05em;text-transform:uppercase;font-weight:600}
.ev.v{color:var(--good)}.ev.p{color:var(--warn)}.ev.u{color:var(--muted)}.ev.r{color:var(--accent)}
.big{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);
 border-radius:0 10px 10px 0;padding:20px 24px;margin-bottom:16px}
.big h3{font-size:18px;margin-bottom:10px}
.big p{font-size:15px;color:var(--muted);line-height:1.65}
.big p+p{margin-top:10px}
.big b{color:var(--ink)}
footer{border-top:1px solid var(--line);margin-top:40px;padding:26px 0 50px;font-size:13px;color:var(--muted)}
#lb{position:fixed;inset:0;background:rgba(8,11,17,.94);display:none;z-index:200;overflow:auto;padding:40px 20px}
#lb.on{display:block}
#lb img{max-width:1100px;width:100%;margin:0 auto;display:block;border-radius:8px}
#lbx{position:fixed;top:14px;right:20px;color:#94a3b8;font-size:13px}
"""

JS = """
document.addEventListener('click',function(e){
  var i=e.target.closest('figure img');
  if(i){var lb=document.getElementById('lb');
    document.getElementById('lbi').src=i.dataset.full||i.src;lb.classList.add('on');
    window.scrollTo(0,0);return;}
  if(e.target.closest('#lb'))document.getElementById('lb').classList.remove('on');
});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape')document.getElementById('lb').classList.remove('on');});
"""


def page(fname, title, body):
    nav = "".join(
        f'<a href="{h}" class="{"on" if h == fname else ""}">{t}</a>'
        for h, t in PAGES)
    out = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &middot; {SITE}</title><style>{CSS}</style></head><body>
<header class="top"><div class="topin">
<div class="brand">Acquisition.com <span>&middot; {FID}</span></div>
<nav class="main">{nav}</nav></div></header>
<div class="wrap">{body}
<footer>Captured {CAPTURED} from acquisition.com and from Will&rsquo;s personal inbox
(williamprodigy@gmail.com). Evidence in
<code>~/UNDERGROUND_FUNNELS_SSOT/01_RAW_FUNNELS/</code>. Registry id {FID}.<br>
Claims are tagged VERIFIED (seen in the capture), PARTIALLY VERIFIED,
READ (our interpretation) or UNVERIFIED (named, not guessed).</footer></div>
<div id="lb"><span id="lbx">click anywhere or press Esc to close</span><img id="lbi" alt=""></div>
<script>{JS}</script></body></html>"""
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(out)
    print("wrote", fname, os.path.getsize(os.path.join(ROOT, fname)) // 1024, "KB")


def esc(s):
    return html.escape(str(s))


def fig(asset, title, url, note):
    link = f'<a href="{url}" target="_blank" rel="noopener">{esc(url)}</a>' if url else ""
    return (f'<figure><span class="shot"><img src="media/thumb_{asset}.jpg" '
            f'data-full="media/web_{asset}.jpg" alt="{esc(title)}" loading="lazy"></span>'
            f'<figcaption><b>{title}</b>{link}<br>{note}</figcaption></figure>')


# ---------------------------------------------------------------- OVERVIEW
STATS = [
    ("$5,000", "per seat"),
    ("2 days", "in person, Vegas HQ"),
    ("56 days", "email loop, exact"),
    ("~100", "seats per workshop"),
    ("22", "application questions"),
    ("0", "guarantee"),
]

index_body = f"""
<div class="hero"><div class="kick">Swipe &middot; {FID} &middot; captured {CAPTURED}</div>
<h1>They sell a $5,000 seat by making you fail an application for something else</h1>
<p>Alex and Leila Hormozi run no webinar, no VSL funnel and almost no paid acquisition for this.
The machine is four complete free courses and a book that has sold 1.4 million copies, feeding a
HubSpot list that gets mailed every two days forever &mdash; on an evergreen loop that repeats on an
exact 56-day clock.</p>
<p>The close is the part worth stealing. Their application is not an application for the workshop.
It is an application to become a <b>portfolio company</b> &mdash; for investment. You answer
revenue and profit three separate ways, and when your numbers come up short the form tells you so
and offers the paid workshop as the way to fix it. The $5,000 seat is the consolation prize for
failing at something more prestigious.</p>
<p><b>Will is inside this funnel personally.</b> He bought $100M Money Models in August 2025 and has
booked their call twice &mdash; Braeden Bowman in May 2026 and Coleman Burgess in July 2026. The
whole sequence, both setter threads and 77 broadcast emails, is sitting in his Gmail.</p></div>

<section><div class="grid g3">
{''.join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>' for n, l in STATS)}
</div></section>

<section><h2 class="sec">The spine</h2>
<p class="lede">Nine steps. Everything before step 4 is free and genuinely useful.</p>
<div class="tablewrap"><table>
<tr><th>#</th><th>Step</th><th>What it actually is</th><th>Evidence</th></tr>
<tr><td class="num">1</td><td>Front door</td><td>Books ($100M Offers / Money Models), podcast, YouTube,
homepage. Podscribe is installed, so they measure the podcast as an acquisition channel.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">2</td><td>The gate</td><td>Four full free courses. All four post to the
<b>same</b> HubSpot form id <code>43c2570a</code>. One list, four doors. Two-step: email, then name and phone.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">3</td><td>The machine</td><td>value@acquisition.com every two days. Track A is an
evergreen selling loop on a 56-day repeat. Track B is &ldquo;Mozi Minute&rdquo;, never repeated, never sells.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">3b</td><td>Segmented magnet</td><td>The Scaling Roadmap is delivered by
<b>your stage</b>, then a 3-email sequence written only for that stage.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">4</td><td>Sales page</td><td>/workshop. Vidalytics VSL, three identical CTAs
anchoring to the embedded booking widget, price stated openly, FAQ does the disqualifying.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">5</td><td>Application</td><td>JotForm 231197990495167, 22 questions, branching.
Framed as applying for investment.</td><td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">6</td><td>Booking</td><td>iClosed embedded inline &mdash; not Calendly, not a redirect.
The iframe leaks an A/B variant: <code>workshop-v1</code>, <code>lp_var=4080-v1</code>.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">7</td><td>Setter</td><td>Named humans on real @acquisition.com addresses, titled
&ldquo;Consultant&rdquo;. Four reminders per booking, plus a pre-call video and a phone-number check.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">8</td><td>Product</td><td>Two days at the Vegas HQ. Day 1 presented frameworks,
day 2 roundtables grouped by revenue band. Deliverable is 3-5 next steps and a packet.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
<tr><td class="num">9</td><td>Launch layer</td><td>On top of the evergreen Scaling Workshop they launch
a new named workshop every few months &mdash; Marketing (May), Offers (July) &mdash; to the same list.</td>
<td><span class="ev v">VERIFIED</span></td></tr>
</table></div></section>

<section><h2 class="sec">Stack</h2>
<div class="grid g4">
<div class="card"><h3>HubSpot</h3><p>CMS, CRM, forms, email, video and the preference centre.
Portal 21368823. Almost the entire funnel is one vendor.</p></div>
<div class="card"><h3>JotForm</h3><p>The application. Deliberately NOT HubSpot &mdash; they wanted the
branching logic.</p></div>
<div class="card"><h3>iClosed</h3><p>Booking. Embedded inline on the sales page.</p></div>
<div class="card"><h3>Vidalytics</h3><p>The sales-page VSL. Id <code>dIKsAOKOfqVMrD08</code>, shared by
/workshop and /o-vegas.</p></div>
<div class="card"><h3>Hyros</h3><p><code>t.acquisition.com/v1/lst/universal-script</code>. Server-side
attribution across the whole property.</p></div>
<div class="card"><h3>Podscribe</h3><p>Podcast attribution. They treat the podcast as a measured
acquisition channel, not brand.</p></div>
<div class="card"><h3>Pixels</h3><p>Meta, TikTok, Snapchat, Reddit, GTM-MHT26J7X. All loaded, all live.</p></div>
<div class="card"><h3>Cookiebot</h3><p>Consent. Which is why the capture shows Allow/Deny buttons on
every page.</p></div>
</div></section>

<section><h2 class="sec">What is missing from this capture</h2>
<p class="lede">Named, not guessed.</p>
<div class="card"><p>The post-opt-in confirmation page, the buyer / post-purchase sequence (we know it
exists &mdash; Alex recycles a video out of it into the cold list), the SMS thread, the iClosed flow past
the embed, and the workshop room itself. Opting in needs Will&rsquo;s approval and the phone field is a
hard stop under the swipe rules &mdash; no research number exists, and fabricating one routes real sales
calls to a real stranger.</p></div></section>
"""

# ---------------------------------------------------------------- FUNNEL
FIGS = [
    ("05_Homepage", "Homepage", "https://www.acquisition.com/",
     "Four free courses stacked above one paid CTA. &ldquo;Attend a Workshop&rdquo; is the only "
     "button on the page that costs money."),
    ("10_Books_hub", "Books hub", "https://www.acquisition.com/books",
     "$100M Offers, 1.4M copies sold by word of mouth. The cheapest entry to the same list. "
     "Will entered here in Aug 2025."),
    ("06_Free_course_-_Scaling", "Free course &mdash; Scaling", "https://www.acquisition.com/training/scalingstart",
     "HubSpot form <code>43c2570a</code>. Two-step: email first, then name + phone + country."),
    ("09_Free_course_-_Money_Models", "Free course &mdash; Money Models", "https://www.acquisition.com/training/money/context",
     "Same form id. Same in-page block: &ldquo;Meet the Acquisition.com Team for a private workshop "
     "in Vegas.&rdquo; The paid offer lives inside the free product."),
    ("08_Free_course_-_Leads", "Free course &mdash; Leads", "https://www.acquisition.com/training/leads",
     "Third door, same list."),
    ("07_Free_course_-_Offers", "Free course &mdash; Offers", "https://www.acquisition.com/training/offers",
     "Fourth door, same list. This one is the on-ramp to the Offers Workshop SKU."),
    ("01_Workshop_sales_page", "Scaling Workshop &mdash; $5,000", "https://www.acquisition.com/workshop",
     "H1: &ldquo;ARE YOU THE THING LIMITING YOUR BUSINESS?&rdquo; Three identical CTAs, all "
     "&ldquo;I&rsquo;M READY TO SCALE&rdquo;, all anchoring to #booking-widget. Price in the FAQ."),
    ("03_Vegas_event_page_o-vegas", "/o-vegas", "https://www.acquisition.com/o-vegas",
     "The same page again on a different slug, same Vidalytics id. Homepage traffic goes here, "
     "email traffic goes to /workshop. Two slugs, one page, split reporting."),
    ("02_Offers_Workshop_sales_page", "Offers Workshop", "https://www.acquisition.com/offers-workshop",
     "&ldquo;BUILD OFFERS SO GOOD THEY SCALE WITHOUT YOU.&rdquo; Sold out 110/110 on 24 Jul 2026. "
     "The CTA now reads BOOK MY CALL and anchors to #waitlist &mdash; a hidden HubSpot form that "
     "still captures phone."),
    ("04_Application", "The application", "https://www.acquisition.com/apply",
     "&ldquo;STEP 1 &mdash; WE SCALE GREAT COMPANIES.&rdquo; A JotForm in a HubSpot page."),
]

funnel_body = f"""
<div class="hero"><div class="kick">The pages</div><h1>Ten pages, captured</h1>
<p>Full-page screenshots, rendered HTML, visible text, forms, prices and the tracker fingerprint are
all in the SSOT. Click any shot to open it full size.</p></div>
<section><div class="grid g2">
{''.join(fig(a, t, u, n) for a, t, u, n in FIGS)}
</div></section>

<section><h2 class="sec">Three things the pages give away</h2>
<div class="big"><h3>1. The price is on the page, and so is the floor</h3>
<p>&ldquo;Tickets are $5k per seat.&rdquo; Then, immediately: &ldquo;If you are under 250k/yr this is
not a fit (yet.)&rdquo; and &ldquo;<b>If you haven&rsquo;t made at least $5k from the free content,
don&rsquo;t do it.</b>&rdquo;</p>
<p>That last line is doing three jobs at once. It disqualifies, so the setter never argues about
budget. It flexes &mdash; the free stuff is worth $5k on its own. And it reframes the price as a
<i>proven</i> multiple rather than a cost. <span class="ev v">VERIFIED</span></p></div>

<div class="big"><h3>2. They justify the price with their staff&rsquo;s salaries</h3>
<p>&ldquo;you work with our directors that are paid $350k, $600k, $900k+ per year.&rdquo; Not
&ldquo;world-class experts&rdquo;. Numbers. It is an unfakeable, checkable, specific claim, and it
makes $5,000 for two days of their time read as cheap. <span class="ev v">VERIFIED</span></p></div>

<div class="big"><h3>3. There is no guarantee anywhere</h3>
<p>No refund policy, no money-back, no risk reversal of any kind on either sales page. The entire
risk reversal is social: the room, the salaries, the sold-out proof, and the industry list.
<span class="ev v">VERIFIED</span> &mdash; searched both captures.</p></div></section>
"""

# ---------------------------------------------------------------- EMAILS
E = json.load(open(os.path.join(D, "emails.json")))
TRACK = {
    "A": ('<span class="tag a">Track A &middot; evergreen</span>', "evergreen selling loop"),
    "B": ('<span class="tag">Mozi Minute</span>', "never repeats, never sells"),
    "L": ('<span class="tag warn">Launch</span>', "a dated workshop launch"),
    "R": ('<span class="tag good">Roadmap</span>', "stage-segmented sequence"),
    "S": ('<span class="tag bad">Setter</span>', "1-to-1, from a named human"),
}

# find the exact repeats
from collections import defaultdict
import datetime
seen = defaultdict(list)
for dt, subj, tr in E["index"]:
    seen[subj].append(dt)
repeats = []
for subj, dts in seen.items():
    if len(dts) > 1:
        ds = sorted(dts)
        gap = (datetime.date.fromisoformat(ds[-1]) - datetime.date.fromisoformat(ds[0])).days
        repeats.append((subj, ds[0], ds[-1], gap))
repeats.sort(key=lambda r: r[1])

rows = "".join(
    f'<tr><td>{esc(s)}</td><td class="num">{a}</td><td class="num">{b}</td>'
    f'<td class="num"><b>{g}</b></td></tr>' for s, a, b, g in repeats)

idx_rows = "".join(
    f'<tr><td class="num">{dt}</td><td>{esc(su)}</td><td>{TRACK[tr][0]}</td></tr>'
    for dt, su, tr in E["index"])

bodies = ""
for b in E["bodies"]:
    tag = TRACK[b["track"]][0]
    sender = b.get("sender", E["sender"])
    paras = "".join(f"<p>{esc(p)}</p>" for p in b["body"].split("\n\n"))
    bodies += (f'<details><summary><span>{esc(b["subject"])}</span>'
               f'<span class="meta">{tag} &middot; {b["date"]} &middot; {esc(sender)}</span></summary>'
               f'<div class="note">{esc(b["note"])}</div><div class="body">{paras}</div></details>')

gaps = sorted({g for _, _, _, g in repeats})
emails_body = f"""
<div class="hero"><div class="kick">The emails</div>
<h1>Two tracks. One of them is on a 56-day clock.</h1>
<p>{len(E['index'])} broadcasts from value@acquisition.com sitting in Will&rsquo;s personal inbox,
plus the two setter threads. Sending is every other day at roughly 15:00 UTC.</p>
<p>Track A is the selling track and it <b>recycles on an exact 56-day repeat</b> &mdash; every
verified pair below is precisely 8 weeks apart, with no exceptions across
{len(repeats)} repeated subject lines. Track B, prefixed &ldquo;Mozi Minute:&rdquo;, is fresh every
single time and never pitches anything.</p></div>

<section><h2 class="sec">The loop, proven</h2>
<p class="lede">Every Track A subject line that has run twice, and the gap between the two sends.
Gap values observed: {', '.join(str(g) for g in gaps)} days. <span class="ev v">VERIFIED</span></p>
<div class="tablewrap"><table>
<tr><th>Subject</th><th>First send</th><th>Second send</th><th>Gap (days)</th></tr>
{rows}</table></div></section>

<section><h2 class="sec">Why this matters more than it looks</h2>
<div class="big"><p>A 56-day evergreen loop means <b>they wrote roughly 28 selling emails once and
have not written a new one since.</b> Every new subscriber walks into the same cycle at whatever
point they joined, and anyone who stays on the list for four months simply sees it twice.</p>
<p>The reason they can get away with it is Track B. The Mozi Minute is genuinely fresh every time,
so the <i>list</i> never feels stale even though half the mail is on repeat. The fresh track buys
permission for the recycled one. <span class="ev r">READ</span></p>
<p>They also never discount the evergreen workshop. Instead they periodically <b>launch a new named
workshop</b> &mdash; Marketing in May, Offers in July &mdash; which manufactures a genuine deadline
without ever devaluing the always-on SKU. <span class="ev v">VERIFIED</span></p></div></section>

<section><h2 class="sec">Full copy &mdash; the ones worth reading</h2>
<p class="lede">Verbatim bodies, tracking links stripped. The two setter emails at the bottom are
1-to-1, not broadcast.</p>
{bodies}</section>

<section><h2 class="sec">Complete index</h2>
<p class="lede">All {len(E['index'])} broadcasts, newest first.</p>
<div class="tablewrap"><table>
<tr><th>Date</th><th>Subject</th><th>Track</th></tr>
{idx_rows}</table></div></section>
"""

# ---------------------------------------------------------------- APPLICATION
Q = [
    ("1", "Which best describes you?", "I own a business &middot; I want to attend a workshop to grow my business &middot; I want to start a business &middot; I want to SELL my business", ""),
    ("2-4", "Would you like to join us in Las Vegas?", "&ldquo;If accepted, you will get the chance to fly down to our headquarters&hellip; join 50 or so other businesses&hellip; first come first serve basis&rdquo;", "Acceptance framing before anything has been asked."),
    ("5", "What problem can I help you solve?", "Getting Leads &middot; Making Sales &middot; Recruiting &amp; Hiring &middot; What To Sell &middot; Other", "Segments the follow-up content."),
    ("6", "How do you prefer to learn/consume info?", "Watching &middot; Listening &middot; Reading", "Segments the format of the follow-up."),
    ("7", "Where is your business based?", "USA &middot; Canada &middot; &hellip;", ""),
    ("8", "What type of business do you have?", "Service &middot; Brick &amp; Mortar &middot; Ecommerce &middot; Software &middot; E-Learning", ""),
    ("9", "Describe your business in 1-3 sentences MAX.", "&ldquo;Ex: I help dentists get more patients using facebook ads for $2000 per month.&rdquo;", "The example does the teaching. It shows them exactly the shape of answer they want."),
    ("10", "Annual Revenue?", "$0-$1M &middot; $1M-$3M &middot; $3M-$5M &middot; $5M-$10M &middot; $10M-$20M &middot; $20M+", ""),
    ("11", "(2/2) Annual Revenue", "$0-$250K &middot; $250K-$500K &middot; $500K-$750K &middot; $750K-$1M", "The sub-band that only fires if you picked $0-$1M. This is where the $250k floor gets enforced."),
    ("12", "EBITDA, past 12 months", "$1M-$2M &middot; $2M-$3M &middot; $10M+ &hellip;", ""),
    ("13", "(2/2) EBITDA, past 12 months", "sub-bands", ""),
    ("14", "THE DOWNSELL", "&ldquo;Based on your answers, you&rsquo;d need to grow in order to qualify as a portfolio company&hellip; and we&rsquo;d like to help. Would you like us to show you exactly what we&rsquo;d do to scale your company? If so, click the button below to attend a <b>paid</b> workshop at our Headquarters in Las Vegas.&rdquo;", "THE WHOLE MECHANIC. Read the note below."),
    ("15", "EBITDA, past 3 months", "$750K-$1.25M &middot; $1.25M-$2.5M &middot; $2.5M+", "A third pass at the same question, on a shorter window, to catch people inflating the annual figure."),
    ("16", "Where did you FIRST hear of Acquisition.com / The Hormozis?", "Instagram &middot; Facebook &middot; Twitter &middot; TikTok &middot; LinkedIn &middot; YouTube &middot; Podcasts/Audio &middot; Book(s) &middot; Other People&rsquo;s Shows", "Self-reported attribution, asked as FIRST touch. This is how they value the podcast and the books."),
    ("17", "Are you a full or part owner and can you decide how to allocate equity?", "YES &middot; NO", "Decision-maker gate, phrased as an equity question so it reads like due diligence."),
    ("19", "What&rsquo;s Your Best Email?", "&ldquo;(where I can send you more stuff to help)&rdquo;", "Email is question NINETEEN."),
    ("20", "Contact Information", "First Name &middot; Last Name &middot; Phone &middot; Company Name &middot; Company Website", "Phone arrives at question twenty, after full qualification."),
    ("22", "Do you want us to consider your company to become a portfolio company?", "&ldquo;If not, please select NO and we will remove your company from consideration and <b>only add you to our email list</b>.&rdquo;", "Even the opt-out puts you on the list, and says so out loud."),
]

qrows = "".join(
    f'<tr><td class="num">Q{n}</td><td><b>{q}</b><br><span style="color:var(--muted)">{o}</span></td>'
    f'<td>{note}</td></tr>' for n, q, o, note in Q)

app_body = f"""
<div class="hero"><div class="kick">The application</div>
<h1>An application to be invested in, that sells you a workshop when you fail</h1>
<p>JotForm <code>231197990495167</code>, embedded in a HubSpot page at /apply. The headline is
&ldquo;WE SCALE GREAT COMPANIES.&rdquo; Nothing about it reads as an order form.</p></div>

<section><div class="big"><h3>The mechanic, verbatim</h3>
<div class="q">Based on your answers, you&rsquo;d need to grow in order to qualify as a portfolio
company&hellip; and we&rsquo;d like to help. Would you like us to show you exactly what we&rsquo;d do to
scale your company? If so, click the button below to attend a <b>paid</b> workshop at our
Headquarters in Las Vegas.
<span class="src">JotForm 231197990495167, question 14 &middot; <span class="ev v">VERIFIED</span></span></div>
<p>You did not come to buy a workshop. You came to be considered for investment &mdash; the highest
status thing they offer. You answered revenue and profit three separate ways. Then the form told you,
based on <i>your own numbers</i>, that you are not big enough yet.</p>
<p>The $5,000 seat arrives as the remedy for a gap you just proved to yourself. That is a completely
different psychological position from &ldquo;buy my workshop&rdquo;, and it is why they can charge
$5,000 with no guarantee and no discount. <span class="ev r">READ</span></p></div></section>

<section><h2 class="sec">All 22 questions, in order</h2>
<p class="lede">Note where the contact details sit.</p>
<div class="tablewrap"><table>
<tr><th>#</th><th>Question &amp; options</th><th>What it is doing</th></tr>
{qrows}</table></div></section>

<section><h2 class="sec">The ordering is the trick</h2>
<div class="grid g2">
<div class="card"><h3>Qualification comes before contact</h3><p>Revenue is Q10-11. EBITDA is Q12-13
and again at Q15. Email is <b>Q19</b>. Phone is <b>Q20</b>. They make you invest nineteen answers
before they will take an address &mdash; and by then the sunk cost makes finishing near-automatic.</p></div>
<div class="card"><h3>Profit asked three ways</h3><p>Annual revenue, 12-month EBITDA, then 3-month
EBITDA. The short window catches anyone inflating the annual number, and the EBITDA framing itself
filters &mdash; an owner who cannot answer it is not the buyer.</p></div>
<div class="card"><h3>The example answer teaches the format</h3><p>&ldquo;Ex: I help dentists get more
patients using facebook ads for $2000 per month.&rdquo; One line that gets them a clean, gradeable
answer instead of a paragraph of waffle.</p></div>
<div class="card"><h3>Even the NO captures</h3><p>Q22&rsquo;s decline option says out loud that you will
&ldquo;only be added to our email list&rdquo;. There is no exit from this form that is not a list add.</p></div>
</div></section>
"""

# ---------------------------------------------------------------- STEAL
steal_body = """
<div class="hero"><div class="kick">What to steal</div><h1>Six moves that port to UGC World</h1>
<p>Their audience is $1M-$100M business owners and ours is creators, so the offer economics do not
transfer. The mechanics do. Ranked by how quickly you could run them.</p></div>

<section>
<div class="big"><h3>1. Make the application a gate to something better than the thing you sell</h3>
<p>This is the big one. Right now our application is understood by the applicant as
&ldquo;applying for the program&rdquo;. Theirs is understood as &ldquo;applying for investment&rdquo;,
and the program is what you get offered when you do not clear the bar.</p>
<p>The UGCW version is not literal investment. It is any higher-status tier: a managed roster, a
brand-partnership desk, a done-for-you placement. Applicants who do not clear it get told so by
their own numbers and offered the coaching as the route to clearing it next time. The DQ stops
being a rejection and becomes the pitch. <span class="ev r">READ &mdash; untested here</span></p></div>

<div class="big"><h3>2. Print the disqualifier on the sales page</h3>
<p>&ldquo;If you haven&rsquo;t made at least $5k from the free content, don&rsquo;t do it.&rdquo; One
sentence that filters, flexes and reframes the price as a proven multiple. Our equivalent is a hard,
public floor tied to the free content &mdash; and it takes the budget objection off the setter&rsquo;s
plate before the call.</p></div>

<div class="big"><h3>3. Two email tracks, not one</h3>
<p>A fresh track that never sells, interleaved with an evergreen selling track on a fixed loop. The
fresh one buys permission for the recycled one. We currently write everything fresh, which is why
email is a bottleneck. Write the selling loop once, then only ever write the fresh track.</p>
<p>Their loop is 56 days at every-other-day, so roughly 28 selling emails. That is a finite,
schedulable job, not a treadmill.</p></div>

<div class="big"><h3>4. Segment the lead magnet by the prospect&rsquo;s stage, then write only to that stage</h3>
<p>They do not send &ldquo;the roadmap&rdquo;. They send <i>Stage 4</i>, then three emails written for
Stage 4 only: day 1 the diagnosis, day 2 the symptom list, day 3 one complete tactic. Every symptom
lands because it was selected for that reader.</p>
<p>Our stages are obvious &mdash; no portfolio, portfolio but no inbound, inbound but no rate card,
booked but not consistent. Four roadmaps, four 3-email sequences. This is the highest-leverage thing
on this page for our DM objections, which are portfolio-perfectionism and no-system, both of which
are stage problems.</p></div>

<div class="big"><h3>5. Launch a dated SKU on top of the evergreen one instead of discounting</h3>
<p>The Scaling Workshop never goes on sale. Instead they launch Marketing in May and Offers in July
to the same list, sell out 110 seats in about 24 hours, then <b>mail the whole list that it sold
out</b> &mdash; including everyone who did not buy. That sold-out email is not a courtesy. It is the
proof that makes the next launch&rsquo;s deadline believable.</p></div>

<div class="big"><h3>6. Fire the setter off consumption, not off a form fill</h3>
<p>Ronney Mboche: &ldquo;saw you were going through some of Alex and Leila&rsquo;s resources
recently&hellip; is it a Supply problem or a Demand problem?&rdquo; Plain text, no links, no pitch, one
binary question, a reply requested. It reads as a human noticing, and the answer routes them.</p>
<p>Ours already has the trigger data. A two-option question beats &ldquo;how can I help?&rdquo;
because it is answerable in one word.</p></div>
</section>

<section><h2 class="sec">What NOT to copy</h2>
<div class="grid g2">
<div class="card"><h3>The no-guarantee position</h3><p>They can drop risk reversal entirely because
Alex Hormozi&rsquo;s name is the guarantee. Ours is not, yet. Removing our guarantee would cost close
rate, not add authority.</p></div>
<div class="card"><h3>The $5k price with no stack</h3><p>The sales page has no bonus stack, no value
build, no anchor. That works on a buyer who already consumed a 1.4M-copy book. Our buyer needs the
build.</p></div>
<div class="card"><h3>Two slugs for one page</h3><p>/workshop and /o-vegas are the same page. It
splits their reporting for no obvious gain and is a maintenance trap. <span class="ev r">READ</span></p></div>
<div class="card"><h3>Phone at Q20</h3><p>Their buyer will grind through 19 questions because the
prize is investment consideration. A creator will not. Port the ordering principle, not the length.</p></div>
</div></section>
"""

# ---------------------------------------------------------------- VSL
TR = open(os.path.join(D, "vsl_transcript.md"), encoding="utf-8").read()
_body = TR.split("---\n", 1)[1] if "---\n" in TR else TR
import re as _re
paras = []
for blk in [b.strip() for b in _body.split("\n\n") if b.strip()]:
    m = _re.match(r"\*\*\[(\d\d:\d\d:\d\d)\]\*\*\s*(.*)", blk, _re.S)
    if m:
        paras.append((m.group(1), m.group(2).strip()))
tr_html = "".join(
    f'<p><span class="ts">{t}</span> {esc(x)}</p>' for t, x in paras)

BEATS = [
    ("00:00:00", "Symptom stack, no claim",
     "Six &ldquo;have you ever&rdquo; symptoms before he says a single thing about himself. "
     "Vacation on the laptop, delegating feels risky, the knowledge is in your head, the team "
     "asks you everything, revenue dies if you get sick, guilty at work and guilty at home."),
    ("00:00:30", "Name the enemy",
     "&ldquo;key man risk&rdquo;. He gives the feeling a technical-sounding name, which makes it "
     "a solvable engineering problem rather than a personal failing."),
    ("00:00:46", "The reframe that does the work",
     "&ldquo;Most of the owners think that they own a business when in reality, they own a very "
     "expensive, high paying job.&rdquo;"),
    ("00:01:15", "One picture",
     "The bridge. A thousand people either side, and if you ARE the bridge, the second you leave "
     "everyone falls in and dies. He reuses &ldquo;the bridge&rdquo; as shorthand for the rest of the video."),
    ("00:01:32", "Proof, as autobiography",
     "He was the key man trying to sell Gym Launch. Fixed it over two years. Sold for "
     "<b>$46.2 million</b>. Portfolio now does $250M/yr. The proof arrives as the story of his own "
     "failure, not as a flex."),
    ("00:02:23", "Pre-empt &ldquo;my business is different&rdquo;",
     "&ldquo;there&rsquo;s the only four ways you can sell stuff&hellip; If you sell in any of those "
     "four ways, we have worked with a business like yours many, many, many times.&rdquo; Collapses "
     "every industry objection into one line."),
    ("00:02:30", "The four-part diagnostic",
     "Key man risk shows up in marketing, sales, product/delivery, or operations. The viewer "
     "self-diagnoses into a bucket &mdash; which is the same question Ronney asks by email."),
    ("00:03:09", "The twist",
     "&ldquo;the more valuable you become, the more of a key man you become&hellip; the better you "
     "get, the worse it is for the business.&rdquo; Punishes the exact behaviour his best prospects "
     "are proudest of."),
    ("00:04:43", "Anti-hype positioning",
     "&ldquo;this is not a room&hellip; a big rah rah&hellip; zero motivational talks. You like read "
     "all the reviews we have online. They&rsquo;re like zero hype, no BS. If anything, people were "
     "like, this is a lot.&rdquo; A negative review used as the proof."),
    ("00:05:31", "Anti-promise",
     "&ldquo;I can&rsquo;t promise that the rainbows are going to come in and unicorns are going to "
     "carry off in the distance.&rdquo; He kills the hype expectation himself, which is cheaper than "
     "a guarantee and does the same job."),
    ("00:06:17", "The real booking objection, named",
     "&ldquo;when you book a call, you can reserve a priority ticket, even if you need a little time "
     "to pick the exact date. It&rsquo;s one of the number one reasons people are like, I&rsquo;m not "
     "sure if I should book a call.&rdquo; He states the objection out loud and removes the date "
     "commitment from the booking decision."),
    ("00:06:40", "Urgency without a timer",
     "The doctor and the sore foot: waiting until it hurts less means it will be harder to walk. "
     "Then the busy-season handle &mdash; &ldquo;if you can learn how to fix the business in a busy "
     "season, then it&rsquo;ll be a breeze during an easy season&hellip; I&rsquo;ve yet to meet a "
     "business owner who says it&rsquo;s an easy season.&rdquo;"),
]
beat_rows = "".join(
    f'<tr><td class="num">{t}</td><td><b>{n}</b></td><td>{d}</td></tr>'
    for t, n, d in BEATS)

vsl_body = f"""
<div class="hero"><div class="kick">The VSL</div>
<h1>7 minutes 21 seconds, and no offer until 4:00</h1>
<p>Vidalytics player on /workshop and /o-vegas, id <code>dIKsAOKOfqVMrD08</code>, media
<code>DwsFbQ3odQ1m08bG</code>. The manifest is JS-negotiated and every direct guess returns 403 &mdash;
it was pulled by sniffing <code>stream.m3u8</code> out of the browser network log at 1080p.</p>
<p>The whole video is one idea: <b>key man risk</b>. You do not own a business, you own a very
expensive high-paying job, and you are the bridge everyone is standing on.</p></div>

<section><div class="grid g3">
<div class="stat"><div class="n">7:21</div><div class="l">runtime</div></div>
<div class="stat"><div class="n">2,087</div><div class="l">words</div></div>
<div class="stat"><div class="n">$46.2M</div><div class="l">Gym Launch exit, stated</div></div>
<div class="stat"><div class="n">1,000+</div><div class="l">businesses hosted, 2 yrs</div></div>
<div class="stat"><div class="n">~80</div><div class="l">average room size</div></div>
<div class="stat"><div class="n">0</div><div class="l">price mentions</div></div>
</div></section>

<section><h2 class="sec">The structure, beat by beat</h2>
<p class="lede">Note where the offer arrives: four minutes into a seven-minute video, and the price
is never said out loud &mdash; it is on the page instead.</p>
<div class="tablewrap"><table>
<tr><th>At</th><th>Beat</th><th>What it is doing</th></tr>
{beat_rows}</table></div></section>

<section><h2 class="sec">The lines worth keeping</h2>
<div class="q">Most of the owners think that they own a business when in reality, they own a very
expensive, high paying job.<span class="src">00:00:46 &middot; <span class="ev v">VERIFIED</span></span></div>
<div class="q">Your business is like a bridge. You have a thousand people on one side and a thousand
people on the other side of the bridge. But if you are the bridge, the second you leave, everyone
falls in the water and dies.<span class="src">00:01:15</span></div>
<div class="q">The more valuable you become, the more of a key man you become to your business. So
it&rsquo;s this double edged sword &mdash; the better you get, the worse it is for the
business.<span class="src">00:03:09</span></div>
<div class="q">Every day that you remain the key man, you are not building the business. You&rsquo;re
building a very comfortable prison.<span class="src">00:05:31</span></div>
<div class="q">I&rsquo;ve yet to meet a business owner who says it&rsquo;s an easy
season.<span class="src">00:07:03</span></div>
<div class="q">If there was one magic bullet that would actually solve a business, everyone would do
it, and it would only be magic bullets.<span class="src">00:04:43</span></div></section>

<section><h2 class="sec">What is NOT in it</h2>
<div class="grid g2">
<div class="card"><h3>No price</h3><p>Never spoken. The $5,000 sits in the FAQ underneath instead, so
the video never has to defend it.</p></div>
<div class="card"><h3>No bonus stack, no anchor</h3><p>No &ldquo;normally $X&rdquo;, no value build,
no countdown. The scarcity is physical &mdash; the room only holds so many.</p></div>
<div class="card"><h3>No testimonials in the video</h3><p>Social proof is a separate strip on the page.
The video is one man, one idea, one story.</p></div>
<div class="card"><h3>No guarantee</h3><p>Replaced by the anti-promise at 05:31. He tells you what he
will NOT claim, which buys more trust than a refund policy would.</p></div>
</div></section>

<section><h2 class="sec">Full transcript</h2>
<p class="lede">whisper.cpp <code>ggml-small.en</code>. Timestamps refer to the source recording in
<code>~/Downloads/ACQUISITION_COM_Swipe/Recording/</code>.</p>
<div class="card">{tr_html}</div></section>
"""

page("index.html", "Overview", index_body)
page("vsl.html", "The VSL", vsl_body)
page("funnel.html", "The pages", funnel_body)
page("emails.html", "The emails", emails_body)
page("application.html", "The application", app_body)
page("steal.html", "What to steal", steal_body)
print("board.html is built separately by build_board.py")
