import spacy
from spacy.matcher import Matcher
from rdflib import Graph

# question1 = "What is COMP 474 about?"
# question2 = "Which courses did Lucas take?"
# question3 = "Which courses cover Expert Systems?"
# Which courses cover Natural Language Processing?
# Who is familiar with Recurrent neural networks
# question4 = "Who is familiar with financial reporting?"
# question5 = "What does Lucas Wang know?"


g = Graph()
g.parse('course_topics_student.ttl', format="ttl")


nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
pattern_course_id = [{"TEXT": {"REGEX": "[A-Z]{4}"}},
                     {"TEXT": {"REGEX": "[0-9]{1,4}"}}]
matcher.add("course_id", None, pattern_course_id)

def get_course_id(doc):
    course_id = ''
    matchers = matcher(doc)
    for match_id, start, end in matchers:
        course_id = doc[start:end].text
    return course_id

def nlp_question(question):
    lemma_list = []
    doc = nlp(question)

    for token in doc:
        lemma_list.append(token.lemma_)

    # student_name = ''
    # topic_name = ''
    # for ent in doc.ents:
    #     if ent.label_ == 'PERSON':
    #         student_name = ent.text
    #     elif ent.label_ == 'ORG':
    #         topic_name = ent.text
    # print("student_name:"+student_name)
    # print("topic_name:" + topic_name)

    entity = ""
    last_one_compound = False
    for token in doc:
        if token.dep_ == 'compound':
            entity = entity + " " + token.text
            last_one_compound = True
        elif token.dep_ != 'compound' and last_one_compound == True:
            entity = entity + " " + token.text
            last_one_compound = False
        else:
            last_one_compound = False

    if entity == "":
        for i in range(0, len(doc)):
            if doc[i].tag_ == 'NN':
                entity = doc[i].text
                if i - 1 >= 0 and doc[i - 1].tag_ == 'JJ':
                    entity = doc[i - 1].text + " " + entity

    if entity == "":
        for i in range(0, len(doc)):
            if doc[i].tag_ == 'NNP':
                entity = doc[i].text

    # print("entity ==== "+entity)
    entity = entity.strip()


    course_about_vocab_list = ['what', 'about']
    course_take_vocab_list = ['which', 'course', 'take']
    course_cover_vocab_list = ['which', 'course', 'cover']
    topic_familiar_vocab_list = ['who', 'familiar']
    student_know_vocab_list = ['what', 'know']

    course_id = get_course_id(doc)
    if(all(x in lemma_list for x in course_about_vocab_list) and course_id != ''):
        question1(course_id,g)
    elif(all(x in lemma_list for x in course_take_vocab_list) and entity != ''):
        question2(entity, g)
    elif(all(x in lemma_list for x in course_cover_vocab_list) and entity != ''):
        question3(entity, g)
    elif(all(x in lemma_list for x in topic_familiar_vocab_list) and entity != ''):
        question4(entity, g)
    elif (all(x in lemma_list for x in student_know_vocab_list) and entity != ''):
        question5(entity, g)
    else:
        print("Sorry, I have no idea.")




# question1 = "What is COMP 474 about?"
def question1(course_id,g):
    if len(course_id.split(' '))<2:
        print("No this course.")
        return

    subject = course_id.split(' ')[0]
    identifier = course_id.split(' ')[1]
    qres = g.query(
    """
       select 
          ?description
       where{
            ?course dc:description ?description.
            ?course dc:subject '%s'.
            ?course dc:identifier '%s'.
      }  
    """%(subject,identifier)
    )
    for row in qres:
        print(row.description)

    if len(qres) == 0 :
        print("No course %s"%course_id)


# question2 = "Which courses did Joan Kennedy take?"
def question2(student_name, g):
    if len(student_name.split(' '))<2:
        print("No this student.")
        return

    givenName = student_name.split(' ')[0]
    familyNanme = student_name.split(' ')[1]

    qres = g.query(
        """
           select 
              ?course_name
           where{
                ?student foaf:givenName '%s'.
                ?student foaf:familyNanme '%s'.
                ?student focu:hasCompletedCourse ?hasCompletedCourse.
                ?hasCompletedCourse focu:completedCourseID ?course.
                ?course foaf:name ?course_name
          }  
        """ % (givenName, familyNanme)
    )
    for row in qres:
        print(row.course_name)

    if len(qres) == 0 :
        print("%s did not take any courses."%student_name)



# question3 = "Which courses cover Expert Systems?"
def question3(topic, g):
    if len(topic)==0:
        print("No this topic.")
        return

    qres = g.query(
        """
           select 
              ?course_name
           where{
                ?course foaf:name ?course_name.
                ?course focu:hasTopic ?topic.
                ?topic rdfs:label '%s'
          }  
        """ % (topic.lower())
    )
    for row in qres:
        print(row.course_name)

    if len(qres) == 0 :
        print("No course covers it")


# question4 = "Who is familiar with Natural Language Processing?"
def question4(topic, g):
    if len(topic)==0:
        print("No this topic.")
        return

    qres = g.query(
        """
        select
            ?givenName ?familyNanme 
          where{
            ?course focu:hasTopic ?topic.
            ?topic rdfs:label "%s".
            ?student foaf:givenName ?givenName.
            ?student foaf:familyNanme ?familyNanme.
            ?student focu:hasCompletedCourse ?completedCourse.
            ?completedCourse focu:completedCourseID ?course.
            ?completedCourse focu:completedCourseGrade ?grade.
            Filter (?grade != 'F') 
          }  
        """ %(topic.lower())
    )
    for row in qres:
        print(row.givenName+" "+row.familyNanme)

    if len(qres) == 0 :
        print("No one familiars with %s."%topic)

# question5 = "What does Lucas Wang know?"
def question5(student_name, g):
    if len(student_name.split(' '))<2:
        print("No this student.")
        return

    givenName = student_name.split(' ')[0]
    familyNanme = student_name.split(' ')[1]
    qres = g.query(
        """
           select 
              distinct ?topicLabel
           where{
            ?student foaf:givenName '%s'.
            ?student foaf:familyNanme '%s'.
            ?student focu:hasCompletedCourse ?completedCourse.
            ?completedCourse focu:completedCourseID ?course.
            ?completedCourse focu:completedCourseGrade ?grade.
            ?course focu:hasTopic ?topic.
            ?topic rdfs:label ?topicLabel.
            Filter (?grade != 'F') 
          }  
        """ %(givenName,familyNanme)
    )
    for row in qres:
        print(row.topicLabel)

    if len(qres) == 0 :
        print("%s knows nothing."%student_name)


def start_chatbot():
    g = Graph()
    g.parse('course_topics_student.ttl', format="ttl")
    print("Please enter your Question, or enter Q to quit.")
    while True:
        question = input(">")
        if question == 'Q':
            break
        else:
            nlp_question(question)


start_chatbot()
