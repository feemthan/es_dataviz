FROM nvidia/cuda:10.1-cudnn7-devel as base

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev \
    git wget sudo ninja-build curl vim zip unzip
RUN apt-get update
RUN ln -sv /usr/bin/python3 /usr/bin/python

WORKDIR /app

RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python3 get-pip.py && \
	rm get-pip.py

# ---- Dependencies ----
FROM base AS dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# ---- Release ----
FROM base as release
WORKDIR /app
COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# install app dependencies
RUN pip install -r requirements.txt

# copy current directory into the container
ADD . /app

ENV PYTHONIOENCODING=utf-8

EXPOSE 8010

CMD ["python", "app.py"]