#!/usr/bin/python3

import praw
from configparser import ConfigParser

class reddit_tools:
    def get_users_modded_subs(username, reddit):
        #Takes a username as a string and returns a list of subreddits that user moderates.  You should also pass your reddit instance as the 2nd parameter
        modded_subs=[]
        path = "/user/{user}/moderated_subreddits".format(user=username)
        try:
            response = reddit.get(path)
            for sub in response["data"]:
                modded_subs.append(sub["sr"])
            modded_subs = [x.lower() for x in modded_subs]
            return(modded_subs)
        except Exception as e:
            print("There was a problem fetching user's modded subs: "+str(e))
            
    def get_contributors(subreddit, reddit):
        contributor_list = []
        try:
            for contributor in reddit.subreddit(subreddit).contributor():
                contributor_list.append(str(contributor))
            contributor_list = [x.lower() for x in contributor_list]
            return(contributor_list)
        except Exception as e:
            print("There was a problem fetching subreddit's contributors: "+subreddit+"-"+str(e))
            print('A 403 error indicates a permissions problem')

    def get_mods(subreddit, reddit):
        mod_list=[]
        try:
            for mod in reddit.subreddit(subreddit).moderator():
                mod_list.append(str(mod))
            mod_list = [x.lower() for x in mod_list]
            return mod_list
        except Exception as e:
            print("There was a problem fetching subs's mods: "+str(e))
      
    def get_config(subreddit, page, reddit):
        config = ConfigParser(allow_no_value=False)
        try:
            wiki_page = reddit.subreddit(subreddit).wiki[page]
            config.read_string(wiki_page.content_md)
            return(config)
        except Exception as e:
            print('There was a problem getting sub config: '+str(e))
            print('A 403 error indicates a permissions problem')
            print('A 404 error indicates the wiki page does not exist')
            
    def get_sub_permissions(subreddit, username, reddit):
        permission_list=[]
        try:
            mods = reddit.subreddit(subreddit).moderator(username)
            return(mods[0].mod_permissions)
        except Exception as e:
            print("There was a problem fetching user's permissions: "+str(e))
            
    def log_output(thread_id, log_text, data1, data2, reddit):
        log_thread = reddit.submission(id=thread_id)
        print(log_text+''+data1+'-'+data2)
        log_thread.reply(log_text+'\n\nData 1:'+data1+'\n\nData 2:'+data2)
        
    def read_wiki(subreddit, page, return_format, reddit):
        try:
            wiki_page = reddit.subreddit(subreddit).wiki[page]
            if return_format == 'list':
                data_list = [y for y in (x.strip() for x in wiki_page.content_md.splitlines()) if y] # Split lines into list
                return(data_list)
            else:
                return(wiki_page.content_md)
        except Exception as e:
            print("There was a problem fetching wiki page's contents: "+str(e))

        
    def write_wiki(subreddit, page, new_data, reddit):
        wiki_page = reddit.subreddit(subreddit).wiki[page]
        try:
             wiki_page.edit(new_data)
        except Exception as e:
            print("There was a problem writing to wiki page: "+str(e))


    def append_wiki(subreddit, page, new_data, reddit):
        old_wiki_data = []
        #separatorString = ''
        
        try:
            wiki_page = reddit.subreddit(subreddit).wiki[page]
            old_wiki_data = [y for y in (x.strip() for x in wiki_page.content_md.splitlines()) if y] # Split lines into list
        except Exception as e:
            print("There was a problem fetching wiki page's contents: "+str(e))
        
        #newWikiData = oldWikiData.copy()
        #newWikiData.append(newData)
        new_wiki_data = old_wiki_data + list(new_data)
        new_wiki_data = '\n'.join(new_wiki_data)
        try:
            print('Committing to wiki')
            print(new_wiki_data)
            wiki_page.edit(new_wiki_data)
        except Exception as e:
            print("There was a problem appending to wiki page: "+str(e))


    def build_log_list(log):
        link_list = ['removelink', 'approvelink', 'removecomment', 'approvecomment', 'distinguish', 'spamlink', 'spamcomment', 'sticky', 'ignorereports', 'markoriginalcontent']
        details_list = ['editsettings', 'wikirevise']
        author_list = ['banuser', 'unbanuser']
        log_list = []
        log_list.append(str(int(log.created_utc)))
        log_list.append(str(log.subreddit))
        log_list.append(str(log.mod))
        log_list.append(str(log.action))
        if log.action in link_list:
            log_list.append(str(log.target_permalink))
        elif log.action in details_list:
            log_list.append(str(log.details))
        elif log.action in author_list:
            log_list.append(str(log.target_author))
        elif log.action == 'editflair':
            if log.target_permalink is None:
                log_list.append(str(log.target_permalink))
            else:
                log_list.append(str(log.target_author))
        else:
            print()
            print('ERROR: Unknown Action type: '+log.action)
            print(vars(log))
            logging.error('ERROR: Unknown Action type: '+log.action)
            logging.error(vars(log))
        return(log_list)

        
    def verify_headers(headers):
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
        
