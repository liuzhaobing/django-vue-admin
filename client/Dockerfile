FROM docker.io/library/node:14.19.1-alpine as builder
WORKDIR /code
COPY . .
RUN npm install
RUN npm run build:prod

FROM docker.io/library/nginx:1.19.2-alpine
COPY --from=builder /code/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
