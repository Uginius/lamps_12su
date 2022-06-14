import datetime
import time
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Product12 import Product12
from utilites import time_track, get_last_file, check_dir


class Getter12:
    def __init__(self):
        self.login_url = 'https://1-2.su/site/guest/id/8'
        self.category_url = 'https://1-2.su/catalog/section/id/31'
        self.src_dir = 'htmls/'
        self.soup = None
        self.product = None
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.workbook = xlsxwriter.Workbook(f'results/{self.date}_data.xlsx')
        self.worksheet = self.workbook.add_worksheet()

    def run(self):
        check_dir(self.src_dir)
        self.get_link()
        self.read_src()
        check_dir('results/')
        self.parse_src()

    def read_src(self):
        with open(get_last_file(), mode='r', encoding='utf8') as file:
            src = file.read()
        self.soup = BeautifulSoup(src, 'lxml').find('table', class_="table table-hover")

    @time_track
    def get_link(self):
        browser = webdriver.Chrome(service=Service(executable_path='SeleniumDrivers/chromedriver.exe'))
        browser.get(self.login_url)
        browser.get(self.category_url)

        pause_time = 0.5
        while True:
            last_height = browser.execute_script("return document.body.scrollHeight")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(pause_time)
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue
        with open(f'{self.src_dir}{self.date}_lamps.html', 'w', encoding='utf8') as file:
            file.write(browser.page_source)

    @time_track
    def parse_src(self):
        trs = self.soup.find_all('tr')
        del trs[0]
        del trs[0]
        self.write_first_line()
        for i, tr in enumerate(trs):
            self.product = Product12(tr)
            self.product.parse()
            self.product.order = i + 1
            self.xlsx_writer()
            # self.product.print_out()
        self.workbook.close()

    def write_first_line(self):
        bold = self.workbook.add_format({'bold': True})
        self.worksheet.set_column(1, 1, 50)
        self.worksheet.set_column(2, 2, 40)
        self.worksheet.write('A1', 'id', bold)
        self.worksheet.write('B1', 'name', bold)
        self.worksheet.write('C1', 'url', bold)
        self.worksheet.write('D1', 'status', bold)
        self.worksheet.write('E1', 'price', bold)

    def xlsx_writer(self):
        i = self.product.order + 1
        self.worksheet.write(f'A{i}', self.product.id)
        self.worksheet.write(f'B{i}', self.product.name)
        self.worksheet.write(f'C{i}', self.product.url)
        self.worksheet.write(f'D{i}', self.product.status)
        self.worksheet.write(f'E{i}', self.product.price)
