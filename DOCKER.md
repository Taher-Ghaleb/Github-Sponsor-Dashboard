# Docker Deployment Guide

This guide provides detailed instructions for deploying the GitHub Sponsor Dashboard using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB of available RAM
- 10GB of free disk space

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Github-Sponsor-Dashboard
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file:**
   - Set `POSTGRES_PASSWORD` (required)
   - Set `PAT` (GitHub Personal Access Token - required for data collection)
   - Set other optional variables as needed

4. **Start all services:**
   ```bash
   docker-compose up -d
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Database: localhost:5432

## Service Details

### Database (PostgreSQL)

- **Image:** `postgres:16-alpine`
- **Port:** 5432 (configurable via `POSTGRES_PORT`)
- **Data persistence:** Stored in Docker volume `postgres_data`
- **Initialization:** Database schema is automatically created from `backend/db/db-schema.sql`

### Backend (Flask API)

- **Port:** 5000
- **Health check:** Available at http://localhost:5000/
- **Logs:** Available in `./backend/logs/` directory
- **Environment variables:** All backend config from `.env` file

### Frontend (React + Nginx)

- **Port:** 3000 (configurable via `FRONTEND_PORT`)
- **Production build:** Built during image creation
- **API proxy:** `/api` requests are proxied to backend

## Development Mode

For development with hot-reloading:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This will:
- Mount source code as volumes for live reloading
- Use development servers (Flask dev server, Vite dev server)
- Enable debug mode

## Common Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
# Or restart specific service
docker-compose restart backend
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build
```

### Access Container Shells

```bash
# Backend container
docker-compose exec backend /bin/bash

# Database shell
docker-compose exec db psql -U postgres -d github_sponsors
```

### Clean Everything (Remove Volumes)

```bash
# WARNING: This will delete all database data
docker-compose down -v
```

## Environment Variables

Key environment variables for Docker deployment:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `POSTGRES_USER` | Database username | No | `postgres` |
| `POSTGRES_PASSWORD` | Database password | Yes | - |
| `POSTGRES_DB` | Database name | No | `github_sponsors` |
| `POSTGRES_PORT` | Database port | No | `5432` |
| `FRONTEND_PORT` | Frontend port | No | `3000` |
| `PAT` | GitHub Personal Access Token | Yes* | - |
| `API_KEY` | OpenAI API key | No | - |
| `EMAIL` | Email for OpenStreetMap | No | - |
| `GH_USERNAME` | GitHub username for scraping | No | - |
| `GH_PASSWORD` | GitHub password for scraping | No | - |

*Required only if running the data collection worker

## Troubleshooting

### Port Already in Use

If you get port conflict errors:

1. **Change ports in docker-compose.yml:**
   ```yaml
   ports:
     - "3001:80"  # Change frontend port
     - "5001:5000"  # Change backend port
     - "5433:5432"  # Change database port
   ```

2. **Or use environment variables:**
   ```bash
   FRONTEND_PORT=3001 POSTGRES_PORT=5433 docker-compose up
   ```

### Database Connection Issues

1. **Check if database is healthy:**
   ```bash
   docker-compose ps
   ```

2. **Check database logs:**
   ```bash
   docker-compose logs db
   ```

3. **Verify environment variables:**
   ```bash
   docker-compose exec backend env | grep POSTGRES
   ```

### Backend Not Starting

1. **Check backend logs:**
   ```bash
   docker-compose logs backend
   ```

2. **Verify database is ready:**
   ```bash
   docker-compose exec db pg_isready -U postgres
   ```

3. **Check environment variables:**
   ```bash
   docker-compose exec backend env
   ```

### Frontend Not Loading

1. **Check if frontend built successfully:**
   ```bash
   docker-compose logs frontend | grep -i error
   ```

2. **Verify backend is accessible:**
   ```bash
   curl http://localhost:5000/
   ```

3. **Check nginx configuration:**
   ```bash
   docker-compose exec frontend nginx -t
   ```

### Permission Issues

If you encounter permission issues with volumes:

```bash
# Fix ownership (Linux/Mac)
sudo chown -R $USER:$USER ./backend/logs
```

## Production Deployment

For production deployment:

1. **Use production Dockerfiles** (already configured)
2. **Set strong passwords** in `.env`
3. **Use environment-specific secrets** (don't commit `.env`)
4. **Configure reverse proxy** (nginx/traefik) for SSL
5. **Set up database backups**
6. **Monitor logs and resources**

## Data Persistence

Database data is stored in a Docker volume named `postgres_data`. To backup:

```bash
# Create backup
docker-compose exec db pg_dump -U postgres github_sponsors > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres github_sponsors < backup.sql
```

## Using Makefile

A `Makefile` is provided for convenience:

```bash
make help          # Show all commands
make build         # Build images
make up            # Start services
make down          # Stop services
make logs          # View logs
make dev           # Development mode
make clean         # Remove volumes
make shell-backend # Backend shell
make shell-db      # Database shell
```

## Next Steps

After successful deployment:

1. **Initialize database** (if not auto-initialized):
   ```bash
   docker-compose exec db psql -U postgres -d github_sponsors -f /docker-entrypoint-initdb.d/01-schema.sql
   ```

2. **Run data collection worker** (optional):
   ```bash
   docker-compose exec backend python -m backend.ingest.worker
   ```

3. **Access the dashboard** at http://localhost:3000
