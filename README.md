# KeywordReplyMiddleware
1.根据配置文件里面的关键词进行回复。关键词和回复词作为一一对应关系，放到配置文件里面。
会同时给主端和从端分别发送一条信息，以keyword系统用户作为发信人。
2.根据配置文件里面的关键词，屏蔽某些信息（全局性的）。

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
keywordsrepeattime: 5
#单位分钟，不设置默认为1分钟
keywords_block:
  - 屏蔽关键词1
  - 屏蔽关键词2
  ...
```

4.其他注意：
因为关键词使用的正则匹配，如果关键词有[]或者{}要特别小心。
