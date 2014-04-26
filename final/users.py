__author__ = 'JeremyShi'

import config

def writeUser(user):
    try:
        fout=open(config.userFile,'a')
        line = '%s '%(user.id,user.firstName,user.lastName,user.gender,user.homeCity,
        fout.write()
