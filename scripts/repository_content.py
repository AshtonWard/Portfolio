"""Snapshot approved public repositories and render their text without executing it."""
import json
import posixpath
import re
import subprocess
import tempfile
import unicodedata
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.content-cache'
EXTENSIONS = {'.md', '.markdown', '.yml', '.yaml', '.ps1', '.sh', '.py', '.json', '.j2', '.ini', '.cfg', '.toml', '.txt'}
MAX_BYTES = 512_000
MAX_FILES = 500

def github_json(path):
    # Deliberately anonymous: private repositories must never be mirrored.
    req = Request('https://api.github.com/' + path, headers={'User-Agent':'AshtonWard-Portfolio-Publisher','Accept':'application/vnd.github+json'})
    with urlopen(req, timeout=30) as response:
        return json.load(response)

def selected(path):
    parts = Path(path).parts
    return (Path(path).suffix.lower() in EXTENSIONS
            and not any(part.startswith('.') for part in parts if part != '.github')
            and not any(part in {'node_modules', 'vendor', '__pycache__'} for part in parts))

def snapshot(source):
    repo = source['repository']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository name')
    info = github_json('repos/' + repo)
    if info.get('private') is not False or info.get('visibility') != 'public':
        raise ValueError(f'Refusing non-public source: {repo}')
    with tempfile.TemporaryDirectory() as temp:
        checkout = Path(temp) / 'repo'
        # No source hooks, build scripts, imports, or submodules are run.
        subprocess.run(['git','-c','core.hooksPath=/dev/null','clone','--depth','1','--single-branch','--branch',info['default_branch'],
                        'https://github.com/' + repo + '.git',str(checkout)],check=True,capture_output=True,timeout=120)
        sha = subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
        files = {}
        for name in subprocess.check_output(['git','-C',str(checkout),'ls-files'],text=True).splitlines():
            p = checkout / name
            if not selected(name) or p.is_symlink() or not p.is_file(): continue
            if p.stat().st_size > MAX_BYTES: continue
            try: text = p.read_text(encoding='utf-8')
            except UnicodeDecodeError: continue
            if '\x00' in text: continue
            files[name] = text
            if len(files) > MAX_FILES: raise ValueError(f'Too many files: {repo}')
    return {'repository':repo,'sha':sha,'synced_at':datetime.now(timezone.utc).isoformat(),'files':files}

def slug(text):
    text = unicodedata.normalize('NFKC',text).lower()
    return re.sub(r'[^\w\- ]','',text).replace(' ','-')

def shell(template, path, title, description, body, tab):
    prefix = '../' * (len(Path(path).parts)-1) or './'
    html = template.replace('<title>About &amp; experience | Ashton Ward</title>', '<title>'+escape(title)+' | Ashton Ward</title>')
    html = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+' | Ashton Ward</title>',html)
    html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="'+escape(description,quote=True)+'">',html)
    html = html.replace('href="./','href="'+prefix).replace('src="./','src="'+prefix)
    html = re.sub(r' aria-current="page"','',html)
    href = prefix + ('repos/'+tab+'/index.html')
    html = html.replace('href="'+href+'"','href="'+href+'" aria-current="page"',1)
    return re.sub(r'<main id="main">.*?</main>',lambda _: '<main id="main">'+body+'</main>',html,flags=re.S)

def render_markdown(text, name, snapshot_data):
    repo, sha, files = (snapshot_data[k] for k in ['repository','sha','files'])
    parser = MarkdownIt('js-default',{'html':False,'linkify':False}).enable('table')
    tokens = parser.parse(text)
    headings = {}
    def rewrite(value, image=False):
        url = urlsplit(value)
        if url.scheme or url.netloc: return value
        source_path = posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(url.path))) if url.path else name
        if source_path.startswith('../'): return 'https://github.com/'+repo
        fragment = '#doc-'+quote(unquote(url.fragment)) if url.fragment else ''
        if not image and source_path in files:
            relative = posixpath.relpath(source_path+'.html',posixpath.dirname(name) or '.')
            return quote(relative,safe='/')+fragment
        if image:
            return 'https://raw.githubusercontent.com/'+repo+'/'+sha+'/'+quote(source_path,safe='/')
        return 'https://github.com/'+repo+'/blob/'+sha+'/'+quote(source_path,safe='/')+('#'+url.fragment if url.fragment else '')
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            text_content = tokens[i+1].content
            key = slug(text_content)
            count = headings.get(key,0); headings[key] = count+1
            token.attrSet('id','doc-'+key+('-'+str(count) if count else ''))
            token.tag = 'h'+str(min(6,int(token.tag[1:])+1))
        elif token.type == 'heading_close': token.tag = 'h'+str(min(6,int(token.tag[1:])+1))
        if token.children:
            for child in token.children:
                if child.type == 'link_open': child.attrSet('href',rewrite(child.attrGet('href')))
                if child.type == 'image':
                    child.attrSet('src',rewrite(child.attrGet('src'),image=True))
                    child.attrSet('loading','lazy')
    return parser.renderer.render(tokens,parser.options,{})

def generate(out, sync=False):
    sources = json.loads((ROOT/'content-sources.json').read_text())['sources']
    template = (ROOT/'about.html').read_text()
    CACHE.mkdir(exist_ok=True)
    manifest = []
    for source in sources:
        if not re.fullmatch(r'[a-z0-9-]+',source['slug']): raise ValueError('Invalid source slug')
        cache = CACHE/(source['slug']+'.json')
        if sync:
            data = snapshot(source)
            cache.write_text(json.dumps(data))
        elif cache.exists(): data = json.loads(cache.read_text())
        else: raise RuntimeError('Missing public-content snapshot. Run scripts/build.py --sync')
        if data['repository'] != source['repository']: raise ValueError('Snapshot source mismatch')
        base = 'repos/'+source['slug']+'/'
        files = data['files']
        stamp = escape(data['synced_at'].replace('T',' ')[:19]+' UTC')
        repo_url = 'https://github.com/'+data['repository']
        provenance = f'<p class="source-meta">Public source: <a href="{repo_url}/tree/{data["sha"]}">{escape(data["repository"])} @ {data["sha"][:7]}</a><br>Snapshot: {stamp}</p>'
        listing = ''.join('<li data-repo-file><a href="'+quote(name,safe='/')+'.html">'+escape(name)+'</a><span>'+('Documentation' if Path(name).suffix.lower() in {'.md','.markdown'} else 'Source')+'</span></li>' for name in sorted(files))
        intro = '<section class="page-intro"><p class="eyebrow">PUBLIC REPOSITORY / AUTO-PUBLISHED</p><h1>'+escape(source['title'])+'</h1><p class="lede">'+escape(source['description'])+'</p>'+provenance+'</section>'
        if source['slug']=='homelab': intro+='<p><a class="text-link" href="../../homelab.html">Read the lab introduction →</a></p>'
        body = intro+'<section class="repo-browser"><label for="file-search">Find a file</label><input id="file-search" type="search" data-file-search placeholder="Search file paths…"><p data-file-count role="status">'+str(len(files))+' files</p><ul class="file-list">'+listing+'</ul><p>Open a file to read documentation or inspect the source. Each page links back to its original on GitHub.</p></section>'
        target = out/base/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(shell(template,base+'index.html',source['title'],source['description'],body,source['slug']))
        for name,text in files.items():
            target = out/base/(name+'.html');target.parent.mkdir(parents=True,exist_ok=True)
            to_index = posixpath.relpath('index.html',posixpath.dirname(name) or '.')
            body = '<section class="page-intro"><p class="eyebrow">'+escape(source['title'])+'</p><h1 class="file-title">'+escape(name)+'</h1><a class="text-link" href="'+to_index+'">← Repository files</a>'+provenance+'</section>'
            if Path(name).suffix.lower() in {'.md','.markdown'}: content = render_markdown(text,name,data)
            else: content = '<pre><code>'+escape(text)+'</code></pre>'
            body += '<article class="prose repository-document">'+content+'</article><p class="source-footer"><a href="'+repo_url+'/blob/'+data['sha']+'/'+quote(name,safe='/')+'">View original on GitHub →</a></p>'
            target.write_text(shell(template,base+name+'.html',name,source['description'],body,source['slug']))
        manifest.append({k:data[k] for k in ['repository','sha','synced_at']})
    (out/'content-manifest.json').write_text(json.dumps(manifest,indent=2))
    print(f'Rendered {len(sources)} public repository snapshots')
