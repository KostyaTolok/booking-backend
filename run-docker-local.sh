docker network create shared-kafka
docker-compose -f compose/docker-compose.users.yml -f compose/docker-compose.notifications.yml -f compose/docker-compose.search.yml -f compose/docker-compose.payments.yml -f compose/docker-compose.yml up $1