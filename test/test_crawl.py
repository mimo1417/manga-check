# -*- coding: utf-8 -*-
# @Author: vietvu
# @Date:   2016-10-11 18:55:14
# @Last Modified by:   Viet Vu
# @Last Modified time: 2016-10-12 10:24:24
import unittest
from manga_check.crawler import MangaCrawler

class TestCrawl(unittest.TestCase):
    crawler = MangaCrawler()
    
    def testCheck(self):    
        self.assertIsInstance(self.crawler.check(), list)

    def testCrawl(self):
        self.assertIsInstance(self.crawler.crawl(1), int)

