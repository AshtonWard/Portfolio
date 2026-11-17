"""Render the complete public resume from one maintained, reviewed data source."""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def text(value):
    return escape(value, quote=True)

def bullets(items):
    return '<ul>' + ''.join('<li>' + text(item) + '</li>' for item in items) + '</ul>'

def render_resume(destination):
    data = json.loads((ROOT / 'content/resume.json').read_text())
    pieces = [
        '<section class="page-intro resume-intro"><p class="eyebrow">// RESUME</p>',
        '<h1>Ashton <em>Ward</em></h1>',
        '<p class="lede">' + text(data['headline']) + '</p>',
        '<p class="resume-facts">' + text(data['location']) + '<span aria-hidden="true"> / </span>' + text(data['clearance']) + '</p>',
        '<div class="resource-links"><a href="https://www.linkedin.com/in/ashtonrjward/">LinkedIn →</a><a href="https://github.com/AshtonWard">GitHub →</a><button class="secondary-button" type="button" data-print-resume hidden>Print / save as PDF</button></div></section>',
        '<nav class="resume-outline" aria-label="Resume sections">'
    ]
    for anchor, label in [('summary','Summary'), ('experience','Experience'), ('skills','Skills'), ('projects','Projects'), ('education','Education'), ('certifications','Certifications')]:
        pieces.append('<a href="#' + anchor + '">' + label + '</a>')
    pieces.append('</nav><div class="prose resume-body"><section class="prose-section" id="summary"><p class="eyebrow">// PROFILE</p><h2>Professional summary</h2>')
    pieces.extend('<p>' + text(paragraph) + '</p>' for paragraph in data['summary'])
    pieces.append('</section><section class="prose-section" id="experience"><p class="eyebrow">// WORK HISTORY</p><h2>Professional experience</h2>')
    for role in data['experience']:
        pieces.extend([
            '<article class="experience resume-role"><p class="eyebrow">' + text(role['employer']) + '</p>',
            '<h3>' + text(role['title']) + '</h3>',
            '<p class="resume-meta"><strong>' + text(role['dates']) + '</strong><br>' + text(role['location']) + ' · ' + text(role['schedule']) + '</p>',
            bullets(role['bullets']), '</article>'
        ])
    pieces.append('</section><section class="prose-section" id="skills"><p class="eyebrow">// TECHNICAL TOOLKIT</p><h2>Technical skills</h2><dl class="resume-skills">')
    for skill in data['skills']:
        pieces.append('<div><dt>' + text(skill['area']) + '</dt><dd>' + text(skill['items']) + '</dd></div>')
    pieces.append('</dl></section><section class="prose-section" id="projects"><p class="eyebrow">// APPLIED WORK</p><h2>Technical projects</h2><p>These projects are personal infrastructure and development work, separate from my civilian and military employment.</p>')
    for project in data['projects']:
        pieces.extend(['<article class="experience resume-project"><h3>' + text(project['name']) + '</h3>', '<p class="resume-project-context">' + text(project['context']) + '</p>', bullets(project['bullets']), '<div class="resource-links">'])
        for link in project['links']:
            pieces.append('<a href="' + text(link['url']) + '">' + text(link['label']) + ' →</a>')
        pieces.append('</div></article>')
    school = data['education']
    pieces.extend([
        '</section><section class="prose-section" id="education"><p class="eyebrow">// ACADEMIC BACKGROUND</p><h2>Education</h2>',
        '<h3>' + text(school['degree']) + '</h3><p>' + text(school['option']) + '<br><strong>' + text(school['institution']) + '</strong> · ' + text(school['location']) + '<br>Graduated ' + text(school['graduated']) + ' · GPA ' + text(school['gpa']) + '</p></section>',
        '<section class="prose-section" id="certifications"><p class="eyebrow">// PROFESSIONAL DEVELOPMENT</p><h2>Certifications</h2>'
    ])
    for certification in data['certifications']:
        pieces.append('<article class="resume-certification"><h3>' + text(certification['name']) + '</h3><p>' + (text(certification['issuer']) + '<br>' if certification['issuer'] else '') + text(certification['details']) + '</p></article>')
    pieces.append('</section></div>')
    template = (ROOT / 'templates/resume.html').read_text()
    page = re.sub(r'<main id="main">.*?</main>', lambda _: '<main id="main">' + '\n'.join(pieces) + '</main>', template, flags=re.S)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page)
