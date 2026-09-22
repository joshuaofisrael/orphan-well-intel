# Orphan Well Intel

Public-record procurement intelligence for orphan, abandoned, idle, and legacy oil and gas well plugging and site reclamation.

**Operating entity:** Joshua Israel Ventures LLC  
**Service name:** Abandoned Oil Wells Project (orphan-well procurement intelligence)  
**Nature:** Information only. This product does not bid, broker work, charge a percentage of a contract, give legal or engineering advice, or speak for any government agency.

Launch geography is Ohio, West Virginia, Kentucky, and Pennsylvania. Stripe checkout is not connected. The pricing page describes intended subscriptions; the request-access form does not send or store a message.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| How it works | `how-it-works.html` |
| Coverage | `coverage.html` |
| Pricing | `pricing.html` |
| Sample digest (22 September 2026 scan) | `sample-digest.html` |
| Market map | `market-map.html` |
| Disclaimer and terms | `disclaimer.html` |
| Request access | `contact.html` |

The sample digest and market map use the 22 September 2026 public-record scan and contractor index. They do not add solicitations, award amounts, or eligibility findings that were not in those records. Contractors must verify official sources. Artificial intelligence is used to organize public material and can be wrong.

## Run locally

From the repository root:

```bash
python3 -m http.server 8000
```

Open [http://localhost:8000/](http://localhost:8000/). Links and assets are relative, so the same files work on your machine and on the GitHub project site.

Regenerate HTML after editing `scripts/build_site.py`:

```bash
python3 scripts/build_site.py
python3 scripts/check_site.py
```

`check_site.py` confirms one `h1` per page, the disclaimer language, the real solicitation IDs, relative links, and the absence of a contact email or Stripe checkout URL.

## GitHub Pages

Expected URL: [https://joshuaofisrael.github.io/orphan-well-intel/](https://joshuaofisrael.github.io/orphan-well-intel/)

This is a **project site**. The site root is `/orphan-well-intel/`, not the domain root. Asset and page links are relative (`css/styles.css`, `pricing.html`) so they resolve under that path. Do not switch them to root-absolute paths such as `/css/styles.css`.

Deploy workflow: [`.github/workflows/pages.yml`](.github/workflows/pages.yml). It runs on every push to `main` (and can be started manually). It checks the HTML, then publishes the site with `actions/deploy-pages`. `.nojekyll` is included so GitHub does not run Jekyll over the HTML if Pages is ever switched to branch deploy.

### Manual step (required once)

Pages is not fully on until the repository source is set:

1. Open the repository **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Merge the workflow to `main` (or push it there). The workflow deploys that branch.
4. After the action succeeds, the site is at the URL above.

If the action fails with a pages-site error before that setting exists, repeat step 2 and re-run the workflow from the Actions tab (`workflow_dispatch` is enabled).

Branch deploy is a fallback, not the default: **Deploy from a branch → `main` → `/ (root)`**. Keep `.nojekyll` in place if you use that option.
