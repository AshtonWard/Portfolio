# Portfolio content review

Initial review: November 16, 2026 (America/Chicago).

## Reviewed sources

| Source | Finding | Publication decision |
| --- | --- | --- |
| Existing Portfolio root and section HTML | Older biography, incomplete navigation, missing resume target, WordPress-era links and assets | Replace public entry point; retain original section files in Git history/current source for review, exclude from `dist` |
| `Education/Education.html` | Describes degree as BS Cyber Security and lists May 2024 | Use the more precise BS Computer Science, Security & Privacy option from the current public profile; omit disputed graduation date |
| `Experience/Experience.html` | Includes January 1970 end dates and incomplete experience | Do not carry dates forward; confirm employment chronology against current resume |
| `CurrentProjects/` and `PastProjects/` | Kali/Parrot and older homelab material links to WordPress pages | Archive as candidates pending review of continued relevance and availability |
| `AshtonWard/AshtonWard` public README | QA/payment systems, Guard networking, tools, automation, homelab and Putler overview | Use as the principal source for introductory copy; do not import contribution-count claims or live statistics |
| `AshtonWard/Ansible` main tree and README | Only README exists; README describes intended examples and workflows | Link as a project repository, explicitly state evidence is still being prepared |
| `AshtonWard/Homelab` main tree | Only README exists | Describe project scope, not a finished public documentation set |
| User's Security+ discussion | User reported passing and shared certificate in earlier conversation | Include certification name; verify dates and credential URL before adding details |

The existing website at ashtonward.tech and its DNS/hosting were not inspected in this pass. Source-repository findings do not establish the current live site's behavior.

## Concrete implementation findings

- Root HTML used obsolete HTML import links, placeholder content, and navigation elements without destinations.
- `index.js` called `bioClick()` during handler registration instead of registering a callback.
- Download link referenced a resume file absent from the repository.
- Global list/float styles and external dependencies did not provide a reliable complete layout.
- Older dates, degree wording, spelling, and stale asset paths need editorial review.

## First draft content

- Homepage: verified professional scope and selected project summaries.
- Automation: high-level workflow and design choices, with evidence limitations stated.
- Homelab: scope and engineering questions; no internal addresses, private hostnames, or live status claims.
- Putler: assistant concept; incident dispatcher clearly marked planned.
- About: broad experience and tools, education wording, certification name, existing public professional links.
- Field note: newly written documentation guidance; no fabricated incident or measured result.
- Resume: dedicated HTML page derived from the reviewed professional scope and prior user-provided Murphy USA background. Employment dates and additional accomplishments remain pending current resume review; no invented dates or metrics are displayed.

No private repository files were read or copied in this pass. Public source review is not a complete secret scan of repository history.

## Remaining review before launch

- [ ] Verify employer, job title, dates, military experience wording, and degree details against current resume.
- [ ] Review and add a current public resume PDF.
- [ ] Verify Security+ credential URL and dates if displayed.
- [ ] Review implementation files intended for the public Ansible repository.
- [ ] Prepare sanitized architecture diagrams and screenshots.
- [ ] Add meaningful configuration and validation evidence to featured projects.
- [ ] Reconcile current monitoring status; the public profile calls deployment planned, while later conversations describe deployment. Do not claim a current status until checked.
- [ ] Review any private material separately before selecting it for publication.

Tracked in #1 and #2. This initial inventory does not complete either issue.
