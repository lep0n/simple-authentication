import uvicorn
import database
import base64
import json

from typing import Optional

from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:
        return templates.TemplateResponse("login.html", {"request": request})

    decoded_username = get_username_from_signed_data(username)
    if not decoded_username:
        response = templates.TemplateResponse("login.html", {"request": request})
        response.delete_cookie(key="username")
        return response

    user_data = database.fetchone("users", "*", decoded_username)
    if user_data != None:
        return Response(f"Hello, {user_data[1]}! Your personal account here.")


@app.get("/reg", response_class=HTMLResponse)
def reg_page(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
def register_page(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if password != confirm_password:
        return Response(
            json.dumps({"success": False, "msg": "The password doesn't match!"}),
            media_type="application/json",
        )

    if database.fetchone("users", "username", username):
        return Response(
            json.dumps({"success": False, "msg": "Username already taken!"}),
            media_type="application/json",
        )

    database.insert(
        "users", {"username": username, "password": hash_password(password)}
    )
    return Response(
        json.dumps({"success": True, "msg": "You are successfuly registred!"}),
        media_type="application/json",
    )


@app.post("/account")
def login_page(username: str = Form(...), password: str = Form(...)):
    user_data = database.fetchone("users", "*", username)

    if (
        user_data == None
        or username not in user_data
        or hash_password(password) not in user_data
    ):
        return Response(
            json.dumps({"success": False, "msg": "Wrong username or password!"}),
            media_type="application/json",
        )

    else:
        signed_username = (
            f"{base64.b64encode(username.encode()).decode()}.{sign_data(username)}"
        )
        response = Response(
            json.dumps(
                {
                    "success": True,
                    "msg": f"Hello, {user_data[1]}! Your personal account here.",
                }
            ),
            media_type="application/json",
        )
        response.set_cookie(key="username", value=signed_username)
        return response


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, host="0.0.0.0", reload=True)
