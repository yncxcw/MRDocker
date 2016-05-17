#!/usr/bin/python

import logging

from cgroup import Cgroup
import os

log = logging.getLogger("RMDocker.Container")

class Container:
  
     
    def __init__(self,id,name,configure):
        self.image = ""
        self.status= ""
        self.name = name
        self.id   = id
        self.testPath="/sys/fs/cgroup/memory/docker/"+str(id)
        self.configure = configure
        self.cgroups = {}
   
    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def setImage(self,image):
        self.iamge=image

    def getImage(self):
        return self.image

    def setStatus(self,status):
        self.status=status

    def getStatus(self):
        return self.status

    def isRunning(self):
        if os.path.exists(self.testPath):
            return True
        else:
            return False

    def addCgroups(self):
        for cgroupName in self.configure.get("cgroup"):
            cgroup = Cgroup(cgroupName,self.id,self.configure)
            cgroup.initialize()
            self.cgroups[cgroupName]=cgroup

    def getValue(self,name,key):
        return self.cgroups[name].get(key)


    def getCgroupKeyValues(self):
        cgroupKeyValues = {}
        for key in self.cgroups.keys():
            cgroupKeyValues[key] = self.cgroups[key].getKeyValues()
        return cgroupKeyValues
  
    def updateValue(self,name,key,value):
        self.cgroups[name].update(key,value)

    def read(self):
        for key in self.cgroups.keys():
            self.cgroups[key].read()
    
    def sync(self):
        isSuccess = False
        for key in self.cgroups.keys():
           self.cgroups[key].sync()     

    def getCgroupSize(self):
        return len(self.cgroups)

    def printContainer(self):
        for cgroupName in self.cgroups.keys():
            self.cgroups[cgroupName].printCgroup()
                 



