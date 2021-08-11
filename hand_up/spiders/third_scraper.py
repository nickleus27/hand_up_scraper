import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd

search = 'https://google.com/search?q='
county = 'santa cruz' #fill this in with cmd line arg
resource = ' soup kitchens and free meals'
mycounter = 0

class QuotesSpider(scrapy.Spider):
    name = "scraper_three"
    start_urls = [
        search + county + resource,
    ]

    def parse(self, response):
        df = pd.DataFrame()
        link_list=[]
        link_text=[]
        div_list = []
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
            filename = '3rd_scrape_output.csv'
            for div in response.css('div::text').getall():
                div_list.append(div)

            for div in div_list:
                print(div)
            print('I AM HERE!!!<---------------------------------------------#####')
            xlink = LinkExtractor()
            for link in xlink.extract_links(response):
                if len(str(link))<200 or 'Santa Cruz' in link.text:
                    print(len(str(link)),link.text,link,"\n")
                    link_list.append(link)
                    link_text.append(link.text)
            df['links']=link_list
            df['link_text']=link_text
            #df['div']=div_list
            df.to_csv(filename)