from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'
comments_count_callable = Comment.objects.count


@pytest.fixture
def form_data():
    return {
        'text': COMMENT_TEXT
    }


@pytest.fixture
def new_form_data():
    return {
        'text': NEW_COMMENT_TEXT
    }


@pytest.fixture
def edit_url(comment_id_for_args):
    return reverse('news:edit', args=comment_id_for_args)


@pytest.fixture
def delete_url(comment_id_for_args):
    return reverse('news:delete', args=comment_id_for_args)


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'


def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    client.post(detail_url, data=form_data)
    assert comments_count_callable() == 0


def test_user_can_create_comment(
    author_client, author, news, detail_url, form_data, url_to_comments
):
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, url_to_comments)
    assert comments_count_callable() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert comments_count_callable() == 0


def test_author_can_delete_comment(author_client, delete_url, url_to_comments):
    response = author_client.post(delete_url)
    assertRedirects(response, url_to_comments)
    assert comments_count_callable() == 0


def test_user_cant_delete_comment_of_another_user(
    admin_client, delete_url, url_to_comments
):
    response = admin_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments_count_callable() == 1


def test_author_can_edit_comment(
    author_client, edit_url, new_form_data, url_to_comments, comment
):
    response = author_client.post(edit_url, data=new_form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
    admin_client, edit_url, new_form_data, comment
):
    response = admin_client.post(edit_url, data=new_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
