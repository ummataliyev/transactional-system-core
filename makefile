COMPOSE = docker compose -f docker/docker-compose.yml

.PHONY: build up down restart logs logs-web logs-celery logs-db shell migrate createsuperuser test testdata clean setup ps exec dbinfo backup restore

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

logs-web:
	$(COMPOSE) logs -f web

logs-celery:
	$(COMPOSE) logs -f celery

logs-db:
	$(COMPOSE) logs -f db

shell:
	$(COMPOSE) exec web python manage.py shell

migrate:
	$(COMPOSE) exec web python manage.py makemigrations
	$(COMPOSE) exec web python manage.py migrate

createsuperuser:
	$(COMPOSE) exec web python manage.py createsuperuser

testdata:
	$(COMPOSE) exec web python manage.py shell < create_test_data.py

test:
	$(COMPOSE) exec web python manage.py test

clean:
	$(COMPOSE) down -v
	docker system prune -f

setup: build up migrate createsuperuser testdata
	@echo "Setup complete! Access:"
	@echo "  - Django: http://localhost:8000"
	@echo "  - Swagger: http://localhost:8000/api/swagger/"
	@echo "  - Flower: http://localhost:5555"

ps:
	$(COMPOSE) ps

exec:
	$(COMPOSE) exec web bash

dbinfo:
	$(COMPOSE) exec db psql -U postgres -d transactional_db -c "\dt"

backup:
	$(COMPOSE) exec db pg_dump -U postgres transactional_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore:
	@read -p "Enter backup file path: " backup_file; \
	$(COMPOSE) exec -T db psql -U postgres transactional_db < $$backup_file
