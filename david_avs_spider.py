import scrapy


class DavidAvsSpider(scrapy.Spider):
    name = 'davidavs'
    allowed_domains = ['davidavs.com']
    start_urls = ['http://davidavs.com']
    links_seen = set()
    links_fetched = set()  # May be different due to 302 redirects

    def parse(self, response, level=1):
        # Check if this url already has been returned
        if response.url in self.links_fetched:
            return
        self.links_fetched.add(response.url)

        # Collect links
        links = set()
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            links.add(full_url)
            if full_url not in self.links_seen:
                self.links_seen.add(full_url)
                yield scrapy.Request(full_url, callback=lambda resp: self.parse(resp, level+1))

        # Collect static objects
        imgs = set()
        for href in response.css('img::attr(src)'):
            full_url = response.urljoin(href.extract())
            imgs.add(full_url)

        # Yield the page
        yield {
            'url': response.url,
            'level': level,
            'links': list(links),
            'images': list(imgs),
        }
