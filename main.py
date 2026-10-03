from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    token = request.cookies.get("session_token")
    # if not token:
        # return RedirectResponse(url=request.url_for("login"), status_code=303)
        
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@app.post("/login")
async def login_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    # Simple hardcoded authentication for demonstration
    if email == "admin@gmail.com" and password == "password123":
        # Redirect to home on successful login
        response = RedirectResponse(url=request.url_for("home"), status_code=303)
        response.set_cookie(key="session_token", value="authenticated")
        return response
    
    # Render login page with error message on failure
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"message": "Invalid email or password. Please try again."}
    )
