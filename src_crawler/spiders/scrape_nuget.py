# -*- coding: utf-8 -*-
import scrapy


class NuGetSpider(scrapy.Spider):
    name = "scrape_nuget"
    start_urls = [
        'https://www.nuget.org/packages',
    ]

    def parse(self, response):
        # follow links to package details
        for pkg in response.css('section.package'):
            href = pkg.css('div.side a::attr("href")').extract_first()
            yield response.follow(href, self.parse_detail)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)


    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name' : extract_with_css('div.package-page-heading h1::text'),
            'latest_version' : extract_with_css('div.package-page-heading h2::text'),
            'decsription' : extract_with_css('div.package-page p::text'),
            'tags' : response.css('ul.tags a::text').extract(),
            'homepage' : response.css('#sideColumn nav a::attr("href")')[0].extract(),
            'license' : response.css('#sideColumn nav a::attr("href")')[1].extract(),
            'download_url' : response.css('#sideColumn nav a::attr("href")')[4].extract(),
        }
