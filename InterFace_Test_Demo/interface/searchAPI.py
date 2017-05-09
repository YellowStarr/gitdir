#coding=utf-8

import requests

class SearchAPI:
    def __init__(self,url):
        self.baseurl=url

    def search_Song(self, keyword, page=1, size=10):
        u'''创建和上传歌曲和图片的接口
            Method:post
            @param: file:{etag,filename} array,userId:number
            @return:
                data{token,key,expired},msg,status
        '''
        url = self.baseurl+'/api/search/song'
        params={'keyword': keyword, 'page': page, 'size': size}
        r = requests.get(url, params=params)
        response = r.json()
        return response

    def search_User(self, keyword, page=1, size=10):
        u'''创建和上传歌曲和图片的接口
            Method:post
            @param: file:{etag,filename} array,userId:number
            @return:
                data{token,key,expired},msg,status
        '''
        url = self.baseurl+'/api/search/user'
        params={'keyword': keyword, 'page': page, 'size': size}
        r = requests.get(url, params=params)
        response = r.json()
        return response

    def search_Hot(self, page=1, size=10):
        u'''创建和上传歌曲和图片的接口
            Method:post
            @param: file:{etag,filename} array,userId:number
            @return:
                data{token,key,expired},msg,status
        '''
        url = self.baseurl+'/api/search/hot/keyword'
        params={'page': page, 'size': size}
        r = requests.get(url, params=params)
        response = r.json()
        return response