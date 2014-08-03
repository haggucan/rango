__author__ = 'hakanyildiz'
import json
import urllib, urllib2
import sys


def search_query(search_terms):
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = "Web"

    resultset_per_page = 10
    offset = 0

    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        resultset_per_page,
        offset,
        query)

    username = ""
    api_key = "81y4thysJ5zvQPxvDlX2OWEFJZLh5bFihqu899wn/hU"

    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, search_url, username, api_key)

    results = []

    try:
        handler = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        response = urllib2.urlopen(search_url).read()

        json_response = json.loads(response)
        for r in json_response["d"]["results"]:
            results.append({
                'title': r['Title'],
                'link': r['Url'],
                'summary': r['Description']})

    except urllib2.URLError, e:
        print "ERROR  ", e

    return results


def test(search_this):
    query_result = search_query(search_this)

    for r in query_result:
        print r["title"].encode('utf-8').strip() + "\n"
        print r["link"].encode('utf-8').strip() + "\n"
        print r["summary"].encode('utf-8').strip() + "\n"
        print "\n"


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) < 2:
        print "usage : python bing_search.py <search_param>"
    else:
        test(arguments[1])


