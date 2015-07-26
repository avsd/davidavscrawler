#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import mock

from davidavscrawler.crawler import DavidAvsSpider, CrawlerCli
from scrapy.http import Response, Request


class TestDavidavsCrawler(unittest.TestCase):

    def test_cli(self):
        cli = CrawlerCli()
        args = cli.parse_args('http://davidavs.com')
        self.assertEqual(args.url, 'http://davidavs.com')
        self.assertEqual(args.file, sys.stdout)


if __name__ == '__main__':
    unittest.main()
