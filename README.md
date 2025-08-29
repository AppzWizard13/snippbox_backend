# SnipBox Backend

SnipBox is a short note saving application that allows users to save and organize short text snippets with tags. This backend API is built using **Django** and **Django REST Framework**, with JWT authentication.

## Features

- **User Authentication**: JWT-based login and token refresh
- **Snippet Management**:
    - Create snippets with title, note, and multiple tags
    - Retrieve snippet details
    - Update snippets
    - Bulk delete snippets
    - List snippets overview
- **Tag Management**:
    - List all tags
    - Retrieve snippets linked to a specific tag


## Prerequisites

- **Docker** and **Docker Compose** installed
- (Optional) Python 3.11+ and pip if running locally without Docker


## Docker Deployment (Mandatory)

Follow these steps to deploy SnipBox using Docker:

**1. Clone the repository**

```bash
git clone https://github.com/AppzWizard13/snippbox_backend.git
cd snipbox_backend
```

**2. Build the Docker image**

```bash
docker build -t snipbox-backend .
```

**3. Start the services using Docker Compose**

```bash
docker-compose up -d
```

**4. Apply migrations inside the container**

```bash
docker-compose exec web python manage.py migrate
```

**5. Create superuser (for admin access)**

```bash
docker-compose exec web python manage.py createsuperuser
```

**6. Access the services**

- API base URL: `http://localhost:8000/api/`
- Django admin panel: `http://localhost:8000/admin/`
- Adminer: `http://localhost:8080/`

**7. Stop the services**

```bash
docker-compose down
```


## API Endpoints

### Authentication

- **POST** `/api/accounts/token/` → Obtain access and refresh token
- **POST** `/api/accounts/token/refresh/` → Refresh access token


### Snippets CRUD

- **GET** `/api/snippets/overview/` → List all snippets of the authenticated user
- **POST** `/api/snippets/create/` → Create a snippet
- **GET** `/api/snippets/detail/<id>/` → Get snippet details
- **PATCH** `/api/snippets/update/<id>/` → Update snippet
- **DELETE** `/api/snippets/delete/` → Bulk delete snippets


### Tags

- **GET** `/api/tags/` → List all tags
- **GET** `/api/tags/detail/<id>/` → List snippets linked to a specific tag


## Example cURL Requests

### Authentication

**Get Token:**

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/token/ \
-H "Content-Type: application/json" \
-d '{"username": "rootadmin", "password": "root"}'
```


### Create Snippet

```bash
curl -X POST http://127.0.0.1:8000/api/snippets/create/ \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "title": "New Note",
  "note": "This is a short note",
  "tags": ["Important", "Work"]
}'
```


### Get Snippet Details

```bash
curl -X GET http://127.0.0.1:8000/api/snippets/detail/1/ \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
-H "Content-Type: application/json"
```


### Update Snippet

```bash
curl -X PATCH http://127.0.0.1:8000/api/snippets/update/1/ \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Title",
  "note": "Updated note content",
  "tags": ["Important", "Work"]
}'
```


### Bulk Delete Snippets

```bash
curl -X DELETE http://127.0.0.1:8000/api/snippets/delete/ \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "snippet_ids": [1, 2, 3]
}'
```


### List Tags

```bash
curl -X GET http://127.0.0.1:8000/api/tags/ \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```


### Get Tag Details (Snippets linked to a tag)

```bash
curl -X GET http://127.0.0.1:8000/api/tags/detail/1/ \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```


## Requirements

**Install dependencies:**

```bash
pip install -r requirements.txt
```


## Notes

- JWT access tokens are required for all API requests except authentication
- Bulk deletion of snippets requires passing an array of snippet IDs in the `DELETE` request body
- Tags are reused if they already exist; new tags are created only when necessary


## Author

**SnipBox Backend** by [SATHEESH A]


