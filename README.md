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
sudo docker compose up
``` 
4. Run a container from the created image:
```bash
sudo docker compose run web
``` 
5. Run a container with tests from the created image:
```bash
sudo docker compose run tests
```
6. Run a Redis from the created image:
```bash
sudo docker compose run redis_db
```
7. Run a PostgresSql from the created image:
```bash
sudo docker compose run database
```

## Usage

To run the FastAPI application, execute the following command:

```bash
uvicorn main:app --reload
```
## Clean cash & other
1. Stop and remove all running Docker containers:
```bash
sudo docker stop $(docker ps -a -q)
```
```bash
sudo docker rm $(docker ps -a -q)
```
2. Remove all Docker images:
```bash
sudo docker rmi $(docker images -a -q)
```
3. Clean up unused Docker volumes:
```bash
sudo docker volume prune
```
4. Remove unused Docker networks:
```bash
sudo docker network prune
```
5. Remove unused Docker cache and dangling images:
```bash
sudo docker system prune -a
```


