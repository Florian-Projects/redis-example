FROM node:20.3.0-alpine3.17 as builder

WORKDIR /app

RUN npm install -g pnpm

COPY ./package.json ./pnpm-lock.yaml ./
RUN pnpm install

COPY . .

RUN NODE_OPTIONS=--max-old-space-size=8192 pnpm run build --configuration production

FROM nginx:1.25.1

COPY --from=builder /app/dist/frontend /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
