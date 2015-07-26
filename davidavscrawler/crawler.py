# -*- coding: utf-8 -*-
from urllib2 import urlparse
import argparse
import sys

from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class DavidAvsSpider(Spider):
    name = 'davidavscrawler'
    extractor = LinkExtractor()

    def __init__(self, *args, **kwargs):
        super(DavidAvsSpider, self).__init__(*args, **kwargs)
        self.links_seen = set()
        self.links_fetched = set()  # May be different due to 302 redirects

    def parse(self, response, level=1):
        # Check if this url already has been returned
        if response.url in self.links_fetched:
            return
        self.links_fetched.add(response.url)

        # Collect links
        links = set()
        # for href in response.css('a::attr(href)'):
        #     full_url = response.urljoin(href.extract())
        for link in self.extractor.extract_links(response):
            full_url = response.urljoin(link.url)
            links.add(full_url)
            if full_url not in self.links_seen:
                self.links_seen.add(full_url)
                yield Request(full_url, callback=lambda resp: self.parse(resp, level+1))

        # Collect static objects
        imgs = set()
        for href in response.css('img::attr(src)'):
            full_url = response.urljoin(href.extract())
            imgs.add(full_url)

        # Yield the page
        yield {
            'url': response.url,
            'level': level,
            'links': filter(self.is_link, links),
            'pages': filter(self.is_page, links),
            'images': list(imgs),
        }

    def is_page(self, url):
        """Return `True` if the url is a page on the website."""
        netloc = urlparse.urlparse(url).netloc.lower()
        return any(map(lambda domain: netloc.endswith(domain), self.allowed_domains))

    def is_link(self, url):
        """Return `True` if the url is an external link."""
        return not self.is_page(url)


class CrawlerCli(object):
    """Command-line interface for crawler"""

    def parse_args(self, *args):
        """Parses command-line arguments"""
        # Command-line interface
        parser = argparse.ArgumentParser(
            description='Simple website parser that parses a single domain and creates a simple JSON sitemap.',
        )
        parser.add_argument('url', help='Starting URL to be parsed.')
        parser.add_argument('file', type=argparse.FileType('w'), default=sys.stdout, nargs='?',
                            help='File to write the JSON output (default: stdout).')
        parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging to stderr')
        return parser.parse_args(args or None)

    def run_crawl(self, args):
        """Run parallel crawling process using Scrapy backed with Twisted"""

        # Crawler process declaration
        process = CrawlerProcess({
            'USER_AGENT': 'David Avs Crawler',
            'FEED_FORMAT': 'json',
            'FEED_URI': 'stdout:',
            'LOG_ENABLED': args.verbose,
        })
        kwargs = dict(
            start_urls=[args.url],
            allowed_domains=[urlparse.urlparse(args.url).netloc.lower()],
        )

        # Run crawling
        old_stdout = sys.stdout
        sys.stdout = args.file
        try:
            process.crawl(DavidAvsSpider, **kwargs)
            process.start()
        finally:
            sys.stdout = old_stdout

    def run(self):
        """The main method"""
        args = self.parse_args()
        self.run_crawl(args)


def main():
    cli = CrawlerCli()
    cli.run()


if __name__ == '__main__':
    main()
