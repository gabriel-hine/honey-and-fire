"""IT → EN translation pairs.

Hand-editable. This is the canonical store of translations consumed by
build_i18n.py. You can edit either side directly here, or edit en/index.html
and let build_i18n.py lift the hand edits back into this file on its next
run (it diffs the regenerated EN against the on-disk EN, finds the
non-matching translations, and rewrites this file).

Order matters when one IT phrase is a substring of another — put the more
specific match first.
"""

TRANSLATIONS = [
    (
        '<title>Honey & Fire — Musica dal Vivo</title>',
        '<title>Honey & Fire — Live Music</title>',
    ),
    (
        'content="Honey & Fire — Band di musica dal vivo per matrimoni, eventi privati e serate indimenticabili. Soul, pop, funk, rock e classici italiani."',
        'content="Honey & Fire — Live music band for weddings, private events and unforgettable nights. Soul, pop, funk, rock and Italian classics."',
    ),
    (
        'content="Honey & Fire — Musica dal Vivo"',
        'content="Honey & Fire — Live Music"',
    ),
    (
        'content="Band di musica dal vivo per matrimoni, eventi privati e serate indimenticabili."',
        'content="Live music band for weddings, private events and unforgettable nights."',
    ),
    (
        '<li><a href="#chi-siamo">Chi Siamo</a></li>',
        '<li><a href="#chi-siamo">About</a></li>',
    ),
    (
        '<li><a href="#la-band">La Band</a></li>',
        '<li><a href="#la-band">The Band</a></li>',
    ),
    (
        '<li><a href="#eventi">Eventi</a></li>',
        '<li><a href="#eventi">Events</a></li>',
    ),
    (
        '<li><a href="#galleria">Galleria</a></li>',
        '<li><a href="#galleria">Gallery</a></li>',
    ),
    (
        '<li><a href="#repertorio">Repertorio</a></li>',
        '<li><a href="#repertorio">Repertoire</a></li>',
    ),
    (
        '<li><a href="#contatti">Contatti</a></li>',
        '<li><a href="#contatti">Contact</a></li>',
    ),
    (
        '<p>Musica dal vivo per matrimoni, eventi privati <br />e serate indimenticabili</p>',
        '<p>Live music for weddings, private events <br />and unforgettable nights</p>',
    ),
    (
        '<a href="#chi-siamo" class="button style2 down">Scopri di pi&ugrave;</a>',
        '<a href="#chi-siamo" class="button style2 down">Discover</a>',
    ),
    (
        '<h2>Chi Siamo</h2>',
        '<h2>About Us</h2>',
    ),
    (
        ('<p><strong>Honey &amp; Fire</strong> &egrave; una band di sei musicisti che porta\n'
     '\t\t\t\t\tenergia e passione in ogni evento. Due voci femminili straordinarie &mdash;\n'
     '\t\t\t\t\t<em>Honey</em> e <em>Fire</em> &mdash; accompagnate da basso, chitarra,\n'
     '\t\t\t\t\ttastiere e batteria.</p>'),
        ('<p><strong>Honey &amp; Fire</strong> is a six-piece band that brings\n'
     '\t\t\t\t\tenergy and passion to every event. Two extraordinary female vocalists &mdash;\n'
     '\t\t\t\t\t<em>Honey</em> and <em>Fire</em> &mdash; backed by bass, guitar,\n'
     '\t\t\t\t\tkeyboards and drums.</p>'),
    ),
    (
        ('<p>Dai matrimoni eleganti alle feste private, dagli eventi aziendali\n'
     '\t\t\t\t\talle serate in locale: il nostro repertorio spazia dal soul al pop,\n'
     '\t\t\t\t\tdal funk al rock, dai grandi classici italiani ai successi internazionali, pi&ugrave; qualche chicca fuori dal coro.</p>'),
        ('<p>From elegant weddings to private parties, from corporate events\n'
     '\t\t\t\t\tto club nights: our repertoire spans soul to pop, funk to rock,\n'
     '\t\t\t\t\tItalian classics to international hits, plus a few off-the-beaten-path gems.</p>'),
    ),
    (
        ('<p>Ogni esibizione &egrave; un viaggio musicale su misura per rendere\n'
     '\t\t\t\t\til vostro evento unico e indimenticabile.</p>'),
        ('<p>Every performance is a tailored musical journey to make your\n'
     '\t\t\t\t\tevent unique and unforgettable.</p>'),
    ),
    (
        '<a href="#la-band" class="button style2 down anchored">Avanti</a>',
        '<a href="#la-band" class="button style2 down anchored">Next</a>',
    ),
    (
        '<h2>La Band</h2>',
        '<h2>The Band</h2>',
    ),
    (
        "<p>Un'unica passione</p>",
        '<p>One shared passion</p>',
    ),
    (
        '<p class="member-role">Chitarra</p>',
        '<p class="member-role">Guitar</p>',
    ),
    (
        '<p class="member-role">Tastiere</p>',
        '<p class="member-role">Keyboards</p>',
    ),
    (
        '<p class="member-role">Basso</p>',
        '<p class="member-role">Bass</p>',
    ),
    (
        '<p class="member-role">Batteria</p>',
        '<p class="member-role">Drums</p>',
    ),
    (
        '<h2>Prossimi Eventi</h2>',
        '<h2>Upcoming Events</h2>',
    ),
    (
        '<p>Le prossime serate dal vivo</p>',
        '<p>Our next live shows</p>',
    ),
    (
        '<span class="event-card-date">Gioved&igrave; 21 Maggio &middot; ore 20:00</span>',
        '<span class="event-card-date">Thursday, May 21 &middot; 8:00 PM</span>',
    ),
    (
        '<p class="event-card-meta">Via Litoranea 24, Ostia (RM)</p>',
        '<p class="event-card-meta">Via Litoranea 24, Ostia (Rome)</p>',
    ),
    (
        '<span class="event-card-cta">Scopri di pi&ugrave; &rarr;</span>',
        '<span class="event-card-cta">Learn more &rarr;</span>',
    ),
    (
        '<h2>Galleria</h2>',
        '<h2>Gallery</h2>',
    ),
    (
        '<p>Momenti dai nostri eventi</p>',
        '<p>Moments from our shows</p>',
    ),
    (
        '<h2>Repertorio</h2>',
        '<h2>Repertoire</h2>',
    ),
    (
        '<p>Oltre 75 brani per ogni momento della vostra serata</p>',
        '<p>Over 75 songs for every moment of your night</p>',
    ),
    (
        '>Tutti</button>',
        '>All</button>',
    ),
    (
        '>Italiano</button>',
        '>Italian</button>',
    ),
    (
        'placeholder="Cerca brano o artista..."',
        'placeholder="Search by song or artist..."',
    ),
    (
        '<p class="repertorio-footer">...e molto altro!</p>',
        '<p class="repertorio-footer">...and many more!</p>',
    ),
    (
        '<h2>Contattaci</h2>',
        '<h2>Contact Us</h2>',
    ),
    (
        '<p>Raccontaci il tuo evento e creeremo insieme la colonna sonora perfetta</p>',
        "<p>Tell us about your event and together we'll create the perfect soundtrack</p>",
    ),
    (
        'Design: <a href="https://gabrielhine.io/v-card.html" target="_blank" rel="noopener">gabrielhine.io</a> &mdash; contattami se ti piace il sito!',
        'Design: <a href="https://gabrielhine.io/v-card.html" target="_blank" rel="noopener">gabrielhine.io</a> &mdash; get in touch if you like the site!',
    ),
    (
        '<!-- Chi Siamo -->',
        '<!-- About Us -->',
    ),
    (
        '<!-- La Band -->',
        '<!-- The Band -->',
    ),
    (
        '<!-- Prossimi Eventi -->',
        '<!-- Upcoming Events -->',
    ),
    (
        '<!-- Galleria -->',
        '<!-- Gallery -->',
    ),
    (
        '<!-- Repertorio -->',
        '<!-- Repertoire -->',
    ),
    (
        '<!-- Contatti -->',
        '<!-- Contact -->',
    ),
]
