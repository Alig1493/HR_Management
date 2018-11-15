# HR-MANAGEMENT HELPER

A project to help facilitate certain HR work on a daily basis.
This project outlines a way in which either hr/manager can view, approve
 certain users of the organizations. This application is tested to the
 best of the impending deadline requirements and comes with a fully
 documented list of APIS. This also happens to be a containerized
 application for cross platform flexibility.

## Get Started
* First you need to need to install [docker](https://www.docker.com/)
* Followed by [docker-compose](https://docs.docker.com/compose/)
* Clone this repository
* Go to your cloned directory
* Run `docker-compose up --build`
* Go to your `0.0.0.0:8000/docs` and you'll see a list of API endpoints
 documented.

### User Role Types breakdown:
* User can have the following roles:
    1. HR
    2. Manager
    3. Regular
    
    Due to lack of clarification on how the user role will be
    defined this is how the application will structure user.
    User signing up as HR and/or Manager will be auto approved
    and verified since there's no super admin verification at
    play here, which is also due to lack of clarification.
    Most users that will request for sign up will be considered
    as Regular users.

* Request status will be as follows:
    1. Open
    2. Processed
    3. HR Reviewed

    Hr is allowed to change status, Manager is only allowed to verify
    HR reviewed people.

### Notable APIS:
* Register: <server_address>:<port>/api/v1/auth/registration/
* Login: <server_address>:<port>/api/v1/auth/login/
* Hr urls (only accessible by HR users): <server_address>:<port>/api/v1/auth/hr/
    1. To see user requests:
    <server_address>:<port>/api/v1/auth/hr/requests/
    2. To change individual user request status:
    <server_address>:<port>/api/v1/auth/hr/requests/<user_id>/
* Manager urls (only accessible by Manager users):
<server_address>:<port>/api/v1/auth/manager/
    1. To see user requests:
    <server_address>:<port>/api/v1/auth/manager/requests/
    2. To approve individual user hr reviewed status:
    <server_address>:<port>/api/v1/auth/manager/requests/<user_id>/
* Log urls (Allows to see user logs. Accessible by HR and/or manager only):
<server_address>:<port>/api/v1/auth/logs/
(see detail for being able to view different type of logs in docs)
* Request urls (Allows to view user requests. Accessible by HR and/or manager only):
<server_address>:<port>/api/v1/auth/requests/
(see detail for being able to view different type of requests in docs)
* PDF urls (Allows to download user requests in pdfs. Accessible by HR and/or manager only):
<server_address>:<port>/api/v1/auth/pdf/
(see detail for being able to view different type of pdf in docs)
