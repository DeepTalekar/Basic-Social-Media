from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from .database import engine
from . import models
from .config import settings

# Routers
from .routers import post, user, auth, vote

# * Since we have Alembic now we don't need it now
# models.Base.metadata.create_all(bind=engine)


description = """
FastAPI backend providing basic social media features

Wherever there is the lock 🔓 icon you have to be an authorized user (you must be logged in) to make that request.

## Authentication 🔐

* User can login using the email and password only

## Users 🧑

* User can be created by following the UserCreate Schema

* User details can be fetched using the id of the user

## Posts 📃

* User can get all the posts or either few of them with the help of query params:

    - ``limit: integer`` -  Limit the number of posts by specifying integer values.

    - ``skip: integer`` - Applies an offset to the posts and returns the newly resulting posts.

    - ``search: string``(Optional) - Search a post title which contains the search string.

* User can also create a post by passing JSON object as a parameter following the PostCreate Schema.

* User can also ask for an individual post.

* User can only Update/Delete his/her own post(s).


## Vote 👍/👎

* It is similar to Facebook's Like button functionality.

* User can vote(like) a post and unvote(dislike) the post that has been voted previously by you.

"""

app = FastAPI(docs_url=None)

# * Cache the OpenAPI schema
# You can use the property .openapi_schema as a "cache", to store your generated schema.
# That way, your application won't have to generate the schema every time a user opens your API docs.
# It will be generated only once, and then the same cached schema will be used for the next requests


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Basic Social Media",
        version="0.0.1",
        description=description,
        routes=app.routes,
    )
    # For Logo on redoc page
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello World"}


@app.get("/docs", include_in_schema=False)
def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Basic Social Media - Swagger UI",
    )
