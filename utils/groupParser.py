
import os, sys
class Groups():
    def __init__(self, groups_file):
        self._file = os.path.realpath(groups_file)

    def getGroups(self):
        groups = []
        try:
            with open(self._file, "r") as f:
                for line in f.read().split("\n"):
                    line = line.strip()
                    if line and line[0] != "#":
                        name,_,gid,members = line.split(":")
                        member = []
                        if members.strip():
                            member += members.split(",")
                        group = {
                            "name" : name,
                            "gid" : gid,
                            "members" : member
                        }
                        groups.append(group)
        except(IOError):
            print("Wrong file path or file not found for group file")
            sys.exit(1)
        except (ValueError):
            print("File not formatted correctly")
            sys.exit(1)
        else:
            return groups
        
    def getGroupByGID(self, gid):
        groups = self.getGroups()
        for group in groups:
            if group["gid"] ==gid:
                return group
        return None

    def getGroupByQuery(self, query):
        groups = self.getGroups()
        for k,vals in query.lists():
            i = len(groups)-1
            tmp = []
            while i >=0:
                if k == "members":
                    if k in groups[i]:
                        match = True
                        for val in vals:
                            if val not in groups[i][k]:
                                match = False
                                break
                        if match : tmp.append(groups[i])
                else:
                    if k in groups[i] and groups[i][k] == ''.join(vals):
                        tmp.append(groups[i])
                i-=1
            groups = tmp[:]
        return groups
