# 买猪计划(buy_pig_plan) Python版
用Python写的『电话攻击，电话轰炸，电话炸弹』，其攻击流程参考了『[aqiongbei/buy_pig_plan](https://github.com/aqiongbei/buy_pig_plan)』
> 为什么开发这个东西?
>
> 为了对付欠钱不还，还拉黑我的老赖。

## 安装搭建
> 1、安装依赖库
>- pip install sqlalchemy
>- pip install colorama
>- pip install selenium
>- pip install cx_Oracle (需要安装oracle客户端,自行百度或参考[帮助](https://oracle.github.io/odpi/doc/installation.html#linux))

> 2、安装谷歌浏览器`已经装了谷歌浏览器可以跳过这步`
>- windows 自己找
>- linux [下载地址](https://www.chrome64bit.com/index.php/google-chrome-64-bit-for-linux)
>- OS X [下载地址](https://www.chrome64bit.com/index.php/google-chrome-64-bit-for-mac)

> 3、下载chromedriver
>- [下载地址](http://chromedriver.storage.googleapis.com/index.html)
>- 注意: 根据自己对应的谷歌浏览器版本下载,比较旧的版本可以参考[对照表](https://www.cnblogs.com/liyanqi/p/7826305.html)

> 4、将下载后的`chromedriver`放置到`Chrome`浏览器所在目录，并将该目录添加至`环境变量`
>
> 例如：`Chrome`目录为 `/opt/google/chrome/`
>
> mv chromedriver /opt/google/chrome/
>
> vim ~/.bash_profile
>
> export PATH=$PATH:/opt/google/chrome/
>
> source ~/.bash_profile

> 5、如果不采用Oracle读取已采集的网站，也可以先自行采集网站放到配置文件中。如果采用这种方法`cx_Oracle`可以不用安装。

## 配置
参考config.py

## 运行
电话攻击: python mySelenium.py

采集网站: python lixianbao/main.py

## 其他说明
### 关于攻击流程
原理是利用百度离线宝、百度商桥，在一些网站留言后，那个网站的销售会根据留言信息或电话号码，进行网络电话回拨，从而达到攻击的目的。我们利用网页自动化测试，在页面上的html元素填入我们的信息，并发送，就可以完成攻击。由于部分网站因为被关闭，或取消了百度业务，或隐藏了百度商桥的元素，另外攻击频率不能太高，成功率大概在5次-15次/100个网站。
### 关于数据
有很多网友找我问网站数据的问题，首先我的数据库不能公开给你们。网站数据可以在该库的SQL文件找到，如果不安装数据库，可以把SQL文件的网站信息先提取出来，然后放到配置文件，然后改你自己的代码，将mySelenium.py里面get_web_infos，改成读你的配置文件网站信息。
### 关于BUG
目前有两个已知BUG：
1、访问网站假如弹出信息框
2、访问网站假如出现重定向
都会影响Selenium的操作，这个你们可以自行修复。
