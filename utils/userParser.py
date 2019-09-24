#!/usr/bin/env python3
""" 
Project: Password as a service 
@Author: Hien Hoang
################
parse helper to get all users from a file
"""
import os, sys
class Users():
    def __init__(self, users_file):
        self._file = os.path.realpath(users_file)

    def getString(self, s):
        """Function convert string to int if applicable"""
        try: 
            num = int(s)
            return str(num)
        except (ValueError):
            return s

    def getUsers(self):
        """Function to parse passwd file input and return all users"""
        users = []
        try:
            with open(self._file, "r") as f:
                for line in f.read().split("\n"):
                    line = line.strip()
                    if line and line[0] != "#":
                        name,_,uid,gid,comment,home,shell = line.strip().split(":")
                        uid = int(uid)
                        gid = int(gid)
                        user = {
                            "name" : name,
                            "uid" : uid, 
                            "gid" : gid,
                            "comment" : comment,
                            "home" : home, 
                            "shell" : shell
                        }
                        users.append(user)
        except(IOError):
            raise IOError("Wrong file path or file not found for passwd file")
        except (ValueError):
            raise ValueError ("Passwd file is NOT formatted correctly")
            sys.exit(1)
        else:
            return users
        
    def getUserByUID(self, uid):
        """Function to get a user given gid"""
        users = self.getUsers()
        for user in users:
            if str(user["uid"]) == self.getString(uid):
                return user
        return None

    def getUserByQuery(self, query):
        """Function to get users given query fields"""
        users = self.getUsers()
        for k,vals in query.lists():
            i = len(users)-1
            tmp = []
            while i >=0:
                if k == "uid" or k == "gid":
                    vals = list(map(lambda x: self.getString(x), vals))
                if k in users[i] and str(users[i][k]) == ''.join(vals) :
                    tmp.append(users[i])
                i-=1
            users = tmp[:]
        return users
