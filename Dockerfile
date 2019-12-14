FROM python:3.7-alpine
LABEL Description="用于scrapy框架" Author="wuhao" Version="1.0"
# 安装gcc编译环境
RUN apk add --no-cache gcc musl-dev

RUN apk add --no-cache libxml2-dev libxslt-dev zlib-dev libffi-dev openssl-dev &&\
    pip install scrapy -i https://pypi.douban.com/simple/

RUN pip install faker -i https://pypi.douban.com/simple/
RUN pip install sqlalchemy pymysql -i https://pypi.douban.com/simple/
RUN pip install redis -i https://pypi.douban.com/simple/
RUN pip install scrapy-redis -i https://pypi.douban.com/simple/

COPY ./taobao /code
WORKDIR /code/taobao
CMD ["scrapy","crawl","goods"]
