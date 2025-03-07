
# Event Management System Using Flask

The Event Management System is a backend application built using Flask, PostgreSQL, Marshmallow, and Alembic. It enables efficient management of events, participants, and organizers through a RESTful API with authentication and authorization.





## Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <project_directory>
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. Set environment variables (for development mode):
   ```sh
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

2. Run the Flask application:
   ```sh
   flask run
   ```

   The application will start at `http://127.0.0.1:5000/`.



## API Reference

### Authentication
Authentication is handled using **JWT (JSON Web Token)**. Users need to include a valid token in the `Authorization` header to access protected routes.

#### Login
```http
POST /login
```
**Description:** Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "access_token": "your.jwt.token"
}
```

#### Signup
```http
POST /signup
```
**Description:** Registers a new user and returns a JWT token.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Logout
```http
POST /logout
```
**Description:** Logs out the user (JWT is invalidated on the client-side).

#### Accessing Protected Routes
To access **protected routes**, include the JWT token in the `Authorization` header:
```http
Authorization: Bearer your.jwt.token
```

### Role-Based Access
This system supports role-based access:
- **Admin**: Full control over events, participants, and organizers.
- **Organizer**: Can manage their own events and participants.

### Event Management

#### Create Event
```http
POST /event/
```
**Description:** Creates a new event.

**Request Body:**
```json
{
  "name": "Tech Conference",
  "description": "Annual tech event",
  "date": "2025-06-15",
  "location": "New York",
  "organizer_id": 1
}
```

#### Get All Events
```http
GET /event/
```
**Description:** Retrieves a list of all events.

#### Get Event by ID
```http
GET /event/{event_id}
```
| Parameter    | Type      | Description                      |
|-------------|----------|----------------------------------|
| `event_id`  | `int`    | **Required**. ID of the event to retrieve |

**Description:** Fetches the details of a specific event.

#### Update Event
```http
PUT /event/{event_id}
```
| Parameter    | Type      | Description                      |
|-------------|----------|----------------------------------|
| `event_id`  | `int`    | **Required**. ID of the event to update |

**Request Body:**
```json
{
  "name": "Updated Event Name",
  "description": "Updated description",
  "date": "2025-07-01",
  "location": "Los Angeles"
}
```

#### Delete Event
```http
DELETE /event/{event_id}
```
| Parameter    | Type      | Description                      |
|-------------|----------|----------------------------------|
| `event_id`  | `int`    | **Required**. ID of the event to delete |

### Organizer Management

#### Create Organizer
```http
POST /organizer/
```
**Description:** Creates a new organizer.

**Request Body:**
```json
{
  "name": "Organizer Name",
  "contact": "123-456-7890",
  "organization": "Tech Corp"
}
```

#### Get All Organizers
```http
GET /organizer/
```
**Description:** Retrieves all organizers.

#### Get Organizer by ID
```http
GET /organizer/{organizer_id}
```
| Parameter       | Type      | Description                      |
|---------------|----------|----------------------------------|
| `organizer_id` | `int`    | **Required**. ID of the organizer to retrieve |

**Description:** Fetches the details of a specific organizer.

#### Update Organizer
```http
PUT /organizer/{organizer_id}
```
| Parameter       | Type      | Description                      |
|---------------|----------|----------------------------------|
| `organizer_id` | `int`    | **Required**. ID of the organizer to update |

**Request Body:**
```json
{
  "name": "Updated Organizer Name",
  "contact": "987-654-3210",
  "organization": "New Tech Corp"
}
```

#### Delete Organizer
```http
DELETE /organizer/{organizer_id}
```
| Parameter       | Type      | Description                       |
|---------------|----------|----------------------------------|
| `organizer_id` | `int`    | **Required**. ID of the organizer to delete |



### Participant API Endpoints
The Participant API handles the management of participants in various events. It allows adding new participants to an event and removing participants as needed.

#### Add Participant to Event
```http
POST /participant/event/{event_id}
```
| Parameter    | Type      | Description                              |
|-------------|----------|------------------------------------------|
| `event_id`  | `int`    | **Required**. ID of the event to join    |

**Description:** Adds a new participant to the specified event. The request should include necessary participant details in the request body.

#### Get All Participants
```http
GET /participant/
```
**Description:** Retrieves a list of all participants across all events.

#### Update Participant
```http
PUT /participant/{participant_id}
```
| Parameter         | Type      | Description                          |
|------------------|----------|--------------------------------------|
| `participant_id` | `int`    | **Required**. ID of the participant to update |

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "updated@example.com",
  "phone": "9876543210"
}
```

#### Remove Participant
```http
DELETE /participant/{participant_id}
```
| Parameter         | Type      | Description                          |
|------------------|----------|--------------------------------------|
| `participant_id` | `int`    | **Required**. ID of the participant to remove |

**Description:** Removes a participant from the system based on their unique participant ID.

