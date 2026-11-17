# Complete resume content review

Reviewed November 17, 2026. This expands the initial published resume instead of preserving its sparse placeholder-level coverage.

## Maintained content

`content/resume.json` contains the complete public resume facts and descriptions. `scripts/build_resume.py` renders them into `dist/resume/index.html` using `templates/resume.html`. The source JSON and review notes are excluded from the published build. Updating the page should preserve the user's established history and wording constraints.

## Source reconciliation

| Topic | Source and decision |
| --- | --- |
| Current role | User-supplied Q4 resume: QA Automation Engineer I, Murphy USA, October 2024–present, full-time 40 hours/week |
| QA responsibilities | User's Q4 resume and earlier work descriptions: 30+ applications, Postman/Python API testing, TCP payment-device test utilities/message relay, Ranorex functional automation, firewall-log investigation, defect reproduction, QA-to-Alpha validation. Describe as software testing, not a cybersecurity operations job. |
| Guard | Most recent correction: Staff Sergeant (E-6), superseding older Sergeant (E-5) descriptions. 25H Network Communication Systems Specialist; January 2019–present; recurring part-time military duty. Include supported communications, networking, server support, team coordination, and accountability responsibilities without overstating training depth. |
| SAU help desk | User's Q4 resume and clarification: August 2021–October 2023, 15 hours/week. Used a boot drive to deploy an existing Windows image created by someone else. Do not claim image engineering or authorship. Include workstation/software/printer support and deployment tasks. |
| Drew Memorial | User's Q4 clarification: May–August 2020, full-time 40 hours/week. Verified backups, prepared approximately 12 Windows computers concurrently, installed software, replaced workstations, handled cabling, printers and cameras. |
| Degree | Latest user-supplied Q4 resume: B.S. Computer Science, Cybersecurity & Privacy Option, Southern Arkansas University; graduated May 2024; GPA 3.34. This resolves the conflicting older memory/draft dates. |
| Security+ | Read the actual user-supplied CompTIA Security+ ce certificate: earned November 12, 2026; valid through November 12, 2029; SY0-701. Display dates and certification only. |
| Six Sigma | Previously confirmed Six Sigma White Belt. No unverified issuer or completion date added. |
| Automation project | Reviewed actual provisioning workflow, inventory script, recovery playbook, Node Exporter tasks, and Prometheus update task in the operational Ansible repository. Verified code contains input validation, template cloning, networking, inventory validation/commit/push, guest reachability, bootstrap, service recovery, and promtool config validation. These are scoped project summaries, not copies of private code or proof of measured performance. |
| Other lab work | Prior confirmed setup/troubleshooting discussions support Proxmox, segmentation, Wazuh, Prometheus/Grafana, WireGuard, Caddy, Docker and Hermes. Present as personal lab work. Keep planned incident dispatcher/specialist workflows labeled planned. |
| Portfolio publishing | Current repository code and successful GitHub Actions/Pages deployment establish daily public-repo publishing, source snapshots, Markdown rendering, file search, link validation and tests. |

## Constraints retained

- Do not list Wireshark. The user explicitly excluded it because they do not feel their experience is strong enough.
- Do not turn Guard tenure into equivalent full-time civilian engineering experience.
- Do not claim enterprise infrastructure ownership, expert-level routing knowledge, production SOC work, or completed autonomous incident response.
- Do not claim authorship of preconfigured Windows images deployed at SAU.
- Do not invent defect counts, uptime, time savings, endpoint totals, training credentials, or certifications. Conflicting older metrics and uncertain endpoint counts were not carried over.
- Do not publish certificate/candidate identifiers, verification codes, home address, private inventory, operational addresses, credentials, or detailed communications-system configurations.
- Use professional contact links already selected for the public site.

## Outstanding editorial work

The page now contains complete supported history rather than generic placeholders. Future changes may add a tailored short downloadable PDF or additional verified accomplishments. Further depth should come from actual duties and evidence, not larger lists of tools or inflated metrics.
