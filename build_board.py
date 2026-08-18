#!/usr/bin/env python3
"""Acquisition.com — Scaling Workshop wired board.

One pannable canvas. Every funnel step is the real captured screenshot.

The spine: free content and books feed a HubSpot list -> a two-track email
machine (an evergreen selling loop on an exact 56-day repeat, interleaved with
a never-repeated Mozi Minute) -> a JotForm application that is framed as
applying to become a PORTFOLIO COMPANY -> you fail the revenue gate -> you get
downsold into a $5,000 seat at a 2-day workshop in Vegas.

Layout rule: one column per funnel STEP. Parallel variants stack vertically
inside that column so an arrow never crosses a card it is not pointing at.

Run:  python3 build_board.py   ->  board.html
"""
import os, sys

sys.path.insert(0, os.path.expanduser("~/scripts/_swipe_builder"))
import boardbuild

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "media", "full")


def img(n):
    return os.path.join(M, n + ".png")


SHOTS = {
    "home": dict(img=img("05_Homepage"), col=2, y=140, lane="ever",
                 step="STEP 1 — FRONT DOOR", title="acquisition.com (homepage)",
                 url="https://www.acquisition.com/",
                 note="Four free courses stacked above one paid CTA. "
                      "&ldquo;Attend a Workshop&rdquo; is the only button on the "
                      "page that costs money, and it points at /o-vegas."),
    "books": dict(img=img("10_Books_hub"), col=2, y=1180, lane="ever",
                  step="STEP 1 — FRONT DOOR", title="Books hub",
                  url="https://www.acquisition.com/books",
                  note="$100M Offers has sold 1.4M copies. The book is the "
                       "cheapest possible entry to the same list. Will bought "
                       "$100M Money Models in Aug 2025 &mdash; that is how he "
                       "entered this funnel."),
    "course": dict(img=img("06_Free_course_-_Scaling"), col=3, y=140, lane="ever",
                   step="STEP 2 — THE GATE", title="Free course opt-in (Scaling)",
                   url="https://www.acquisition.com/training/scalingstart",
                   note="All FOUR free courses use the SAME HubSpot form id "
                        "43c2570a-9455-4388-820d-dfe287669afb. One list, four "
                        "doors. Two-step form: email first, then name + phone."),
    "course2": dict(img=img("09_Free_course_-_Money_Models"), col=3, y=1000, lane="ever",
                    step="STEP 2 — THE GATE", title="Free course (Money Models)",
                    url="https://www.acquisition.com/training/money/context",
                    note="Identical shell, different course. Every one of them "
                         "carries the same in-page block: &ldquo;Meet the "
                         "Acquisition.com Team for a private workshop in "
                         "Vegas.&rdquo; The paid offer is inside the free product."),
    "workshop": dict(img=img("01_Workshop_sales_page"), col=5, y=140, lane="event",
                     step="STEP 4 — SALES PAGE", title="Scaling Workshop &mdash; $5,000/seat",
                     url="https://www.acquisition.com/workshop",
                     note="Price stated ON the page. Vidalytics VSL, three "
                          "identical CTAs all anchoring to #booking-widget, "
                          "then an FAQ that does the disqualifying."),
    "offers": dict(img=img("02_Offers_Workshop_sales_page"), col=5, y=2050, lane="event",
                   step="STEP 4 — SALES PAGE", title="Offers Workshop (2nd SKU)",
                   url="https://www.acquisition.com/offers-workshop",
                   note="&ldquo;BUILD OFFERS SO GOOD THEY SCALE WITHOUT YOU.&rdquo; "
                        "Sold out 110/110 on 24 Jul 2026. CTA is now #waitlist "
                        "&mdash; a hidden HubSpot form that captures phone."),
    "ovegas": dict(img=img("03_Vegas_event_page_o-vegas"), col=5, y=3900, lane="event",
                   step="STEP 4 — SALES PAGE", title="/o-vegas (duplicate page)",
                   url="https://www.acquisition.com/o-vegas",
                   note="Byte-for-byte the same page as /workshop, different "
                        "slug, same Vidalytics id dIKsAOKOfqVMrD08. The "
                        "homepage sends traffic here; email sends it to "
                        "/workshop. Two slugs, one page, split reporting."),
    "apply": dict(img=img("04_Application"), col=6, y=140, lane="event",
                  step="STEP 5 — APPLICATION", title="The application (JotForm)",
                  url="https://www.acquisition.com/apply",
                  note="JotForm 231197990495167. Headline is &ldquo;WE SCALE "
                       "GREAT COMPANIES&rdquo; &mdash; you believe you are "
                       "applying for investment, not for a seat."),
}

DATA = {
    "traffic": dict(col=1, y=140, lane="ever", step="TRAFFIC",
                    title="Owned audience, not paid acquisition",
                    kv=[("Pixels live", "Meta, TikTok, Snap, Reddit"),
                        ("Attribution", "Hyros (t.acquisition.com)"),
                        ("Podcast attribution", "Podscribe"),
                        ("Tag manager", "GTM-MHT26J7X"),
                        ("CMS / CRM", "HubSpot 21368823"),
                        ("Consent", "Cookiebot")],
                    note="Every major pixel is loaded, plus Podscribe for "
                         "podcast attribution &mdash; they measure the podcast "
                         "as a paid channel. VERIFIED from the rendered HTML."),
    "email": dict(col=4, y=140, lane="ever", step="STEP 3 — THE MACHINE",
                  title="Two-track email machine",
                  kv=[("Sender", "value@acquisition.com"),
                      ("Cadence", "every 2 days, ~15:00 UTC"),
                      ("Track A", "evergreen selling loop"),
                      ("Loop length", "EXACTLY 56 days"),
                      ("Track B", "&ldquo;Mozi Minute:&rdquo; &mdash; never repeats"),
                      ("Emails in Will's inbox", "77 from this sender")],
                  note="THE finding. Track A recycles on a hard 56-day clock: "
                       "&ldquo;Behind the scenes of our workshops&rdquo; ran 23 May "
                       "and again 18 Jul. &ldquo;Are you the bottleneck?&rdquo; 13 May "
                       "and 8 Jul. 23 subject lines checked, zero exceptions. "
                       "Track B is fresh every time and never sells."),
    "roadmap": dict(col=4, y=1050, lane="ever", step="STEP 3 — THE MACHINE",
                    title="Scaling Roadmap &mdash; segmented lead magnet",
                    kv=[("Delivered as", "Stage-specific PDF + video"),
                        ("Will's segment", "Stage 4 (5-9 employees)"),
                        ("Follow-up", "3 emails, same stage"),
                        ("Every one ends", "&ldquo;see if you qualify&rdquo;")],
                    note="They do not send one lead magnet. They diagnose your "
                         "stage and send THAT stage's PDF, then run a 3-email "
                         "sequence written only for people at that stage. Day 1 "
                         "the diagnosis, day 2 the symptom list, day 3 one "
                         "tactic (the 80/20 customer audit). Workshop pitch in "
                         "the P.S. of all three."),
    "booking": dict(col=7, y=140, lane="event", step="STEP 6 — BOOKING",
                    title="iClosed booking widget",
                    url="https://app.iclosed.io/e/Acquisition/acquisition-com-scaling-workshop",
                    kv=[("Tool", "iClosed (not Calendly)"),
                        ("Embed", "inline iframe on /workshop"),
                        ("A/B variant seen", "workshop-v1 &middot; lp_var 4080-v1"),
                        ("Meeting name", "ACQ Scaling Workshop Meeting")],
                    note="Booking is embedded in the page, not a redirect. The "
                         "referrerUrl in the iframe leaks that the page Will "
                         "landed on was /workshop-v1 with an lp_var &mdash; they "
                         "are split-testing the sales page."),
    "setters": dict(col=8, y=140, lane="event", step="STEP 7 — SETTER",
                    title="Named human setters, from a real @acquisition.com address",
                    kv=[("Seen in Will's inbox", "3 reps"),
                        ("Braeden Bowman", "May 2026 call"),
                        ("Coleman Burgess", "Jul 2026 call"),
                        ("Ronney Mboche", "cold re-engagement"),
                        ("Reminders per booking", "4")],
                    note="Titled &ldquo;Consultant&rdquo;, never &ldquo;setter&rdquo;. "
                         "Ronney's email opens &ldquo;saw you were going through "
                         "some of Alex and Leila's resources recently&rdquo; and "
                         "signs off &ldquo;P.S. YES I'm a real human haha&rdquo;."),
    "product": dict(col=9, y=140, lane="event", step="STEP 8 — THE PRODUCT",
                    title="2 days, in person, Las Vegas HQ",
                    kv=[("Price", "$5,000 per seat"),
                        ("Capacity", "~100 seats"),
                        ("Day 1", "frameworks, presented"),
                        ("Day 2", "roundtables by revenue band"),
                        ("Deliverable", "3-5 tactical next steps + packet"),
                        ("Guarantee", "NONE")],
                    note="No guarantee anywhere on the page. The risk reversal "
                         "is entirely social &mdash; the room, the directors' "
                         "salaries, and the sold-out proof."),
    "seq": dict(col=6, y=1500, lane="event", step="STEP 5 — APPLICATION",
                title="The 22-question branching application",
                kv=[("Q1", "own / want to start / want to sell"),
                    ("Q10", "annual revenue band"),
                    ("Q12", "EBITDA, last 12 months"),
                    ("Q15", "EBITDA, last 3 months"),
                    ("Q16", "where you FIRST heard of them"),
                    ("Q17", "can you allocate equity?"),
                    ("Q22", "consider you as a portfolio co?")],
                note="Revenue and profit are asked THREE separate ways before "
                     "any contact detail. Email is Q19, phone is Q20 &mdash; "
                     "they qualify you completely before they will even take "
                     "your address."),
    "skus": dict(col=9, y=1150, lane="event", step="STEP 8 — THE PRODUCT",
                 title="Three workshop SKUs off one list",
                 kv=[("Scaling Workshop", "always-on, $5,000"),
                     ("Offers Workshop", "launched 10 Jul, sold out 24 Jul"),
                     ("Marketing Workshop", "launched 15 May 2026"),
                     ("Sell-out claim", "&ldquo;last one sold out in ~24 hours&rdquo;"),
                     ("Offers seats", "110, two dates")],
                 note="The evergreen Scaling Workshop is the floor. On top of "
                      "it they LAUNCH a new named workshop every few months to "
                      "the same list, which manufactures a real deadline "
                      "without ever discounting the evergreen one."),
}

BRANCH = [
    dict(x=boardbuild.X[6], y=2450, state="good", cond="IF revenue / EBITDA is too small",
         body="Q14 fires: &ldquo;Based on your answers, you&rsquo;d need to grow in order to "
              "qualify as a portfolio company&hellip; and we&rsquo;d like to help. Would you "
              "like us to show you exactly what we&rsquo;d do to scale your company? If so, "
              "click the button below to attend a <b>paid</b> workshop at our Headquarters "
              "in Las Vegas.&rdquo; The $5,000 workshop is the consolation prize for FAILING "
              "an application to something more prestigious.",
         ev="VERIFIED &mdash; JotForm 231197990495167, question 14, verbatim"),
    dict(x=boardbuild.X[5], y=5750, state="good", cond="SELF-DISQUALIFICATION, on the sales page",
         body="&ldquo;If you are under 250k/yr this is not a fit (yet.)&rdquo; and &ldquo;If you "
              "haven&rsquo;t made at least $5k from the free content, don&rsquo;t do it.&rdquo; "
              "They print the floor in the FAQ so the setter never has to argue it, and it "
              "doubles as a flex: the free stuff is worth $5k on its own.",
         ev="VERIFIED &mdash; acquisition.com/workshop FAQ, captured 11 Aug 2026"),
    dict(x=boardbuild.X[8], y=1000, state="good", cond="IF the phone number looks dead",
         body="Braeden Bowman, 90 minutes before Will&rsquo;s call: &ldquo;we&rsquo;ve been "
              "sending a few texts to +1 626-385-8203 and haven&rsquo;t gotten any response "
              "yet. Is this the best phone number to reach you on?&rdquo; then &ldquo;before "
              "our call &mdash; would you be able to watch this quick video of Alex? It&rsquo;ll "
              "help save time!&rdquo; A show-rate play disguised as a data-hygiene question.",
         ev="VERIFIED &mdash; braeden.bowman@acquisition.com, 4 May 2026, Will&rsquo;s inbox"),
    dict(x=boardbuild.X[7], y=1000, state="warn", cond="PRE-CALL CONSUMPTION",
         body="Both booking paths push a video to watch BEFORE the call, and the post-purchase "
              "sequence has its own private video sent to buyers &ldquo;as they prepared to fly "
              "out to our HQ&rdquo;. Alex then recycles that same post-purchase video back into "
              "the cold list as an email &mdash; &ldquo;Private video from me&rdquo;.",
         ev="PARTIALLY VERIFIED &mdash; email text confirms the video, the buyer sequence itself is not captured"),
    dict(x=boardbuild.X[4], y=1950, state="warn", cond="RE-ENGAGEMENT ON BEHAVIOUR",
         body="Ronney Mboche, 17 Jul: &ldquo;saw you were going through some of Alex and "
              "Leila&rsquo;s resources recently. Quick question: is it a <b>Supply problem</b> or "
              "a <b>Demand problem?</b>&rdquo; One binary question, a reply asked for, no link, "
              "no pitch. Fires off content consumption, not off a form fill.",
         ev="VERIFIED &mdash; ronney.mboche@acquisition.com, 17 Jul 2026"),
    dict(x=boardbuild.X[2], y=2350, state="unver", cond="MISSING FROM THIS CAPTURE",
         body="Not captured: the post-opt-in confirmation page, the buyer/post-purchase "
              "sequence, the SMS thread (they text &mdash; Braeden&rsquo;s email proves it), the "
              "iClosed booking flow past the embed, and the workshop room itself. Opting in "
              "would need Will&rsquo;s approval and the phone field is a hard stop under the "
              "swipe rules.",
         ev="UNVERIFIED &mdash; named, not guessed"),
]

EDGES = [
    ("traffic", "home", "h"), ("home", "course", "h"), ("books", "course", "h"),
    ("course", "email", "h"), ("course2", "email", "h"),
    ("email", "workshop", "h"), ("roadmap", "workshop", "h"),
    ("email", "roadmap", "v"),
    ("workshop", "apply", "h"), ("offers", "apply", "h"), ("ovegas", "apply", "h"),
    ("apply", "seq", "v"),
    ("apply", "booking", "h"), ("booking", "setters", "h"), ("setters", "product", "h"),
    ("product", "skus", "v"),
    ("home", "books", "v"), ("course", "course2", "v"),
    ("workshop", "offers", "v"), ("offers", "ovegas", "v"),
]

LABELS = [
    dict(x=boardbuild.X[1], y=60, t="FREE &mdash; owned audience"),
    dict(x=boardbuild.X[5], y=60, t="PAID &mdash; $5,000 seat"),
]

cfg = dict(
    OUT=os.path.join(HERE, "board.html"),
    TITLE="Acquisition.com &mdash; the Scaling Workshop funnel",
    KICK="Swipe &middot; captured 11 August 2026 &middot; F133",
    BLURB="Alex and Leila Hormozi sell a $5,000 seat at a 2-day workshop at their Las Vegas HQ. "
          "There is no webinar, no VSL funnel and no paid acquisition to speak of. The whole "
          "machine is: give away four full courses and a 1.4M-copy book, mail the list every "
          "two days forever on an exact 56-day loop, then route everyone into an application "
          "for something they cannot have &mdash; becoming a portfolio company &mdash; and sell "
          "the workshop as the consolation prize for failing it. Will is inside this funnel "
          "himself: he bought the book in Aug 2025 and has booked their call twice.",
    SHOTS=SHOTS, DATA=DATA, BRANCH=BRANCH, EDGES=EDGES, LABELS=LABELS,
    LEGEND=[("ever", "Free / evergreen &mdash; the content engine"),
            ("event", "Paid &mdash; the $5,000 workshop path")],
    HOME="index.html",
)

boardbuild.build(cfg)
