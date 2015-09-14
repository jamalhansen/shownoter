"""
Pytest Testing Module
"""

import requests_mock
import pytest
from shownoter import re_link, file_type, get_title


def test_re_link_detect_http():
    assert re_link('http://google.com')
    
def test_re_link_detect_https():
    assert re_link('https://google.com')

def test_re_link_detect_www():  
    assert re_link('www.google.com')

def test_re_link_detect_dot_text():
    assert re_link('a.bc')

def test_re_link_does_not_detect_strings_without_periods():
    assert not re_link('google dot com')

def test_re_link_does_not_detect_sentences_using_proper_grammar():
    assert not re_link('This is a serious one. It should not detect sentences')

def test_re_link_detects_multiple_lines():
    links = 'google.com\ntwitter.com'
    assert len(re_link(links)) == 2

def test_re_link_only_detects_links_and_nothing_else():
    links = 'duckduckgo.com is the best'
    result = re_link(links)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert 'duckduckgo.com' in result

# Test Link class
@pytest.fixture
def link_object():
    link_object = Link(title = 'foo', url = 'foo.com')
    return link_object

def test_Link_has_url_attr(link_object):
    assert link_object.url == 'foo.com'
    

def test_Link_has_title_attr(link_object):
    assert link_object.title == 'foo'

def test_Link_has_markdownerize(link_object):
    assert link_object.markdownerize() == '[foo](foo.com)'
    

# Test Image Class
@pytest.fixture
def image_object():
    image_object = Image(title = 'foo', url = 'foo.jpg')
    return image_object

def test_Image_inherits_title_attr_from_link(image_object):
    assert image_object.title == 'foo'

def test_Image_inherits_url_attr_from_link(image_object):
    assert image_object.url == 'foo.jpg'

def test_image_overides_markdownerize(image_object):
    assert image_object.markdownerize() == '![foo](foo.jpg)'


def test_file_type_can_detect_png():
    image_path = 'foo.png'
    result = file_type(image_path)
    assert result == '.png'

def test_file_type_can_detect_jpg():
    image_path = 'foo.jpg'
    result = file_type(image_path)
    assert result == '.jpg'

def test_file_type_can_detect_jpeg():
    image_path = 'foo.jpeg'
    result = file_type(image_path)
    assert result == '.jpeg'

def test_file_type_can_detect_gif():
    image_path = 'foo.gif'
    result = file_type(image_path)
    assert result == '.gif'

def test_file_type_can_detect_swf():
    image_path = 'foo.swf'
    result = file_type(image_path)
    assert result == '.swf'

def test_file_type_can_detect_xvf():
    image_path = 'foo.xvf'
    result = file_type(image_path)
    assert result == '.xvf'

def test_file_type_does_not_detect_files_outside_of_image_extensions():
    path = 'foo.com'
    result = file_type(path)
    assert not result
