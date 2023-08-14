ARG ROOT_TAG=6.28.04-ubuntu22.04

FROM rootproject/root:$ROOT_TAG
MAINTAINER Ceyhun Uzunoglu ceyhunuzngl@gmail.com

USER root
# Required Python version with its minor for FastAPI
ENV PYVERSION=3.10

# Check Python3 version. REQ_VER is PYVERSION as int tuple (3,10), SYS_VER is system version tuple (3,10).
RUN echo python --version python -c 'import sys,os; REQ_VER=tuple(int(i) for i in os.getenv("PYVERSION").split(".")); SYS_VER=sys.version_info[:2]; print("Py OK!") if SYS_VER >= REQ_VER else print(f"ERROR! Py required {SYS_VER}, actual:{REQ_VER}") | sys.exit(1);'

# Install required packages
RUN apt-get update -y &&  \
    apt-get install -y python3-pip &&  \
    pip install --upgrade pip  &&  \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*