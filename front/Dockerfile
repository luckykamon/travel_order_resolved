FROM node:alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install --force
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 3006
CMD ["npm", "run", "start"]



#FROM cypress/browsers
#
#WORKDIR /usr/src/app
#EXPOSE 3006
#
#RUN npm install -g npm cypress
#
#COPY . .
#RUN npm install --force
#
#CMD ["npm", "run", "start"]


