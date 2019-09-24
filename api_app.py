#!/usr/bin/env python3
""" 
Project: Password as a service 
@Author: Hien Hoang
################
Main App to create rest api app
Preps: flask, Flask-RESTful, gunicorn
ENV vars in config.py

Usage: 
    For testing: python api_app.py
    For deployment: gunicorn api_app:app --access-logfile <path to log file> 

"""
from flask import Flask, url_for, request, jsonify
import sys, os
import config
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir,"utils/"))
import userParser, groupParser

app = Flask(__name__)
app.config["userObj"] = userParser.Users(config.PASSWD_FILE)
app.config["groupObj"] = groupParser.Groups(config.GROUP_FILE)
app.config.from_object('config.{}'.format(config.MODE))

@app.route('/', methods = ['GET'])
def api_root():
    """Home Page"""
    return 'Welcome To Passwd As A Service Rest API'

@app.route('/users/')
@app.route('/users', methods = ['GET'])
def api_users():
    """Get all users from passwd file"""
    userObj = app.config["userObj"]
    users = userObj.getUsers()
    return jsonify(users)

@app.route('/users/query', methods = ['GET'])
def api_users_query():
    """Get all users matching query"""
    args = request.args
    userObj = app.config["userObj"]
    users = userObj.getUserByQuery(args)
    return jsonify(users)

@app.route('/users/<uid>/')
@app.route('/users/<uid>', methods = ['GET'])
def api_user_by_uid(uid):
    """Get a user given uid"""
    userObj = app.config["userObj"]
    res = userObj.getUserByUID(uid)
    if res:
        return jsonify(res)
    else:
        return not_found()

@app.route('/users/<uid>/groups/')
@app.route('/users/<uid>/groups', methods = ['GET'])
def api_group_of_user(uid):
    """Get group for a user given uid"""
    userObj = app.config["userObj"]
    groupObj = app.config["groupObj"]
    groups = []
    res = userObj.getUserByUID(uid)
    all_groups = groupObj.getGroups()
    for group in all_groups:
        if res and group["gid"] == res["gid"]:
            groups.append(group)
    return jsonify(groups)

@app.route('/groups/')
@app.route('/groups', methods = ['GET'])
def api_groups():
    """Get all groups from group file"""
    groupObj = app.config["groupObj"]
    groups = groupObj.getGroups()
    return jsonify(groups)

@app.route('/groups/query', methods = ['GET'])
def api_groups_query():
    """Get all groups matching query"""
    groupObj = app.config["groupObj"]
    args = request.args
    groups = groupObj.getGroupByQuery(args)
    return jsonify(groups)

@app.route('/groups/<gid>/')
@app.route('/groups/<gid>', methods = ['GET'])
def api_group_by_gid(gid):
    """Get a group given gid"""
    groupObj = app.config["groupObj"]
    res = groupObj.getGroupByGID(gid)
    if res:
        return jsonify(res)
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    """Function handle 404 error in case route not found"""
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    res = jsonify(message)
    res.status_code = 404
    return res

if __name__ == "__main__":
    app.run(host= config.HOST, port=config.PORT)
