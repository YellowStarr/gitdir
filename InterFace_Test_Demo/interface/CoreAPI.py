#coding=utf-8

import requests

class CoreAPI:
    def __init__(self,url):
        self.baseurl=url

    def core_UploadToken(self,file,userId):
        u'''创建和上传歌曲和图片的接口
            Method:post
            @param: file:{etag,filename} array,userId:number
            @return:
                data{token,key,expired},msg,status
        '''
        url = self.baseurl+'/api/storage/audio/uploadToken'
        json={'file':file,'useId':userId}
        r = requests.post(url, json=json)
        response = r.json()
        return response

    def core_Compose(self,token,type,title,audios,images,latitude,longitude,lyric,userid,description='',isPublic=True):
        u'''创建和上传歌曲和图片的接口
            Method:post
            :param: type:string
            :param: audios:array <object>[{key,duration,lyric}]
            :param:isPublic:boolean 吐槽才有
            @return:
                data{id},msg,status
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        if type == 'rap':
            url = self.baseurl + '/api/audio/rap/compose'
            jsons = {'title': title, 'audios': audios, 'images': images, 'latitude': latitude, 'longitude': longitude,
                    'lyric': lyric, 'description': description, 'userId':userid}

        elif type == 'complaint':
            url = self.baseurl + '/api/audio/complaint/compose'
            jsons = {'title': title, 'audios': audios, 'images': images, 'latitude': latitude, 'longitude': longitude,
                    'lyric': lyric, 'userId': userid, 'description':description}
        r = requests.post(url, json=jsons, headers=headers)
        response = r.json()
        return response

    def core_Comment_V1(self, id, page=1, size=10, sort=1):
        u'''作品评论
            Method:get
            @param: 歌曲id，sort 0 热门 1 最新,page,size
            @return:
                data{comments:[{userName,id,userId,commentContent,commentTime,commentStatus 99 已删除 0 正常}]},msg,status
        '''
        url = self.baseurl + '/api/comment/v1'
        params={'id': id, 'page': page, 'size': size, 'sort':sort}
        r = requests.get(url, params=params)
        response = r.json()
        return response

    def core_RecommendLyrics(self,size=10):
        u'''推荐歌词
            @Method:get
            @return:
                data{lyrics:[{lyricsContent,id,lyricsName,userName}]},mes,status
        '''
        url = self.baseurl + '/api/recommendLyrics'
        r = requests.get(url, params={'size': size})
        response = r.json()
        return response

    def core_Listen(self,id,token):
        u'''歌曲收听
            @Method:post
            @param: 歌曲id，token
            @return:
                data{count},status,msg
        '''
        url = self.baseurl + '/api/user/listen'
        r = requests.post(url,json={'id':id,'token':token})
        response = r.json()
        return response

    def core_SongDetail_V1(self,id):
        u'''歌曲详情
            @Method:get
            @param: 歌曲id
            @return:
                data:{songs:[
                      images,songName,collectCount,songUrl,userName,praiseCount,fanCount,portrait,
                      listenCount,id,shareHtmlUrl,description,creatTime,songDuration,commentCount,category,lyric
                      ]},msg,status
        '''
        url = self.baseurl + '/api/songDetail/v1'
        r = requests.get(url,params={'id':id})
        response = r.json()
        return response

    def core_JoinBattle(self,token, id, des, lyric, autios, latitude, longitude):
        u'''加入battle
            @Method:post
            @param: battle id
            @return:
                msg,status
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + ' /api/audio/battle/join'
        json={'id':id,'description':des,'lyric':lyric,'autios':autios,'latitude':latitude,'longitude':longitude}
        r = requests.post(url, json=json, headers=headers)
        response = r.json()
        return response

    def core_CreateMedley(self, title, images, maxcount, autios, longitude):
        u'''创建串烧
            @Method:post
            @param: audios:[{"key":"", "duration": "", "lyric":""}]
            :param images:array
            @return:
                data{id}msg,status
        '''
        url = self.baseurl + '/api/audio/createMedley'
        json={'title':title,'images':images,'maxCount':maxcount,'autios':autios,'longitude':longitude}
        r = requests.post(url,json=json)
        response = r.json()
        return response

    def core_Comment_Praise(self, token, id, idtype):
        u'''评论点赞
            @Method:post
            @param: id:string 评论/子评论id
            @return:
                data{count}msg,status
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/comment/praise'
        json = {'id': id, 'idType': idtype}
        r = requests.post(url, json=json, headers=headers)
        response = r.json()
        return response

    def core_Comment_CancelPraise(self, token, id, idtype):
        u'''评论取消点赞
            @Method:post
            @param: id:string 评论/子评论id
            @return:
                data{count}msg,status
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/comment/praise/cancle'
        json = {'idType': idtype, 'id': id}
        r = requests.post(url, json=json, headers=headers)
        response = r.json()
        return response


    def core_Get_SubComment(self,songCommentId,size=10,page=1, sort='hot'):
        u'''评论回复详情
            @Method:get
            @param: id:string 评论/子评论id
            @return:
                data{subComments:[{hasPraise,commentContent,id,commentPraiseCount,commentTime,
                    commentUser 评论用户,calledUser 被回复的用户,commentAsset}]}msg,status
        '''
        url = self.baseurl + '/api/subComments'
        param = {'size': size, 'songCommentId': songCommentId, 'page':page, 'sort':sort}
        r = requests.get(url, params=param)
        response = r.json()
        return response


    def core_Post_SubComment(self,token,songCommentId,toCommentId,content,toUserId,toUserName,commentAsset=[]):
        u'''评论评论
            @Method:get
            @param: songCommentId:string 评论/子评论id
            @param: toCommentId:string 被评论的子评论id
            @param: content:string
            @param: toUserId:string 被评论子评论的用户id
            @param: toUserName:string 被评论子评论的用户名
            @param: commentAsset:array [{resourceType:1|2,url}] 评论/子评论id

            @return:
                data{subComments:[{hasPraise,commentContent,id,commentPraiseCount,commentTime,
                    commentUser 评论用户,calledUser 被回复的用户,commentAsset}]}msg,status
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/subComments'
        param = {'toCommentId': toCommentId, 'songCommentId': songCommentId, 'content':content, 'toUserId':toUserId,
                 'toUserName':toUserName, 'commentAsset':commentAsset}
        r = requests.post(url, json=param, headers=headers)
        response = r.json()
        return response

    def core_Del_SubComment(self,token,commentid):
        u'''评论回复详情
            @Method:get
            @param: id:string 评论/子评论id
            @return:
                data{subComments:[{hasPraise,commentContent,id,commentPraiseCount,commentTime,
                    commentUser 评论用户,calledUser 被回复的用户,commentAsset}]}msg,status
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/subComments'
        param = {'commentId':commentid}
        r = requests.delete(url, params=param, headers=headers)
        response = r.json()
        return response


    def core_Hot_Music(self,type,size=10,page=1):
        u'''获取热门歌曲信息
        :type raps|medleys|complaints|battles
        @return
        {data:{song:[{fanCount,maxCount,createTime,personTimes,userId,portrait,commentCount,
            songName,id,image,currCount,lyric,listenCount,praiseCount,status,userName,shareCount,
            collectCount,description}],msg,status}
        '''
        url = self.baseurl + '/api/hot/' + type
        param = {'size': size, 'page': page}
        r = requests.get(url, params=param)
        response = r.json()
        return response

    def core_Del_Music(self, token, type, id):
        u'''删除我的歌曲
            :type raps|medleys|complaints|battles
            @return
            {data,msg,status}
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/user/'+type+'/delete'
        param = {'id': id}
        r = requests.post(url, json=param, headers=headers)
        response = r.json()
        return response

    def core_JoinMedley(self, token, audios, songId):
        u'''加入串烧'''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/audio/joinMedley'
        param = {'audios': audios,'songId':songId}
        r = requests.post(url, json=param, headers=headers)
        response = r.json()
        return response

    """def core_getMedley(self,size=10,page=1):
        u'''获取串烧
        :param status 0:获取最新可加入(串烧中)的串烧列表 | status为1:获取热门串烧
        :param sort:综合规则发现0, 非综合规则 latest 1 ,hot 2
        @return :
            {data:[songs:{portrait,userName,image,collectCount,category,listenCount,praiseCount,
                songName,currCount,commentCount,id,des}]},msg,status
        '''
        url = self.baseurl + '/api/getMedleys'
        param = {'size':size, 'page':page}
        r = requests.post(url, params=param)
        response = r.json()
        return response"""

    def core_songComment(self,token, id, content, resource=[]):
        u'''评论歌曲
            @Method:post
            @param: id:string 歌曲id
            @return:
                data{id 评论id},msg,status 0 成功 1 失败
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/song/comment'
        param = {'id': id, 'content': content, 'resource':resource}
        r = requests.post(url, json=param, headers=headers)
        response = r.json()
        return response

    def core_Del_Comment(self, token, commentid):
        u'''删除评论
            @Method:post
            @param: id:string 评论ID
            @return:
                data{id 评论id},msg,status 0 成功 1 失败
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/song/comment/delete'
        param = {'id': commentid}
        r = requests.post(url, json=param, headers=headers)
        response = r.json()
        return response

    def core_Praise(self, token, id):
        u'''点赞
            :param id:number 歌曲id
            @:return data:{count}
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/user/praise'
        params = {'id':id}
        r = requests.post(url, json=params, headers=headers)
        response = r.json()
        return response

    def core_cancelPraise(self, token, id):
        u'''点赞
            :param id:number 歌曲id
            @:return data:{count}
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/user/cancelPraise'
        params = {'id':id}
        r = requests.post(url, json=params, headers=headers)
        response = r.json()
        return response

    def core_Collect(self, token, id):
        u'''收藏
            :param id:number 歌曲id
            @:return data:{[songs:{category,collectCount,commentCount,createTime,description...}]}
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/user/collect'
        params = {'id':id}
        r = requests.post(url, json=params, headers=headers)
        response = r.json()
        return response

    def core_cancelCollect(self, token, id):
        u'''取消收藏
            :param id:number 歌曲id
            @:return data:{[songs:{category,collectCount,commentCount,createTime,description...}]}
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/user/cancelCollect'
        params = {'id':id}
        r = requests.post(url, json=params, headers=headers)
        response = r.json()
        return response

    def core_MyCollection(self,token,page=1,size=100):
        u'''我的收藏列表

            @:return data:{[songs:{category,collectCount,commentCount,createTime,description...}]}
        '''
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/user/collectList'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        response = r.json()
        return response

    def core_Rank(self,page=1,size=50):
        u'''排行榜

            @:return data:{[songs:{category,collectCount,commentCount,createTime,description...}]}
        '''
        url = self.baseurl + '/api/song/ranking'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        response = r.json()
        return response


