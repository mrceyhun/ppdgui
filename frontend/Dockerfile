# build stage
FROM node:20 as build-stage
RUN apt-get update -y

# jsroot dependencies
#   "node-gyp" requires additional packages
#   "gl" requires `which python` command which is not exist in node image, so symbolic link solves it
#   "npm i gl" takes longer, no solution for it yet

# RUN apt-get install -y software-properties-common make gcc g++  build-essential libxi-dev libglu-dev libglew-dev pkg-config git
RUN apt-get install -y make gcc g++  build-essential libxi-dev libglu-dev libglew-dev pkg-config git
RUN ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Ref https://www.middlewareinventory.com/blog/docker-vuejs/

# docker build -t test .
# docker run -it --rm -p 8080:80  test