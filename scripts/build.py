"""Copy only the current public site into dist; exclude legacy pages and review docs."""
from pathlib import Path
import shutil
import argparse
from repository_content import generate

parser = argparse.ArgumentParser()
parser.add_argument("--sync", action="store_true", help="Fetch fresh public repository snapshots")
args = parser.parse_args()
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for name in ['index.html', 'about.html', 'homelab.html', 'notes.html']:
    shutil.copy2(ROOT / name, OUT / name)
for name in ['assets', 'projects', 'notes', 'resume']:
    shutil.copytree(ROOT / name, OUT / name)
generate(OUT, sync=args.sync)
print('Built static site in dist/')
