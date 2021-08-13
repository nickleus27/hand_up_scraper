import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "sc_food_scraper"


    def start_requests(self):
        urls = [
            'https://www.freefood.org/c/ca-santa_cruz',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        global file
        divs = response.xpath('//*/div[contains(@class, "event-box")]')
        if len(divs) != 0:#check to see if in starting url or one of the links
            for link in divs:
                details_link =  link.css('a').attrib['href']
                if details_link is not None:
                    yield scrapy.Request(url=details_link, callback=self.parse)

        ###---------> BREAK CODE BELOW INTO HELPER FUNCTIONS <-----------###
        else:#code to scrape info from each link
            print('<-------------------------###')
            details_div = response.xpath('//*/div[contains(@class, "col-md-6")]')
            contact_links = details_div.xpath('//*/div[contains(@style, "margin-top:20px;")]').css('a::attr(href)').getall()#this gets all the contact url links
            phone_soup = details_div.xpath('//*/div[contains(@style, "margin-top:20px;")]').get()

            #hours and times open, needs work
            times = response.xpath('//*/div[contains(@class, "text-box")]').css('ul').css('li').getall()#hours and days open
            time_string = ''
            p = re.compile(r'<.*?>')
            for line in times:
                days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                line = p.sub('', line)
                hour_match = re.search(r'\d:\d{2}', line)
                if(hour_match):
                    time_string += line + '\n'
                    continue
                for day in days:
                    if day in line:
                        time_string += line + '\n'

            #this is a regex for finding where it says "Phone:" and extracting the phone number afterwards
            phone_match = re.search(r"Phone: (\(\d+\)) (\d+-\d+)", phone_soup)#phone number regex
            phone_num = phone_match.group(1) + phone_match.group(2) 


            #this is for extracting email and  webpage link
            email = ''
            weblink = ''
            #contact_links = contact_div.css('a::attr(href)').getall()#this gets all the contact url links
            for links in contact_links:
                if links == email or links == weblink:
                    continue
                email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'#regex to check for emails string
                #regex to check if url
                web_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                if len(links)>=7:
                    if links[:7] == 'mailto:':#removes the mailto: that prefixes the mail addresses
                        links = links[7:]
                        if(re.fullmatch(email_regex, links)):
                            email = links
                            continue
                url = re.findall(web_regex, links)
                if len(url)>0:
                    temp = ''
                    for x in url:
                        temp = x[0] #extradts the url that is at first index of find all list
                        break
                    if 'facebook' in temp or 'instagram' in temp: # makes sure that this is not a facebook or instagram link...only want website url<---MAY MAKE THIS TITER CODE
                        pass
                    else:
                        weblink = temp
            #extracting email and webpage link ends

            name = details_div.css('h3::text').get()#name of organization

            #this is for extracting addresss
            info = str(details_div.css("div.col-md-6::text").getall())#information soup for extacting address
            p = re.compile(r'\\r+|\\n+|\\t+|\[+|\]+|\'+|,+|-+')#regex to get rid of new line/ return/ tab: \r \n \t
            rep = p.sub('', info)#replaces above charactes with empty string
            rep.replace(" ", "")#gets rid of whitespace
            address = " ".join(rep.split())#adds spaces between words
            #address extraction ends

            print(name, address, phone_num, email, weblink, time_string)
            filename = f'sc_food_scrape_3.txt'
            with open(filename, 'a') as f:
                f.write(name + '\n' + address + '\n' + phone_match.group(1) + phone_match.group(2) + '\n' + email + '\n' + weblink +'\n' + time_string + '\n' + '\n')
            self.log(f'Saved file {filename}')
    