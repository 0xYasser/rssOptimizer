import config
import requests
import json

FEEDLY_URI = "http://cloud.feedly.com"

def get_subscriptions():
    # reutrn subscriptions of the user
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/subscriptions'
    url = FEEDLY_URI + uri
    subscriptions = requests.get(url=url, headers=headers).json()
    return subscriptions

def get_unread_in_category(id):
    # id: category id
    # return unred items for a given category
    MAX_ENTRIES = 10000 # max number of entry ids to return based on feedly doc
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/streams/ids?streamId='+id+'&count='+str(MAX_ENTRIES)+'&unreadOnly=true'
    url = FEEDLY_URI + uri
    unread = requests.get(url=url, headers=headers).json()
    return unread

def get_categories():
    # reutrn a list of the ids of the user categories
    client_secret = config.FEEDLY_CONFIG['CLIENT_SECRET']
    headers = {'Authorization': 'Bearer '+client_secret}
    uri = '/v3/categories'
    url = FEEDLY_URI + uri
    categories = requests.get(url=url, headers=headers).json()
    data = [""] * len(categories)
    for i in range(len(categories)):
        if(categories[i]['title'] != 'Must Read'):
            data[i] = categories[i]['id']
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
