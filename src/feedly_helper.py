import config
import requests
import json
import jellyfish
import re
FEEDLY_URI = "http://cloud.feedly.com"
mark_read = []
marked_count = 0

def get_subscriptions():
    # reutrn subscriptions of the user
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/subscriptions'
    url = FEEDLY_URI + uri
    subscriptions = requests.get(url=url, headers=headers).json()
    return subscriptions

def get_unread_entries_in_category(ids):
    # id: category id
    # return unred items for a given category
    unread = []
    MAX_ENTRIES = 10000 # max number of entry ids to return based on feedly doc
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    for i in range(len(ids)):
        uri = '/v3/streams/ids?streamId='+ids[i]+'&count='+str(MAX_ENTRIES)+'&unreadOnly=true'
        url = FEEDLY_URI + uri
        unread.append(requests.get(url=url, headers=headers).json())
    return unread

def get_categories():
    # reutrn a list of the ids of the user categories
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/categories'
    url = FEEDLY_URI + uri
    categories = requests.get(url=url, headers=headers).json()
    data = []
    for i in range(len(categories)):
        if(categories[i]['label'] != 'Must Read'):
            data.append(categories[i]['id'])
    return data

def delete_category(id):
    # id: category id
    # delete the given category id from feedly
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/categories/' + id
    url = FEEDLY_URI + uri
    response = requests.delete(url=url, headers=headers).json()
    return response

def get_entry_contents(id):
    #id: entry ids list
    # return a list of the titles of all entries
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/entries/.mget'
    url = FEEDLY_URI + uri
    contents = requests.post(url=url, headers=headers, json=id).json()
    return contents

def clean_content(data):
    # data: list of all the content
    # return a dictunary with {id:{title:url}}
    clean_data = []
    for i in range(len(data)):
        single = [""] * 3
        single[0] = data[i]['id']
        single[1] = data[i]['title']
        single[2] = data[i]['alternate'][0]['href']
        clean_data.append(single)
    return clean_data

def check_similarity(data1, data2):
    # data1, data2 two lists size 2
    # return bool based on title score using jaro scoring algorithm or = urls
    title_score = jellyfish.jaro_winkler(data1[1].lower(),data2[1].lower()) * 100
    #if title_score > 80:
    #    print('\n',data1[1].lower(),'--' ,data2[1].lower(),':',title_score)
    rx = re.compile(r'[^(http:/|https:/)].*$')
    t1 = rx.findall(data1[2].lower())[0]
    t2 = rx.findall(data2[2].lower())[0]
    url_score = (t1 == t2)
    if( url_score  or title_score > 85):
        return True
    return False

def get_duplicates_content(data):
    # data: content
    # return dict of the duplicates
    similar = False
    dub_id = []
    added = []
    for i in range(len(data)):
        for j in range(len(data)):
            if(i != j):
                similar = check_similarity(data[i],data[j])
                if (similar and data[j][0] not in dub_id and data[i][0] not in dub_id):
                    #print(data[j][1],"\n ",data[i][1],"\n ",data[j][2],"\n ",data[i][2])
                    dub_id.append(data[j][0])
    return dub_id

def mark_read(body_data):
    # data: list of ids to mark read
    # return a dictunary with {id:{title:url}}
    count = len(body_data)
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret, 'Content-type': 'application/json'}
    uri = '/v3/markers'
    url = FEEDLY_URI + uri
    body = create_read_body(body_data)
    contents = requests.post(url=url, headers=headers, data=json.dumps(body))
    result = "The request returned \"{}\", and {} marked read".format(contents.reason, count)
    return result

def create_read_body(data):
    # data: list of ids to mark read
    # return a JSON format with the feedly body
    body = {}
    body['action'] = 'markAsRead'
    body['type'] = 'entries'
    body['entryIds'] = data
    return body


def work():
    category = get_categories()
    unread = get_unread_entries_in_category(category)
    contents = get_entry_contents(unread)
    clean = clean_content(contents)
    dubs = get_duplicates_content(clean)
    mark = mark_read(dubs)
    print(mark)

work()
