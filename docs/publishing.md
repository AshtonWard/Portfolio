# Repository-driven portfolio publishing

The portfolio is the presentation layer. Public repositories remain the source of truth for technical documents and code. Curated project pages explain the work; repository pages expose the current public material without duplicating editorial maintenance.

## Sources and destinations

| Source | Website section | Update method |
| --- | --- | --- |
| AshtonWard/Ansible default branch | Ansible Playbooks (`repos/ansible/`) | Build-time public snapshot |
| AshtonWard/Homelab default branch | Homelab Documentation (`repos/homelab/`) | Build-time public snapshot |
| Portfolio `notes/` and `notes.html` | Writeups | Portfolio commit triggers a build |
| Reviewed professional information | About | Reviewed edits in Portfolio; LinkedIn remains a contact link |

To add a dedicated public writeup repository later, add a source entry with a unique slug, title, repository, and description in `content-sources.json`, then add a navigation link. The allowlist is tracked code, not supplied by dispatch payloads.

## What a build does

1. Query GitHub anonymously and require each configured source to be public.
2. Clone only the public default branch into a temporary directory; capture its exact commit.
3. Select supported UTF-8 text files. Skip symlinks, binary files, hidden files other than `.github` content, oversized files, and dependency directories. Never execute source-repository code or workflows.
4. Render Markdown with raw HTML disabled, Markdown tables, namespaced heading anchors, and relative links rewritten to mirrored pages where available. Display code/configuration as escaped text. Unsupported local assets link back to GitHub; Markdown images use commit-pinned raw source URLs.
5. Generate a searchable file index and a page per file, with original-source links and snapshot provenance. The manifest at `content-manifest.json` records repository commits and refresh times.
6. Validate local resources and fragments, then upload the build artifact.
7. If publication is enabled, deploy that same artifact to Pages.

The content cache is ignored and generated pages live only in `dist/`. Each refresh clones anew, so deleted source files disappear on the next successful build. No automated commits are needed and generated content cannot create a commit loop.

Current limits: plain Markdown and tables are supported; raw HTML is escaped, diagrams such as Mermaid are displayed as code, and GitHub-specific widgets are not reproduced. Heading anchors use a simplified slugger, so unusual formatted/Unicode heading references may need adjustment. Files are limited to 512 KB each and 500 selected files per repository. A fetch/build failure stops deployment; it does not publish a partial snapshot.

A source becoming private or unavailable fails the refresh. It does **not** remove a previous public deployment automatically; unpublish any existing copy when changing a source's visibility. This publisher is intended only for deliberately public material.

## Refresh modes

- **Portfolio push:** source/content edits on `main` rebuild automatically.
- **Scheduled:** at minute 23 of each hour, fetch public source changes. GitHub may delay or skip scheduled runs; this is not a real-time guarantee.
- **Manual:** use Actions → Build and refresh portfolio → Run workflow.
- **Immediate source notification (optional):** copy `docs/examples/notify-portfolio.yml` to each source repository and configure `PORTFOLIO_DISPATCH_TOKEN`. That workflow posts a `public-content-updated` repository dispatch to Portfolio. The Portfolio workflow must exist on the default branch.

A source repository's ordinary `GITHUB_TOKEN` cannot write to another repository. The optional example requires a separate token restricted to Portfolio with repository-dispatch permission (fine-grained PAT: Contents write), or a GitHub App installation token with equivalent access. Configure credentials through GitHub secrets; none have been created or stored by this change. Hourly public fetching needs no such token.

## Activate after review

1. Merge the draft after content and design review.
2. In Portfolio Settings → Pages, select GitHub Actions as the publishing source.
3. Set the repository Actions variable `PORTFOLIO_PUBLISH` to `true`.
4. Run the workflow manually and verify the resulting Pages URL.
5. Complete the custom domain and HTTPS migration checklist before routing ashtonward.tech.
6. Optionally add source notification workflows and their scoped credential.

Workflow and repository settings have not been activated by this draft. PR builds never deploy. If the setting stays unset, the workflow produces downloadable preview artifacts only.

## LinkedIn and other services

The site currently uses reviewed professional facts and links to LinkedIn. It does not scrape or claim to synchronize LinkedIn. Automatic profile import needs an explicitly supported authenticated API/connector or an agreed export process; changes should be reviewed before publication. Other public document repositories can use the same allowlisted publishing path.

## Reference documentation

- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://markdown-it-py.readthedocs.io/en/latest/security.html
