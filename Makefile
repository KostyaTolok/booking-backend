FILES := -f compose/docker-compose.users.yml -f compose/docker-compose.notifications.yml -f compose/docker-compose.search.yml -f compose/docker-compose.payments.yml -f compose/docker-compose.yml

all: run

stop:
	docker-compose $(FILES) down

run: stop
	docker network create shared-kafka; \
    docker-compose $(FILES) up --build --detach; \
    docker system prune --volumes -f;

logs:
	docker-compose $(FILES) logs -f $(service)
