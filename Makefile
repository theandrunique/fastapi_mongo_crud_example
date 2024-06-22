APP=./docker/docker-compose.app.yml
DEV=./docker/docker-compose.app.dev.yml
MONGO=./docker/docker-compose.mongo.yml
POSTGRESS=./docker/docker-compose.postgres.yml
PROXY=./docker/docker-compose.proxy.yml
PROXY_TLS=./docker/docker-compose.proxy.yml
ENV_FILE = --env-file ./.env
APP_SERVICE=app


shell:
	docker compose -f ${APP} exec -it ${APP_SERVICE} bash

up-local:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-config logger_config.yml 

up-dev:
	docker compose -f ${APP} -f ${DEV} -f ${MONGO} -f ${POSTGRESS} ${ENV_FILE} up --build --abort-on-container-exit --attach ${APP_SERVICE} --no-log-prefix

down:
	docker compose -f ${APP} -f ${DEV} -f ${MONGO} down

up-proxy:
	docker compose -f ${APP} -f ${PROXY} -f ${MONGO} ${ENV_FILE} up -d --build

down-proxy:
	docker compose -f ${APP} -f ${PROXY} -f ${MONGO} down

up-proxy-tls:
	docker compose -f ${APP} -f ${PROXY_TLS} -f ${MONGO} ${ENV_FILE} up -d --build

down-proxy-tls:
	docker compose -f ${APP} -f ${PROXY_TLS} -f ${MONGO} down
