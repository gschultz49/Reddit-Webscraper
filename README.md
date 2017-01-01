# Reddit webscraper
All commands are executed in the
<code>/reddit_scraper/reddit/reddit/spiders  </code> directory

# See the results of Reddit's front page in your command line
Run <code>scrapy crawl reddit</code>

# To crawl a specific subreddit
<code>scrapy crawl reddit -a subr=SUBREDDIT_NAME</code>


ex: <code>scrapy crawl reddit -a subr=programming</code>

# Store the results of any call in a file
<code>scrapy crawl reddit -o FILE.EXT</code>


ex: <code>scrapy crawl reddit -a subr=programming -o program.json </code>


Supported file extensions: 'xml', 'jsonlines', 'jl', 'json', 'csv', 'pickle', 'marshal'





