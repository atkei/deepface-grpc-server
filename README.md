# Deepface gRPC Server

Biometric face feature extraction, matching and verification gRPC server implementation using [Deepface](https://github.com/serengil/deepface).

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

## Configuration

Support the following environment variables.  

|Name|Description|Default|
|---|---|---|
|FACE_SERVICE_LISTEN_PORT|gRPC server listen port|50051|
|FACE_SERVICE_LOG_LEVEL|Logging level (INFO, DEBUG)|INFO|
|FACE_SERVICE_SIM_METRICS|Similality metrics of face matching (cosine, euclidean, euclidean_l2)|cosine|
|FACE_SERVICE_SIM_THRESHOLD|Similality threshold of face matching|0.5|
|FACE_SERVICE_RECOGNITION_MODEL|Face recognition model for matching and verification (Facenet, VGG-Face, Facenet512, ArcFace, OpenFace)|Facenet|
|FACE_SERVICE_DETECT_BACKEND|Face detection backend (opencv, ssd, mtcnn, retinaface)|opencv|
|FACE_SERVICE_DB_NAME|Database name|face_db|
|FACE_SERVICE_DB_USER|Database username|postgres|
|FACE_SERVICE_DB_PASS|Database password|postgres|
|FACE_SERVICE_DB_HOST|Database host|localhost|
|FACE_SERVICE_DB_PORT|Database port|35432|
|FACE_SERVICE_DB_MAX_POOL_SIZE|Database maximum connection pool size|20|
