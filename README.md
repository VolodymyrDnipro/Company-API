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


## Usage

To run the FastAPI application, execute the following command:

```bash
uvicorn main:app --reload
```
