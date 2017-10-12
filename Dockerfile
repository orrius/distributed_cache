FROM python:3.6
WORKDIR /distributed-cache
ADD requirements.txt /distributed-cache
RUN pip install -r ./requirements.txt
ADD server.py /distributed-cache
EXPOSE 5557
EXPOSE 5556
ADD client.py /distributed-cache
ADD proxy.py /distributed-cache
CMD ["python", "./server.py"]
