# NightJobCrawler
A simple crawler that scrapes night shift jobs from a job board and outputs them to a CSV feed. 
The CSV feed has two columns: url and title.

<h3>How do I run this program?</h3>
1. Launch your terminal
2. Run "pip install -r requirements.txt"
3. Run "python scraper.py" with the following arguments:
<pre>
<code>
-s --storage_dir    :   The directory the csv file is created at
-j --job_board      :   The name of the job board 
-p --page_limit     :   The number of search pages to scrape
</code>
</pre>

<h4>Example:</h4> 
<code>
python scraper.py -s "/home/user/Documents/jobs/" -j "monster" -p 12
</code>

The above command scrapes Monster.com jobs from 12 search pages and outputs them to /home/user/Documents/jobs/night_urls.csv.

<h3>Note:</h3>
This currently only supports the Monster job board.

<h3>TODO</h3>
<ul>Add support for other job boards like LinkedIn, CareerBuilder, SimplyHired.</ul>
<ul>Add more job fields like location, description, etc.</ul>
<ul>Add a command-line argument for search terms.</ul>
