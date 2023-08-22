# build stage
FROM node:20 as build-stage
LABEL maintainer="ceyhunuzngl@gmail.com"
LABEL org.label-schema.url="https://github.com/mrceyhun/ppdgui/tree/main/frontend"

# jsroot dependencies:
#   headless-gl requires `which python` command which is not exist in node image, so symbolic link solves it
#   headless-gl dependencies: https://github.com/stackgl/headless-gl#system-dependencies
RUN apt-get update -y && \
    apt-get install -y make gcc g++  build-essential git libxi-dev libglu1-mesa-dev libglew-dev pkg-config mesa-utils xvfb libgl1-mesa-dri libglapi-mesa libosmesa6 && \
    ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./frontend/run.sh /
EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]

# Ref https://www.middlewareinventory.com/blog/docker-vuejs/

# docker build -t front -f frontend/Dockerfile frontend/
# docker run -it --rm -p 8080:80  front
