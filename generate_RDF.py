import rdflib
from rdflib import Graph
from rdflib import Namespace
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, RDFS,DC,OWL

from annotation_description import get_annotate
from extract_grad_all_course import get_faculty_course_url
from extract_grad_cs_courses import get_all_cs_courses

import pandas as pd

from extract_undergraduate_courses import get_all_undergraduate_courses

focu = Namespace("http://focu.io/schema#")
focudata = Namespace("http://focu.io/data#")
dbpedia = Namespace("http://dbpedia.org/")

def creat_a_rdf():
    g = Graph()
    g.bind('foaf', u'http://xmlns.com/foaf/0.1/')
    g.bind('dc', u'http://purl.org/dc/elements/1.1/')
    g.bind('focu', u'http://focu.io/schema#')
    g.bind('dbpedia', u'http://dbpedia.org/')
    g.bind('focudata', u'http://focu.io/data#')
    g.bind('owl', u'http://www.w3.org/2002/07/owl#')

    g.add((focu.Student, RDF.type, RDFS.Class))
    g.add((focu.Student, RDFS.subClassOf, FOAF.Person))
    g.add((focu.Student, RDFS.label, Literal('Student')))
    g.add((focu.Student, RDFS.comment, Literal('The class of student')))

    g.add((focu.University, RDF.type, RDFS.Class))
    g.add((focu.University, RDFS.subClassOf, FOAF.Organization))
    g.add((focu.University, RDFS.label, Literal('University')))
    g.add((focu.University, RDFS.comment, Literal('The class of University')))

    g.add((focu.Course,RDF.type, RDFS.Class))
    g.add((focu.Course, RDFS.label, Literal('Course')))
    g.add((focu.Course, RDFS.comment, Literal('The class of course')))

    # g.add((focu.Course,RDF.type, RDFS.Class))
    # g.add((focu.Course, RDF.type, RDFS.Class))

    g.add((focu.offeredAt, RDF.type, RDFS.Class))
    g.add((focu.offeredA, RDFS.label, Literal('offered at')))
    g.add((focu.offeredA, RDFS.comment, Literal('relationship')))
    g.add((focu.offeredA, RDFS.domain, focu.Course))
    g.add((focu.offeredA, RDFS.range, focu.University))

    g.add((focu.Topic, RDF.type, RDFS.Class))
    g.add((focu.Topic, RDFS.label, Literal('Topic')))
    g.add((focu.Topic, RDFS.comment, Literal('The class of topic')))

    g.add((focu.hasTopic, RDF.type, RDFS.Class))
    g.add((focu.hasTopic, RDFS.label, Literal('has a topic')))
    g.add((focu.hasTopic, RDFS.comment, Literal('relationship')))
    g.add((focu.hasTopic, RDFS.domain, focu.Course))
    g.add((focu.hasTopic, RDFS.range, focu.Topic))

    g.add((focu.completedCourse, RDF.type, RDFS.Class))
    g.add((focu.completedCourse, RDFS.label, Literal('completed Course')))
    g.add((focu.completedCourse, RDFS.comment, Literal('completed Course')))

    g.add((focu.hasCompletedCourse, RDF.type, RDFS.Class))
    g.add((focu.hasCompletedCourse, RDFS.label, Literal('has a completed Course')))
    g.add((focu.hasCompletedCourse, RDFS.comment, Literal('relationship')))
    g.add((focu.hasCompletedCourse, RDFS.domain, focu.Student))
    g.add((focu.hasCompletedCourse, RDFS.range, focu.completedCourse))

    g.add((focu.completedCourseID, RDF.type, RDFS.Class))
    g.add((focu.completedCourseID, RDFS.label, Literal('ID of the completed Course')))
    g.add((focu.completedCourseID, RDFS.comment, Literal('relationship')))
    g.add((focu.completedCourseID, RDFS.domain, focu.completedCourse))
    g.add((focu.completedCourseID, RDFS.range, focu.Course))

    g.add((focu.completedCourseGrade, RDF.type, RDFS.Class))
    g.add((focu.completedCourseGrade, RDFS.label, Literal('grade of the completed Course')))
    g.add((focu.completedCourseGrade, RDFS.comment, Literal('relationship')))
    g.add((focu.completedCourseGrade, RDFS.domain, focu.completedCourse))
    g.add((focu.completedCourseGrade, RDFS.range, RDFS.Literal))


    g.add((focu.completedCourseTerm, RDF.type, RDFS.Class))
    g.add((focu.completedCourseTerm, RDFS.label, Literal('term of the completed Course')))
    g.add((focu.completedCourseTerm, RDFS.comment, Literal('relationship')))
    g.add((focu.completedCourseTerm, RDFS.domain, focu.completedCourse))
    g.add((focu.completedCourseTerm, RDFS.range, RDFS.Literal))

    # export rdfs
    f = open("RDFS.ttl", "wb")
    f.write(g.serialize(format='turtle'))
    f.close()


    # add data
    # add concordia university
    g.add((focudata.cu, RDF.type, focu.University))
    g.add((focudata.cu, FOAF.name, Literal('Concordia')))
    g.add((focudata.cu, RDFS.seeAlso, URIRef('https://www.concordia.ca')))

    return g


def add_course(g,course_info_list):
    for course_info in course_info_list:
        subject = course_info[0]
        id = course_info[1]
        name = course_info[2]
        description = course_info[3]
        url = course_info[4]

        course_code = subject+id
        course = URIRef(u'http://focu.io/data#'+course_code)

        g.add((course, RDF.type, focu.Course))
        g.add((course, FOAF.name, Literal(name)))
        g.add((course, RDFS.seeAlso, URIRef(url)))
        g.add((course, DC.subject, Literal(subject)))
        g.add((course, DC.identifier, Literal(id)))
        g.add((course, focu.offeredAt, focudata.cu))
        g.add((course, DC.description, Literal(description)))


def add_topics(g,topics_info_list):
    existed_topic = []
    for topic in topics_info_list:
        course_code = topic[0]
        topic_label = topic[1]
        topic_uri = topic[2]
        topic = URIRef(u'http://focu.io/data#' + topic_label.replace(" ", "_"))
        if topic_label not in existed_topic:
        # add a new topic entity
            g.add((topic, RDF.type, focu.Topic))
            g.add((topic, RDFS.label, Literal(topic_label)))
            g.add((topic, OWL.sameAs, URIRef(topic_uri)))
            existed_topic.append(topic_label)
        course = URIRef(u'http://focu.io/data#'+course_code)
        g.add((course, focu.hasTopic, topic))


def add_course_topics(g, course_info_list):
    add_course(g,course_info_list)
    topics_info_list = get_annotate(course_info_list)
    add_topics(g,topics_info_list)


def add_student_info(g):
    with open('Dataset/student_info_new.txt', 'r') as student_file:
        for info in  student_file:
            print(info)
            info = info.strip()
            info_list = info.split(';')
            student_id = info_list[0]
            name = info_list[1].split(' ')
            first_name = name[0]
            last_name = name[1]
            email = info_list[2]

            student = URIRef(u'http://focu.io/data#'+student_id)
            # focudata.student  # = rdflib.term.URIRef(uri)
            g.add((student, RDF.type, focu.Student))
            g.add((student, FOAF.givenName, Literal(first_name)))
            g.add((student, FOAF.familyNanme, Literal(last_name)))
            g.add((student, FOAF.mbox, Literal(email)))

            if len(info_list)>3: # get completed course information
                completed_courses_list = info_list[3].split(',')
                for completed_course in completed_courses_list:
                    completed_course_info = completed_course.split(' ')
                    course_code = completed_course_info[0]
                    term = completed_course_info[1]
                    grade = completed_course_info[2]

                    completed_code = student_id+"_"+course_code+"_"+term
                    completed_course = URIRef(u'http://focu.io/data#' + completed_code)
                    course = URIRef(u'http://focu.io/data#' + course_code)

                    g.add((completed_course, RDF.type, focu.completedCourse))
                    g.add((completed_course, focu.completedCourseID, course))
                    g.add((completed_course, focu.completedCourseGrade, Literal(grade)))
                    g.add((completed_course, focu.completedCourseTerm, Literal(term)))
                    g.add((student, focu.hasCompletedCourse, completed_course))




def write_to_excle(all_coures,filename):
    df = pd.DataFrame(all_coures)
    df.to_excel(filename)


def generate_RDF():
    all_courses = []
    g = creat_a_rdf()

    fasc_course = get_faculty_course_url('https://www.concordia.ca/academics/graduate/calendar/current/fasc.html')
    all_courses.extend(fasc_course)
    print("1 course count:")
    print(len(fasc_course))

    fofa_course = get_faculty_course_url('https://www.concordia.ca/academics/graduate/calendar/current/fofa.html')
    all_courses.extend(fofa_course)
    print("2 course count:")
    print(len(fofa_course))
    #
    jmsb_course = get_faculty_course_url('https://www.concordia.ca/academics/graduate/calendar/current/jmsb.html')
    all_courses.extend(jmsb_course)
    print("3 course count:")
    print(len(jmsb_course))
    #
    cs_course = get_all_cs_courses()
    all_courses.extend(cs_course)
    print("3 course count:")
    print(len(cs_course))

    undergraduate_course = get_all_undergraduate_courses('https://www.concordia.ca/academics/undergraduate/calendar/current/courses-quick-links.html')
    all_courses.extend(undergraduate_course)
    print("4 undergraduate_course count:")
    print(len(undergraduate_course))

    print("total course count:")
    print(len(all_courses))
    write_to_excle(all_courses, "Dataset/all_courses.xlsx")

    add_course_topics(g,all_courses)
    add_student_info(g)

    f = open("course_topics_student.nt", "wb")
    f.write(g.serialize(format='nt'))
    f.close()

    f = open("course_topics_student.ttl", "wb")
    f.write(g.serialize(format='turtle'))
    f.close()

def modify_graph():
    g = Graph()
    g.parse('course_topics_student.ttl', format="ttl")
    topic1 = ["COMP474","expert system","http://dbpedia.org/resource/Expert_system"]
    topic2 = ["COMP474","expert systems", "http://dbpedia.org/resource/Expert_system"]
    topics_list = [topic1,topic2]
    add_topics(g,topics_list)
    add_student_info(g)

    f = open("course_topics_student.ttl", "wb")
    f.write(g.serialize(format='turtle'))
    f.close()





# modify_graph()




# generate_RDF()


