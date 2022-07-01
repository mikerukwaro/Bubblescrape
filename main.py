from selenium.webdriver.common.by import By
from xlsxwriter import Workbook
from selenium import webdriver
import datetime
import time
import re


def clean_text_content(inner_body):
    inner_body_less_tnr = inner_body.strip("\t\n \r")
    non_ascci_removed = re.sub(r"[^\x00-\x7F]+", " ", inner_body_less_tnr)
    extra_space_removed = re.sub(" +", " ", non_ascci_removed)
    body_single_newline = re.sub(r"\n\s*\n", "\n\n", extra_space_removed)
    url_stripped_content = re.sub(r"http\S+", "", body_single_newline)
    return url_stripped_content


class OnlyProfessors:
    def __init__(self):
        self.driver = None
        self.sitemap_to_search = None
        #self.homepage_link = None
        self.sitemaps = None
        self.account_name = "assignmentbay"
        self.minimum_characters = 10
        self.scrap_complete = False
        self.discarded = 0

    def initialize_defaults(self):
        self.driver = webdriver.Chrome(
            "assets/chromedriver.exe"
        )

    def homepage(self):
        self.homepage_link = "https://assignmentbay.org/sitemap_index.xml"
        self.driver.get(self.homepage_link)

    def driver_setup(self):
        self.driver.maximize_window()
        time.sleep(4)

    def sitemap(self):
        all_sitemaps = self.driver.find_elements(
            By.XPATH, '//*[@id="sitemap"]/tbody/tr/td/a'
        )
        sitemap_urls = [map_.get_attribute("href") for map_ in all_sitemaps]
        for url in sitemap_urls[:2]:
            self.driver.get(url)
            self.articles(url)

    def articles(self, url):
        all_articles = self.driver.find_elements(
            By.XPATH, '//*[@id="sitemap"]/tbody/tr/td/a'
        )
        articles_urls = [art_.get_attribute("href") for art_ in all_articles]

        articles_to_save = []
        for article in articles_urls[:20]:
            self.driver.get(article)
            with open("last.txt", "w+") as f:
                f.write(url)
            with open("last.txt", "a+") as f:
                f.write("\n" + article)
            question_details = self.get_question_title_content()
            if question_details[-1] is not None:
                articles_to_save.append(question_details)

        chunked_list = self.create_chunks(articles_to_save, 10)
        for chunk in chunked_list:
            self.excel_saver(chunk)
            time.sleep(5)

    def create_chunks(self, raw_list, chunk_size):
        chucked_list = []

        for i in range(0, len(raw_list), chunk_size):
            chucked_list.append(raw_list[i : i + chunk_size])

        return chucked_list

    def get_question_title_content(self):
        title_raw = self.driver.find_element(By.CLASS_NAME, "entry-header")
        title = title_raw.text
        content = self.get_article_content()
        clean_content = clean_text_content(content)
        return title, clean_content

    def get_article_content(self):
        try:
            content_raw = self.driver.find_element(
                By.XPATH, '//div[@class="entry-content"]'
            )
            return content_raw.text
        except:
            return None

    def excel_saver(self, get_question_title_content):  # will take a list of tuples
        link_name = (
            str(datetime.datetime.now())
            .replace(" ", "_")
            .replace(":", "_")
            .split(".")[0]
        )
        with Workbook(f"{self.account_name}_{link_name}.xlsx") as workbook:
            worksheet = workbook.add_worksheet()
            row, col = 0, 0

            for question in get_question_title_content:
                title = question[0]
                content = question[-1]
                try:
                    if len(content) > self.minimum_characters:
                        worksheet.write(row, col, title)
                        worksheet.write(row, col + 1, content)
                        row += 1

                except Exception as e:
                    print(e, "inner save while loop")

    def run(self):
        self.initialize_defaults()
        self.homepage()
        self.driver_setup()
        self.sitemap()


if __name__ == "__main__":
    scrapper = OnlyProfessors()
    scrapper.run()
