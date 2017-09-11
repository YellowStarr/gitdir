# -*-coding:utf-8 -*-
class errorCodeConst:

    @property
    def ARGS_NUM_LOST(self):
        """
        列表参数个数错误(一般是参数和实际需要参数个数不一致)
        :return:
        """
        return 100101

    @property
    def ARGS_TYPE_ERROR(self):
        """
        参数类型错误(参数类型和实际需要的参数类型不一致,比如数字和字符)
        :return:
        """
        return 100102

    @property
    def   ARGS_VALUE_ERROR(self):
        """
        参数取值错误(一般用于有参数列表的值,比如定义了三个值,但是传递的是之外的值)
        :return:
        """
        return 100103

    @property
    def ARGS_JSON_ERROR(self):
        """
        参数json反序列化错误(json格式存在问题)
        :return:
        """
        return 100104

    @property
    def ARGS_NULL(self):
        """
        参数为空
        :return:
        """
        return 100105

    @property
    def HEIPAMESSAGE_LOST(self):
        """
        HttpHeader中缺少HeipaAppMessage
        :return:
        """
        return 100106

    @property
    def HEIPAMESSAGE_LACK_ARG(self):
        """
        HttpHeader中HeipaAppMessage值不完整
        :return:
        """
        return 100107

    @property
    def ARG_LENGTH_ERROR(self):
        """
         参数长度不对
        :return:
        """
        return 100108

    @property
    def ACCESS_TOKEN_LOST(self):
        """
         缺少access token(没有access token)
        :return:
        """
        return 100201

    @property
    def ACCESS_TOKEN_INVALID(self):
        """
        access token无效(access token过期)
        :return:
        """
        return 100202

    @property
    def WITHOUT_USERID(self):
        """
        需要重新登录(token中只有deviceId没有userId)
        :return:
        """
        return 100203

    @property
    def CLIENT_TYPE_ERROR(self):
        """
        终端类型错误(终端不在登录的列表中,比如ios和安卓之外的)
        :return:
        """
        return 100204

    @property
    def CLIENT_ERROR(self):
        """
        终端类型错误(与上次申请token时的终端不一致)
        :return:
        """
        return 100205

    @property
    def CLIENT_ID_ERROR(self):
        """
        终端唯一码错误(与上次申请token时的终端唯一码不一致)
        :return:
        """
        return 100206

    @property
    def REFRESH_TOKEN_LOST(self):
        """
        缺少 refresh token(没有 refresh token)
        :return:
        """
        return 100207

    @property
    def REFRESH_TOKEN_INVALID(self):
        """
        refresh token无效(refresh token过期)
        :return:
        """
        return 100208

    @property
    def USER_HAS_EXISTED(self):
        """
        注册用户已存在(已经注册过的用户,不可以再次注册)
        :return:
        """
        return 100401

    @property
    def USERNAME_UNEXIST(self):
        """
         用户名不存在(无效的用户名,没有注册过)
        :return:
        """
        return 100402

    @property
    def PASSWORD_NULL(self):
        """
        用户账号或密码为空(账号或者密码有一个为空或者全为空)
        :return:
        """
        return 100403

    @property
    def PASSWORD_ERROR(self):
        """
        账号或密码错误(账号或密码错误,一般指的是密码错误)
        :return:
        """
        return 100404

    @property
    def USER_STATE_ERROR(self):
        """
        用户状态异常(比如用户被封之类的状态异常导致的无法登录)
        :return:
        """
        return 100405

    @property
    def ACCONT_ALREADY_BANDING_PHONE(self):
        """
        用户已经绑定别的手机号
        :return:
        """
        return 100406

    @property
    def ACCOUNT_ALREADY_BANDING_THIRD(self):
        """
        用户已经绑定同一个平台的第三方账号
        :return:
        """
        return 100407

    @property
    def USER_INVALID(self):
        """
        无法找到用户或者用户无效
        :return:
        """
        return 100408

    @property
    def USER_EXIST(self):
        """
        用户已经存在
        :return:
        """
        return 100409

    @property
    def UNMATCHING_MACHINEID_TO_DEVICEID(self):
        """
        机器码与设备号对应错误（设备号要使用注册时服务器返回的）
        :return:
        """
        return 100410

    @property
    def ACCONT_ALREADY_BANDING_PHONE(self):
        """
        用户已经绑定别的手机号
        :return:
        """
        return 100406

    @property
    def API_INVALID(self):
        """
        不存在的API(无效的api,无定义或者无效)
        :return:
        """
        return 100501

    @property
    def DATABASE_CONNECTION_ERROR(self):
        """
        数据库连接错误(数据库连接错误,一般是数据库配置错误)
        :return:
        """
        return 200101

    @property
    def DATABASE_OPERATION_ERROR(self):
        """
        数据库操作失败(数据库处理过程错误)
        :return:
        """
        return 200102

    @property
    def AUTH_ERROR(self):
        """
        无权限操作
        :return:
        """
        return 200201

    @property
    def DATABASE_ARG_NULL(self):
        """
        参数为空
        :return:
        """
        return 200301

    @property
    def SENDING_MESSAGE_ERROR(self):
        """
        发送短信错误
        :return:
        """
        return 200401

    @property
    def ENCODING_ERROR(self):
        """
        加密错误
        :return:
        """
        return 200502

    @property
    def DECODING_ERROR(self):
        """
        解密错误
        :return:
        """
        return 200502

    @property
    def USER_INFO_ERROR(self):
        """
        用户信息异常
        :return:
        """
        return 200601

    @property
    def ALREADY_IN_BLACKLIST(self):
        """
        拉黑不能关注
        :return:
        """
        return 200602

    @property
    def CAN_NOT_BLACKLIST(self):
        """
        关注不能拉黑
        :return:
        """
        return 200603

    @property
    def RECORD_UNEXIST(self):
        """
        记录不存在
        :return:
        """
        return 200701

    @property
    def STATE_ERROR(self):
        """
        状态不正确
        :return:
        """
        return 200702

    @property
    def ALREADY_PRAISED(self):
        """
        不可以重复点赞
        :return:
        """
        return 200703

    @property
    def ALREADY_COLLECTED(self):
        """
        不可以重复收藏
        :return:
        """
        return 200704

    @property
    def CAN_NOT_PRAISE_SELF(self):
        """
        不可以点赞自己的作品
        :return:
        """
        return 200705

    @property
    def CAN_NOT_COLLECT_SELF(self):
        """
        不可以收藏自己的作品
        :return:
        """
        return 200706

    @property
    def UNKNOWN_ERROR(self):
        """
        未知错误
        :return:
        """
        return 209901


