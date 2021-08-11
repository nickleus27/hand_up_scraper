import scrapy


search = 'https://google.com/search?q='
county = 'santa cruz' #fill this in with cmd line arg
resource = ' soup kitchens and free meals'
mycounter = 0

class QuotesSpider(scrapy.Spider):
    name = "scraper_two"
    start_urls = [
        search + county + resource,
    ]

    def parse(self, response):
        global mycounter
        #for quote in response.css('div.quote'):
            #yield {
                #'text': quote.css('span.text::text').get(),
                #'author': quote.css('small.author::text').get(),
                #'tags': quote.css('div.tags a.tag::text').getall(),
            #}
            #yield scrapy.Request(url=url, callback=self.parse)
        if mycounter == 0:
            mycounter += 1        
            next_page = response.css('a::attr(href)')[23].get()
            #print(next_page)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                print('second print ' + next_page)
                yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            print('I AM HERE!!!<---------------------------------------------#####')
            #print(response.css('div'))
            filename = f'2nd_scrape_output.txt'
            with open(filename, 'wt') as f:
                for div in response.css('div::text').getall():
                    f.write(div + '\n')
            self.log(f'Saved file {filename}')