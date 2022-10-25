# github-scraper
A Python script that outputs to a .txt file the clone URLs of each public repo of a given organization or user set at the top of the script.

This project is released under the [Unlicense]([https://github.com/Zesix/cloc-runner/blob/master/LICENSE](https://github.com/Zesix/github-scraper/blob/main/LICENSE), meaning you can do whatever you want with it.

## Usage ##

1. Edit github_scraper.py and edit the input_url variable to be the organization or user you wish to scrape. Example:

     input_url = 'https://github.com/orgs/salesforce/repositories'

2. Ensure you have installed the required dependences for the script:

    pip install requests
    pip install lxml
    
3. Open an Administrator Powershell, Command Window, or other Terminal and run:

    ./github_scraper.py

When it is finished, you can see the results in the output.txt file created in the same folder. There will also be a log.txt file that contains the execution log of the script.

## Setup ##

If you are behind a corporate proxy, ensure port 443 can reach GitHub.com.

Required Dependencies:

 - Python 3
 - requests (Python package)
 - lxml (Python package)
