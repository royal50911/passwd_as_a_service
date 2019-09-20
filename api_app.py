""" 
Project: Password as a service 
@Author: Hien Hoang
################
Main App to create rest api app
Preps: flask, Flask-RESTful

usage: python api_app.py [-h] [-pf PASSWD_FILE] [-gf GROUP_FILE]
                         [-c CONFIG_MODE]

optional arguments:
  -h, --help            show this help message and exit
  -pf PASSWD_FILE, --passfile PASSWD_FILE
                        path to password file if specified, 
                        sys path by default in config.py
  -gf GROUP_FILE, --groupfile GROUP_FILE
                        path to group file if specified, 
                        sys path by default in config.py
  -c CONFIG_MODE, --config CONFIG_MODE
                        environment config: [dev, prod, testing]; dev by
                        default

"""
from flask import Flask, url_for, request, jsonify
import sys, os, argparse
import config
sys.path.append(os.path.join(config.basedir,"utils/"))
import userParser, groupParser

def create_app(passwd_file, group_file):
    """Function to create app"""
    app = Flask(__name__)
    userObj = userParser.Users(passwd_file)
    groupObj = groupParser.Groups(group_file)

    @app.route('/', methods = ['GET'])
    def api_root():
        return 'Welcome To My Rest API App'

    @app.route('/users/')
    @app.route('/users', methods = ['GET'])
    def api_users():
        users = userObj.getUsers()
        return jsonify(users)

    @app.route('/users/query', methods = ['GET'])
    def api_users_query():
        args = request.args
        users = userObj.getUserByQuery(args)
        return jsonify(users)

    @app.route('/users/<uid>/')
    @app.route('/users/<uid>', methods = ['GET'])
    def api_user_by_uid(uid):
        res = userObj.getUserByUID(uid)
        return jsonify(res)

    @app.route('/users/<uid>/groups/')
    @app.route('/users/<uid>/groups', methods = ['GET'])
    def api_group_of_user(uid):
        res = userObj.getUserByUID(uid)
        if res:
            user = groupObj.getGroupByGID(res["gid"])
            return jsonify(user)
        else:
            return jsonify(res)

    @app.route('/groups/')
    @app.route('/groups', methods = ['GET'])
    def api_groups():
        groups = groupObj.getGroups()
        return jsonify(groups)

    @app.route('/groups/query', methods = ['GET'])
    def api_groups_query():
        args = request.args
        groups = groupObj.getGroupByQuery(args)
        return jsonify(groups)

    @app.route('/groups/<gid>/')
    @app.route('/groups/<gid>', methods = ['GET'])
    def api_group_by_gid(gid):
        res = groupObj.getGroupByGID(gid)
        return jsonify(res)

    @app.errorhandler(404)
    def not_found(error=None):
        """Function handle error in case route not found"""
        message = {
                'status': 404,
                'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

    return app

def validate_input(passwd_file, group_file, mode):
    """Functionn to validate inputs for files and config mode"""
    try:     
        userObj = userParser.Users(passwd_file)
        userObj.getUsers()
        groupObj = groupParser.Groups(group_file)
        groupObj.getGroups()
    except (IOError, ValueError) as e:
        print(e)
        sys.exit(1)

    if mode not in config.modes:
        print ("Wrong config mode value. Must be in one " + \
            "these fields: [dev, prod, testing]")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("python " + os.path.basename(__file__))
    parser.add_argument('-pf', '--passfile', 
            help='passwd file path. Otherwise sys path by default in config.py',
                action='store', dest='passwd_file')
    parser.add_argument('-gf', '--groupfile', 
            help='group file path. Otherwise sys path by default in config.py',
                action='store', dest='group_file')
    parser.add_argument('-c', '--config', 
                help='environment config: [dev, prod, testing]; dev by default',
                action='store', default="dev", dest='config_mode')
    arguments = parser.parse_args()
    
    passwd_file = config.SysFiles.PASSWD_FILE
    group_file = config.SysFiles.GROUP_FILE
    if arguments.passwd_file:
        passwd_file = arguments.passwd_file
    if arguments.group_file:
        group_file = arguments.group_file

    # valid input before running
    validate_input(passwd_file, group_file,arguments.config_mode)

    mode = config.modes[arguments.config_mode]
    app = create_app(passwd_file,group_file)
    app.config.from_object('config.{}'.format(mode))
    app.run(host= config.host, port=config.port)
