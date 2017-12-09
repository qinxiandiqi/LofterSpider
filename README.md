# LofterSpider

## Lofter爬虫

本项目可以爬去Lofter图片，依赖Python的BeautifulSoup4第三方库，使用本项目需要先安装BeautifulSoup4。

### 安装依赖库：  
安装BeautifulSoup4：  
* Debain或Ubuntu可以通过系统软件包管理安装：  
``` bash
$ sudo apt-get install Python-bs4 
```

* 使用easy_install安装：  
``` bash
$ sudo easy_install beautifulsoup4
```

* 使用pip安装：
``` bash
$ sudo pip install beautifulsoup4
```

#### easy_install和pip是Python的发行包管理工具，同样需要先安装才能使用，这里介绍easy_install的安装方法：  
1. Mac OS X 系统可以在终端执行以下命令： 
```bash 
curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python   
```
2. Linux系统可以执行以下命令：  
```bash
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python   
```
3. Window系统:  
下载[ez_setup.py](https://bootstrap.pypa.io/ez_setup.py)并运行   

### 运行：  
运行lofter.py文件爬取网站一：  
1. 不带参数运行：直接运行lofter.py，使用默认配置参数。  
2. 可用参数：  
* -s 或 --startpage ：起始扫描页面，默认值为1，从第一页开始扫描  
* -e 或 --endpage ：最后扫描页面，默认值为65589。  
* -d 或 --dir ：相对当前文件，下载图片保存位置，默认为images文件夹  
* -m 或 --max ：获取页面失败后最大重试次数，默认为3  
* -n 或 --new ：只获取最新更新的图片，强制设置起始扫描页为1，获取完毕后自动退出  
* --domain ：爬取目标lofter的二级域名，不输入则使用默认二级域名
* --groupByDate ：是否将爬取图片按照作者发布日期归类，默认按发布日期归类

例子，从第10页开始扫描到第12页，图片保存文件夹为cache，获取页面失败最多可以尝试3次：
```bash
LofterSpider$ ./lofter.py -s 10 -e 12 -d cache -m 3   
```
3. 运行期间可以随时按回车键退出程序。  

### ~~运行atlas.py文件爬取网站二：~~  **已失效**  
1. 不带参数运行：直接运行atlas.py，使用默认配置参数，从主页开始爬取。  
2. 可用参数：  
* -d 或 --dir ：相对当前文件，下载图片保存位置，默认为atlas_images文件夹  
* -m 或 --max ：获取页面失败后最大重试次数，默认为3  
* -v 或 --view ：查看当前已知标签和标签id  
* -t 或 --tag ：爬取指定标签名的图片，同时提供标签id时，本标签无效  
* -i 或 --id ：爬取指定标签id的图片  
* -l 或 --last ：是否从上次退出的地方继续爬取，默认为false  
3. 运行过程中可以随时按Ctrl+C退出，退出时如果还有新发现标签没有归类，归类后自动退出。  
4. setting文件中为已归类标签和最后抓取位置缓存，请勿删除。  

### 测试环境：  
python 2.7 测试通过  

## License

    Copyright 2015 Jianan - qinxiandiqi@foxmail.com

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
