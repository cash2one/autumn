# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import base64
import requests

BING_KEY = 'LVqAJDmakLrIedU54RutHL2qGxHlEILdYVCkBrE+t1A'
# BING_KEY = 'ubiPp/TvIIR/GJqLfqWXjuGr3VOdUSq8naDOiOq9Zck='


def main():
    query = "sunshine"
    print bing_search(query, 'Web')
    # print bing_search(query, 'Image')


def bing_search(query, search_type):
    # search_type: Web, Image, News, Video
    key = BING_KEY
    query = urllib.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    # print ':%s' % key
    # credentials = (':%s' % key).encode('base64')
    # print [credentials]
    # auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Bing/Search/' + search_type + '?Query=%27' + query + '%27&top=5&format=json'
    print url
    request = urllib2.Request(url)
    request.add_header('Authorization', 'Basic ' + base64.b64encode(':' + key))
    # request.add_header('Authorization', 'Basic ' + BING_KEY)
    request.add_header('User-Agent', user_agent)

    response = urllib2.urlopen(request)
    # request_opener = urllib2.build_opener()
    # response = request_opener.open(request)

    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    print result_list
    return result_list


def _bing_search(query):
    from urllib import quote_plus
    # Your base API URL
    url = "https://api.datamarket.azure.com/Bing/Search/v1/Web"

    # Query parameters. Don't try using urlencode here.
    # Don't ask why, but Bing needs the "$" in front of its parameters.
    # The '$top' parameter limits the number of search results.
    url += "?$format=json&$top=10&Query=%27{}%27".format(quote_plus(query))

    # You can get your primary account key at https://datamarket.azure.com/account
    r = requests.get(url, auth=("", BING_KEY))
    print r.content
    resp = json.loads(r.content)
    return (resp)

if __name__ == "__main__":
    main()
# /
#     _bing_search('django')

    # from py_bing_search import PyBingWebSearch
    # search_term = "Python Software Foundation"
    # bing_web = PyBingWebSearch(BING_KEY, search_term, web_only=False)
    # print bing_web.search(limit=50, format='json')
