# Docker Setup for Meta Takas

This guide explains how to run the Meta Takas project using Docker.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Copy environment file:**
   ```bash
   cp sample.env .env
   ```

2. **Edit the .env file** with your actual values:
   ```bash
   # Update these values in .env
   SECRET_KEY="your-secret-key-here"
   EMAIL_USER="your-email@gmail.com"
   EMAIL_PASS="your-app-password"
   ```

3. **Build and run the containers:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Web application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## Development Mode

For development with hot reloading:

```bash
# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop containers
docker-compose down
```

## Production Deployment

For production, consider:

1. **Update .env with production values:**
   - Use a strong SECRET_KEY
   - Configure proper email settings
   - Set DEBUG=False in settings.py

2. **Use production database:**
   - Consider using managed PostgreSQL service
   - Update DATABASE_URL accordingly

3. **Configure reverse proxy:**
   - Use nginx or similar for SSL termination
   - Set up proper domain names

## Troubleshooting

### Common Issues:

1. **Database connection errors:**
   ```bash
   # Check if database is running
   docker-compose ps
   
   # View database logs
   docker-compose logs db
   ```

2. **Static files not loading:**
   ```bash
   # Rebuild static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

3. **Tailwind CSS not compiling:**
   ```bash
   # Check tailwind process
   docker-compose exec web ps aux | grep tailwind
   ```

4. **Permission issues:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Reset Everything:

```bash
# Stop and remove everything
docker-compose down -v

# Remove all images
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

## File Structure

```
├── Dockerfile              # Main application container
├── docker-compose.yml      # Multi-container setup
├── .dockerignore          # Files to exclude from build
├── .env                   # Environment variables (create from sample.env)
├── sample.env             # Template for environment variables
└── requirements.txt       # Python dependencies
```

## Environment Variables

Required environment variables in `.env`:

- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `EMAIL_USER`: Email username
- `EMAIL_PASS`: Email password
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `DOCKER_DATABASE_URL`: Database URL for Docker containers 