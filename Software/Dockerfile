FROM node:20.17.0 AS build

WORKDIR /app
COPY website/package*.json ./
RUN npm install
COPY website .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
