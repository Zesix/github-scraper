import traceback
import os
import os.path
from datetime import datetime
import multiprocessing
import requests
from lxml import html

# input github url
input_url = 'https://github.com/orgs/salesforce/repositories'

output_file_name = 'output.txt'

def print_log(msg: str):
    """
    print message and writes to log.txt
    :param msg:
    :return:
    """
    try:
        print(msg)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("log.txt", 'a+') as f:
            f.write('[{}] {}\n'.format(now, msg))
    except Exception as e:
        print(traceback.format_exc())

def save_report(links, filename):
    """
    :param message_text:
    :return:
    """
    try:
        with open(filename, 'w') as f:
            for link in links:
                f.writelines(link + '\n')
        print_log("Saved to: {}".format(filename))
    except Exception:
        print("Exception in save_report: {}".format(str(e)))
        print_log(traceback.format_exc())

def get_all_repos(url):
    """
    :param url: URL of the org (please use the same format as above)
    :return: links to the repos
    """
    try:
        headers = {
            'Accept': 'text/html',
            'Accept-Language': 'en-GB,en;q=0.9',
            'If-None-Match': 'W/"5b617a3654aee51abdc38903571a1a69"',
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
            'Referer': 'https://github.com/orgs/salesforce/repositories?q=&type=public&language=&sort=name',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
        }
        global_links = []
        page = 0
        # iterating pages
        while True:
            page += 1
            print(url + "?language=&page={}&q=&sort=&type=public".format(str(page)))
            response = requests.get(url.strip() + "?language=&page={}&q=&sort=&type=public".format(str(page)),
                                    headers=headers)
            print_log("Processing page:{}".format(str(page)))
            # parsing response is response code  is 200
            if response.status_code == 200:
                tree = html.fromstring(response.content.decode('utf-8'))
                # extrracting all the repo links via XPATH
                links = tree.xpath('//a[@data-hovercard-type="repository"]/@href')
                links = ['https://github.com' + x for x in links]
                # adding to global list of links
                global_links.extend(links)
                if len(links) == 0:
                    break
                print_log("New {} links extracted".format(len(links)))
            else:
                print_log("Request failed: {}".format(str(response.status_code)))
                break
        return global_links
    except Exception as e:
        print_log("Exception in process_links: {}".format(str(e)))
        print_log(traceback.format_exc())

def recreate_log_file():
    """
    recreats log.txt file
    :return:
    """
    try:
        # removing LOG file of previous session if exists
        if os.path.exists("log.txt"):
            os.remove("log.txt")
    except Exception as e:
        print_log("Except exception in recreate_log_file: {}".format(str(e)))
        print_log(traceback.format_exc())

def main():
    """
    the main pipeline
    :return:
    """
    try:
        # recrreating LOG.txt (jsut a log file)
        recreate_log_file()
        print_log("Started!")
        print_log("URL: {}".format(input_url))
        # getting all thelinks
        links = get_all_repos(input_url)
        # saving to .txt file
        save_report(links, output_file_name)
        print_log("Finished!")
    except Exception as e:
        print_log("Except exception in main: {}".format(str(e)))
        print_log(traceback.format_exc())

# we should check if the method is main to call it from other scripts and threds0520.pdf
if __name__ == '__main__':
    # freeze support allows to use multiprocessing on Windows
    multiprocessing.freeze_support()
    main()
