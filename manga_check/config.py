# -*- coding: utf-8 -*-
# Config file for Manga crawler
# @Author: vietvu
# @Date:   2016-10-11 17:56:14
# @Last Modified by:   Viet Vu
# @Last Modified time: 2016-10-12 11:01:21
import os
from tempfile import gettempdir


def _soup_mangapanda(soup):
    """Crawler for MangaPanda.com
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the site
    
    Returns:
        int: latest chapter
    """
    return int(soup.select('div#latestchapters a')[0].text.split(' ')[-1])


def _soup_truyentranhtuan(soup):
    """Crawler for TruyenTranhTuan.com
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the site
    
    Returns:
        int: latest chapter
    """
    return int([s for s in soup.select('div#manga-chapter a')[0].text.split(' ') if s.isdigit()][-1])


def _soup_mangastream(soup):
    """Crawler for mangastream.com

    Args:
        soup (BeautifulSoup): BeautifulSoup object of the site

    Returns:
        int: latest chapter
    """
    return int([s.strip() for s in soup.select('table.table-striped td')[0].text.split('-') if s.strip().isdigit()][0])

def _soup_manga_rock(soup):
    """Crawler for MangaRock
    
    Args:
        soup (BeautifulSoup):
    """
    s = soup.select('tbody[data-test=chapter-table] td')
    return int(s[0].find('a').text.split(':')[0].split('Chapter ')[1])


# list of manga
MANGAS = {
    0: {
        'id': 0,
        'name': 'One Piece MS',
        'url': 'http://mangastream.com/manga/one_piece',
        'function': _soup_mangastream
    },
    1: {
        'id': 1,
        'name': 'Gintama',
        'url': 'http://www.mangapanda.com/gintama',
        'reddit': 'https://www.reddit.com/r/Gintama/',
        'function': _soup_mangapanda
    },
    3: {
        'id': 3,
        'name': 'The Ruler Of The Land (Vietnamese)',
        'url': 'http://truyentranhtuan.com/hiep-khach-giang-ho',
        'function': _soup_truyentranhtuan
    },
    4: {
        'id': 4,
        'name': 'One Punch man',
        'url': 'http://readms.net/manga/onepunch_man',
        'function': _soup_mangastream
    },
    5: {
        'id': 5,
        'name': 'Boruto',
        'url': 'http://mangastream.com/manga/boruto',
        'function': _soup_mangastream
    },
    6: {
        'id': 6,
        'name': 'Dragonball Super',
        'url': 'https://mangarock.com/manga/mrs-serie-64116',
        'function': _soup_manga_rock
    },
    
}

# data storage
DATA_FILE_NAME = 'manga_check.csv'
# DATA_FILE = os.path.join(gettempdir(), DATA_FILE_NAME) # cannot store here, files are cleaned up at every boot
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), DATA_FILE_NAME))
