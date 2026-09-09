# arcobaleno.cloud

Public landing page for **Arcobaleno Research** — backtest forensics and research due diligence.

One self-contained static file. No build step, no dependencies, no server-side code.

| file | purpose |
|---|---|
| `index.html` | the entire site |
| `CNAME` | binds the GitHub Pages custom domain to `arcobaleno.cloud` — do not delete |

## Editing

**Do not hand-edit `index.html`.** It is generated. The source lives in the private research repo at
`funding/forensics/page.html`; rebuild with `funding/forensics/build_site.py`, which validates
document structure and refuses to build a page with no contact address, then copy the output here.

## Deploying

GitHub Pages serves `main` at the repository root. Pushing to `main` deploys.
DNS lives at Hostinger; only the apex `A` records point here. **Mail records (`MX`, SPF/DKIM `TXT`,
`_dmarc`) are unrelated to this repo and must never be changed for a deployment.**
