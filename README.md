# Scraper

## Introduction
Welcome to Scraper.
This application is a very simple program with a command-line interface and its purpose was
initially to automate a very simple scraping algorithm that was often by the author.
The application features numerous commands that work to give control over the interface itself, the
csv file that is specified and the scraping options.
While web scraping remains a task that has numerous tools and demands, this application attempts to
keep it simple by allowing the user to simply specify 2 things:
-HTML Element
-Element Class
While one might want to scrape on the basis of id or options other than class, the author has deemed
for the sake of simplicity class to be the best and only option to feature in this application.
As this application has been born from a necessity to automate some simple scraping, it is regularly
updated to meet first and foremost the needs of its author.
Commands have been made very simple and short, but perhaps at the cost of total off-the-bat clarity
of what they do. However, proper documentation has been provided for the commands and can be viewed
using help/? <cmd>.
The application requires some peculiar things as well:
1)Parser
-lxml
-html.parser
-html5lib
2)Webpages
-An initial webpage
-A template for the rest of the pages replacing page number in the url with $
Follow command documentation carefully.
  
 ## Requirements
 -Python3
 -Beautiful Soup Library (bs4)
 -Colorama
 -Selenium
 -Chrome WebDriver
