# -*- coding: utf-8 -*-
# Manga crawler class
import operator
from manga_check.config import DATA_FILE, MANGAS
import csv
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import traceback


class MangaCrawler(object):
    """Manga crawler class"""

    def __init__(self, logger=lambda _: None):
        try:
            file_data = csv.reader(open(DATA_FILE, 'r'))
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

        self.write_to_file()
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

    def write_to_file(self):
        writer = csv.writer(open(DATA_FILE, 'w'))
        for _, data in self.data.items():
            writer.writerow([data['id'], data['chapter'], data['is_read']])

    def update_view_manga(self, manga_id):
        self.data[manga_id]['is_read'] = 1
        self.write_to_file()
