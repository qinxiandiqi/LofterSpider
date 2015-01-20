#Sexy

Python 爬虫

本项目依赖Python的BeautifulSoup4第三方库，使用本项目需要先安装BeautifulSoup4。

步骤一 安装依赖库：
安装BeautifulSoup4：
1.Debain或Ubuntu可以通过系统软件包管理安装
	$sudo apt-get install Python-bs4
2.使用easy_install或者pip安装：
	$ sudo easy_install beautifulsoup4
	或$ sudo pip install beautifulsoup4

easy_install和pip是Python的发行包管理工具，同样需要先安装才能使用，这里介绍easy_install的安装方法：
1.Mac OS X 系统可以在终端执行以下命令：
	curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python
2.Linux系统可以执行以下命令：
	wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python
3.Window系统:
	下载ez_setup.py文件然后运行，链接地址：https://bootstrap.pypa.io/ez_setup.py

步骤二 运行：
确保BeautifulSoup4安装完毕后就可以运行sexy.py文件。
1.不带参数运行：直接运行sexy.py，使用默认配置参数。
2.可用参数：
	-s 或 --startpage ：起始扫描页面，默认值为1，从第一页开始扫描
	-e 或 --endpage ：最后扫描页面，默认值为65589。
	-d 或 --dir ：相对当前文件，下载图片保存文件，默认为images文件夹
	-m 或 --max ：获取页面失败后最大重试次数，默认为3
例子：Sexy$ ./sexy.py -s 10 -e 12 -d cache -m 3 
	表示从第10页开始扫描到第12页，图片保存文件夹为cache，获取页面失败最多可以尝试3次。
3.运行期间可以随时按回车键退出程序。
