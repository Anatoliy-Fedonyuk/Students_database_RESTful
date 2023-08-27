# "SQL" - RESTful API application for work with PostgreSQL databases

##    The application allows you to administer the personal data of students, their distribution into groups, as well
## as the selection, recording and removal of students to (from) active training courses of a small educational
## institution (for example, a college).

##    This application allows you to administer: insert/select/update/delete data in the database using sqlalchemy
## and flask restful framework. The application uses two PostgreSQL databases deployed in
## Docker Compose containers for its work.

##    The application architecture is close to the best practices of Web API Design. The processes inside
## the application are implemented according to the RESTful API standards and are provided by the full range of CRUD
## methods. Developed for the application Documentation for the OpenApi specification using Swagger. 
## The full range of tests was performed using the PyTest test framework and using a separate Postgrey test 
## database deployed in a Docker container.

###   When working on the application and deploying it, the GitLab repository and Docker Hub were used.


## Work with PostgreSQL DB was carried out entirely using ORM SQLalchemy and the following Models were created:

- [ ] [GroupsModel]
- [ ] [StudentsModel]
- [ ] [CoursesModel]
- [ ] [Associative model Student-Course]

