import scrapy

class TranscriptSpider(scrapy.Spider):

    name = 'transcript'
    start_urls = ['https://www.fool.com/earnings-call-transcripts/?page=' + str(n) for n in range(1, 101)]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 4,
    }

    def parse(self, response):
        transcript_links = response.css('article > div.text > h4 > a::attr(href)').extract()
        for url in transcript_links:
            yield scrapy.Request(response.urljoin(url), callback=self.transcript_text)


    def transcript_text(self, response):
        header = response.css('section > header > h1::text').extract_first()
        content_list = response.css('div.main-col > section > span.article-content > p::text').extract()
        path_folder = '/home/coffeeincodeout/developer/earnings-transcripts/transcripts/transcripts/transcript_texts/'
        content = " ".join(content_list)
        f = open(path_folder + header + ".txt", "w+")
        f.write(content)
        f.close()

