# KeywordReplyMiddleware
1.安装

```pip install git+https://github.com/QQ-War/efb-keyword-reply.git```

2.注册到middleware

```
master_channel: blueset.telegram
slave_channels:
- honus.CuteCatiHttp
middlewares:
- 其他middleware
- QQ_War.keyword_reply
```

3.修改配置文件config.yaml，放到QQ_War.keyword_reply目录，如果关键字或者回复词有特殊字符，需要用双引号包起来，不然不用引号，关键词支持正则匹配。

```
keywords:
  关键字1: 回复词1
  关键字2: 回复词2
  ...
```
