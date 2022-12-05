# Face Feature Service

Biometric face feature extraction, matching and verification service server.  

## Prerequisite

- Python 3.10
- PostgreSQL

## How to Run

Install dependencies.

```sh
pip install pipenv
pipenv install
pipenv shell
```

Start the PostgreSQL server.  
The following is an example for using Docker Compose.

```sh
cd docker
docker-compose up -d postgres
```

Run the database migration.

```sh
cd server
piccolo migrations forwards face_service 
```

Start the server.

```sh
python server.py
```

## Docker Build and Run

Build a docker image.

```sh
docker build face-service -t face-service .
```

Run the server as a docker container.

```sh
cd docker
docker-compose up -d
```
