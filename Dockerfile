from ultralytics/ultralytics:latest-cpu

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask

COPY best.pt /usr/src/ultralytics/models/

COPY serve.py  /usr/src/ultralytics 

COPY run.sh /home

CMD ["sh", "/home/run.sh"]
