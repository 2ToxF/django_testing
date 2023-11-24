import pytest
from django.conf import settings
from django.urls import reverse

HOME_URL = reverse('news:home')


@pytest.mark.usefixtures('many_news_list')
def test_news_count(client):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('many_news_list')
def test_news_order(client):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.usefixtures('create_two_comments')
def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, detail_url):
    response = admin_client.get(detail_url)
    assert 'form' in response.context
