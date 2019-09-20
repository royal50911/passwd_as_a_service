from flask import Flask, url_for, request, jsonify
import sys, os, argparse
import config
sys.path.append(os.path.join(config.basedir,"utils/"))
import userParser, groupParser

def create_app(passwd_file, group_file):
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
        if res:
            return jsonify(res)
        else:
            return not_found()

    @app.route('/users/<uid>/groups/')
    @app.route('/users/<uid>/groups', methods = ['GET'])
    def api_group_of_user(uid):
        res = userObj.getUserByUID(uid)
        if res:
            user = groupObj.getGroupByGID(res["gid"])
            return jsonify(user)
        else:
            return not_found()

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
        if res:
            return jsonify(res)
        else:
            return not_found()

    @app.errorhandler(404)
    def not_found(error=None):
        message = {
                'status': 404,
                'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser("python " + os.path.basename(__file__))
    parser.add_argument('-pf', '--passfile', help='password file path',
                action='store', dest='passwd_file')
    parser.add_argument('-gf', '--groupfile', help='group file path',
                action='store', dest='group_file')
    parser.add_argument('-c', '--config', 
                help='environment config: [dev, prod, testing]; dev by default',
                action='store', default="dev", dest='config_mode')
    arguments = parser.parse_args()
    
    mode = config.modes[arguments.config_mode]
    passwd_file = config.SysFiles.PASSWD_FILE
    group_file = config.SysFiles.GROUP_FILE
    if arguments.passwd_file:
        passwd_file = arguments.passwd_file
    if arguments.group_file:
        group_file = arguments.group_file

    app = create_app(passwd_file,group_file)
    app.config.from_object('config.{}'.format(mode))
    app.run(host= config.host, port=config.port)
