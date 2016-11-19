# -*- coding: utf-8 -*-
# Manga crawler class
# @Author: vietvu
# @Date:   2016-10-11 18:02:02
# @Last Modified by:   Viet Vu
# @Last Modified time: 2016-10-12 10:42:14
from config import DATA_FILE, MANGAS
import csv
import requests
from bs4 import BeautifulSoup


class MangaCrawler(object):
    """Manga crawler class"""

    def __init__(self):
        try:
            file_data = csv.reader(open(DATA_FILE, 'rb'))
        except IOError as e:
            file_data = {}
        self.data = dict((int(row[0]), int(row[1])) for row in file_data)
        self.updated_data = []

    def check(self):
        """Run check on all mangas in config

        Returns:
            list: list of manga that have been updated
        """
        for id, manga in MANGAS.iteritems():
            latest = self.crawl(id)
            if id in self.data:
                cur_latest = self.data[id]
            else:
                cur_latest = 0
                self.data[id] = 0
            if latest > cur_latest:
                self.updated_data.append((id, latest))
                self.data[id] = latest

        self.write_to_file()

        return_data = []
        for udata in self.updated_data:
            _udata = dict(MANGAS[udata[0]])
            _udata['latest'] = udata[1]
            _udata.pop('function', None)
            return_data.append(_udata)
        return return_data

    def crawl(self, manga_id):
        """Run crawl on manga'id

        Args:
            url (string): url of the manga

        Returns:
            int: latest chapter
        """

        url = MANGAS[manga_id]['url']
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'html.parser')
        latest_chapter = MANGAS[manga_id]['function'](soup)

        return latest_chapter

    def write_to_file(self):
        writer = csv.writer(open(DATA_FILE, 'wb'))
        for id, data in self.data.items():
            writer.writerow([id, data])
