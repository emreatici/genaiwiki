FROM node:18-alpine

WORKDIR /app

# Package files kopyala
COPY package*.json ./

# Dependencies yükle
RUN npm install

# Uygulama dosyalarını kopyala
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
