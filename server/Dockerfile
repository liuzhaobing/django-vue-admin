FROM docker.io/library/python:3.11-slim
WORKDIR /code
ADD . .
RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ gunicorn &&\
    pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ supervisor &&\
    pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ -r ./requirements.txt
EXPOSE 80
ENTRYPOINT ["/bin/bash","-C","/code/start.sh"]
