import requests
import json


def test_server_sends_200_response():
    """Test homepage works."""
    response = requests.get('http://127.0.0.1:3000')
    assert response.status_code == 200
    assert response.text[:15] == '<!DOCTYPE html>'


def test_server_sends_404_response():
    """Test nonroute throws correct error."""
    response = requests.get('http://127.0.0.1:3000/monkey')
    assert response.status_code == 404
    assert response.text == 'Not Found'


def test_server_sends_200_cowsay():
    """Test route works."""
    response = requests.get('http://127.0.0.1:3000/cowsay')
    assert response.status_code == 200
    assert response.text[:15] == ' ______________'


def test_server_sends_qs_back():
    """Test query string works."""
    response = requests.get('http://127.0.0.1:3000/cow?msg=hello world')
    assert response.status_code == 200
    assert response.text[15:30] == '\n< hello world '


def test_server_sends_qs_back_nothing():
    """Test non key throws correct error."""
    response = requests.get('http://127.0.0.1:3000/cow?tim=oops')
    assert response.status_code == 400
    assert response.text == 'Use msg as the querystring key.'


def test_post_correct():
    """Post grabs correct data."""
    response = requests.post('http://127.0.0.1:3000/cow?msg=hello world')
    assert response.status_code == 200
    assert json.loads(response.text)['content'][15:30] == '\n< hello world '


def test_post_incorrect():
    """Fail on wrong key."""
    response = requests.post('http://127.0.0.1:3000/cow?tim=oops')
    assert response.status_code == 400
    assert response.text[64:95] == 'Use msg as the query string key'
