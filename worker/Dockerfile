FROM docker.io/library/python:3.11-slim
WORKDIR /code
ADD . .
RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ -r ./requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "/code/start.py"]
