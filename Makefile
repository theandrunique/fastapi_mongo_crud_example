APP=./docker/docker-compose.app.yml
MONGO=./docker/docker-compose.mongo.yml
DEV=./docker/docker-compose.dev.yml
PROXY=./docker/docker-compose.proxy.yml
PROXY_TLS=./docker/docker-compose.proxy.yml


dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-config logger_config.yml 

up-dev:
	docker compose -f ${APP} -f ${DEV} -f ${MONGO} up --build --abort-on-container-exit --attach app --no-log-prefix

down:
	docker compose -f ${APP} -f ${DEV} -f ${MONGO} down

up-proxy:
	docker compose -f ${APP} -f ${PROXY} -f ${MONGO} up -d --build

down-proxy:
	docker compose -f ${APP} -f ${PROXY} -f ${MONGO} down

up-proxy-tls:
	docker compose -f ${APP} -f ${PROXY_TLS} -f ${MONGO} up -d --build

down-proxy-tls:
	docker compose -f ${APP} -f ${PROXY_TLS} -f ${MONGO} down
