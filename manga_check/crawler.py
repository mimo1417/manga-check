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

    def __init__(self, logger=lambda _: None):
        try:
            file_data = csv.reader(open(DATA_FILE, 'rb'))
        except IOError as e:
            file_data = {}
        # data from csv file
        self.data = dict((int(row[0]), {
            'id': int(row[0]),
            'chapter': int(row[1]),
            'is_read': int(row[2]),
        }) for row in file_data)
        self.logger = logger

    def check(self):
        """Run check on all mangas in config

        Returns:
            list: list of manga that have been updated
        """
        self.logger('... checking ...')

        return_data = []
        for id, manga in MANGAS.iteritems():
            self.logger('checking [{}] "{}" at {}'.format(
                manga['id'], manga['name'], manga['url']))
            latest = self.crawl(id)
            # already been crawled
            if id in self.data:
                cur_latest = self.data[id]['chapter']
            # if haven't crawled before
            else:
                cur_latest = 0
                self.data.setdefault(id, {})
                self.data[id]['id'] = id
                self.data[id]['chapter'] = 0
                self.data[id]['is_read'] = 0

            # if is read and greater than current
            if latest > cur_latest:
                self.logger(' > found!')
                self.data[id]['chapter'] = latest
                self.data[id]['is_read'] = 0

            # if new chaoter or simply not read
            if latest > cur_latest or self.data[id]['is_read'] == 0:
                data = dict(MANGAS[id])
                data['latest'] = latest
                data.pop('function', None)
                return_data.append(data)

        self.write_to_file()
        self.logger('..done.')
        return return_data

    @staticmethod
    def crawl(manga_id):
        """
        crawl based on manga'id in config
        :param manga_id: 
        :return: 
        """

        url = MANGAS[manga_id]['url']
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'html.parser')
        latest_chapter = MANGAS[manga_id]['function'](soup)

        return latest_chapter

    def write_to_file(self):
        writer = csv.writer(open(DATA_FILE, 'wb'))
        for id, data in self.data.items():
            writer.writerow([data['id'], data['chapter'], data['is_read']])

    def update_view_manga(self, manga_id):
        self.data[manga_id]['is_read'] = 1
        self.write_to_file()
