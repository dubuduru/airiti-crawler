from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import re

JOURNALS = [
            ("10232842", "Sun Yat-sen Management Review"), 
            ("P20140110001", "Taiwan Accounting Review"), 
            ("10287353", "Journal of Technology Management"), 
            ("10222898", "Journal of Financial Studies")
            ]

driver = webdriver.Chrome('your-chromedriver-path')
SAVE_PATH = "your/save/path/"
CATEGORY = "subdir_name/"

PAGE = "https://www.airitilibrary.com/Publication/alPublicationJournal?PublicationID="


for (CODE, NAME) in JOURNALS:
    FILE_NAME = SAVE_PATH + CATEGORY + NAME + ".csv"
    with open(FILE_NAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        url = PAGE + CODE #airiti library journal main page
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        tree = soup.find("ul", attrs={"class": "tree", "id": "tree"})

        year_li = tree.find("li", attrs={"class": "collapsable"})
        issue_lis = year_li.find_all("li")
        issue_year = year_li.find("a").contents[0]
        print(issue_lis)
        goto = 0
        if issue_lis is None or len(issue_lis) < 1:
            goto = 1
        
        if goto == 0:
            for issue_li in issue_lis:
                print(issue_li)
                issue_index = issue_li.find("a")["id"]
                print(issue_index)
                issue_url = url + "&IssueID=" + issue_index

                driver.get(issue_url)
                time.sleep(1)

                issue_html = driver.page_source
                issue_soup = BeautifulSoup(issue_html, 'html.parser')
                issue_info = issue_soup.find("div", attrs={"class": "txt"})
                if issue_info is None or len(issue_info.contents) < 1:
                    continue
                issue_info = re.findall(r'\d+', issue_info.contents[0])
                print(issue_info)

                if issue_info is None or len(issue_info) < 1:
                    continue
                
                issue_num = str(issue_info[0])
                if len(issue_info) > 1:
                    issue_num = issue_num + "." + str(issue_info[1])

                for inner in issue_soup.find_all("td", attrs={"class": "titleB"}):
                    href = inner.find("a")["href"]
                    inner_url = "https://www.airitilibrary.com" + href
                    print(inner_url)
                    
                    driver.get(inner_url)
                    time.sleep(1)

                    inner_html = driver.page_source
                    inner_soup = BeautifulSoup(inner_html, 'html.parser')

                    abstract = inner_soup.find("textarea", attrs={"class": "TextArea2"})
                    if abstract is None or len(abstract.contents) < 1:
                        continue
                    abstract = abstract.contents[0]

                    if len(abstract) < 2:
                        continue

                    if abstract[0] > "z" and abstract[1] > "z" and abstract[-2] > "z":
                        abstract = inner_soup.find("textarea", attrs={"class": "TextArea1"})
                        if abstract is None or len(abstract.contents) < 1:
                            continue
                        abstract = abstract.contents[0]

                    inner_info = inner_soup.find("div", attrs={"class": "detail"}).find_all("p")
                    if len(inner_info) != 6:
                        continue

                    title = inner_info[1].find("a")
                    if title is None or len(title.contents) < 1:
                        continue
                    title = title.contents[0]

                    if len(title) < 2:
                        continue

                    if title[0] > "z" and title[1] > "z" and title[-2] > "z":
                        title = inner_info[0].find("a")
                        if title is None or len(title.contents) < 1:
                            continue
                        title = title.contents[0]

                    authors = []
                    for author in inner_info[2].find_all("a"):
                        if len(author.contents) < 1:
                            continue
                        if "(" in author.contents[0]:
                            author = re.findall('\(([^)]+)', author.contents[0])
                        else:
                            author = [author.contents[0]]
                        authors = authors + author

                    doi_url = inner_info[4].find("a")
                    if doi_url is None:
                        doi_url = ""
                    else:
                        doi_url = doi_url["href"]

                    keywords = set()
                    for keyword in inner_info[5].find_all("a"):
                        if len(keyword.contents) < 1:
                            continue
                        if len(keyword.contents[0]) > 0:
                            if keyword.contents[0][0] <= "z" and keyword.contents[0][-1] <= "z":
                                keywords.add(keyword.contents[0])
                    keywords = list(keywords)

                    print(abstract)

                    if abstract != "":
                        writer.writerow([title,  ", ".join(authors), ", ".join(keywords), abstract, inner_url, issue_num, issue_year, doi_url])

        for year_li in tree.find_all("li", attrs={"class": "expandable"}):
            issue_lis = year_li.find_all("li")
            issue_year = year_li.find("a").contents[0]
            print(issue_lis)
            if issue_lis is None or len(issue_lis) < 1:
                continue
            
            for issue_li in issue_lis:
                print(issue_li)
                issue_index = issue_li.find("a")["id"]
                print(issue_index)
                issue_url = url + "&IssueID=" + issue_index

                driver.get(issue_url)
                time.sleep(1)

                issue_html = driver.page_source
                issue_soup = BeautifulSoup(issue_html, 'html.parser')
                issue_info = issue_soup.find("div", attrs={"class": "txt"})
                if issue_info is None or len(issue_info.contents) < 1:
                    continue
                issue_info = re.findall(r'\d+', issue_info.contents[0])
                print(issue_info)

                if issue_info is None or len(issue_info) < 1:
                    continue
                
                issue_num = str(issue_info[0])
                if len(issue_info) > 1:
                    issue_num = issue_num + "." + str(issue_info[1])

                for inner in issue_soup.find_all("td", attrs={"class": "titleB"}):
                    href = inner.find("a")["href"]
                    inner_url = "https://www.airitilibrary.com" + href
                    print(inner_url)
                    
                    driver.get(inner_url)
                    time.sleep(1)

                    inner_html = driver.page_source
                    inner_soup = BeautifulSoup(inner_html, 'html.parser')

                    abstract = inner_soup.find("textarea", attrs={"class": "TextArea2"})
                    if abstract is None or len(abstract.contents) < 1:
                        continue
                    abstract = abstract.contents[0]

                    if len(abstract) < 2:
                        continue

                    if abstract[1] > "z" and abstract[-2] > "z":
                        abstract = inner_soup.find("textarea", attrs={"class": "TextArea1"})
                        if abstract is None or len(abstract.contents) < 1:
                            continue
                        abstract = abstract.contents[0]

                    inner_info = inner_soup.find("div", attrs={"class": "detail"}).find_all("p")
                    if len(inner_info) != 6:
                        continue

                    title = inner_info[1].find("a")
                    if title is None or len(title.contents) < 1:
                        continue
                    title = title.contents[0]

                    if len(title) < 2:
                        continue

                    if title[1] > "z" and title[-2] > "z":
                        title = inner_info[0].find("a")
                        if title is None or len(title.contents) < 1:
                            continue
                        title = title.contents[0]

                    authors = []
                    for author in inner_info[2].find_all("a"):
                        if len(author.contents) < 1:
                            continue
                        if "(" in author.contents[0]:
                            author = re.findall('\(([^)]+)', author.contents[0])
                        else:
                            author = [author.contents[0]]
                        authors = authors + author

                    doi_url = inner_info[4].find("a")
                    if doi_url is None:
                        doi_url = ""
                    else:
                        doi_url = doi_url["href"]

                    keywords = set()
                    for keyword in inner_info[5].find_all("a"):
                        if len(keyword.contents) < 1:
                            continue
                        if len(keyword.contents[0]) > 0:
                            if keyword.contents[0][0] <= "z" and keyword.contents[0][-1] <= "z":
                                keywords.add(keyword.contents[0])
                    keywords = list(keywords)

                    if abstract != "":
                        writer.writerow([title,  ", ".join(authors), ", ".join(keywords), abstract, inner_url, issue_num, issue_year, doi_url])


                        

