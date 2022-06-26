from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_create_posts):
    res = authorized_client.get("/posts/")
    # print(res.json())

    # * Verifying the output is in valid Schema
    # * If its not in valid schema then it will throw an error and hence the test will fail
    def verifyPostWithVotesSchema(post):
        return schemas.Post_With_Votes(**post)

    posts_map = map(verifyPostWithVotesSchema, res.json())
    posts: List[schemas.Post_With_Votes] = list(posts_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_create_posts)


def test_unauthorized_user_get_all_posts(client, test_create_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_create_posts):
    res = client.get(f"/posts/{test_create_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_create_posts):
    res = authorized_client.get("/posts/78987")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_create_posts):
    res = authorized_client.get(f"/posts/{test_create_posts[0].id}")
    print(res.json())
    post = schemas.Post_With_Votes(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_create_posts[0].id


@pytest.mark.parametrize("title, content, published", [
    ('Awesome Title', 'Awesome Content', True),
    ('Pizza News', 'Some pizza news', True),
    ('War crimes', 'News on war crimes', False),
])
def test_create_post(title, content, published, authorized_client, test_user, test_create_posts):
    res = authorized_client.post(
        "/posts/", json={'title': title, 'content': content, 'published': published})

    created_post = schemas.Post_With_User_Data(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published(authorized_client, test_user, test_create_posts):
    res = authorized_client.post(
        "/posts/", json={'title': 'Beautiful Title', 'content': 'Cool Content'})

    created_post = schemas.Post_With_User_Data(**res.json())

    assert res.status_code == 201
    assert created_post.title == 'Beautiful Title'
    assert created_post.content == 'Cool Content'
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_create_posts):
    res = client.post(
        "/posts/", json={'title': 'Beautiful Title', 'content': 'Cool Content'})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_create_posts):
    res = client.delete(f"/posts/{test_create_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_create_posts):
    res = authorized_client.delete(f"/posts/{test_create_posts[0].id}")

    total_posts = authorized_client.get("/posts/")

    assert res.status_code == 204
    # * Checking if the total no. of posts is reduced by 1 or not
    assert len(total_posts.json()) == len(test_create_posts) - 1


def test_delete_post_not_exist(authorized_client, test_user, test_create_posts):
    res = authorized_client.delete("/posts/9785646")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_create_posts):
    res = authorized_client.delete(f"/posts/{test_create_posts[3].id}")

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_create_posts):
    res = client.put(f"/posts/{test_create_posts[0].id}", json={
                     'title': 'Beautiful Title', 'content': 'Cool Content'})
    assert res.status_code == 401


def test_update_post(authorized_client, test_user, test_create_posts):
    data = {
        "title": "Updated Title by test",
        "content": "Updated Content by test",
        "id": test_create_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_create_posts[0].id}", json=data)

    updated_post = schemas.Post_With_User_Data(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_create_posts):
    data = {
        "title": "Updated Title by test",
        "content": "Updated Content by test",
        "id": test_create_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_create_posts[3].id}", json=data)

    assert res.status_code == 403


def test_update_post_not_exist(authorized_client, test_user, test_create_posts):
    data = {
        "title": "Updated Title by test",
        "content": "Updated Content by test",
        "id": test_create_posts[0].id
    }
    res = authorized_client.put(f"/posts/13231", json=data)

    assert res.status_code == 404
