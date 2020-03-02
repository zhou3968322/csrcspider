# -*- coding: utf-8 -*-

# Scrapy settings for python123demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random, os

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

BOT_NAME = 'csrcspider'

SPIDER_MODULES = ['csrc.spiders']
NEWSPIDER_MODULE = 'csrc.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
user_agent_list = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]

USER_AGENT = random.choice(user_agent_list)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'csrc.middlewares.CsrcSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}


DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'csrc.pipelines.CrawlItemFilterPipeline': 100,
    'csrc.pipelines.FileItemFilterPipeline': 200,
    'csrc.pipelines.CsrcFilesPipeline': 300,
    'csrc.pipelines.FileMetaItemWriterPipeline': 400,
    'csrc.pipelines.CrawlMetaItemWriterPipeline': 500
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


"""
日志配置
"""

LOG_STDOUT = True

"""
SPLASH配置
"""

SPLASH_URL = 'http://127.0.0.1:8050'

"""
文件的日期过滤
"""
if "RELEASE_MIN_DATE" in os.environ:
    RELEASE_MIN_DATE = os.environ["RELEASE_MIN_DATE"]
else:
    RELEASE_MIN_DATE = "2019-10-31 23:59:59"

if "RELEASE_MAX_DATE" in os.environ:
    RELEASE_MAX_DATE = os.environ["RELEASE_MAX_DATE"]
else:
    RELEASE_MAX_DATE = "2020-12-31 23:59:59"

"""
数据的存储地方
"""

if "DATA_DIR" in os.environ:
    DATA_DIR = os.environ["DATA_DIR"]
else:
    DATA_DIR = os.path.join(PROJECT_ROOT_PATH, 'data')

"""
文件Meta的保存位置
"""
META_DIR = os.path.join(DATA_DIR, 'meta')
if not os.path.isdir(META_DIR):
    os.mkdir(META_DIR)
FILE_MD5_SUFFIX = "_file_meta_md5.txt"
FILE_META_SUFFIX = "_file_meta.txt"
CRAWL_MD5_SUFFIX = "_crawl_meta_md5.txt"
CRAWL_META_SUFFIX = "_crawl_meta.txt"


"""
文件保存目录
"""

FILES_STORE = os.path.join(DATA_DIR, 'files')
if not os.path.isdir(FILES_STORE):
    os.mkdir(FILES_STORE)
FILES_URLS_FIELD = 'file_url'

