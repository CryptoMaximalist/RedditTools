#!/usr/bin/python3

import praw
from configparser import ConfigParser

class redditTools:
    def getUsersModdedSubs(username, reddit):
        #Takes a username as a string and returns a list of subreddits that user moderates.  You should also pass your reddit instance as the 2nd parameter
        moddedSubs=[]
        path = "/user/{user}/moderated_subreddits".format(user=username)
        try:
            response = reddit.get(path)
            for sub in response["data"]:
                moddedSubs.append(sub["sr"])
            return(moddedSubs)
        except Exception as e:
            print("There was a problem fetching user's modded subs: "+str(e))
            
    def getContributors(subreddit, reddit):
        contributorList = []
        try:
            for contributor in reddit.subreddit(subreddit).contributor():
                contributorList.append(str(contributor))
            return(contributorList)
        except Exception as e:
            print("There was a problem fetching user's modded subs: "+str(e))
            print('A 403 error generally indicates a permissions problem')

    def getMods(subreddit, reddit):
        modList=[]
        try:
            for mod in reddit.subreddit(subreddit).moderator():
                modList.append(str(mod))
            return modList
        except Exception as e:
            print("There was a problem fetching subs's mods: "+str(e))
      
    def getConfig(subreddit, page, reddit):
        config = ConfigParser(allow_no_value=False)
        try:
            wikiPage = reddit.subreddit(subreddit).wiki[page]
            config.read_string(wikiPage.content_md)
            return(config)
        except Exception as e:
            print('There was a problem getting sub config: '+str(e))
            print('A 403 error generally indicates a permissions problem')
            print('A 404 error generally indicates the wiki page does not exist')
            
    def getSubPermissions(subreddit, username, reddit):
        permissionList=[]
        try:
            mods = reddit.subreddit(subreddit).moderator(username)
            return(mods[0].mod_permissions)
        except Exception as e:
            print("There was a problem fetching user's permissions: "+str(e))
            
    def logOutput(threadID, logText, data1, data2, reddit):
        logThread = reddit.submission(id=threadID)
        print(logText+''+data1+'-'+data2)
        logThread.reply(logText+'\n\n'+data1+'\n\n'+data2)
        
    def readWiki(subreddit, page, reddit):
        try:
            wikiPage = reddit.subreddit(subreddit).wiki[page]
            return(wikiPage.content_md)
        except Exception as e:
            print("There was a problem fetching wiki page's contents: "+str(e))
        
    def writeWiki(subreddit, page, newData, reddit):
        wikiPage = reddit.subreddit(subreddit).wiki[page]
        try:
            wikiPage.edit(newData) 
        except Exception as e:
            print("There was a problem writing to wiki page: "+str(e))


