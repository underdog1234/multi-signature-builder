# Multi email signature builder

A small web page where staff type in their name, job title, email and phone, choose an office (Auckland or Christchurch), pick a logo style and a brand colour, and get:

- a ready-to-use **HTML signature** (download, or copy and paste into Outlook or Gmail),
- the whole signature as a **transparent PNG picture**, for email apps where you upload an image as your signature, and
- the logo on its own as a **transparent PNG**.

The website (multi-media.co.nz) is fixed, and the address comes from the office list, so staff can't change either.

There is no server and no build step. It is one page (`index.html`) plus a folder of logo PNGs, so it runs on GitHub Pages as is.

## Offices

The two offices live in the `OFFICES` list near the top of the script in `index.html`. Add or edit an entry there to change an address.

## How the logo is hosted

Signatures point at the logo PNGs in `logos/` on this site, for example
`https://<account>.github.io/<repo>/logos/multi-logo-purple.png`.
Because every signature that has been sent uses those addresses, **don't rename or move the files in `logos/`**.

If the site moves, change `PUBLISHED_LOGO_BASE` near the top of the script in `index.html`.
When the page is served from `github.io` it uses its own address automatically.

## Logo styles and colours

| Style | Colours |
| --- | --- |
| MULTI wordmark | all 10 palette colours |
| Heritage lockup (Since 1974) | Multi Red, Warm Grey, White, Light Grey, Charcoal, Warm Black |
| Company lockup (Multi-Media Systems Ltd.) | the same six |

Lockups are only offered in the colours that exist in the official logo files. Palette values come from `Multi Colour Palette.pdf`.

## Updating the logos

The PNGs in `logos/` are generated from the official brand files:

```
pip install pillow
python tools/make_logos.py "<path to>/01_Logos/For Screen"
```

Each file is the palette colour with the official logo's transparency, at 4x the size shown in the signature so it stays sharp on high-resolution screens.

## Signature layout

Arial 11pt, text in Charcoal (`#575757`), bold name and job title, then email, phone, address and website, then the logo. The email, phone and website are links but keep the plain grey text colour.
