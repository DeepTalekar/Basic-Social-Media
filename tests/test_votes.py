import pytest
from app import models


@pytest.fixture
def posts_with_vote(test_create_posts, session, test_user):
    new_vote = models.Vote(
        post_id=test_create_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)

    session.commit()


def test_votes_on_posts(authorized_client, test_create_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_create_posts[3].id, 'dir': 1})

    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_create_posts, posts_with_vote):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_create_posts[3].id, 'dir': 1})

    assert res.status_code == 409


def test_delete_vote(authorized_client, test_create_posts, posts_with_vote):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_create_posts[3].id, 'dir': 0})

    assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_create_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_create_posts[3].id, 'dir': 0})

    assert res.status_code == 404


def test_vote_not_exist(authorized_client, test_create_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': 804122, 'dir': 1})

    assert res.status_code == 404


def test_unauthorized_user_vote_post(client, test_create_posts):
    res = client.post("/vote/", json={
        'post_id': test_create_posts[3].id, 'dir': 1})
    assert res.status_code == 401
