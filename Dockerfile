FROM python:3.10-alpine

WORKDIR /srv

COPY requirements.txt /srv/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip && pip install -r /srv/requirements.txt

COPY *.py /srv/

# 启动服务
CMD ["python","webui.py"]
