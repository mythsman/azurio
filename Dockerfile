FROM python:3.10-alpine

WORKDIR /srv

COPY requirements.txt /srv/requirements.txt

RUN pip install --upgrade pip && pip install -r /srv/requirements.txt && rm -rf .cache/pip

COPY *.py /srv/

# 启动服务
CMD ["python","webui.py"]
