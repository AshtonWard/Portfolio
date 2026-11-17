# Launch checklist

Target: ashtonward.tech. Source: AshtonWard/Portfolio. Issues #1–#4 track the full effort.

## Content

- [ ] Complete publication review in `content-review.md`.
- [ ] Add reviewed diagrams, screenshots, configuration examples, and validation results.
- [ ] Add the current resume PDF and a working download link.
- [ ] Review final wording with Ashton.

## Verification

- [ ] Run `python3 scripts/build.py` and `python3 scripts/check.py`.
- [ ] Check all pages at narrow mobile and desktop widths, keyboard-only navigation, JavaScript disabled, and reduced motion.
- [ ] Check actual external project and professional profile destinations.
- [ ] Review print rendering if a printable resume is added.

## Hosting and domain

- [ ] Inspect the current live site, domain registrar/DNS provider, and hosting configuration.
- [ ] Back up existing live content and record current DNS before a migration.
- [ ] Select GitHub Pages (Actions publishing source) or another static host and deploy `dist/` only.
- [ ] Merge the reviewed publishing workflow and enable `PORTFOLIO_PUBLISH=true` when ready.
- [ ] Optionally configure immediate cross-repo notification using `docs/examples/notify-portfolio.yml`.
- [ ] Verify the hosting preview before changing domain routing.
- [ ] Configure ashtonward.tech, HTTPS, www handling, and canonical metadata.
- [ ] Determine whether legacy WordPress query URLs require host-level redirects or a migration notice.
- [ ] Verify the custom domain, page paths, favicon, resume, and HTTPS.
- [ ] Update GitHub profile README and LinkedIn to the final public URL.

## Rollback

Retain the previous hosting and DNS values until the new site is verified. If the migration fails, restore the prior DNS/host routing. Revert the site release to the previously verified commit or deployment artifact, then verify its URLs and HTTPS again.
