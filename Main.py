from bs4 import BeautifulSoup
import requests
import time
import os
import datetime

import scraping_joy as sj # Модуль для парсинга.



def main():
    link = "https://joyreactor.cc/tag/%D0%BC%D0%B8%D0%BB%D0%BE%D1%82%D0%B0"

    if os.path.exists("outputs") == True:
        pass
    else:   
        os.mkdir("outputs")

    fileName = ((sj.get_title(link)).split("/")[0]).strip()
    
    if os.path.exists("outputs/"+fileName) == True:
        pass
    else:   
        os.mkdir("outputs/"+fileName)

    pageCount = sj.find_count_pages(sj.get_page(link))

    for i in range(1, pageCount):
        print(i)
        targetLink = link + "/" + str(i)
        targetPage = sj.get_page(targetLink)
        posts = sj.find_posts(targetPage)

        j = 0
        for post in posts:
            print(i, j)
            sj.img_in_post(post, adress = ("outputs\\"+fileName+"\\"+(str(i)+"-"+str(j))))
            j += 1



if __name__ == '__main__':
    main()
