# hand_up_scraper
A webcrawler to extract data for hand_up app. A mobile app to provide resources for people experiencing houslessness. This webcrawler extracts data of free food pantries and free soup kitchens per counties in California. The webcrawler parses the data to a text file with each line containing information such as:
	1.	Organizations name
	2.	Address
	3.	Phone number
	4.	Email
	5.	Webiste
	6.	Hours Open
The next step is to run a program that reads a line in at a time from the text file, and adds to a row in a SQLite database for the hand_up mobile app.
What I have learned: I have learned how to use the scrapy framework for making webcrawler in python, I learned how to parse data from a html, and how to filter text with regular expressions. Also, I experimented with saving text data with pandas library to .csv file.
