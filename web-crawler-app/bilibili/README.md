## bilibili-crawler项目代码说明

这个git目录下存档了当前正在使用的b站爬虫的相关脚本，所有封装的api接口均是从bilibili的安卓APP（版本：2016-01-15 Android 4.10.5）破解的，若需要更加详细的说明，可以尝试使用mitmptoxy工具抓包后查看。
***
### bilibili.py 和 bilimember.py
bilibili.py 和 bilimember.py 两个文件封装了已经破解的b站相关api接口，下面简要说明其使用方式和参数意义。

首先需要将这两个文件import进来：
```python
import bilibili
import bilimember
```

* **bilibili.py**
	**sign(base_url)**：接受一条url参数，返回一个*str*类型的的sign。注意该版本的sign对应的是安卓版本的api.bilibili.com的api接口，对于B站新版的app.bilibili.com并不适用。
	**get_author_by_avid(avid)**：接受一个视频id参数avid，返回该视频的作者（*str*类型）
	**get_video_info(avid)**：接受一个视频id参数avid，返回这个视频的详细信息（*dict*类型）。注意，这个函数中同时还调用了 get_video_stat(avid), get_video_comment(avid), get_video_comment(avid), get_video_reply(avid)等函数，以将视频信息补充全面。
	**get_video_comment(avid)**：接受一个视频id参数avid，返回该视频的弹幕（*str*类型）。由于访问权限限制，只能获取最多1500条弹幕。
	**get_video_stat(avid)**：接受一个视频id参数avid，返回该视频的统计信息（*dict*类型），如点赞数，分享量等等。
	**get_video_reply(avid)**：接受一个视频id参数avid，返回该视频的热门回复和全部回复的两个信息（*tuple(dict, dict)*类型）。
	**get_video_recommend(avid)**：接受一个视频id参数avid，返回该视频的相关推荐视频（*dict*类型）。
	**bilibili_search(keyword, duration)**：接受一个关键字keyword（*str*类型，可以是中文）和一个时长duration（*int*类型，分别为{0: 全部时长，1:1~10分钟，2:10~30分钟}）参数

* **bilimember.py**
	**get_member_info(mid)**：接受一个用户id参数mid，返回该用户的详细信息，包括名牌，粉丝，收藏夹，已上传视频等信息（*dict*类型）。注意，这个函数也调用了 update_favourite(), update_archive(), update_card(), update_bangumi() 四个函数。
	**get_member_info_lite(mid)**：与 get_member_info() 函数的实现基本一致，不过过滤掉了收藏夹中视频的多余信息，仅保留了收藏夹视频的avid号和duration时长两个参数。
	**get_member_favourite(mid)**：接受一个用户id参数mid，返回该用户的收藏夹详细信息（*dict*类型）。 
	**update_card(info, mid)**：在 get_member_info 中配合使用，更新用户的名牌信息。
	**update_fans(info, mid)**：在 get_member_info 中配合使用，更新用户的粉丝（follower）信息。
	**update_favourite(info, mid)**：在 get_member_info 中配合使用，更新用户的收藏夹信息。
	**update_archive(info, mid)**：在 get_member_info 中配合使用，更新用户的上传视频信息。

*以上 `update_*` 相关代码经过简单改动也可以单独使用。*

***

### download_video.py
download_video.py 实现的功能是：在 MongoDB 数据库（需要自己实现一个RESTful的MongoDB　api接口，或者参考官方文档直接从本机拿）中拿到用户的收藏夹信息，筛选时长在 6 分钟以下的视频并下载为mp4格式的文件。

* Constant 中的参数意义：
	**memberSt**：需要遍历的起始用户的id。
	**memberEnd**：需要遍历的终止用户的id。
	**processNum**：多进程进程池的大小。
	**threshold**：所需的时长，目前设置的 361s，对应6分钟。
	**DIR**：下载文件的保存路径。
	**TIMEOUT**：http请求的超时时间。
	**VERIFY_STATUS**：requests请求中的验证要求，默认为 False，在系统要求验证时可以设置为True。

***

### 其他一些脚本文件：

* verify_connection.py：用于在服务器上检测爬虫关键网站 bilibili.com, api.bilibili.com, app.bilibili.com 的网络状态，其结果是输出访问成功 200，被禁封无权限 403 等网络请求状态。
