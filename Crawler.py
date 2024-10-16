from TwitterSearch import *
import json
import sys
import time
import os 
import datetime;
  
State = str(sys.argv[1])  #'Makkah' #'Riyad' #'Madenna
date_since = str(sys.argv[2]) #'2021-06-25'
date_until = str(sys.argv[3]) #'2021-06-24'
language = str(sys.argv[4]) # 'en' #'ar'

if (language == 'en'):
	keywords_file = "Keywords/EnglishKeywords"
else:
	keywords_file = "Keywords/ArabicKeywords_collected4"
print (keywords_file)

try:
    # it's about time to create a TwitterSearch object with your secret tokens
    ts = TwitterSearch(
  	 consumer_key = '',
	 consumer_secret = '',
  	 access_token= '',
	 access_token_secret= '')
	
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
    def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = current_ts_instance.get_statistics()
        if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
            time.sleep(60) # sleep for 60 seconds
		
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
    def retrieve_tweets(search_url, previous_count):
    	tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    	print (search_url)
    	tso.set_search_url(search_url)
    	
    	open('tweets_'+State+'_'+date_since+'_'+language+'_duplicates.json', 'a') 
    	open('tweets_'+State+'_'+date_since+'_'+language+'_duplicates.csv', 'a')
    	
    	count = 0
    	for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
    		with open('tweets_'+State+'_'+date_since+'_'+language+'_duplicates.json', 'a') as f:
    				f.write(json.dumps(tweet))
    				f.write(",")
	    			f.write("\n")
	    			
    		with open('tweets_'+State+'_'+date_since+'_'+language+'_duplicates.csv', 'a') as f:
    			f.write(str(tweet['id'])+','+State+','+geo_code)
    			f.write("\n")    
    			
    		#print ('@%s %s tweeted: %s %s geo:%s' % ( tweet['user']['screen_name'],tweet['user']['location'], tweet['created_at'], tweet['full_text'],tweet['geo'] ) )
    		#print('\n')
    		count = count +1
    	print('\n')
    	print('Total number of returned tweets: ', count)	   		
    	return count
    
    
    ########################################################################################################################################################################################
    with open('tweets_'+State+'_'+date_since+'_'+language+'_duplicates.json', 'a') as f:
    		f.write("[") 
      			
    with open('Circles/'+State+'.txt', 'r') as circles_file:
    	circles_lines = circles_file.readlines()
    
    with open(keywords_file, 'r') as keywords_file:
    	keywords_lines = keywords_file.readlines()
    		
    count = 0
    circles_count =0 
    for circle_line in circles_lines:
    		circles_count = circles_count + 1
    		items=circle_line.split(' ')
    		radius= items[2].replace('\n','')
    		geo_code = items[0]+","+items[1]+","+radius+"km"
    		print (geo_code)
    		keywords_count = 0
    		for keywords_line in keywords_lines:
    			url = '?q='+keywords_line+'&until='+date_until+'&since='+date_since+'&lang='+language+'&geocode='+geo_code+'&count=100&tweet_mode=extended'
    			count = retrieve_tweets(url,count)
    			keywords_count = keywords_count + 1
    			print(str(datetime.datetime.now())+" Processed circles so far: "+ str(circles_count)+'/'+str(len(circles_lines))) 
    			print(str(datetime.datetime.now())+" Processed keywords so far: "+ str(keywords_count)+'/'+str(len(keywords_lines)))
      			
    with open('tweets_'+State+'_'+date_since+'_'+language+'_duplicates.json', 'a') as f:
    		f.seek(f.tell() - 2, os.SEEK_SET)
    		f.truncate()
    		f.write("]")
    
except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
