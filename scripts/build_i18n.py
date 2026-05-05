#!/usr/bin/env python3
"""Generate en/index.html from index.html (the Italian master).

The IT page is the single source of truth — edit headings, copy and
markup there. This script applies a list of (IT → EN) string
replacements and a small set of lang-specific adjustments
(canonical/og URLs, asset path prefixes, language-switcher active
state, hreflang, etc.) to produce en/index.html.

Workflow on a content change:

    1. edit index.html
    2. python scripts/build_i18n.py
    3. python scripts/cache-bust.py
    4. git commit + push

Each translation pair must match exactly once in the source. The
script bails loudly if a string is missing or matches multiple times,
so silent drift is impossible.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
DST = ROOT / "en" / "index.html"


# --- IT → EN translation pairs ------------------------------------------------
# Add a new entry here whenever the IT page introduces translatable copy.
# Order matters when later strings are substrings of earlier ones — put the
# more specific match first.
TRANSLATIONS = [
    # <title>
    ("<title>Honey & Fire — Musica dal Vivo</title>",
     "<title>Honey & Fire — Live Music</title>"),

    # Meta description
    ('content="Honey & Fire — Band di musica dal vivo per matrimoni, eventi privati e serate indimenticabili. Soul, pop, funk, rock e classici italiani."',
     'content="Honey & Fire — Live music band for weddings, private events and unforgettable nights. Soul, pop, funk, rock and Italian classics."'),

    # Open Graph
    ('content="Honey & Fire — Musica dal Vivo"',
     'content="Honey & Fire — Live Music"'),
    ('content="Band di musica dal vivo per matrimoni, eventi privati e serate indimenticabili."',
     'content="Live music band for weddings, private events and unforgettable nights."'),

    # Nav menu
    ('<li><a href="#chi-siamo">Chi Siamo</a></li>',
     '<li><a href="#chi-siamo">About</a></li>'),
    ('<li><a href="#la-band">La Band</a></li>',
     '<li><a href="#la-band">The Band</a></li>'),
    ('<li><a href="#eventi">Eventi</a></li>',
     '<li><a href="#eventi">Events</a></li>'),
    ('<li><a href="#galleria">Galleria</a></li>',
     '<li><a href="#galleria">Gallery</a></li>'),
    ('<li><a href="#repertorio">Repertorio</a></li>',
     '<li><a href="#repertorio">Repertoire</a></li>'),
    ('<li><a href="#contatti">Contatti</a></li>',
     '<li><a href="#contatti">Contact</a></li>'),

    # Hero
    ('<p>Musica dal vivo per matrimoni, eventi privati <br />e serate indimenticabili</p>',
     '<p>Live music for weddings, private events <br />and unforgettable nights</p>'),
    ('<a href="#chi-siamo" class="button style2 down">Scopri di pi&ugrave;</a>',
     '<a href="#chi-siamo" class="button style2 down">Discover</a>'),

    # Chi Siamo / About
    ('<h2>Chi Siamo</h2>', '<h2>About Us</h2>'),
    ('<p><strong>Honey &amp; Fire</strong> &egrave; una band di sei musicisti che porta\n'
     '\t\t\t\t\tenergia e passione in ogni evento. Due voci femminili straordinarie &mdash;\n'
     '\t\t\t\t\t<em>Honey</em> e <em>Fire</em> &mdash; accompagnate da basso, chitarra,\n'
     '\t\t\t\t\ttastiere e batteria.</p>',
     '<p><strong>Honey &amp; Fire</strong> is a six-piece band that brings\n'
     '\t\t\t\t\tenergy and passion to every event. Two extraordinary female vocalists &mdash;\n'
     '\t\t\t\t\t<em>Honey</em> and <em>Fire</em> &mdash; backed by bass, guitar,\n'
     '\t\t\t\t\tkeyboards and drums.</p>'),
    ('<p>Dai matrimoni eleganti alle feste private, dagli eventi aziendali\n'
     '\t\t\t\t\talle serate in locale: il nostro repertorio spazia dal soul al pop,\n'
     '\t\t\t\t\tdal funk al rock, dai grandi classici italiani ai successi internazionali, pi&ugrave; qualche chicca fuori dal coro.</p>',
     '<p>From elegant weddings to private parties, from corporate events\n'
     '\t\t\t\t\tto club nights: our repertoire spans soul to pop, funk to rock,\n'
     '\t\t\t\t\tItalian classics to international hits, plus a few off-the-beaten-path gems.</p>'),
    ('<p>Ogni esibizione &egrave; un viaggio musicale su misura per rendere\n'
     '\t\t\t\t\til vostro evento unico e indimenticabile.</p>',
     "<p>Every performance is a tailored musical journey to make your\n"
     "\t\t\t\t\tevent unique and unforgettable.</p>"),
    ('<a href="#la-band" class="button style2 down anchored">Avanti</a>',
     '<a href="#la-band" class="button style2 down anchored">Next</a>'),

    # La Band / The Band
    ("<h2>La Band</h2>", "<h2>The Band</h2>"),
    ("<p>Un'unica passione</p>", "<p>One shared passion</p>"),
    ('<p class="member-role">Chitarra</p>', '<p class="member-role">Guitar</p>'),
    ('<p class="member-role">Tastiere</p>', '<p class="member-role">Keyboards</p>'),
    ('<p class="member-role">Basso</p>', '<p class="member-role">Bass</p>'),
    ('<p class="member-role">Batteria</p>', '<p class="member-role">Drums</p>'),

    # Eventi / Events
    ("<h2>Prossimi Eventi</h2>", "<h2>Upcoming Events</h2>"),
    ("<p>Le prossime serate dal vivo</p>", "<p>Our next live shows</p>"),
    ('<span class="event-card-date">Gioved&igrave; 21 Maggio &middot; ore 20:00</span>',
     '<span class="event-card-date">Thursday, May 21 &middot; 8:00 PM</span>'),
    ('<p class="event-card-meta">Via Litoranea 24, Ostia (RM)</p>',
     '<p class="event-card-meta">Via Litoranea 24, Ostia (Rome)</p>'),
    ('<span class="event-card-cta">Scopri di pi&ugrave; &rarr;</span>',
     '<span class="event-card-cta">Learn more &rarr;</span>'),

    # Galleria / Gallery
    ("<h2>Galleria</h2>", "<h2>Gallery</h2>"),
    ("<p>Momenti dai nostri eventi</p>", "<p>Moments from our shows</p>"),

    # Repertorio / Repertoire
    ("<h2>Repertorio</h2>", "<h2>Repertoire</h2>"),
    ("<p>Oltre 75 brani per ogni momento della vostra serata</p>",
     "<p>Over 75 songs for every moment of your night</p>"),
    (">Tutti</button>", ">All</button>"),
    (">Italiano</button>", ">Italian</button>"),
    ('placeholder="Cerca brano o artista..."',
     'placeholder="Search by song or artist..."'),
    ('<p class="repertorio-footer">...e molto altro!</p>',
     '<p class="repertorio-footer">...and many more!</p>'),

    # Contatti / Contact
    ("<h2>Contattaci</h2>", "<h2>Contact Us</h2>"),
    ("<p>Raccontaci il tuo evento e creeremo insieme la colonna sonora perfetta</p>",
     "<p>Tell us about your event and together we'll create the perfect soundtrack</p>"),

    # Footer attribution
    ('Design: <a href="https://gabrielhine.io/v-card.html" target="_blank" rel="noopener">gabrielhine.io</a> &mdash; contattami se ti piace il sito!',
     'Design: <a href="https://gabrielhine.io/v-card.html" target="_blank" rel="noopener">gabrielhine.io</a> &mdash; get in touch if you like the site!'),

    # Section comments — invisible to users but nice to keep tidy.
    ("<!-- Chi Siamo -->", "<!-- About Us -->"),
    ("<!-- La Band -->", "<!-- The Band -->"),
    ("<!-- Prossimi Eventi -->", "<!-- Upcoming Events -->"),
    ("<!-- Galleria -->", "<!-- Gallery -->"),
    ("<!-- Repertorio -->", "<!-- Repertoire -->"),
    ("<!-- Contatti -->", "<!-- Contact -->"),
]


def main() -> int:
    text = SRC.read_text()

    # 1) Apply IT → EN string substitutions, requiring an exact single match.
    missing = []
    multi = []
    for it_str, en_str in TRANSLATIONS:
        n = text.count(it_str)
        if n == 0:
            missing.append(it_str[:80])
            continue
        if n > 1:
            multi.append((it_str[:80], n))
            continue
        text = text.replace(it_str, en_str, 1)

    if missing or multi:
        for s in missing:
            sys.stderr.write(f"MISSING in source: {s!r}\n")
        for s, n in multi:
            sys.stderr.write(f"AMBIGUOUS ({n}x match): {s!r}\n")
        return 1

    # 2) Document language attribute.
    text = text.replace('<html lang="it">', '<html lang="en">', 1)

    # 3) Canonical + Open Graph URLs point at /en/ on the EN page.
    text = text.replace(
        '<link rel="canonical" href="https://www.honeyandfire.band/" />',
        '<link rel="canonical" href="https://www.honeyandfire.band/en/" />',
        1,
    )
    text = text.replace(
        'property="og:url" content="https://www.honeyandfire.band/"',
        'property="og:url" content="https://www.honeyandfire.band/en/"',
        1,
    )

    # 4) Local asset paths: index.html lives at root, en/index.html one
    # folder deep. Rewrite href/src that start with assets/ or images/.
    text = re.sub(
        r'((?:href|src)=")(assets/|images/)',
        r"\1../\2",
        text,
    )
    # Locandina + .ics live at root too.
    text = text.replace(
        'href="locandina-260521.html"', 'href="../locandina-260521.html"'
    )
    text = text.replace(
        'href="honey-and-fire-260521.ics"',
        'href="../honey-and-fire-260521.ics"',
    )

    # 5) Language switcher: flip the active state to UK on the EN page.
    text = text.replace(
        '<li class="nav-lang nav-lang-active" aria-current="page">\n'
        '\t\t\t\t\t\t\t<a href="/" hreflang="it"',
        '<li class="nav-lang">\n\t\t\t\t\t\t\t<a href="/" hreflang="it"',
        1,
    )
    text = text.replace(
        '<li class="nav-lang">\n\t\t\t\t\t\t\t<a href="/en/" hreflang="en"',
        '<li class="nav-lang nav-lang-active" aria-current="page">\n'
        '\t\t\t\t\t\t\t<a href="/en/" hreflang="en"',
        1,
    )

    # 6) SVG clipPath id distinguishes the two pages so the inline
    # SVG block stays self-contained when both are crawled.
    text = text.replace('id="uk-clip-it"', 'id="uk-clip-en"')
    text = text.replace("url(#uk-clip-it)", "url(#uk-clip-en)")

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(text)
    print(f"wrote {DST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
