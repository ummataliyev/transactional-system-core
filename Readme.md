# Transactional System Core ⚡️
## Production-Ready Django Transaction Processing API

A production-ready **Django + DRF + Celery** boilerplate for internal employee wallet transfers and bonus processing.

---

## Features

- ✅ Wallet and Transaction models with full CRUD
- ✅ POST `/api/transfer` endpoint for wallet-to-wallet transfers
- ✅ Atomic transactions with **race condition protection**
- ✅ Automatic commission calculation (>1000 units → 10% commission to admin wallet)
- ✅ Async notifications to recipients via Celery with automatic retries (3 attempts, 3 seconds apart)
- ✅ Dockerized environment (PostgreSQL, Redis)
- ✅ Structured logging
- ✅ Swagger/OpenAPI documentation

---

## Getting Started

### 1. Clone the repository
```bash
git clone git@github.com:ummataliyev/transactional-system-core.git
cd transactional-system-core
```

2. **Create .env file**
Create a .env file for development:
```bash
cp docker/.env-example docker/.env
```

3. **Usage:**
    - All common Docker and project tasks can be run using `make`:

    ##### `make up` - Build and start all services 
    ##### `make down` - Stop all services 
    ##### `make restart` - Restart API container 
    ##### `make logs` - Show logs 
    ##### `make shell` - Open a bash shell inside the API container 
    ##### `make psql` - Connect to PostgreSQL database 
    ##### `make clean`- Remove all containers and volumes (clean start) 
    ##### `make build` - Build Docker images 
    ##### `make upgrade` - Apply all database migrations 
    ##### `make revision` - Create a new migration (prompts for comment) 
    ##### `make test` - Run tests 
    ##### `make lint` - Run code linting 
    ##### `make format` - Auto-format and fix code issues 

4. **Access the application:**
    - API documentation is available at:

- **Swagger UI:** `http://127.0.0.1:8000/swagger`

5. **Admin panel design**

<img src="https://github.com/ummataliyev/transactional-system-core/raw/main/image.png" alt="Admin dashboard" width="600"/>
<img src="https://github.com/ummataliyev/transactional-system-core/raw/main/image-1.png" alt="Admin dashboard" width="600"/>
