from bs4 import BeautifulSoup
import requests
import time


allHeaders = {
    "Referer": "https://joyreactor.cc/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


def valid_link(artist_link):
    """
        Input: ссылка в виде строки.
        Output: логическое значение или значение ошибки в виде строки.
        Функция для проверки доступа к ссылке. Если при подключении возникает
        ошибка - возвращается False. В ином случае следует проверка на статус 
        подключения. Если с подключением всё впорядке - подключаемся. В ином 
        случае выводим номер ошибки.
    """
    try:
        url = requests.get(artist_link, headers = allHeaders, verify=False)
    except:
        return False
    if url.status_code == 200:
        url.close()
        return True
    else:
        return url.status_code

def get_page(artist_link):
    """
        Input: ссылка в виде строки
        Output: элемент типа BeautifulSoup или результат функции валидации.
        Функция для получения страницы. Сначала проверяется ссылка.
        Если подключения не происходи, возвращаем результат функции валидации.
        В ином случае получаем код страницы и возвращаем его.
    """
    if valid_link(artist_link) == True:
        url = requests.get(artist_link, headers = allHeaders, verify=False)
        page = BeautifulSoup(url.text, "lxml")
        url.close()
        return page
    else: 
        return valid_link(artist_link)

def img_in_post(post, adress):
    """
        Input: пост в виде объекта супа.
        Output: ничего.
        Функция для выгрузки изображений из поста. 
    """

    try:
        postCont = post.find("div", class_ = "post_content")
        img_list = postCont.find("div", class_ = "image")

        img_link_list = img_list.find_all("a")
        if len(img_list) == 0:
            img_link_list = img_list.find_all("img")
            img_link_list = [i.get("src") for i in img_link_list]
        else:
            img_link_list = [i.get("href") for i in img_link_list]

        print(img_link_list)
        for i in range(len(img_link_list)):
            img = requests.get("https:"+img_link_list[i], headers = allHeaders, verify=False)
            # with open(f"{adress}{str(i)}.jpg", 'wb') as f:
            #     f.write(img.content)

            if (img_link_list[i])[-3:] == "gif":
                with open(f"{adress}-{i}_t-{taglist_in_post(post)}_r-{raiting_in_post(post)}.gif", 'wb') as f:
                    f.write(img.content)
            elif (img_link_list[i])[-3:] == "jpg":
                with open(f"{adress}-{i}_t-{taglist_in_post(post)}_r-{raiting_in_post(post)}.jpg", 'wb') as f:
                    f.write(img.content)
            elif (img_link_list[i])[-3:] == "png":
                with open(f"{adress}-{i}_t-{taglist_in_post(post)}_r-{raiting_in_post(post)}.png", 'wb') as f:
                    f.write(img.content)
            elif (img_link_list[i])[-3:] == "ebm":
                with open(f"{adress}-{i}_t-{taglist_in_post(post)}_r-{raiting_in_post(post)}.webm", 'wb') as f:
                    f.write(img.content)
            else:
                with open(f"{adress}-{i}_t-{taglist_in_post(post)}_r-{raiting_in_post(post)}.jpg", 'wb') as f:
                    f.write(img.content)
    except:
        print("ErrorIn-img_in_post")

def taglist_in_post(post):
    """
    post - пост, в котором нужно найти список тегов.
    Возвращает список тегов.
    """
    try:
        tagList = post.find("h2", class_ = "taglist")
        tagList = tagList.find_all("b")
        for i in range(len(tagList)):
            tagList[i] = tagList[i].find("a")
        for i in range(len(tagList)):
            tagList[i] = str(tagList[i].get("title"))
        tagList = "_".join(tagList)
    except:
        print("ErrorIn-taglist")
        tagList = "ErrorIn-taglist"
    
    return tagList

def raiting_in_post(post):
    try:
        raiting = post.find("span", class_ = "post_rating").text
        raiting = raiting.strip()
    except:
        print("ErrorIn-raiting_in_post")
        raiting = "ErrorIn-raiting_in_post"

    return raiting

def find_posts(page):
    """
    page - страница для поиска постов.
    Функция получает страницу, а затем возвращает список постов в ней.
    """
    posts = page.find_all("div", class_ = "postContainer")
    return posts

def get_title(url):
    page = get_page(url)
    return (page.find("title")).text


def find_count_pages(res):
    """
    res - целевая страница. Функция получает уже готовый документ и 
    смотрит внизу этого документа количество страниц.
    Функция получает список тегов a, а затем выводит значение наибольшего 
    из них.
    """
    pages = res.find("div", class_ = "pagination_expanded")
    pages = pages.find_all("a")
    return int(pages[-1].text) if int(pages[-1].text) > int(pages[0].text) else int(pages[0].text)+1
