import urllib.request
from bs4 import BeautifulSoup
import re


def get_courses_info_from_web(url,filename):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(str(response.read().decode('utf-8')))

    all_course_descriptions = soup.find_all("div", class_="rte")

    all_cousre_info_list = []
    for courses in all_course_descriptions:
        courses_detail = courses.find_all("span", class_="large-text")

        for courses_detail_list in courses_detail:

            if re.match(r'^[A-Z]{4}\s[0-9]{3,4}.*\(.*(credit|credits)\).*', courses_detail_list.get_text()):
                course = []
                # match courses which have description
                items = re.match(r'(^[A-Z]{4})\s([0-9]{3,4})(.*)([\s\S]*)', courses_detail_list.get_text())
                # items = re.match(r'(^[A-Z]{4}) ([0-9]{3,4}).*\(.*(credit|credits)\).*\\n(.*)', courses_detail_list.get_text())

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
                        name = waste_info_match.group(1).strip()

                    # check descript
                    descript = items.group(4).strip()

                    # print(subject)
                    # print(id)
                    # print(name)
                    # print(descript)

                    course.append(subject)
                    course.append(id)
                    course.append(name)
                    course.append(descript)
                    course.append(url)

                    all_cousre_info_list.append(course)

    return all_cousre_info_list


def get_all_cs_courses():
    courses_list = []
    url_encs = 'https://www.concordia.ca/academics/graduate/calendar/current/encs/engineering-courses.html#course-descriptions'
    encs_courses = get_courses_info_from_web(url_encs,'encs')
    courses_list.extend(encs_courses)

    url_cs = 'https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html'
    cs_courses = get_courses_info_from_web(url_cs,'cs')
    courses_list.extend(cs_courses)

    return courses_list

# get_all_cs_courses()



