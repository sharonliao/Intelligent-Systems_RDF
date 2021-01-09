from rdflib import Graph


def generate_output_file(g,filename):
    f = open(filename, "wb")
    f.write(g.serialize(format='turtle'))
    f.close()

# 1. Total number of triples in the KB
def query_total_triples(g):
    qres = g.query(
        """
        CONSTRUCT {
        _:v  rdfs:label ?Triples.
        _:v  rdfs:comment 'Total number of triples in the KB'.
          }
        where{ 
            select (COUNT(*) as ?Triples) 
             WHERE
             {
                 ?s ?p ?o
                } 
        }
        """
    )
    for row in qres:
        print(row)

    generate_output_file(qres, 'query_output/q1-out.ttl')


# 2. Total number of students, courses, and topics
def query_total_students_courses_topics(g):

    qres = g.query(
        """
        CONSTRUCT {
        _:v  rdfs:label ?Triples.
        _:v  rdfs:comment 'Total number of students, courses, and topics'.
          }
        where{ 
          SELECT (COUNT(*) as ?Triples) 
            WHERE {
             {?student rdf:type focu:Student.}
             union
             {?course rdf:type focu:Course.}
             union
             {?topic rdf:type focu:Topic.}
             }
             }
        """
    )
    for row in qres:
        print(row)

    generate_output_file(qres, 'query_output/q2-out.ttl')


# 3. For a course c, list all covered topics using their (English) labels and their link to DBpedia
def query_course_topic(g,course_name):
    qres = g.query(
        """
          construct {
            ?topic owl:sameAs ?link.
            ?topic rdfs:label ?label.
          }
          where{
            ?course focu:hasTopic ?topic.
            ?topic owl:sameAs ?link.
            ?topic rdfs:label ?label.
            ?course foaf:name '%s'.
          }  
        """%course_name
    )
    for row in qres:
        print(row)

    generate_output_file(qres, 'query_output/q3-out.ttl')



# 4. For a given student, list all courses this student completed, together with the grade
def query_completed_course(g,first_name, last_name):
    qres = g.query(
        """
          construct{ 
            ?completedCourse foaf:name ?courseName.
            ?completedCourse focu:completedCourseGrade ?grade.
          }
          where{
            ?student foaf:givenName '%s'.
            ?student foaf:familyNanme '%s'.
            ?student focu:hasCompletedCourse ?completedCourse.
            ?completedCourse focu:completedCourseID ?course.
            ?course foaf:name ?courseName.
            ?completedCourse focu:completedCourseGrade ?grade.
          }  
        """%(first_name,last_name)
    )
    for row in qres:
        print(row)

    generate_output_file(qres, 'query_output/q4-out.ttl')

# 5. For a given topic, list all students that are familiar with the topic (i.e., took, and did not fail, a course that covered the topic)
def query_student_familiar_topic_1(g, topic):
    qres = g.query(
        """ 
          construct{ 
            ?student foaf:givenName ?givenName.
            ?student foaf:familyNanme ?familyNanme.
           }
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
        """%topic
    )
    for row in qres:
        print(row)

    generate_output_file(qres, 'query_output/q5-out.ttl')



# 6. For a student, list all topics (no duplicates) that this student is familiar with (based on the completed courses for this student that are better than an “F” grade)

def query_student_familiar_topic_2(g, first_name, last_name):
    qres = g.query(

        """
         construct {
         ?student foaf:konws ?topicLabel
         }
         where{
           select 
              distinct ?topicLabel ?student
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
         }
        """%(first_name,last_name)
    )
    for row in qres:
        print(row)

    # FILTER (?age >= 24)
    # FILTER regex(?g, "r")
    # SELECT(AVG(?y) AS ?avg)
    # WHERE
    # {
    # ?a: x ?x;
    # :y ?y.
    # }
    # GROUP BY ?x
    # HAVING(AVG(?size) > 10)

    generate_output_file(qres, 'query_output/q6-out.ttl')





def query_student_number(g):
    qres = g.query(
    """
       select 
          (COUNT(*) as ?Triples) 
       where{
        ?student rdf:type focu:Student.
      }  
    """
    )
    for row in qres:
        print(row)

def query_course_number(g):
    qres = g.query(
    """
       select 
          (COUNT(*) as ?Triples) 
       where{
        ?student rdf:type focu:Course.
      }  
    """
    )
    for row in qres:
        print(row)

def query_topic_number(g):
    qres = g.query(
    """
       select 
          (COUNT(*) as ?Triples) 
       where{
        ?student rdf:type focu:Topic.
      }  
    """
    )
    for row in qres:
        print(row)

def query_failed_student(g):
    qres = g.query(
    """
       select 
          ?givenName ?familyNanme ?courseName ?term
       where{
        ?completedCourse focu:completedCourseGrade "F".
        ?completedCourse focu:completedCourseTerm ?term.
        ?student focu:hasCompletedCourse ?completedCourse.
        ?student foaf:givenName ?givenName.
        ?student foaf:familyNanme ?familyNanme.
        ?completedCourse focu:completedCourseID ?course.
        ?course foaf:name ?courseName.
      }  
    """
    )
    for row in qres:
        print(row)

def query_subject_course(g):
    qres = g.query(
    """
       select 
         ?courseID ?courseName
       where{
        ?course dc:subject "FMST".
        ?course foaf:name ?courseName.
        ?course dc:identifier ?courseID.
      }  
    """
    )
    for row in qres:
        print(row)


def query_subject_student(g):
    qres = g.query(
    """
       select 
         ?givenName  ?familyNanme
       where{
        ?course dc:subject "COMP".
        ?completedCourse focu:completedCourseID ?course.
        ?student focu:hasCompletedCourse ?completedCourse.
        ?student foaf:givenName ?givenName.
        ?student foaf:familyNanme ?familyNanme.
        
      }  
    """
    )
    for row in qres:
        print(row)


g = Graph()
g.parse('course_topics_student.ttl',format="ttl")
# print('1. Total number of triples in the KB')
# query_total_triples(g)
#
# print('\n2. Total number of students, courses, and topics')
# query_total_students_courses_topics(g)
#
# print('\n3. For a course c, list all covered topics using their (English) labels and their link to DBpedia')
# query_course_topic(g,' Applied Artificial Intelligence (*) ')
#
# print('\n4. For a given student, list all courses this student completed, together with the grade')
# query_completed_course(g,'Doris','Hunter')
#
# print('\n5. For a given topic, list all students that are familiar with the topic (i.e., took, and did not fail, a course that covered the topic)')
# query_student_familiar_topic_1(g,'automated reasoning')
#
# print('\n6. For a student, list all topics (no duplicates) that this student is familiar with (based on the completed courses for this student that are better than an “F” grade)')
# query_student_familiar_topic_2(g,'Cheryl','Mason')
#
#
#
#
# print("\n total number of student")
# query_student_number(g)
# print("\n total number of course")
# query_course_number(g)
# print("\n total number of topic")
# query_topic_number(g)
# print("\nQ13 the student faile")
# query_failed_student(g)
# print("\nQ13 the FMST course")
# query_subject_course(g)


query_subject_student(g)