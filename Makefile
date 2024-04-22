APP=./docker/app-compose.yml
MONGO=docker/mongo-compose.yml
DEV=./docker/dev-compose.yml


up:
	docker compose -f ${APP} -f ${MONGO} up -d --build

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-config logger_config.yml 

up-dev:
	docker compose -f ${DEV} -f ${MONGO} up --build --abort-on-container-exit --attach dev-app --no-log-prefix

down:
	docker compose -f ${DEV} -f ${APP} -f ${MONGO} down