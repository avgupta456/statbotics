FROM node:16

WORKDIR /frontend

COPY ./package.json /frontend/
RUN yarn install --network-timeout 1000000

COPY ./ /frontend

CMD ["yarn", "start"]