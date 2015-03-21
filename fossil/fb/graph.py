# -*- coding: utf-8 -*-
import requests
import json


class Graph:
    graph_api_url = 'https://graph.facebook.com/v2.2/'

    def __init__(self, token):
        self._token = token

    def _url(self, path):
        return self.graph_api_url + path

    def feed_post(self, path, data):
        url = self._url(path)
        data['access_token'] = self._token
        response = requests.post(url, data=data)
        return response.json()

    def feed_get(self, path, params):
        url = self._url(path)
        params['access_token'] = self._token
        response = requests.get(url, params=params)
        return response.json()

    def get_groups(self, group_name=None):
        url = self._url('/me/groups')
        result = []

        while True:
            response = requests.get(url, params={
                'access_token': self._token,
            })
            if 'error' in response.content:
                raise ValueError

            data = response.json()
            if len(data['data']) == 0:
                break

            result.extend(data['data'])
            url = data['paging']['next']

        if group_name:
            return (item for item in result if item['name'] == group_name).next()
        return json.loads(result)

    def next_pagenation(self, link):
        response = requests.get(link)
        return response.json()
