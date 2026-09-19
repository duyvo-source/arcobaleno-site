# arcobaleno.cloud

Public landing page for **Arcobaleno Research** — backtest forensics and research due diligence.

Static files, no build step on this side, no dependencies, no server-side code. The HTML is
**generated** in a private repo and copied here; this repo is the deploy target, not the source.

| path | purpose |
|---|---|
| `index.html` | the landing page |
| `method/index.html` | what an audit checks, in detail |
| `card.png` | the `og:image` / `twitter:image` social card, 1200×630 |
| `tools/` | published `fctools` bundles, their `.sha256` / `.asc`, the release public key, and `bootstrap.sh` |
| `CNAME` | binds the GitHub Pages custom domain to `arcobaleno.cloud` — do not delete |

**Published bundles under `tools/` are immutable.** A report may cite a version's hash, and a
citation that stops resolving is worse than an old artifact. Never delete or overwrite one;
`bootstrap.sh` always points at the current version.

## Editing

**Do not hand-edit `index.html`, `method/index.html` or `card.png`.** All three are generated. The
sources live in the private research repo:

- pages — `funding/forensics/page.html` and `method.html`, built by `funding/forensics/build_site.py`,
  which validates document structure, refuses to build a page with no contact address, refuses to
  ship a dead internal link, and refuses to ship an `og:image` that is missing or not the exact
  size the meta tags declare
- card — `funding/forensics/card.html`, rendered by `funding/forensics/build_card.sh`

Rebuild there, then copy the output here.

## Deploying

GitHub Pages serves `main` at the repository root. Pushing to `main` deploys.
DNS lives at Hostinger; only the apex `A` records point here. **Mail records (`MX`, SPF/DKIM `TXT`,
`_dmarc`) are unrelated to this repo and must never be changed for a deployment.**
