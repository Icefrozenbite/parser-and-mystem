import requests, os, time, csv
from bs4 import BeautifulSoup


date_ear = '01/07/2015'
date_lat = '31/12/2018'
date_ear = time.strptime(date_ear, "%d/%m/%Y")
date_lat = time.strptime(date_lat, "%d/%m/%Y")



def url_list():#Функция производит список адрессов новостей каждого дня.
    URLs = []
    for year in range(2015,2019):
        for month in range(1,13):
            for day in range(1,32):
                try:
                    date = str(year) + '/'  + str(month) + '/' + str(day)
                    date_norm = time.strptime(date, "%Y/%m/%d")
                    if date_norm > date_ear and date_norm < date_lat:
                        url = 'https://www.mk.ru/news/' + date
                        URLs.append(url)
                except:
                    pass

    return URLs


def url_grabber(url_list):#Функция берет адрессы каждых новостей, и пишет результаты в файл.
    written_url = []
    grabbed_url = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
    with open('essay_link.txt','a',encoding='utf-8') as file:
        for url in url_list:
            url = url + '/'
            r = requests.get(url, headers=headers).text
            soup = BeautifulSoup(r, 'lxml', from_encoding='utf-8')
            date_link = soup.find_all('a')
            for line in date_link:
                line = line.get('href')
                try:
                    if 'https://www.mk.ru/politics' in line or 'https://www.mk.ru/economics' in line or 'https://www.mk.ru/social' in line or 'https://www.mk.ru/incident' in line:
                        if line not in written_url:
                            line_split = line.split('//')
                            line_split = line_split[1].split('/')
                            if line_split[2] in ['2015','2016','2017','2018']:
                                written_url.append(line)
                                file.write(line)
                                file.write(' ')
                                print(line)
                except:
                    pass



def text_grabber(grabbed_url): #Функция берет тексты из сайтов и пишет их в фйлы.
    with open('file_list.csv', 'a', encoding='utf-8') as file_list:
        file_list_writer = csv.writer(file_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_list_writer.writerow(['path', 'author', 'date', 'source', 'title', 'url', 'wordcount'])

        relative_path = os.path.split(os.path.abspath(grabbed_url))[0]
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
        with open(grabbed_url, 'r', encoding='utf-8') as essay_link:
            essay_link = essay_link.read()
            essay_link = essay_link.split(' ')
            for url in essay_link:
                try:
                    r = requests.get(url, headers=headers).text
                    soup = BeautifulSoup(r, 'lxml', from_encoding='utf-8')

                    title = soup.find('h1')
                    title = title.get_text()

                    file_name = title + '.txt'



                    date = soup.find('span',{'class','date'})
                    date = date.get_text()
                    date = date.split('\t')
                    date = date[3].split(' ')
                    date = date[0]
                    year = date.split('.')[2]
                    month = date.split('.')[1]

                    text_sum = []
                    text = soup.find_all('p')
                    for paragraph in text:
                        paragraph = paragraph.get_text()
                        paragraph = paragraph.strip('\xa0')
                        text_sum.append(paragraph)
                    text = text_sum[0:len(text_sum) - 7]
                    text = ''.join(text)


                    source = soup.find('div',{'class','article_info'})
                    source = source.get_text()
                    if source != None:
                        source = source.split(':')
                        source = source[1]
                    else:
                        source = 'Unknown'

                    word_count = len(text.split(' '))

                    author = 'Unknown'

                    path = relative_path + '\\plain text\\' + year + '\\' + month + '\\' + file_name
                    dir = relative_path + '\\plain text\\' + year + '\\' + month + '\\'

                    try:
                        os.makedirs(dir)
                    except:
                        pass
                    with open(path, 'a', encoding='utf-8') as file:
                        file.write(text)

                    file_list_writer.writerow([path, author, date, source, title, url, word_count])
                    print([path, author, date, source, title, url, word_count])




                except:
                    pass


if __name__ == '__main__':
    text_grabber('essay_link.txt')
