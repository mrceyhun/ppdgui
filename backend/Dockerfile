ARG ROOT_TAG=6.28.04-ubuntu22.04

FROM rootproject/root:$ROOT_TAG
LABEL maintainer="ceyhunuzngl@gmail.com"
LABEL org.label-schema.url="https://github.com/mrceyhun/ppdgui/tree/main/backend"

USER root
# Required Python version(greater than or equal) for FastAPI
ENV REQ_PY_VERSION=3.10

ENV WDIR /data
WORKDIR $WDIR
COPY ./backend ${WDIR}/backend

ENV PATH="${PATH}:${WDIR}"
ENV PYTHONPATH="${PYTHONPATH}:${WDIR}"

# export PYTHONPATH=BASE/ppdgui:$PYTHONPATH
# Check Python3 version. REQ_VER is REQ_PY_VERSION as int tuple (3,10), SYS_VER is system version tuple (3,10).
RUN python -c 'import sys,os; REQ_VER=tuple(int(i) for i in os.getenv("REQ_PY_VERSION").split(".")); SYS_VER=sys.version_info[:2]; print("Py OK!") if SYS_VER >= REQ_VER else print(f"ERROR! Py required {SYS_VER}, actual:{REQ_VER}") | sys.exit(1);'

# Install required packages: python and kerberos
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y &&  \
    apt-get install -y python3-pip krb5-user libpam-krb5 cron &&  \
    pip install --upgrade pip  &&  \
    pip install --no-cache-dir --upgrade -r ${WDIR}/backend/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8081
#CMD ["python",  "backend/main.py"]
# python backend/main.py >>/proc/1/fd/1 2>&1 &

# docker build -t mrceyhun/ppdgui-back:0.0.0 -f backend/Dockerfile .
# docker run -it --rm -p 8081:8081 mrceyhun/ppdgui-back:0.0.0 /bin/bash
# docker push mrceyhun/ppdgui-back:0.0.0
