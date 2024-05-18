# Tiny Task Marketplace

This is a Tiny Task Marketplace application built with FastAPI. The application includes features like user management, task management, messaging, payment processing, and task ratings.

## Features

- User

 Authentication and Authorization
 
- CRUD Operations for Users, Clients, Workers, Tasks, Messages, Payments, and Ratings
- Role-Based Access Control with Casbin
- Password Hashing and JWT Authentication
- Docker and Docker Compose for Containerization

## Requirements

- Python 3.9+
- Docker
- Docker Compose

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/tiny_task_marketplace.git
cd tiny_task_marketplace
```

2. Create a virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

5. Open your browser and go to `http://127.0.0.1:8000`.

## Running with Docker

1. Build and run the Docker containers:

```bash
docker-compose up --build
```

2. Open your browser and go to `http://127.0.0.1:8000`.

## API Documentation

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
