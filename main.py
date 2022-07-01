import datetime
from bs4 import BeautifulSoup
import requests
from xlsxwriter import Workbook
import time


class youtube_link:
    def __init__(self):
        self.minimum_characters = 1
        self.account_name = "bundlescrape"


    def driver_setup(self):
        url = "https://coreyms.com/"
        source = requests.get(url).text
        self.soup = BeautifulSoup(source, "lxml")
        self.article_search()

    def article_search(self):
        articles = self.soup.find_all("article", itemtype="https://schema.org/CreativeWork")
        content_lists = []
        for article in articles:
            headline = article.find("a", class_= "entry-title-link").text
            headline = headline.split(",")
            headline_string_ ="".join(headline)
            print(headline_string_)

            content = article.find("div", class_= "entry-content").text
            for cont_ in content:
                cont_.split(",")
                #print(content)
            try:
                infame = article.find("iframe")["src"]
                split1 = infame.split("/")[4]
                video_id = split1.split("?")[0]
            except:
                pass

            yt_link = f"https//:youtube.com/watch?v={video_id}"
            yt_link = yt_link.split(",")
            yt_link_string_ = "".join(yt_link)#convering list to string
            print(yt_link_string_)

            art_tuple = (headline_string_, yt_link_string_, content)
            content_lists.append(art_tuple)

        self.excel_saver(content_lists)

    def excel_saver(self, content_lists):  # will take a list of tuples
        link_name = (str(datetime.datetime.now()).replace(" ", "_").replace(":", "_").split(".")[0])
        with Workbook(f"{self.account_name}_{link_name}.xlsx") as workbook:
            worksheet = workbook.add_worksheet()
            row, col = 0, 0

            for marks in content_lists:
                headline_string_ = marks[0]
                yt_link_string_ = marks[1]
                content = marks[2]
                try:
                    worksheet.write(row, col, headline_string_)
                    worksheet.write(row, col + 1, yt_link_string_)
                    worksheet.write(row, col + 2, content)
                    row += 1
                except Exception as e:
                    print(e, "inner save while loop")

    def run(self):
        self.driver_setup()

if __name__== "__main__":
    scrapper = youtube_link()
    scrapper.run()