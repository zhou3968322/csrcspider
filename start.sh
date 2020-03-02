#!/usr/bin/env bash
cd `dirname $0`
nohup scrapy crawl csrc_spider -s JOBDIR=jobs/csrc_spider-1 &
