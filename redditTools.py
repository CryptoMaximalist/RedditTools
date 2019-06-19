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
            moddedSubs = [x.lower() for x in moddedSubs]
            return(moddedSubs)
        except Exception as e:
            print("There was a problem fetching user's modded subs: "+str(e))
            
    def getContributors(subreddit, reddit):
        contributorList = []
        try:
            for contributor in reddit.subreddit(subreddit).contributor():
                contributorList.append(str(contributor))
            contributorList = [x.lower() for x in contributorList]
            return(contributorList)
        except Exception as e:
            print("There was a problem fetching subreddit's contributors: "+subreddit+"-"+str(e))
            print('A 403 error indicates a permissions problem')

    def getMods(subreddit, reddit):
        modList=[]
        try:
            for mod in reddit.subreddit(subreddit).moderator():
                modList.append(str(mod))
            modList = [x.lower() for x in modList]
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
            print('A 403 error indicates a permissions problem')
            print('A 404 error indicates the wiki page does not exist')
            
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
        logThread.reply(logText+'\n\nData 1:'+data1+'\n\nData 2:'+data2)
        
    def readWiki(subreddit, page, returnFormat, reddit):
        try:
            wikiPage = reddit.subreddit(subreddit).wiki[page]
            if returnFormat == 'list':
                data_list = [y for y in (x.strip() for x in wikiPage.content_md.splitlines()) if y] # Split lines into list
                return(data_list)
            else:
                return(wikiPage.content_md)
        except Exception as e:
            print("There was a problem fetching wiki page's contents: "+str(e))

        
    def writeWiki(subreddit, page, newData, reddit):
        wikiPage = reddit.subreddit(subreddit).wiki[page]
        try:
             wikiPage.edit(newData)
        except Exception as e:
            print("There was a problem writing to wiki page: "+str(e))


    def appendWiki(subreddit, page, newData, reddit):
        oldWikiData = []
        separatorString = ''
        
        try:
            wikiPage = reddit.subreddit(subreddit).wiki[page]
            oldWikiData = [y for y in (x.strip() for x in wikiPage.content_md.splitlines()) if y] # Split lines into list
        except Exception as e:
            print("There was a problem fetching wiki page's contents: "+str(e))
        
        newWikiData = oldWikiData.copy()
        newWikiData.append(newData)
        newWikiData = '\n'.join(newWikiData)
        try:
            print('Committing to wiki')
            wikiPage.edit(newWikiData)
        except Exception as e:
            print("There was a problem writing to wiki page: "+str(e))


    def buildLogList(log):
        linkList = ['removelink', 'approvelink', 'removecomment', 'approvecomment', 'distinguish', 'spamlink', 'spamcomment', 'sticky', 'ignorereports', 'markoriginalcontent']
        detailsList = ['editsettings', 'wikirevise']
        authorList = ['banuser', 'unbanuser']
        logList = []
        logList.append(str(int(log.created_utc)))
        logList.append(str(log.subreddit))
        logList.append(str(log.mod))
        logList.append(str(log.action))
        if log.action in linkList:
            logList.append(str(log.target_permalink))
        elif log.action in detailsList:
            logList.append(str(log.details))
        elif log.action in authorList:
            logList.append(str(log.target_author))
        elif log.action == 'editflair':
            if log.target_permalink is None:
                logList.append(str(log.target_permalink))
            else:
                logList.append(str(log.target_author))
        else:
            print()
            print('ERROR: Unknown Action type: '+log.action)
            print(vars(log))
        return(logList)

        
    def verifyHeaders(headers):
        #Get old wiki data and write new data
        #Unfinished
        pipedHeaders = '|'.join(headers)
        for i in headers:
            separatorString = separatorString+'|-'
        separatorString = separatorString[1:]
        #print(pipedHeaders)
        #print(separatorString)
        #print(oldWikiData[0])
        print(oldWikiData)
        print(len(oldWikiData))
        if (len(oldWikiData) < 2) or (oldWikiData[0] != pipedHeaders) or (oldWikiData[1] != separatorString):
            print('Prepending headers')
            oldWikiData.insert(0,separatorString)
            oldWikiData.insert(0,pipedHeaders)
        
