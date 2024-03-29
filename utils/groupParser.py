#!/usr/bin/env python3
""" 
Project: Password as a service 
@Author: Hien Hoang
################
parse helper to get all groups from a file
"""
import os, sys
class Groups():
    def __init__(self, groups_file):
        self._file = os.path.realpath(groups_file)

    def getString(self, s):
        """Function convert string to int if applicable"""
        try: 
            num = int(s)
            return str(num)
        except (ValueError):
            return s

    def getGroups(self):
        """Function to parse group file input and return all groups"""
        groups = []
        try:
            with open(self._file, "r") as f:
                for line in f.read().split("\n"):
                    line = line.strip()
                    if line and line[0] != "#":
                        name,_,gid,members = line.split(":")
                        gid = int(gid)
                        member = []
                        if members.strip():
                            member += list(set(members.split(",")))
                        group = {
                            "name" : name,
                            "gid" : gid,
                            "members" : member
                        }
                        groups.append(group)
        except(IOError):
            raise IOError("Wrong file path or file not found for group file")
        except (ValueError):
            raise ValueError("Group file is NOT formatted correctly")
        else:
            return groups
        
    def getGroupByGID(self, gid):
        """Function to get a group given gid"""
        groups = self.getGroups()
        for group in groups:
            if str(group["gid"]) == self.getString(gid):
                return group
        return None

    def getGroupByQuery(self, query):
        """Function to get groups given query fields"""
        groups = self.getGroups()
        for k,vals in query.lists():
            i = len(groups)-1
            tmp = []
            while i >=0:
                if k == "member":
                    match = True
                    for val in vals:
                        if val not in groups[i]["members"]:
                            match = False
                            break
                    if match : tmp.append(groups[i])
                else:
                    if k == "gid":
                        vals = list(map(lambda x: self.getString(x),vals))
                    if k in groups[i] and str(groups[i][k]) == ''.join(vals):
                        tmp.append(groups[i])
                i-=1
            groups = tmp[:]
        return groups
