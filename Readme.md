# Basic Social Media Backend

![Github Actions Workflow Status](https://github.com/DeepTalekar/Basic-Social-Media/actions/workflows/build-deploy.yml/badge.svg)
![GitHub Production Deployment Status](https://img.shields.io/github/deployments/DeepTalekar/Basic-Social-Media/Production?style=flat-square 'App Deployment Status')
[![dependency - fastapi](https://img.shields.io/badge/dependency-fastapi-blue?logo=fastapi&logoColor=white&style=flat-square)](https://pypi.org/project/fastapi)
[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=flat-square)](https://basic-social-media.herokuapp.com/docs 'Go to project documentation')
<img title="Swagger UI Validtion Status" alt="Swagger UI Validation Status" src="https://validator.swagger.io/validator?url=https://basic-social-media.herokuapp.com/openapi.json" />

[![Repo Hits](https://hits.sh/github.com/DeepTalekar/Basic-Social-Media.svg?view=today-total&style=flat-square&label=repo%20hits)](https://hits.sh/github.com/DeepTalekar/Basic-Social-Media/)
[![Website Hits](https://hits.sh/basic-social-media.herokuapp.com.svg?view=today-total&style=flat-square&label=website)](https://hits.sh/basic-social-media.herokuapp.com/)
![GitHub repo size](https://img.shields.io/github/repo-size/DeepTalekar/Basic-Social-Media?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FastAPI?style=flat-square)

FastAPI backend providing basic social media features

[Visit the docs to know more](https://basic-social-media.herokuapp.com/docs)

> **Note for Docs:** Wherever there is the lock 🔓 icon you have to be an authorized user (you must be logged in) to make that request.

## Features:

### Authentication 🔐

- User can login using the email and password only

### Users 🧑

- User can be created by following the UserCreate Schema

- User details can be fetched using the id of the user

### Posts 📃

- User can get all the posts or either few of them with the help of query params:

  - `limit: integer` - Limit the number of posts by specifying integer values.

  - `skip: integer` - Applies an offset to the posts and returns the newly resulting posts.

  - `search: string`(Optional) - Search a post title which contains the search string.

- User can also create a post by passing JSON object as a parameter following the PostCreate Schema.

- User can also ask for an individual post.

- User can only Update/Delete his/her own post(s).

### Vote 👍/👎

- It is similar to Facebook's Like button functionality.

- User can vote(like) a post and unvote(dislike) the post that has been voted previously by you.
