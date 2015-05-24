import logging
import argparse
import requests
import time
import os
import csv
from bs4 import BeautifulSoup

class Scraper(object):
    def __init__(self):
        self.search_terms = []

    def storeUrls(self, jobs, storage_dir):
        file_path = os.path.join(storage_dir, 'night_urls.csv')
        download_file = open(file_path, 'wb')
        csv_writer = csv.writer(download_file)
        #header row
        csv_writer.writerow(jobs[0].keys())
        #add data rows
        for job in jobs:
            csv_writer.writerow(list(job.values()))

        download_file.close()
        logging.debug('Downloaded {} urls to {}'.format(len(jobs), file_path))

    def downloadUrl(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Non-OK status code:{}'.format(r.status_code))
        return r.text
    
    def monsterJobs(self, storage_dir, page_limit):
        """ Return all Monster job urls per term"""
        base_url  = 'http://jobsearch.monster.com/search/?'
        time_limit = 'tm=Last-30-days'
        jobs = []
    
        for search_term in self.search_terms:
            query_url = base_url + time_limit + '&q=' +  search_term.replace(' ', '-')
            page = 0
            count = 0 
            while True:
                page += 1
                logging.debug('Crawling "{}" search page {}...'.format(search_term, page))
                current_page = self.downloadUrl(query_url + '&p=' + str(page))
                time.sleep(1)
                
                bs = BeautifulSoup(current_page)
                #all jobs on a single search page
                all_posts = bs.findAll('div',{'class' : 'jobTitleContainer'})
                if all_posts is not None:
                    for post in all_posts:
                        job_url = post.find('a')
                        job_title = post.text.encode('ascii', 'ignore').replace('\n', '')
                        jobs.append({"url":job_url['href'], "title":job_title})
                        count += 1
                else:
                    #last job page
                    break
                 #TODO set max pages, placeholder for now
                if page == 100 or page == page_limit:
                    break
            logging.debug('Found {} job urls for search term: {}'.format(count, search_term))
        if count > 0:
            self.storeUrls(jobs, storage_dir)   

    def downloadJobs(self, storage_dir, job_board, page_limit):
        self.search_terms = ['night shift', 'evening shift']
        #TODO add support for more job boards
        all_boards = ['monster']
        if job_board.lower() in all_boards:
            self.monsterJobs(storage_dir, page_limit)
        else:
            print 'Job board not supported. Please specify another board from list: '
            print ', '.join(all_boards)
            exit()

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(description='Download night jobs')
    parser.add_argument('-s', '--storage_dir', dest='storage_dir', required=True)
    parser.add_argument('-j', '--job_board', dest='job_board', required=True, 
            help='Specify job board')
    parser.add_argument('-p', '--page_limit', dest='page_limit', 
            help='Specify number of pages to crawl', 
            nargs ='?', 
            default=10, 
            type=int)
    args = parser.parse_args()
    scraper = Scraper()
    scraper.downloadJobs(args.storage_dir, args.job_board, args.page_limit)

if __name__ == '__main__':
    main()
