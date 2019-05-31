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