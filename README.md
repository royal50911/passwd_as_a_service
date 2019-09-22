# passwd_as_a_service
A simple rest api app to expose the user and group information on a UNIX-like system that is usually locked away in the UNIX /etc/passwd and /etc/groups files

## Highlights
- Exposes passwd file system
- Exposes group file system
- Get all users in systems
- Search for a user by uid
- Search for groups of a user by uid
- Get all groups in systems
- Search for a group by gid

## REST api summary
##### GET /users
* Return a list of all users on the system, as defined in the /etc/passwd file.
* Example Response:
    ```bash
    [{“name”: “root”, “uid”: 0, “gid”: 0, “comment”: “root”, “home”: “/root”,
    “shell”: “/bin/bash”},
    {“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:
    “/home/dwoodlins”, “shell”: “/bin/false”} ]
    ```
##### GET /users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=< hq>][&shell=<sq>]
* Return a list of users matching all of the specified query fields. 
The bracket notation indicates that any of the following query parameters may be supplied:
- name
- uid
- gid
- comment
- home
- shell
Only exact matches need to be supported.
* Example Query: ​GET /users/query?shell=%2Fbin%2Ffalse
* Example Response:
    ```bash
    [{“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, 
    “home”: “/home/dwoodlins”, “shell”: “/bin/false”}]
    ```

##### GET /users/<uid>
* Return a single user with <uid>. Return 404 if <uid> is not found.
* Example Response:
    ```bash
    {“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, 
    “home”: “/home/dwoodlins”, “shell”: “/bin/false”}
    ```

##### GET /users/<uid>/groups
* Return all the groups for a given user.
* Example Response:
    ```bash
    [{“name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]}]
    ```

##### GET /groups
* Return a list of all groups on the system, a defined by /etc/group.
* Example Response:
    ```bash
    [{“name”: “_analyticsusers”, “gid”: 250, “members”:
    [“_analyticsd’,”_networkd”,”_timed”]},
    {“name”: “docker”, “gid”: 1002, “members”: []}]
    ```

##### GET /groups/query[?name=<nq>][&gid=<gq>][&member=<mq1>[&member=<mq2>][&. ..]]
* Return a list of groups matching all of the specified query fields. 
The bracket notation indicates that any of the following query parameters may be supplied:
- name
- gid
- member (repeated)
Any group containing all the specified members should be returned, i.e. 
when query members are a subset of group members.

* Example Query: ​GET /groups/query?member=_analyticsd&member=_networkd 
* Example Response 
    ``` bash
    [{“name”: “_analyticsusers”, “gid”: 250, “members”: [“_analyticsd’,”_networkd”,”_timed”]}]
    ```

##### GET /groups/<gid>
* Return a single group with <gid>. Return 404 if <gid> is not found.
* Example Response:
    ``` bash
    {“name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]}
    ```

## Example of the app deployed on heroku
* **[passwd-as-a-service](https://passwd-as-a-service.herokuapp.com/users)**

## File Structure
    .
    ├── api_app.py              # main app file to run application
    ├── config                  # config file contains all setup env config
    ├── .gitignore              # git ignore files list
    ├── Makefile                # Makefile for automate run/test command
    ├── tests                   # test dir for unit tests
    │   ├── group_mock          # sample file for group file
    │   ├── passwd_mock         # sample file for passwd file
    │   └── test_restapi.py     # main script to run unit tests
    ├── utils                   # utilities for main app
    │   ├── groupParser.py      # helper class to parse group file
    │   ├── userParser.py       # helper class to parse passwd ile
    └── README.md
    
## Setup and Usage

##### Tech Required
* **[Python3](https://www.python.org/downloads/)** 
* **[Flask](https://pypi.org/project/Flask/)** - A web microframework for Python 
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - Python virtual environments
* **[Pytest](https://pypi.org/project/pytest/)** - Python unit tests framework
* **[pip](https://pypi.org/project/pip/)** - Package installer for Python
* **[gunicorn](https://pypi.org/project/gunicorn/)** - A Python WSGI HTTP Server for UNIX

##### Environment setup
* First ensure you have python3 and pip need to be installed first 
globally installed in your computer.
If not, you can get
* python3 [here](https://www.python.org). 
* pip [here](https://pypi.org/project/pip/)

* REST api app can be running on either python virtenv or your own workspace env
* For python virtual env:
    ```bash
        $ pip install virtualenv
    ```
* Create and activate your virtual environment in python3 in your workspace:
    ```bash
    $ virtualenv -p python3 venv
    $ pip install autoenv
    $ source venv/bin/activate
    ```
##### Clone the repo
    ```
    $ git clone https://github.com/royal50911/passwd_as_a_service.git
    $ cd passwd_as_a_service
    ```

##### Install dependencies
    ```
    $ pip install -r requirements.txt
    ```

##### Run the app
* App Usage:
    ```
    For testing: python api_app.py
    For deployment: gunicorn api_app:app -b 0.0.0.0:8000
    ```
* Simple run
    ```
    $ python api_app.py
    ```
* Run app in background and output into log file
    ```
    $ gunicorn api_app:app -b 0.0.0.0:8000 --access-logfile <path to log file> &
    ```
* Kill app running in background
    ```
    $ pkill -f gunicorn
    ```

##### Enviroment configuration vars
* All config vars are in config.py. To update or run different configure files,
update it in config.py
- MODE: running mode for flask , dev by default
- GROUP_FILE: path to group file, file sys "/etc/group" by default
- PASSWD_FILE: path to passwd file, file sys "/etc/passwd" by default

##### Unit Tests
    ```
    $ pytest -v tests/test_restapi.py  
    ```

##### Easy run/test with Makefile
* Run app
    ```bash
    $ make app
    ```
* Shutdown app
    ```bash
    $ make kill_app
    ```
* Run unit tests
    ```bash
    $ make test
    ```
