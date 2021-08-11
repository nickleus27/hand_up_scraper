import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd

#learn how to use command line arguments to put in different counties / resources: food/ shelt...etc

search = 'https://google.com/search?q='
county = 'santa cruz' #fill this in with cmd line arg
resource = ' soup kitchens and free meals'

class QuotesSpider(scrapy.Spider):
    name = "sc_food"

    def start_requests(self):
        urls = [
            search + county + resource
            #'https://google.com/search?q=santa cruz soup kitchens'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        df = pd.DataFrame()
        link_list=[]
        link_text=[]
        text = []
        page = '1st'
        filename = f'{page}_scrape_links-text'
        xlink = LinkExtractor()
        for link in xlink.extract_links(response):
            if len(str(link))<200 or 'Santa Cruz' in link.text:
                print(len(str(link)),link.text,link,"\n")
                text.append(link.text)
                link_list.append(link)
                link_text.append(link.text)
        print(text)
        df['links']=link_list
        df['link_text']=link_text
        df.to_csv('1st_scrape_output.csv')
        with open(filename, 'wb') as f:
            for line in text:
                f.write(line + '\n')
            self.log(f'Saved file {filename}')
