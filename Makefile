up:
	docker-compose -f ./docker/docker-compose.yml up -d --build

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-config logger_config.yml 