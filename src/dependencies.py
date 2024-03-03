import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

root_dir = Path(__file__).parent.parent.resolve()
source_dir = root_dir / "src"
template_root = root_dir / "templates"
tmp_root = os.path.join(root_dir, "tmp")
db_root = 'sqlite:///' + os.path.join(source_dir, 'inventory.db')
static_root = StaticFiles(directory=root_dir / "static")
templates = Jinja2Templates(directory=template_root)
