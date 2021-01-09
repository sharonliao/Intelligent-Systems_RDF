import urllib.request
from bs4 import BeautifulSoup
# 创建一个Request对象
import re


def get_faculty_course_url(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(str(response.read().decode('utf-8')))

    all_course_url = soup.find_all(adhocenable="false")
    course_url_list = []
    faculty_courses = []

    match_faculty_name = re.match('https://www.concordia.ca/academics/graduate/calendar/current/(.*)\..*', url).group(1)
    print(match_faculty_name)

    for tag_url in all_course_url:
        url = tag_url.get('href')
        if match_faculty_name == 'jmsb':
            match_pattern = '/academics/graduate/calendar/current/%s/.*\.html' % match_faculty_name
        else:
            match_pattern = '/academics/graduate/calendar/current/%s/.*\-.*' % match_faculty_name

        if re.match(match_pattern,url):
            full_url = 'https://www.concordia.ca'+url
            match_result = re.match('.*/(.*)\.html',url)
            if match_result is not None:
                filename = match_result.group(1)
                print(filename)
                course_url_list.append(full_url)
                page_course = get_courses_info_from_web(full_url, filename)
                faculty_courses.extend(page_course)

    save_name = "Dataset/" + match_faculty_name + "_urls.txt"
    f = open(save_name, "w")
    for url in course_url_list:
        url = "%s\n" % url
        f.write(url)
    return faculty_courses


def get_courses_info_from_web(url,filename):
    # url = 'http://www.concordia.ca/academics/graduate/calendar/current/jmsb/acco.html'
    req = urllib.request.Request(url)
    req.encoding = 'utf-8'
    # 使用Request对象发送请求
    response = urllib.request.urlopen(req)

    soup = BeautifulSoup(str(response.read().decode('utf-8')))

    all_course_descriptions = soup.find_all("div", class_="rte")

    all_cousre_info_list = []
    for courses in all_course_descriptions:
        courses_detail = courses.find_all("span", class_="large-text")

        for courses_detail_list in courses_detail:
            if re.match(r'^[A-Z]{4}\s[0-9]{3,4}.*', courses_detail_list.get_text()):
                course = []
                # match courses which have description
                items = re.match(r'(^[A-Z]{4}) ([0-9]{3,4}) (.*)([\s\S]*)', courses_detail_list.get_text())
                if items is not None:
                    subject = items.group(1)
                    id = items.group(2)
                    name = items.group(3)
                    # remove credit from title
                    credit_match = re.match(r'(.*)\(.*', name)
                    if credit_match is not None:
                        name = credit_match.group(1)
                    # filter out waste info from title
                    waste_info_match = re.match(r'(.*)\\n.*', name)
                    if waste_info_match is not None:
                        name = waste_info_match.group(1)

                    # check descript
                    descript = items.group(4).strip()
                    clean_data_match = re.match(r'^%s [0-9]{3,4}[\s\S]*' % subject, descript)
                    if clean_data_match is None :
                        # print('subject:'+subject)
                        # print('id:'+id)
                        # print('name:'+name)
                        # print('descript:'+descript)

                        course.append(subject)
                        course.append(id)
                        course.append(name)
                        course.append(descript)
                        course.append(url)

                        all_cousre_info_list.append(course)

    return all_cousre_info_list






def get_all_graduate_course():

    fasc_course = get_faculty_course_url('https://www.concordia.ca/academics/graduate/calendar/current/fasc.html')

    fofa_course = get_faculty_course_url('https://www.concordia.ca/academics/graduate/calendar/current/fofa.html')

    jmsb_course = get_faculty_course_url('https://www.concordia.ca/academics/graduate/calendar/current/jmsb.html')





def filter_test():
    name = 'HEBR 210      Introductory Course in Hebrew (6 credits)\nA beginners’ course in Hebrew, with readings of classical and modern texts.\nNOTE: Students who have taken Hebrew at the Cegep level, or whose schooling has been conducted in Hebrew, will not be admitted to this course.\n\n'
    items = match_pattern = re.match(r'(^[A-Z]{4}) ([0-9]{3,4})      (.*) \(.*\)\n([\s\S]*)\n\n', name)
    if items is not None:
        print("3333333")
        subject = items.group(1)
        id = items.group(2)
        name = items.group(3)
        # remove credit from title
        credit_match = re.match(r'(.*)\(.*', name)
        if credit_match is not None:
            name = credit_match.group(1)
        # filter out waste info from title
        waste_info_match = re.match(r'(.*)\\n.*', name)
        if waste_info_match is not None:
            name = waste_info_match.group(1)

        # check descript
        descript = items.group(4).strip()
        if re.match(r'(.*)\\n.*', name) is None:
            print('subject:' + subject)
            print('id:' + id)
            print('name:' + name)
            print('descript:' + descript)


# get_all_graduate_course()
# filter_test()
# get_courses_info_from_web('http://www.concordia.ca/academics/graduate/calendar/current/fasc/biol-dip.html','test_test_test.txt')

