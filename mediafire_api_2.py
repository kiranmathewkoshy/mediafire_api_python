import urllib2
import hashlib
import urllib
import json
print 'Welcome.'
print 'Programmed by Kiran Mathew Koshy'

#Global Variables

API_VERSION=''
SESSION_TOKEN=''		
TOS=''
ACCEPTANCE_TOKEN=''
#App data
APP_ID=''
API_KEY=''

#User Data
EMAIL=''
PASSWORD=''
FIRST_NAME=''
LAST_NAME=''
DISPLAY_NAME=''
BASE_STORAGE=''
#Services
#Service for Data retrieval
def data_service(base_url,params):
	url=base_url+ '?' + urllib.urlencode(params)
	response = json.loads(urllib2.urlopen(url).read())
	if response['response']['result']!='Success':
		print 'Error in Connection'
	if 'response' in response:
		return response['response']

def download(url,filename):
	file=open(filename,'w')
	response=urllib2.urlopen(url).read()
	file.write(response)
	file.close()

#Service to get session token(Logging in)
def get_session_token():
	global APP_ID
	global API_KEY
	global SESSION_TOKEN
	global API_VERSION
	global EMAIL
	global PASSWORD
	print 'Authenticating with server..'
	m=hashlib.sha1()
	m.update(EMAIL+PASSWORD+APP_ID+API_KEY)
	hash=m.hexdigest()
	url_base='https://www.mediafire.com/api/user/get_session_token.php'
	params={
		  'email': EMAIL,
		  'password': PASSWORD,
		  'application_id': APP_ID,
		  'signature': hash,
		  'response_format':'json'
		}
	data=data_service(url_base,params)
	if data:
		print 'Successfully authenticated as '+EMAIL
	resp_action=data['action']
	API_VERSION=data['current_api_version']
	SESSION_TOKEN=data['session_token']
	return SESSION_TOKEN

#Service for Accessing user info.

def get_info():
	print 'Reading Data...'
	global SESSION_TOKEN
	global FIRST_NAME
	global LAST_NAME
	global DISPLAY_NAME
	global BASE_STORAGE
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json'
	}
	url_base='http://www.mediafire.com/api/user/get_info.php'
	data=data_service(url_base,params)
	FIRST_NAME=data['user_info']['first_name']
	LAST_NAME=data['user_info']['last_name']
	DISPLAY_NAME=data['user_info']['display_name']
	BASE_STORAGE=data['user_info']['base_storage']
	print 'Welcome, '+FIRST_NAME +' '+LAST_NAME

def renew_session_token():
	global SESSION_TOKEN
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json'
	}
	url_base='http://www.mediafire.com/api/user/renew_session_token.php'
	data=data_service(url_base,params)
	print 'Session Token renewed'
	SESSION_TOKEN=data['session_token']

def fetch_tos():
	global TOS
	global SESSION_TOKEN
	global ACCEPTANCE_TOKEN
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json'
	}
	url_base='http://www.mediafire.com/api/user/fetch_tos.php'
	data=data_service(url_base,params)
	TOS=data['terms_of_service']
	if 'acceptance_token' in data:
		ACCEPTANCE_TOKEN=data['acceptance_token']

def accept_tos():
	global SESSION_TOKEN
	global ACCEPTANCE_TOKEN
	params={
	  'session_token':SESSION_TOKEN,
	  'acceptance_token':ACCEPTANCE_TOKEN,
	  'response_format':'json'
	}
	url_base='http://www.mediafire.com/api/user/fetch_tos.php'
	data=data_service(url_base,params)


#File Access Services


def get_content_folders(folder_key=''):			#Accessing folders in a folder 				#To modify later
	global SESSION_TOKEN
	params={
	  'session_token':SESSION_TOKEN,
	  'content_type':'folders',
	  'response_format':'json'
	}
	if folder_key!='':
		params={
	  		'folder_key':folder_key,
	  		'session_token':SESSION_TOKEN,
	  		'content_type':'folders',
	  		'response_format':'json'
		}
	url_base='http://www.mediafire.com/api/folder/get_content.php'
	data=data_service(url_base,params)
	print 'Folders:'
	for i in range(0,len(data['folder_content']['folders'])):
		print '\nFolder '+str(i)+':'
		for j in data['folder_content']['folders'][i]:
			print j+': '+str(data['folder_content']['folders'][i][j])



def get_content_files(folder_key=''):			#Accessing files in a folder 				#To modify later
	global SESSION_TOKEN
	params={
	  'session_token':SESSION_TOKEN,
	  'content_type':'files',
	  'response_format':'json'
	}
	if folder_key!='':
		params={
	  		'folder_key':folder_key,
	  		'session_token':SESSION_TOKEN,
	  		'content_type':'files',
	  		'response_format':'json'
		}
	url_base='http://www.mediafire.com/api/folder/get_content.php'
	data=data_service(url_base,params)
	print 'Files:'
	for i in range(0,len(data['folder_content']['files'])):
		print '\nFile '+str(i)+':'
		for j in data['folder_content']['files'][i]:
			print j+': '+str(data['folder_content']['files'][i][j])



def ls(folder_key=''):						#Similar to the UNIX ls command:
	global SESSION_TOKEN

	#Displaying folders in the given folder	
	params={
	  'session_token':SESSION_TOKEN,
	  'content_type':'folders',
	  'response_format':'json'
	}	
	if folder_key!='':
		params={
	  		'folder_key':folder_key,
	  		'session_token':SESSION_TOKEN,
	  		'content_type':'folders',
	  		'response_format':'json'
		}
	url_base='http://www.mediafire.com/api/folder/get_content.php'
	data=data_service(url_base,params)
	for i in range(0,len(data['folder_content']['folders'])):
		print str(data['folder_content']['folders'][i]['name'])
	#End of displaying folders
	print ''
	#Displying files in the folder
	params={
	  'session_token':SESSION_TOKEN,
	  'content_type':'files',
	  'response_format':'json'
	}	
	if folder_key!='':
		params={
	  		'folder_key':folder_key,
	  		'session_token':SESSION_TOKEN,
	  		'content_type':'files',
	  		'response_format':'json'
		}
	url_base='http://www.mediafire.com/api/folder/get_content.php'
	data=data_service(url_base,params)
	for i in range(0,len(data['folder_content']['files'])):
		print str(data['folder_content']['files'][i]['filename'])


#get_info of a folder
def get_info_folder(folder_key=''):
	url_base='http://www.mediafire.com/api/folder/get_info.php'
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json'
	}	
	if folder_key!='':
		params={
	  		'folder_key':folder_key,
	  		'session_token':SESSION_TOKEN,
	  		'response_format':'json'
		}
	data=data_service(url_base,params)
	print 'Folder details :'
	for i in data['folder_info']:
		print i +' : '+ data['folder_info'][i]

#get_info of a file
def get_info_file(quick_key):
	url_base='http://www.mediafire.com/api/file/get_info.php'
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json',
	  'quick_key': quick_key
	}
	data=data_service(url_base,params)
	print 'Folder details :'
	for i in data['file_info']:
		print i+' : '+data['file_info'][i]

#Delete a file
def file_delete(quick_key):
	url_base='http://www.mediafire.com/api/file/delete.php'
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json',
	  'quick_key': quick_key
	}
	data=data_service(url_base,params)
	print data

#Download API

#Direct download API

def direct_download_link(quick_key):
	url_base='http://www.mediafire.com/api/file/get_links.php'
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json',
	  'quick_key': quick_key,
	  'link_type': 'direct_download'
	}
	data=data_service(url_base,params)
	print 'Direct Download Link : '+str(data['links'][0]['direct_download'])
	print 'Quick Key : '+str(data['links'][0]['quickkey'])



def direct_download(quick_key,filename):
	url_base='http://www.mediafire.com/api/file/get_links.php'
	params={
	  'session_token':SESSION_TOKEN,
	  'response_format':'json',
	  'quick_key': quick_key,
	  'link_type': 'direct_download'
	}
	data=data_service(url_base,params)
	print 'Direct Download Link : '+str(data['links'][0]['direct_download'])
	print 'Quick Key : '+str(data['links'][0]['quickkey'])
	download(data['links'][0]['direct_download'],filename)



#System-Related Queries:

def get_version():
	url_base='http://www.mediafire.com/api/system/get_version.php'
	params={
	  'response_format':'json',
	}
	data=data_service(url_base,params)
	print data['current_api_version']

get_session_token()
#get_info()
#renew_session_token()
#fetch_tos()
#accept_tos()
#get_content_folders()
#get_content_files()
#ls()
#get_info_folder()
#get_info_file('iu72twpa6chca5j')
#download('http://205.196.123.179/kn0offywkx0g/rzq7ca5d1d7r2mm/1.txt','output.txt')
#get_version()
#direct_download_link('iu72twpa6chca5j')
#direct_download('iu72twpa6chca5j','output.txt')
#file_delete('iu72twpa6chca5j')


