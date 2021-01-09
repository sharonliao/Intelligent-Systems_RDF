import pandas as pd
from spotlight import SpotlightException, annotate


def get_annotate(course_list):
    host = 'http://localhost:2222/rest/annotate'
    confidence = 0.8
    support = 20
    count = 0
    topics_list = []
    f = open("Dataset/topics_uri.txt", "a+")
    for course in course_list:
        description = course[2] + ": " + course[3]
        count = count + 1
        if description != '':
            try:
                course_id = course[0]+course[1]
                annotations = annotate(host, description, confidence, support)
                # print(annotations)

                for topics in annotations:
                    uri = topics['URI']
                    topic_name = topics['surfaceForm']
                    if uri is not None:
                        topic = []
                        topic.append(course_id)
                        topic.append(topic_name)
                        topic.append(uri)
                        topics_list.append(topic)

                        topic_info = "%s-----%s-----%s\n" % (course_id,topic_name, uri)
                        print(topic_info)
                        f.write(topic_info)
            except SpotlightException:
                pass
    f.close()
    return topics_list

def test_get_annotate():
    host = 'http://localhost:2222/rest/annotate'
    # host = 'http://api.dbpedia-spotlight.org/en/annotate'
    test_txt = 'Overview of current software engineering testing methods, techniques and standards for testing system implementations. Classical white-box testing; dataflow testing; classical black-box testing; integration testing; system testing. Testing measures; test plan. IEEE standard. Object-oriented testing. Test-driven development. Testing quality measures. Test reduction techniques. Techniques for test automation. Tools and techniques for formal verification of software system designs: model checking and theorem proving. A project is required..'
    test_txt = 'The requirements engineering (RE) process. Requirements engineering in different software lifecycle models. Problem analysis. Requirements elicitation. Requirements evaluation. Inconsistency management. Risk analysis. Requirements prioritization and negotiation. Requirements specification: natural language documentation, IEEE and ISO standards. Use cases. Agile processes and user stories. Introduction to formal specification: logics, formal languages. Requirements quality assurance. RE tools. Requirements evolution. Traceability. Domain modelling: UML, ontologies, domain-specific languages. Modelling behaviour. Acceptance criteria. Test cases. Cost models. A project is required.\n Note: Students who have received credit for COMP 6481 may not take this course for credit.'
    confidence = 1
    support = 20

    f = open("course_dataset/topics_uri.txt", "a+")
    try:
        annotations = annotate(host, test_txt, confidence, support)
        print(annotations)
        for topics in annotations:
            uri = topics['URI']
            topic_name = topics['surfaceForm']
            if uri is not None:
                topic_info = "%s-----%s\n" % (topic_name,uri)
                f.write(topic_info)
    except SpotlightException:
        pass
    f.close()


def annotation_performance_test():
    test_file = open('test_data/annotate_test.txt', 'r')
    course_info = test_file.readlines()
    print(len(course_info))
    course_list = []
    for course in course_info:
        info = course.split('	')
        course_list.append(info)
    topic_list = get_annotate(course_list)
    print(len(topic_list))
    df = pd.DataFrame(topic_list)
    df.to_excel("test_data/annotation_performance_test.xlsx")

# get_annotate()
# test_get_annotate()
# annotation_performance_test()



