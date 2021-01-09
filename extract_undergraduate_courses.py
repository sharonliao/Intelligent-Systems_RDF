import urllib.request
from bs4 import BeautifulSoup
import re

i = 0
course_count = 0
course_code_set = set()

def get_courses_info_from_web(url,filename):
    course_info_list = []
    # url = 'http://www.concordia.ca/academics/graduate/calendar/current/jmsb/acco.html'
    req = urllib.request.Request(url)
    req.encoding = 'utf-8'

    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(str(response.read().decode('utf-8')))

    all_text = soup.get_text()
    # print(soup.get_text())
    rough_data = all_text.split('\n\n')


    for data in rough_data:
        # print(data)
        # match_pattern = re.findall(r'([A-Z]{4}) ([0-9]{3,4})\s\s*(.*)\(.*\)\n(.*\n.*)', data)
        # match_pattern = re.findall(r'([A-Z]{4}) ([0-9]{3,4})\s\s*(.*)\(.*\)\n([\s\S]*)', data)
        match_pattern = re.findall(r'([A-Z]{4}) ([0-9]{3,4})\s\s*(.*)\(.*\)\n(.*)', data)
        for course in match_pattern:
            global i
            subject = course[0]
            id = course[1]
            name = course[2]
            descript = course[3]
            if len(name.strip()) == 0:
                name = descript.strip()
                descript = ''
            clean_data_match = re.match(r'^%s [0-9]{3,4}[\s\S]*'%subject,descript)
            if clean_data_match is None:

                course_info = [subject,id,name,descript,url]

                global course_code_set
                if subject+id not in course_code_set:
                    course_code_set.add(subject+id)
                    course_info_list.append(course_info)
                    i = i + 1

    print("course_count:")
    print(len(course_code_set))

    return course_info_list

def get_all_undergraduate_courses(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(str(response.read().decode('utf-8')))
    all_course_url = soup.find_all('a')
    course_url_list = []
    undergraduate_courses = []

    match_course_page_pattern = '(/academics/undergraduate/calendar/current/.*html)#.*'
    for tag_url in all_course_url:
        url = tag_url.get('href')
        if url is not None:
            match_result = re.match(match_course_page_pattern,url)
            if match_result:
                filename = tag_url.get_text()
                # print(filename)
                full_url = 'https://www.concordia.ca'+match_result[1]
                print('url')
                print(full_url)
                if full_url not in course_url_list and re.match('/academics/undergraduate/calendar/current/sec18.*',url) is None:
                    course_url_list.append(full_url)
                    # print('url',url)
                    page_course = get_courses_info_from_web(full_url, filename)
                    undergraduate_courses.extend(page_course)

    save_name = "Dataset/undergraduate_urls.txt"
    f = open(save_name, "w")
    for url in course_url_list:
        url = "%s\n" % url
        f.write(url)
    return undergraduate_courses

# get_all_undergraduate_courses('https://www.concordia.ca/academics/undergraduate/calendar/current/courses-quick-links.html')

