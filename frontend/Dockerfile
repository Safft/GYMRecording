FROM node:18

WORKDIR /frontend

COPY . /frontend

RUN npm install

RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]

EXPOSE 3000
