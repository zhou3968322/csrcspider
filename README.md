# 证监会信息公开爬虫 说明

__请先阅读[scrapy爬虫工程示例](https://docs.scrapy.org/en/latest/intro/tutorial.html#)__

## 1.pycharm 配置

注意：这仅仅是方便debug采取的做法，这里我是用miniconda的环境

![pycharm配置debug示例](./docx/pycharm_debug_config.png)

也可以参看[pycharm scrapy debug](https://stackoverflow.com/questions/21788939/how-to-use-pycharm-to-debug-scrapy-projects)

## 2.启动 scrapy-splash 镜像

使用这个工具主要是为了动态加载javascript，安装和配置参看[splash文档](./docx/SPLASH_README.rst)

## 3.编写splash lua脚本

文档可以查看[splash文档](https://splash.readthedocs.io/en/stable/index.html)

使用时候有几个难点：

* splash:select中的参数是css选择器，常用的css选择器可以参看[w3c CSS选择器](https://www.w3school.com.cn/cssref/css_selectors.asp)

* splash:runjs, splash:evaljs, splash:jsfunc， 相关调试的时候可以使用chrome的console来调试测试

* 页面加载过程中看到的元素实际上在html中并不存在，例如\<iframe src\>类似的结构，这种类型的需要spash:go重定向到另一个url中再获取数据等。

关于splash的脚本使用测试用例中的test_splash_scripts.py 测试感受！！

着重说下第三点，可以使用测试用例中的test_get_page_document样例看到，当已经把整体页面都点击获取是获得的[debug网页文件](./tests/samples/document_debug.html)，当运行
```lua
local container = splash:select('#documentContainer') 
-- container为nil
```
必须先找到html中存在的iframe结构，运行:
```lua
local dataList = splash:select('#DataList') 
```
通过


