# My FastAPI Project

This is a sample FastAPI project.

## Running the Application in Docker

1. Clone the repository:
```bash
git clone https://github.com/VolodymyrDnipro/Meduzzen_intership_backend.git
``` 

2. Change into the project directory:

3. Build the Docker image using the docker build command:
```bash
docker compose up
``` 
## Clean cash & other
1. Stop and remove all running Docker containers:
```bash
docker stop $(docker ps -a -q)
```
```bash
docker rm $(docker ps -a -q)
```
2. Remove all Docker images:
```bash
docker rmi $(docker images -a -q)
```
3. Clean up unused Docker volumes:
```bash
docker volume prune
```
4. Remove unused Docker networks:
```bash
docker network prune
```
5. Remove unused Docker cache and dangling images:
```bash
docker system prune -a
```

## Usage

1.To run the FastAPI application, execute the following command:

```bash
uvicorn main:app --reload
```
2.Create a migration:
```bash
alembic --config db/alembic.ini revision --autogenerate -m "create_user_table"
```
3.Applying migrations:
```bash
alembic --config db/alembic.ini upgrade head
```