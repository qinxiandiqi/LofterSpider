#Sexy

Python 爬虫

本项目依赖Python的BeautifulSoup4第三方库，使用本项目需要先安装BeautifulSoup4。

步骤一 安装依赖库：<br>
安装BeautifulSoup4：<br>
1.Debain或Ubuntu可以通过系统软件包管理安装<br>
	$sudo apt-get install Python-bs4 <br>
2.使用easy_install或者pip安装：<br>
	$ sudo easy_install beautifulsoup4
	或$ sudo pip install beautifulsoup4

easy_install和pip是Python的发行包管理工具，同样需要先安装才能使用，这里介绍easy_install的安装方法：<br>
1.Mac OS X 系统可以在终端执行以下命令：<br>
	curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python <br>
2.Linux系统可以执行以下命令：<br>
	wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python <br>
3.Window系统:<br>
	下载[ez_setup.py](https://bootstrap.pypa.io/ez_setup.py)并运行 <br>

步骤二 运行：<br>
确保BeautifulSoup4安装完毕后就可以运行sexy.py文件。<br>
1.不带参数运行：直接运行sexy.py，使用默认配置参数。<br>
2.可用参数：<br>
	-s 或 --startpage ：起始扫描页面，默认值为1，从第一页开始扫描<br>
	-e 或 --endpage ：最后扫描页面，默认值为65589。<br>
	-d 或 --dir ：相对当前文件，下载图片保存文件，默认为sexy_images文件夹<br>
	-m 或 --max ：获取页面失败后最大重试次数，默认为3<br>
	-n 或 --new ：只获取最新更新的图片，强制设置起始扫描页为1，获取完毕后自动退出<br>
例子：Sexy$ ./sexy.py -s 10 -e 12 -d cache -m 3 <br>
	表示从第10页开始扫描到第12页，图片保存文件夹为cache，获取页面失败最多可以尝试3次。<br>
3.运行期间可以随时按回车键退出程序。<br>

测试环境：<br>
	python 2.7 测试通过<br>
