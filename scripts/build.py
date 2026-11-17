"""Copy only the current public site into dist; exclude legacy pages and review docs."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for name in ['index.html', 'about.html', 'homelab.html', 'notes.html']:
    shutil.copy2(ROOT / name, OUT / name)
for name in ['assets', 'projects', 'notes']:
    shutil.copytree(ROOT / name, OUT / name)
print('Built static site in dist/')
