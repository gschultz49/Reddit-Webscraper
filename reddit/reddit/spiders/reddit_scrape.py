# Reddit scraper

# Step 1, activate the virtual env 
# From desktop in terminal
# source scrapey_test_env/bin/activate
# cd into the tutorial>tutorial>spiders


# type of calls in terminal:
# scrapy crawl <NAME> -a subr=<SUBREDDIT NAME> -o <OUTPUTFILE.EXTENSION>
# scrapy crawl reddit -o HomePagePosts.json
# scrapy crawl reddit -a subr=tifu -o tifuposts.jl
# scrapy crawl reddit -a subr=gaming -o gamingposts.json
# Default call:  scrapy crawl reddit 


# NOTE this only scrapes the "hot" page
    
import scrapy
# Because I like terminal colors
class bcolors:
    #PINK
    HEADER = '\033[95m'
    #DARKBLUE
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    #YELLOW
    WARNING = '\033[93m'
    #RED
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Has capacity to choose a singular subreddit to parse, without argument the default is homepage
class RedditScraper(scrapy.Spider):
    # name to call in argument "scrapy crawl <name>"
    name = "reddit"
    def start_requests(self):
        subr = getattr(self, 'subr', None)
        if subr==None:
            start_urls =[
                # default if no subreddit requested
                'https://reddit.com/'
            ]
        else:
            start_urls = [
                'https://www.reddit.com/r/'+subr
            ]
        # Subreddit identification
        if subr!=None:
            print bcolors.WARNING + "Subreddit to parse: " + subr + bcolors.ENDC
            print bcolors.WARNING +start_urls[0] +bcolors.ENDC

        # start Request and parse callback
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # actually does the work based on CSS selector
    def parse(self, response):  
        for post in response.css('.link'):
            # to add colors to terminal
            print  bcolors.OKGREEN + "NEW POST" + bcolors.ENDC
            # kick out for the json
            yield{
                'Post Title': post.css('.title::text').extract_first(),
                'PublishDateTime' : post.css('.tagline .live-timestamp::attr(title)').extract_first(),
                # Reddit is weird and stores 3 different vote settings, upvotes are last
                'Upvotes': post.css('.thing .score::text').extract()[2],
                'Link' : post.css('.link .title::attr(href)').extract_first(),
            }
            print  bcolors.OKGREEN + "END POST" + bcolors.ENDC
        
        # -----Searching for next page-------
        # full URL of next page
        next_page = response.css('.next-button a::attr(href)').extract_first()
        
        #getting some weird cap out, maybe reddit limits
        try:
            next_page_index= next_page.find('?')
        except:
            return
        # chopped url starting at '?'
        next_page_url=next_page[next_page_index:]

        if next_page_url is not None:
            print bcolors.HEADER + "------NEW PAGE------" + bcolors.ENDC
            # urljoing is a weird af method
            next_page = response.urljoin(next_page_url)
            print bcolors.HEADER + "NEW PAGE URL:  " +next_page + bcolors.ENDC
            # recursive call
            yield scrapy.Request(next_page, callback=self.parse)


# command to save the data in posts.jl, (optional stuff)
# scrapy crawl reddit (-a subr=tifu) (-o posts.jl)
