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

> 2、安装谷歌浏览器`已经装了谷歌浏览器可以跳过这步`
>- windows 自己找
>- linux [下载地址](https://www.chrome64bit.com/index.php/google-chrome-64-bit-for-linux)
>- OS X [下载地址](https://www.chrome64bit.com/index.php/google-chrome-64-bit-for-mac)

> 3、下载chromedriver
>- [下载地址](http://chromedriver.storage.googleapis.com/index.html)
>- 注意: 根据自己对应的谷歌浏览器版本下载,比较旧的版本可以参考[对照表](https://www.cnblogs.com/liyanqi/p/7826305.html)

> 将下载后的`chromedriver`放置到`Chrome`浏览器所在目录，并将该目录添加至`环境变量`

## 配置
参考config.py

## 运行
电话攻击: python mySelenium.py

采集网站: python lixianbao/main.py