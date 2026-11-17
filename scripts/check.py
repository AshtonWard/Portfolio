"""Check published HTML for missing local resources and broken fragment links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parents[1] / 'dist'
class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.headings = set(), [], 0
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID: {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'h1': self.headings += 1
        for attr in ['href', 'src']:
            if attrs.get(attr): self.links.append(attrs[attr])
docs = {p: Document(p) for p in ROOT.rglob('*.html')}
assert docs, 'Build the site first'
count = 0
for path, doc in docs.items():
    assert doc.headings == 1, f'{path}: expected one h1'
    for link in doc.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(ROOT), f'Link escapes site: {link}'
        assert target.exists(), f'{path.name}: missing {link}'
        if url.fragment:
            assert target in docs and unquote(url.fragment) in docs[target].ids, f'{path.name}: missing fragment {link}'
        count += 1
print(f'Passed: {len(docs)} pages, {count} local links/resources, one h1 per page, unique IDs.')
