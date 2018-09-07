# -*- coding: utf-8 -*-
# Manga crawler class
import operator
import csv
import traceback

import pymongo
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from manga_check.config import MANGAS
from manga_check.storage import Storage

class MangaCrawler(object):
    """Manga crawler class"""

    def __init__(self, logger=lambda _: None):
        self.storage = Storage()
        try:
            storage_data = self.get_data()
        except Exception:
            storage_data = []

        self.data = dict((int(row['id']), {
            'id': int(row['id']),
            'chapter': int(row['chapter']),
            'is_read': int(row['is_read']),
        }) for row in storage_data)
        self.logger = logger

    def check(self):
        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(self.async_check())
        ioloop.close()

    async def async_check(self):
        """Run check on all mangas in config

        Returns:
            list: list of manga that have been updated
        """
        self.logger('... checking ...')

        futures = [self.crawl(manga_id) for manga_id in MANGAS]
        done_tasks, _ = await asyncio.wait(futures)

        return_data = []
        len_names_url = [(len(manga['name']), len(manga['url']))
                         for _, manga in MANGAS.items()]
        len_names, len_urls = list(zip(*len_names_url))
        max_name_len, max_url_len = max(len_names), max(len_urls)
        
        results = []
        for task in done_tasks:
            manga_id, latest = None, None
            try:
                manga_id, latest = task.result()
                results.append((manga_id, latest))
            except Exception as e:
                self.logger(e)
                self.logger("Something is wrong: {}".format(
                    traceback.format_exc()))
        
        results.sort(key=operator.itemgetter(0))
        
        for manga_id, latest in results:
            manga = MANGAS[manga_id]

            # already been crawled
            if manga_id in self.data:
                cur_latest = self.data[manga_id]['chapter']

            # if haven't crawled before
            else:
                cur_latest = 0
                self.data.setdefault(manga_id, {})
                self.data[manga_id]['id'] = manga_id
                self.data[manga_id]['chapter'] = 0
                self.data[manga_id]['is_read'] = 0

            self.logger(
                'checking [{id}] {name} at {url} :: {latest} ~ {cur_latest}'
                .format(id=manga['id'], latest=latest, cur_latest=cur_latest,
                        name=manga['name'].ljust(max_name_len),
                        url=manga['url'].ljust(max_url_len)))

            # if is read and greater than current
            if latest > cur_latest:
                self.logger(' > found!')
                self.data[manga_id]['chapter'] = latest
                self.data[manga_id]['is_read'] = 0

            # if new chapter or simply not read
            if latest > cur_latest or self.data[manga_id]['is_read'] == 0:
                data = dict(MANGAS[manga_id])
                data['latest'] = latest
                data.pop('function', None)
                return_data.append(data)

        self.store_data()
        return return_data

    async def crawl(self, manga_id):
        """
        crawl based on manga'id in config
        :param manga_id:
        :return:
        """
        url = MANGAS[manga_id]['url']

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                latest_chapter = MANGAS[manga_id]['function'](soup)

                return manga_id, latest_chapter

    def get_data(self):
        """get data  from storage
        """
        return self.storage.get()


    def store_data(self):
        """store data to storage
        """
        self.storage.update(self.data)

    def update_view_manga(self, manga_id):
        self.data[manga_id]['is_read'] = 1
        self.store_data()
