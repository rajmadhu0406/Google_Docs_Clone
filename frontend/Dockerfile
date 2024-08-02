# Docker file
FROM node:20.11

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY . /app

RUN npm run build

EXPOSE 3000

RUN npm install -g serve
CMD ["serve","-s","build","-l","3000"]

# CMD ["npm","run","build"]



#docker exec -it <container_name> /bin/bash
