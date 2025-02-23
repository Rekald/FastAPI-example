import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse

from config import get_settings
from src.auth import router as auth
from src.inventory import router as inventory
from src.dependencies import templates, static_root
from src.auth.services import oauth2_scheme, verify_token

app = FastAPI()
settings = get_settings()

app.include_router(auth.auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(inventory.inventory_router, prefix="/inventory",
                   tags=["Inventory"], dependencies=[Depends(oauth2_scheme)])
app.mount("/static", static_root, name="static")


@app.get('/Home', dependencies=[Depends(oauth2_scheme)])
def index(request: Request):
    return templates.TemplateResponse("home.html", {'request': request})


@app.get('/401')
def index(request: Request):
    authorization: str = request.cookies.get("access_token")
    if not verify_token(authorization):
        return templates.TemplateResponse("401.html", {'request': request})
    return RedirectResponse("/Home")


@app.get('/')
def index(request: Request):
    authorization: str = request.cookies.get("access_token")
    if not verify_token(authorization):
        return templates.TemplateResponse("login.html", {'request': request})
    return RedirectResponse("/Home")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOSTNAME.host, port=settings.HOSTNAME.port)
