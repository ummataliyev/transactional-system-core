COMPOSE = docker compose -f docker/docker-compose.yml

.PHONY: build up down restart logs logs-web logs-celery logs-db shell migrate createsuperuser test testdata clean setup ps exec dbinfo backup restore

# Build Docker images
build:
	$(COMPOSE) build

# Start all services
up:
	$(COMPOSE) up -d

# Stop all services
down:
	$(COMPOSE) down

# Restart all services
restart:
	$(COMPOSE) restart

# View logs
logs:
	$(COMPOSE) logs -f

# View specific service logs
logs-web:
	$(COMPOSE) logs -f web

logs-celery:
	$(COMPOSE) logs -f celery

logs-db:
	$(COMPOSE) logs -f db

# Django shell
shell:
	$(COMPOSE) exec web python manage.py shell

# Run migrations
migrate:
	$(COMPOSE) exec web python manage.py makemigrations
	$(COMPOSE) exec web python manage.py migrate

# Create superuser
createsuperuser:
	$(COMPOSE) exec web python manage.py createsuperuser

# Create test data
testdata:
	$(COMPOSE) exec web python manage.py shell < create_test_data.py

# Run tests
test:
	$(COMPOSE) exec web python manage.py test

# Clean up containers and volumes
clean:
	$(COMPOSE) down -v
	docker system prune -f

# Full setup (first time)
setup: build up migrate createsuperuser testdata
	@echo "Setup complete! Access:"
	@echo "  - Django: http://localhost:8000"
	@echo "  - Swagger: http://localhost:8000/api/swagger/"
	@echo "  - Flower: http://localhost:5555"

# Check running containers
ps:
	$(COMPOSE) ps

# Execute command in web container
exec:
	$(COMPOSE) exec web bash

# Show database info
dbinfo:
	$(COMPOSE) exec db psql -U postgres -d transactional_db -c "\dt"

# Backup database
backup:
	$(COMPOSE) exec db pg_dump -U postgres transactional_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database from backup
restore:
	@read -p "Enter backup file path: " backup_file; \
	$(COMPOSE) exec -T db psql -U postgres transactional_db < $$backup_file
