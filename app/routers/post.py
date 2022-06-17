from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Post']
)


@router.get("/", response_model=List[schemas.Post_With_Votes])
# @router.get("/")
def get_posts(limit: int = 10, skip: int = 0, search: Optional[str] = "", db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # * RAW SQL Queries
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()

    # * Query Parameter
    # print(limit)

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # * Retrieving only the Post of the User who is logged in
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    # * Performing Joins for getting the votes on Post
    # * By default it is Left Inner Join
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    print(results[0]._asdict())

    return results


# * Default Successful status code
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post_With_User_Data)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # * RAW SQL Queries
    # ! Insert like this to prevent SQL Injection
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
    #                (post.title, post.content, post.published))

    # new_post_created = cursor.fetchone()

    # * Saving the changes into the database
    # conn.commit()

    # Pydantic model to Python Dict
    # print(post.dict())

    # * Unpacking the dict to make a call to the model like below
    # new_post = models.Post(title=post.title, content=post.content,
    #                         published=post.published)

    print(current_user.email, current_user.id)
    new_post = models.Post(**post.dict(), owner_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post_With_Votes)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(id)
    post = None

    # * RAW SQL Queries
    # * NOTE: To add the `,` after `id` to make it tuple
    # cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id,))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    # * Performing Joins for getting the votes on Post
    # * By default it is Left Inner Join
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # * Retrieving only the Post of the User who is logged in
    # post = db.query(models.Post).filter(models.Post.id ==
    #                                      id and models.Post.owner_id == current_user.id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    # * For Retrieving only the Post of the User who is logged in
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not Authorised to perform requested action")

    response.status_code = status.HTTP_200_OK
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    postIndex = None

    # * RAW SQL Queries
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()

    # conn.commit()

    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    print(deleted_post)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with {id} doesn't exists")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorised to perform requested action")

    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#selecting-a-synchronization-strategy
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post_With_User_Data)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(id)
    print(post.dict())

    # * RAW SQL Queries
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #                (post.title, post.content, post.published, id,))

    # updated_post = cursor.fetchone()

    # conn.commit()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()

    print(updated_post)

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with {id} doesn't exists")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorised to perform requested action")

    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = updated_post_query.first()

    return updated_post
