#FROM python:3.12
FROM public.ecr.aws/lambda/python:3.12

WORKDIR /tmp

COPY . /tmp

RUN pip install --trusted-host pypi.python.org -r requirements.txt 

RUN yum install -y yum-utils

RUN yum update && yum install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    yum install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    yum clean

CMD ["python", "main.py"]