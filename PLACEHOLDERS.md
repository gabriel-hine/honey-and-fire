# Honey & Fire — Placeholder Checklist

## Immagini sfondi sezione
- [ ] `#hero` in `main.css` — Foto hero band (1920x1080+, band sul palco)
- [ ] `#chi-siamo` in `main.css` — Foto Chi Siamo (1920x1080+, venue/palco)

## Foto membri (`images/members/`)
- [ ] `honey.jpg` — Honey, voce (400x400, quadrata)
- [ ] `fire.jpg` — Fire, voce (400x400, quadrata)
- [ ] `bass.jpg` — Bassista (400x400, quadrata)
- [ ] `guitar.jpg` — Chitarrista (400x400, quadrata)
- [ ] `keys.jpg` — Tastierista (400x400, quadrata)
- [ ] `drums.jpg` — Batterista (400x400, quadrata)

## Galleria (`images/thumbs/` + `images/fulls/`)
- [ ] 01-06.jpg — Sostituire con foto reali di eventi/concerti
  - thumbs: 400x300 circa
  - fulls: 1200x800+ circa

## Contenuti in `index.html`
- [ ] Bio dei membri (sezione La Band)
- [ ] Nomi dei musicisti (basso, chitarra, tastiere, batteria)
- [ ] YouTube video ID (sezione Video — sostituire l'embed URL)
- [ ] Numero di telefono (sezione Contatti)
- [ ] Email (sezione Contatti)
- [ ] URL Instagram (sezione Contatti + footer)
- [ ] URL Facebook (sezione Contatti + footer)
- [ ] URL YouTube (footer)
- [ ] Form action Formspree (registrarsi su https://formspree.io, creare endpoint)
- [ ] Favicon

## Nota
Quando sostituite le foto placeholder dei membri, rimuovete la classe `placeholder`
e il `data-initial` dal div, e inserite un `<img>`:
```html
<div class="member-photo">
    <img src="images/members/honey.jpg" alt="Honey" />
</div>
```
