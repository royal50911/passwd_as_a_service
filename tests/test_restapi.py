
import os, sys
currdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currdir)
sys.path.append(parentdir)

import api_app
import pytest
import json

passwd_file = os.path.join(currdir,"passwd_mock")
group_file = os.path.join(currdir,"group_mock")

app = api_app.create_app(passwd_file,group_file )
app.testing = True
app = app.test_client()

def test_home():
    resp = app.get('/')
    content = resp.get_data(as_text=True)
    assert resp.status_code == 200 
    assert content ==  "Welcome To My Rest API App"

def test_users():
    resp = app.get('/users')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 18
    assert content[0] == {
        "comment": "Unprivileged User", 
        "gid": "-2", 
        "home": "/var/empty", 
        "name": "nobody", 
        "shell": "/usr/bin/false", 
        "uid": "-2"
    }

def test_users_by_query():
    resp = app.get('/users/query?home=%2Fvar%2Fempty')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 12
    assert content[0] == {
        "comment": "_launchservicesd", 
        "gid": "239", 
        "home": "/var/empty", 
        "name": "_launchservicesd", 
        "shell": "/usr/bin/false", 
        "uid": "239"
    }

def test_users_by_uid():
    resp = app.get('/users/239')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 6
    assert content == {
        "comment": "_launchservicesd", 
        "gid": "239", 
        "home": "/var/empty", 
        "name": "_launchservicesd", 
        "shell": "/usr/bin/false", 
        "uid": "239"
    }

def test_user_groups_by_uid():
    resp = app.get('/users/221/groups')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 3
    assert content == {
        "gid": "221", 
        "members": [
            "_teamsserver", 
            "_devicemgr"
        ], 
        "name": "_webauthserver"
    }

def test_groups():
    resp = app.get('/groups')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 57
    assert content[0] == {
        "gid": "-2", 
        "members": [], 
        "name": "nobody"
    }

def test_groups_by_query():
    resp = app.get('/groups/query?members=_analyticsd&members=_networkd')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 1
    assert content[0] == {
        "gid": "250", 
        "members": [
        "_analyticsd", 
        "_networkd", 
        "_timed", 
        "_reportmemoryexception"
        ], 
        "name": "_analyticsusers"
    }

def test_groups_by_gid():
    resp = app.get('/groups/13')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 3
    assert content == {
        "gid": "13", 
        "members": [
            "_taskgated"
        ], 
        "name": "_taskgated"
    }

def test_reflect_on_changes():

    with open(passwd_file, "a+") as f:
        f.write("testing_passwd:*:256:256:testing user:/testing/user:/usr/bin/false")

    with open(group_file, "a+") as f:
        f.write("_testing_group:*:256:_devicemgr,_testGroup,_teamsserver")

    resp = app.get('/users')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 19

    resp = app.get('/groups')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 58

    resp = app.get('/users/256/groups')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 3
    assert content["name"] == "_testing_group"

    os.system("sed -i '' '/testing_passwd/d' {}".format(passwd_file))
    os.system("sed -i '' '/testing_group/d' {}".format(group_file))

    resp = app.get('/users')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 18

    resp = app.get('/groups')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 57
