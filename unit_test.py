from app import shownoter
import pytest
import requests_mock

@pytest.fixture
def mock_html():
    return '<html><head><title>Test</title></head></html>'

class TestResult(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.content = '<html><head><title>Test</title></head></html>'

def mock_get(url):
    return TestResult(url)

def test_link_detect_finds_one_link_text():
    sample_text = '''This is a test
    to see if our regex
    will find link.com
    and return them both'''
    assert shownoter.link_detect(sample_text) == ['link.com']

def test_link_detect_finds_multiple_links():
    sample_text = '''This is a test
    to see if our regex
    will find link.com
    and link.net
    and foo.bar
    and returns them all'''
    assert shownoter.link_detect(sample_text) == ['link.com', 'link.net', 'foo.bar']

def test_valid_link_inserts_prefix_if_none(monkeypatch):
    monkeypatch.setattr(shownoter, 'get', mock_get)

    link = shownoter.Link('link.com')
    assert 'http://link.com' == link.url

def test_valid_link_does_nothing_if_prefix_exists(monkeypatch):
    monkeypatch.setattr(shownoter, 'get', mock_get)

    link = shownoter.Link('http://link.com')
    assert 'http://link.com' == link.url

@requests_mock.Mocker(kw='mock')
def test_title(mock_html, **kwargs):
    link = 'http://link.com'
    html = kwargs['mock'].get(link, text=mock_html)
    title = shownoter.title(link)
    assert html.called
    assert title == "Test"

def test_link_markdown():
    link = 'link.com'
    title = 'Test'
    assert '[Test](link.com)' in shownoter.link_markdown(title, link)

def test_image_markdown():
    link = 'link.png'
    title = ''
    assert '![](link.png)' in shownoter.image_markdown(title, link)

def test_image_detect_detects_png():
    link = 'link.png'
    assert shownoter.image_detect(link)

def test_image_detect_detects_jpg():
    link = 'link.jpg'
    assert shownoter.image_detect(link)

def test_image_detect_detects_gif():
    link = 'link.gif'
    assert shownoter.image_detect(link)

def test_image_detect_does_not_detect_outside_other_links():
    link = 'link.foo'
    assert not shownoter.image_detect(link)

@requests_mock.Mocker(kw='mock')
def test_title(mock_html, **kwargs):
    link = 'http://link.com'
    html = kwargs['mock'].get(link, text=mock_html)
    sample_link = shownoter.Link(link)
    assert html.called
    assert sample_link.url == 'http://link.com/'
    assert sample_link.title == 'Test'
    assert sample_link.markdown == '* [Test](http://link.com/)'


