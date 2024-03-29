#!/usr/bin/env python3
""" 
Project: Password as a service 
@Author: Hien Hoang
################
unit tests for main app
Preps: flask, Flask-RESTful, pytest
Usage: pytest -v test_restapy.py
"""
import os, sys
currdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currdir)
utilsdir = os.path.join(currdir,"utils/")
sys.path.append(parentdir)
sys.path.append(utilsdir)
import api_app, userParser, groupParser
import pytest, json

passwd_file = os.path.join(currdir,"passwd_mock")
group_file = os.path.join(currdir,"group_mock")

app = api_app.app
app.config["userObj"] = userParser.Users(passwd_file)
app.config["groupObj"] = groupParser.Groups(group_file)
app.testing = True
app = app.test_client()

def test_home():
    resp = app.get('/')
    content = resp.get_data(as_text=True)
    assert resp.status_code == 200 
    assert content ==  "Welcome To Passwd As A Service Rest API"

def test_not_found_page():
    resp = app.get('/no_page')
    assert resp.status_code == 404 

def test_users():
    resp = app.get('/users')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 18

def test_users_by_query():
    ## existing user
    resp = app.get('/users/query?home=%2Fvar%2Fempty')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 12
    assert content[0]["home"] == "/var/empty"

    resp = app.get('/users/query?uid=0239')
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 1
    assert content[0]["uid"] == 239

    # invalid field or non existing user
    resp = app.get('/users/query?home=%2Fvar')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 0
    assert content == []

def test_users_by_uid():
    ## exisitng user
    resp = app.get('/users/239')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 6
    assert content["uid"] == 239

    resp = app.get('/users/0239')
    assert resp.status_code == 200 

    resp = app.get('/users/+239')
    assert resp.status_code == 200

    # non existing user
    resp = app.get('/users/2390')
    assert resp.status_code == 404

def test_user_groups_by_uid():
    resp = app.get('/users/221/groups')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 1
    assert content[0]["gid"] == 221

    resp = app.get('/users/0221/groups')
    assert resp.status_code == 200 

    resp = app.get('/users/+221/groups')
    assert resp.status_code == 200

    # user with no groups
    resp = app.get('/users/2210/groups')
    assert resp.status_code == 200 
    content = json.loads(resp.get_data(as_text=True))
    assert content == []

def test_groups():
    resp = app.get('/groups')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 57

def test_groups_by_query():
    resp = app.get('/groups/query?member=_analyticsd&member=_networkd')
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 1
    assert ("_analyticsd" in content[0]["members"]) == True
    assert ("_networkd" in content[0]["members"]) == True

    resp = app.get('/groups/query?gid=013')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 1
    assert content[0]["gid"] == 13

    # invalid field or non existing group
    resp = app.get('/groups/query?members=_testing')
    assert resp.status_code == 200 
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 0
    assert content == []

def test_groups_by_gid():
    resp = app.get('/groups/13')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 3
    assert content["gid"] == 13

    resp = app.get('/groups/013')
    assert resp.status_code == 200 

    resp = app.get('/groups/+13')
    assert resp.status_code == 200 

    # non existing group
    resp = app.get('/groups/1324')
    assert resp.status_code == 404

def test_reflect_on_changes():
    # add new user and group
    passwd_cont = ""
    with open(passwd_file, "r") as f:
        passwd_cont = f.read()
    group_cont = ""
    with open(group_file, "r") as f:
        group_cont = f.read()

    with open(passwd_file, "a+") as f:
        f.write("testing_passwd:*:256:256:testing user:/testing/user:/usr/bin/false")
    with open(group_file, "a+") as f:
        f.write("_testing_group:*:256:_devicemgr,_testGroup,_teamsserver")

    resp = app.get('/users/256')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 6
    assert content["uid"] == 256

    resp = app.get('/groups/256')
    assert resp.status_code == 200 
    assert resp.content_type == 'application/json'
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 3
    assert content["gid"] == 256

    resp = app.get('/users/256/groups')
    assert resp.status_code == 200
    content = json.loads(resp.get_data(as_text=True))
    assert len(content) == 1
    assert content[0]["gid"] == 256

    # remove prev user n group just added
    with open(passwd_file, "w+") as f:
        f.write(passwd_cont)
    with open(group_file, "w+") as f:
        f.write(group_cont)

    # test if prev user and group has been removed
    resp = app.get('/users/256')
    assert resp.status_code == 404

    resp = app.get('/groups/256')
    assert resp.status_code == 404
