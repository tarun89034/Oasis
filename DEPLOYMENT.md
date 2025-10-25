# Oasis - Production Deployment Guide

This guide provides instructions for deploying the Oasis application in production environments.

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Configuration](#database-configuration)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Scaling](#scaling)

## Deployment Options

Oasis supports multiple deployment options:

- **Docker Compose** (Recommended for local/development)
- **Heroku** (Simple cloud deployment)
- **AWS ECS/EKS** (Enterprise cloud deployment)
- **Traditional VPS** (Manual deployment)

## Docker Deployment

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+

### Deployment Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd oasis
   ```

2. Build and start services:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Production Docker Configuration

For production, update the `docker-compose.yml` file with:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DB_HOST=db
      - DB_NAME=oasis_db
      - DB_USER=oasis_user
      - DB_PASSWORD=secure_password
      - MODEL_DIR=/app/models
    env_file:
      - .env.production
    depends_on:
      - db
    restart: unless-stopped
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - backend
    restart: unless-stopped
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: oasis_db
      POSTGRES_USER: oasis_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
```

## Heroku Deployment

### Prerequisites

- Heroku CLI
- Git

### Deployment Steps

1. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

2. Set environment variables:
   ```bash
   heroku config:set API_HOST=0.0.0.0
   heroku config:set API_PORT=$PORT
   heroku config:set DATABASE_URL=<your-database-url>
   ```

3. Deploy the application:
   ```bash
   git push heroku main
   ```

4. Scale the dynos:
   ```bash
   heroku ps:scale web=1
   ```

## AWS Deployment

### Prerequisites

- AWS CLI configured
- Docker installed
- AWS account with appropriate permissions

### Deployment Steps

1. Create an ECR repository:
   ```bash
   aws ecr create-repository --repository-name oasis-backend
   aws ecr create-repository --repository-name oasis-frontend
   ```

2. Build and push Docker images:
   ```bash
   # Backend
   docker build -t oasis-backend .
   docker tag oasis-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/oasis-backend:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/oasis-backend:latest

   # Frontend
   docker build -t oasis-frontend ./frontend
   docker tag oasis-frontend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/oasis-frontend:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/oasis-frontend:latest
   ```

3. Deploy to ECS or EKS using the provided task definitions.

## Environment Configuration

### Environment Variables

Create a `.env.production` file with the following variables:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False

# Database Configuration
DB_HOST=your-db-host
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_PORT=5432

# Model Configuration
MODEL_DIR=/app/models
DEFAULT_EPOCHS=50
DEFAULT_BATCH_SIZE=32
DEFAULT_LOOKBACK_DAYS=60

# Scheduler Configuration
SCHEDULER_ENABLED=True
DATA_UPDATE_INTERVAL_HOURS=1
MODEL_RETRAIN_HOUR=2

# Logging Configuration
LOG_LEVEL=WARNING
```

## Database Configuration

### PostgreSQL Setup

1. Install PostgreSQL:
   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

2. Create database and user:
   ```sql
   CREATE DATABASE oasis_db;
   CREATE USER oasis_user WITH ENCRYPTED PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE oasis_db TO oasis_user;
   ```

3. Update connection settings in `.env.production`.

## Monitoring and Logging

### Application Monitoring

The application uses structured logging. Configure your logging infrastructure to capture:

- API request logs
- Model training logs
- Error logs
- Performance metrics

### Health Checks

The API provides health check endpoints:

- `/` - Basic API status
- `/docs` - API documentation

### Performance Monitoring

Monitor key metrics:

- API response times
- Model prediction accuracy
- Database query performance
- Resource utilization (CPU, memory, disk)

## Scaling

### Horizontal Scaling

For high-traffic scenarios:

1. Increase backend workers in `gunicorn.conf.py`
2. Scale frontend instances
3. Use a load balancer
4. Implement database read replicas

### Vertical Scaling

For increased capacity per instance:

1. Increase container resources (CPU, memory)
2. Optimize database indexes
3. Tune model parameters

### Auto-scaling

Configure auto-scaling based on:

- CPU utilization
- Memory usage
- Request rate
- Response time

## Security Considerations

### API Security

- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Sanitize outputs

### Database Security

- Use strong passwords
- Limit database permissions
- Encrypt sensitive data
- Regular security updates

### Network Security

- Restrict database access
- Use firewalls
- Implement network segmentation
- Regular security audits

## Backup and Recovery

### Data Backup

1. Regular database backups
2. Model checkpoint storage
3. Configuration backups

### Disaster Recovery

1. Automated backup verification
2. Recovery procedures documentation
3. Regular recovery testing

## Maintenance

### Regular Tasks

- Database maintenance (vacuum, analyze)
- Log rotation
- Security updates
- Performance tuning

### Model Retraining

- Scheduled model retraining
- Performance monitoring
- A/B testing new models

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database credentials
   - Verify network connectivity
   - Ensure database is running

2. **Model Loading Failures**
   - Check model file permissions
   - Verify model compatibility
   - Check disk space

3. **API Performance Issues**
   - Monitor resource usage
   - Check database query performance
   - Optimize model inference

### Support

For support, contact the development team or check the documentation.