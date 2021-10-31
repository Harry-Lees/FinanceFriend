FROM node:latest

WORKDIR /app

COPY . .

RUN npm install -g serve
RUN npm install --save
RUN npm run build

CMD serve -s dist
