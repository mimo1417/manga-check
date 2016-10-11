# -*- coding: utf-8 -*-
# Config file for Manga crawler
# @Author: vietvu
# @Date:   2016-10-11 17:56:14
# @Last Modified by:   Viet Vu
# @Last Modified time: 2016-10-12 00:03:24
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
    return int(soup.select('div#manga-chapter a')[0].text.split('-')[-1])


# list of manga
MANGAS = [
    {
        'id': 0,
        'name': 'One Piece',
        'url': 'http://www.mangapanda.com/one-piece',
        'function': _soup_mangapanda
    },
    {
        'id': 1,
        'name': 'Gintama',
        'url': 'http://www.mangapanda.com/gintama',
        'function': _soup_mangapanda
    },
    {
        'id': 2,
        'name': 'Fairy Tail',
        'url': 'http://www.mangapanda.com/fairy-tail',
        'function': _soup_mangapanda
    },
    {
        'id': 3,
        'name': 'The Ruler Of The Land (Vietnamese)',
        'url': 'http://truyentranhtuan.com/hiep-khach-giang-ho/',
        'function': _soup_truyentranhtuan
    }
]

# data storage
DATA_FILE_NAME = 'manga_check.csv'
DATA_FILE = os.path.join(gettempdir(), DATA_FILE_NAME)