FROM rootproject/root:6.30.04-ubuntu22.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt update && apt-get install -y tzdata
RUN apt update && apt install -y \
    python-is-python3 \
    python3-pip \
    git
    