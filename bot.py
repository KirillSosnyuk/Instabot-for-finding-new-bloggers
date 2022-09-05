from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from langdetect import DetectorFactory, detect_langs
import time
import random
import datetime

class InstaBot():

    def __init__(self):
        self.browser = webdriver.Edge('C:/Users/PC/Desktop/InstProject/edgedriver/msedgedriver.exe')
        self.search_requests = []


    def login(self, login, password):
        try:
            self.browser.get('https://www.instagram.com')
            time.sleep(random.randrange(5,7))
            #self.browser.find_element(By.XPATH, '/html/body/div[4]/div/div/button[1]').click()
            time.sleep(1)
            username_input = self.browser.find_element(By.NAME, 'username')
            username_input.clear()
            username_input.send_keys(login)

            time.sleep(1)

            password_input = self.browser.find_element(By.NAME, 'password')
            password_input.clear()
            password_input.send_keys(password)

            time.sleep(1)

            password_input.send_keys(Keys.ENTER)

            time.sleep(10)
        except Exception as ex:
            print(ex)
            self.browser.close()
            self.browser.quit()


    def search(self):

        try:
            self.browser.get('https://www.instagram.com/explore/search/keyword/')

            search_input = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input')

            for item in search_list:
                search_input.clear()
                search_input.send_keys(item)
                time.sleep(5)

                hrefs = self.browser.find_elements(By.TAG_NAME, 'a')

                for i in hrefs:
                    blogger = i.get_attribute('href')
                    if not blogger in self.search_requests and blogger not in ban_list and not '%' in blogger and not 'locations' in blogger and not 'tags' in blogger:
                        self.search_requests.append(blogger)
                    time.sleep(0.2)

                search_input.clear()
        except Exception as ex:
            print(ex)
            print('Ошибочка!')
            self.browser.close()
            self.browser.quit()
        print(self.search_requests)
        time.sleep(10)


    def sorting(self):

        result = []
        new_ban_list = []
        today = datetime.datetime.now()

        try:
            for bloger_link in self.search_requests:

                self.browser.get(bloger_link)
                likes_count = 0
                fails = 0
                time.sleep(random.randrange(20,36))

                try:
                    subs = int(self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span').get_attribute('title').replace(',', ''))

                    if subs >= 5000 and self.description():
                        hrefs = self.browser.find_elements(By.TAG_NAME, 'a')
                        links = [i.get_attribute('href') for i in  hrefs if '/p/' in i.get_attribute('href')]
                        flag = False

                        for num, j in enumerate(links):
                            self.browser.get(j)
                            time.sleep(random.randrange(30,45))

                            if num < 4:

                                publication_date = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div[1]/a/div/time').get_attribute('datetime')
                                public_date = datetime.datetime(int(publication_date[:4].lstrip('0')), int(publication_date[5:7].lstrip('0')), int(publication_date[8:10].lstrip('0')))
                                period = today - public_date

                                
                                if period.days <= 8 and not flag:
                                    time.sleep(1)
                                    flag = True

                                try:
                                    likes_count += int(self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span').text.replace(',', ''))
                                except:
                                    fails += 1
                                    continue

                            elif num >= 4 and flag:
                                publication_date = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div[1]/a/div/time').get_attribute('datetime')
                                public_date = datetime.datetime(int(publication_date[:4].lstrip('0')), int(publication_date[5:7].lstrip('0')), int(publication_date[8:10].lstrip('0')))

                                if public_date < datetime.datetime(2022, 3, 14):
                                    break

                                try:
                                    likes_count += int(self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span').text.replace(',', ''))
                                except:
                                    fails += 1
                                    continue

                        if flag and (int(likes_count / (num+1-fails)) >= int(subs/200 *0.8)):
                            result.append(bloger_link)

                except Exception as ex:
                    print(ex)
                    print(bloger_link, '-', 'закрытый аккаунт')
                    new_ban_list.append(bloger_link)


            self.browser.close()
            self.browser.quit()

        except Exception as ex:
            print(ex)
            print('Ошибочка в сортировке')
            self.browser.close()
            self.browser.quit()

        print(result)
        general_ban = new_ban_list + result


        with open('blogers.txt', 'a', encoding='utf-8') as file, open('new_blogers.txt', 'w', encoding='utf-8') as new_file:
            for i in general_ban:
                file.write(i + '\n')
            for i in result:
                new_file.write(i + '\n')


    def description(self):
        time.sleep(2)

        try:
            description = filter(lambda x: str(x)[:2] in ('ru', 'en'), detect_langs(self.browser.find_element(By.CSS_SELECTOR, '._a3gq ._aa_c').text))

            return any(description)
        except Exception as ex:
            print(ex)
            print('Ошибочка в определении языка описания аккаунта')
            return True


    def post_text(self):
        try:
            description = filter(lambda x: str(x)[:2] in ('ru', 'en'), detect_langs(self.browser.find_element(By.CSS_SELECTOR, '._a3gq ._a9zr').text))
            return any(description)
        except Exception as ex:
            print(ex)
            print('Ошибочка в определении языка поста')
            return True


DetectorFactory.seed = 0

search_list = ['торты', 'кондитер', 'тарты', 'муссовые торты', 'макарун', 'макарунс', 'бенто торт', 'эклеры', 
'бисквитный торт', 'сахарная флористика', 'капкейки', 'десерты', 'пирожные']
random.shuffle(search_list)

ban_list = []
with open('blogers.txt', 'r', encoding='utf-8') as file:
    for i in file.readlines():
        ban_list.append(i.rstrip('\n'))


test = InstaBot()
test.login('udjine_korgi', 'Lighttop130499')
test.search()
test.sorting()