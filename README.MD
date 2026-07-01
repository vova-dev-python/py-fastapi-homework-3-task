# Movie Theater API Project

## Table of Contents

- [Project Overview](#project-structure-overview)
- [Project Structure Overview](#project-structure-overview)
  - [Root Directory](#root-directory)
  - [Commands](#commands)
  - [Source Directory](#source-directory-src)
  - [Tip: Using `get_db` for Dependency Injection in FastAPI](#tip-using-get_db-for-dependency-injection-in-fastapi)
- [Services Overview](#services-overview)
  - [Database Service](#1-database-service-db)
  - [pgAdmin Service](#2-pgadmin-service-pgadmin)
  - [Backend Service](#3-backend-service-web)
  - [Database Migrator Service](#4-database-migrator-service-migrator)
- [Volumes](#volumes)
- [Networks](#networks)
- [How to Run the Project](#how-to-run-the-project)
- [Run project with PyCharm](#run-project-with-pycharm)
- [Models and Entities Overview](#models-and-entities-overview)
  - [Accounts Models](#accounts-models)
    - [UserGroupModel](#1-usergroupmodel)
    - [UserModel](#2-usermodel)
    - [UserProfileModel](#3-userprofilemodel)
    - [TokenBaseModel](#4-tokenbasemodel)
    - [ActivationTokenModel](#5-activationtokenmodel)
    - [PasswordResetTokenModel](#6-passwordresettokenmodel)
    - [RefreshTokenModel](#7-refreshtokenmodel)
  - [Movie Models](#movie-models)
    - [MovieModel](#1-moviemodel)
    - [GenreModel](#2-genremodel)
    - [ActorModel](#3-actormodel)
    - [CountryModel](#4-countrymodel)
    - [LanguageModel](#5-languagemodel)
    - [Association Tables](#6-association-tables)
- [Task Description: Extending the Cinema Application](#task-description-extending-the-cinema-application)
  - [Implement User Registration Endpoint](#task-implement-user-registration-endpoint)
  - [Implement User Account Activation Endpoint](#task-implement-user-account-activation-endpoint)
  - [Implement Password Reset Token Request Endpoint](#task-implement-password-reset-token-request-endpoint)
  - [Implement Password Reset Completion Endpoint](#task-implement-password-reset-completion-endpoint)
  - [Implement User Login Endpoint](#task-implement-user-login-endpoint)
  - [Implement Access Token Refresh Endpoint](#task-implement-access-token-refresh-endpoint)
- [Tips and Guidance](#tips-and-guidance)


Welcome to the **Movie Theater API** project! This educational assignment is designed to help you develop and refine
your skills in creating robust web applications using FastAPI, SQLAlchemy, and Docker. Here's what the project offers:

- **Database setup**:
    - **PostgreSQL for development**: The application uses PostgreSQL as the main database for the development
      environment, configured via Docker Compose.
    - **SQLite for testing**: A lightweight SQLite database is utilized for testing, ensuring fast and isolated test
      execution.

- **Data population**:
    - The database can be automatically populated with movie data from a provided dataset. This includes associated
      entities such as genres, actors, languages, and countries, ensuring a rich and interconnected data structure.

- **Docker integration**:
    - The project is fully Dockerized, allowing seamless setup and execution of the application and its dependencies.
      Docker Compose simplifies the orchestration of services like the FastAPI application, PostgreSQL database, and any
      other required components.

- **Project structure**:
    - A well-organized and modular project structure is provided, including:
        - Database models and schemas for movies and related entities.
        - Routing logic for managing API endpoints.
        - Utility scripts for tasks like data seeding and database migrations.

### Project Structure Overview

The **Movie Theater API** project follows a modular and organized structure to simplify development, 
testing, and deployment. Below is an overview of the main components:

Here is a visual representation of the project structure:

```
.
├── Dockerfile
├── README.MD
├── README_old.md
├── alembic.ini
├── commands
│   ├── run_migration.sh
│   └── run_web_server_dev.sh
├── docker-compose.yml
├── init.sql
├── poetry.lock
├── pyproject.toml
├── pytest.ini
└── src
    ├── __pycache__
    ├── config
    │   ├── dependencies.py
    │   └── settings.py
    ├── database
    │   ├── models
    │   │   ├── accounts.py
    │   │   ├── base.py
    │   │   └── movies.py
    │   ├── migrations
    │   │   ├── env.py
    │   │   └── versions
    │   │       ├── 2da0dc469be8_temp_migration.py
    │   │       ├── 32b1054a69e3_initial_migration.py
    │   │       └── 41cdafa531cf_temp_migration.py
    │   ├── populate.py
    │   ├── seed_data
    │   │   ├── imdb_movies.csv
    │   │   └── test_data.csv
    │   ├── session_postgresql.py
    │   ├── session_sqlite.py
    │   └── validators
    │       └── accounts.py
    ├── exceptions
    │   └── security.py
    ├── main.py
    ├── routes
    │   ├── accounts.py
    │   └── movies.py
    ├── schemas
    │   ├── accounts.py
    │   ├── examples
    │   │   └── movies.py
    │   └── movies.py
    ├── security
    │   ├── interfaces.py
    │   ├── passwords.py
    │   ├── token_manager.py
    │   └── utils.py
    └── tests
        ├── conftest.py
        └── test_integration
            ├── test_accounts.py
            └── test_movies.py
```

#### **Root Directory**

- **`README.MD`**: Provides detailed documentation for the project.
- **`README_old.md`**: Archived version of the original documentation for reference.
- **`docker-compose.yml`**: Orchestrates the application and its dependencies, such as PostgreSQL, in a development environment.
- **`alembic.ini`**: Configuration file for Alembic, the tool used for database migrations.
- **`poetry.lock`** and **`pyproject.toml`**: Manage dependencies and project configurations using Poetry.
- **`pytest.ini`**: Configuration file for pytest, specifying test settings and options.

#### **Commands**

- **`run_migration.sh`**: A script to execute database migrations.
- **`run_web_server_dev.sh`**: A script to start the FastAPI development server.

#### **Source Directory (`src`)**

1. **`config`**:
    - **`dependencies.py`**: Defines reusable dependency functions for routes.
    - **`settings.py`**: Contains the project configuration, including database connection details.

2. **`database`**:
    - **`models`**: Organized into separate files for accounts, movies, and base models.
    - **`populate.py`**: Contains logic for populating the database with initial data.
    - **`session_postgresql.py`**: Manages PostgreSQL sessions for development.
    - **`session_sqlite.py`**: Manages SQLite sessions for testing.
    - **`validators/accounts.py`**: Includes validation logic for accounts.

3. **`exceptions`**:
    - **`security.py`**: Custom exceptions for security-related operations.

4. **`routes`**:
    - **`accounts.py`**: Handles endpoints related to user accounts.
    - **`movies.py`**: Handles endpoints for managing movies.

5. **`schemas`**:
    - **`accounts.py`**: Defines schemas for account-related requests and responses.
    - **`examples/movies.py`**: Contains examples for Swagger documentation.

6. **`security`**:
    - **`interfaces.py`**: Provides interfaces for security operations.
    - **`passwords.py`**: Manages password hashing and validation.
    - **`token_manager.py`**: Handles token creation and validation.
    - **`utils.py`**: Contains helper functions for security.

7. **`tests`**:
    - **`conftest.py`**: Defines shared test fixtures.
    - **`test_integration/`**: Contains integration tests for API endpoints.

### Tip: Using `get_db` for Dependency Injection in FastAPI

The `get_db` function is a generator that provides a SQLAlchemy session for interacting with the database. This function is particularly useful in FastAPI as it can be injected into route handlers using the `Depends` mechanism. Here’s how you can use it effectively:

```python
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db  # Import the get_db generator

router = APIRouter()


@router.get("/example")
async def example_route(db: AsyncSession = Depends(get_db)):
    """Use the db session here to interact with the database"""
    pass
```

#### Key Points:

- The `Depends` function simplifies injecting dependencies like the database session into your route handlers.
- The `get_db` function ensures proper session handling: the session is created before the route logic executes and is closed automatically afterward.
- This approach promotes cleaner, more testable code by separating dependency setup from business logic.
- Additional dependency injection functions like `get_settings` and `get_jwt_auth_manager` can be imported from the `config` package for other common application needs:

```python
from src.config import get_settings, get_jwt_auth_manager
``` 

You can use this pattern across your application for any routes that need database access or other common dependencies. This modular approach improves code maintainability and testability.

### Services Overview

The project is configured with the following services in the `docker-compose.yml` file. These services collectively
support the development, testing, and deployment of the Movie Theater API:

#### **1. Database Service (`db`)**

- **Image**: `postgres:latest`
- **Purpose**: Acts as the primary database for the project, running a PostgreSQL instance.
- **Configuration**:
    - Loads initial SQL setup from `init.sql`.
    - Stores persistent data using a named Docker volume `postgres_theater_data`.
    - Exposes PostgreSQL on port `5432`.
- **Health Check**: Ensures the database is ready by using the `pg_isready` command.
- **Network**: Attached to `theater_network`.

#### **2. pgAdmin Service (`pgadmin`)**

- **Image**: `dpage/pgadmin4`
- **Purpose**: Provides a web-based interface for managing and monitoring the PostgreSQL database.
- **Configuration**:
    - Exposes pgAdmin on port `3333`.
    - Stores pgAdmin data in the `pgadmin_theater_data` volume.
- **Dependency**: Starts only after the `db` service is healthy.
- **Network**: Attached to `theater_network`.

#### **3. Backend Service (`web`)**

- **Build Context**: Builds the FastAPI application from the local directory (`.`).
- **Purpose**: Runs the FastAPI application, serving the Movie Theater API backend.
- **Configuration**:
    - Exposes the backend on port `8000`.
    - Uses the `run_web_server_dev.sh` script to start the development server.
    - Watches for file changes in the `src` directory using `WATCHFILES_FORCE_POLLING=true`.
    - Mounts the `src` directory to `/usr/src/fastapi` inside the container for live development.
- **Dependency**: Starts only after the `db` service is healthy.
- **Network**: Attached to `theater_network`.

#### **4. Database Migrator Service (`migrator`)**

- **Build Context**: Shares the same build context as the backend service.
- **Purpose**: Runs database migrations using Alembic to ensure the schema is up-to-date.
- **Configuration**:
    - Executes the `run_migration.sh` script to apply migrations.
    - Uses the `src` directory as the source for migration scripts.
- **Dependency**: Starts only after the `db` service is healthy.
- **Network**: Attached to `theater_network`.

### Volumes

- **`postgres_theater_data`**:
    - Stores persistent PostgreSQL data.
- **`pgadmin_theater_data`**:
    - Stores persistent data for pgAdmin.

### Networks

- **`theater_network`**:
    - A bridge network connecting all services, enabling inter-service communication.

### Services Overview

The project is configured with the following services in the `docker-compose.yml` file. These services collectively
support the development, testing, and deployment of the Movie Theater API:

#### **1. Database Service (`db`)**

- **Image**: `postgres:latest`
- **Purpose**: Acts as the primary database for the project, running a PostgreSQL instance.
- **Configuration**:
    - Loads initial SQL setup from `init.sql`.
    - Stores persistent data using a named Docker volume `postgres_theater_data`.
    - Exposes PostgreSQL on port `5432`.
- **Health Check**: Ensures the database is ready by using the `pg_isready` command.
- **Network**: Attached to `theater_network`.

#### **2. pgAdmin Service (`pgadmin`)**

- **Image**: `dpage/pgadmin4`
- **Purpose**: Provides a web-based interface for managing and monitoring the PostgreSQL database.
- **Configuration**:
    - Exposes pgAdmin on port `3333`.
    - Stores pgAdmin data in the `pgadmin_theater_data` volume.
- **Dependency**: Starts only after the `db` service is healthy.
- **Network**: Attached to `theater_network`.

#### **3. Backend Service (`web`)**

- **Build Context**: Builds the FastAPI application from the local directory (`.`).
- **Purpose**: Runs the FastAPI application, serving the Movie Theater API backend.
- **Configuration**:
    - Exposes the backend on port `8000`.
    - Uses the `run_web_server_dev.sh` script to start the development server.
    - Watches for file changes in the `src` directory using `WATCHFILES_FORCE_POLLING=true`.
    - Mounts the `src` directory to `/usr/src/fastapi` inside the container for live development.
- **Dependency**: Starts only after the `db` service is healthy.
- **Network**: Attached to `theater_network`.

#### **4. Database Migrator Service (`migrator`)**

- **Build Context**: Shares the same build context as the backend service.
- **Purpose**: Runs database migrations using Alembic to ensure the schema is up-to-date.
- **Configuration**:
    - Executes the `run_migration.sh` script to apply migrations.
    - Uses the `src` directory as the source for migration scripts.
- **Dependency**: Starts only after the `db` service is healthy.
- **Network**: Attached to `theater_network`.

### Volumes

- **`postgres_theater_data`**:
    - Stores persistent PostgreSQL data.
- **`pgadmin_theater_data`**:
    - Stores persistent data for pgAdmin.

### Networks

- **`theater_network`**:
    - A bridge network connecting all services, enabling inter-service communication.

### How to Run the Project

Follow these steps to set up and run the **Movie Theater API** project on your local machine.

#### **1. Clone the Repository**

Start by cloning the project repository from GitHub:

```bash
git clone <repository-url>
cd <repository-folder>
```

#### **2. Create and Activate a Virtual Environment**

It is recommended to use a virtual environment to isolate project dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

#### **3. Install Dependencies with Poetry**

This project uses Poetry for dependency management. Install dependencies as follows:

```bash
# Install Poetry if not already installed
pip install poetry

# Install project dependencies
poetry install
```

#### **4. Create a `.env` File**

Create a `.env` file in the project root directory with the following variables. Customize the values as needed:

```env
# PostgreSQL
POSTGRES_DB=movies_db
POSTGRES_DB_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=some_password
POSTGRES_HOST=postgres_theater
# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=admin
# JWT keys
SECRET_KEY_ACCESS=838qKq7dGp34hWij3c8txA5ZD2qm9ybt
SECRET_KEY_REFRESH=cFzRk8kllHMW71wQKLXBqDzl24fkhisw
JWT_SIGNING_ALGORITHM=HS256
```

#### **5. Run the Project with Docker Compose**

The project is Dockerized for easy setup. To start all the required services (PostgreSQL, pgAdmin, FastAPI app, and
Alembic migrator), run:

```bash
docker-compose up --build
```

**Note**: On the first run, the database will be populated with data from the dataset. This process may take some time,
so please be patient.

#### **6. Access the Services**

- **API**: The Movie Theater API will be available at `http://localhost:8000`.
- **pgAdmin**: The pgAdmin web interface will be available at `http://localhost:3333`. Use the credentials you defined
  in the `.env` file to log in.

#### **7. Verify Setup**

After all services are running, you can test the API by accessing the OpenAPI documentation:

```plaintext
http://localhost:8000/docs
```

### Run project with PyCharm

1. Mark the `src` directory as root
    ![mark src directory as root](./assets/images/1_mark_directory_as_source_root.png)
2. Close all open code tabs
3. Restart `PyCharm`
4. Create a new Run Configuration for the `FastAPI` project
    ![create new fastapi run configuration](./assets/images/2_create_new_run_config.png)
5. Add the required environment variables to the Run Configuration.
6. Start the local Docker Compose services:
    ```bash
    docker-compose -f docker-compose-local.yml up --build -d
    ```
7. Wait for the initial database seeding to finish (this may take a moment the first time).
    ![seed db](./assets/images/4_seed_db.png)  
8. Run the project via `PyCharm` and use breakpoints for debugging
9. If you need to apply database migrations manually, run:
    ```bash
    docker-compose -f docker-compose-local.yml up --build migrator
    ```

### Models and Entities Overview

The project defines the following entities and relationships using SQLAlchemy. Each entity represents a table in the database and maps to a specific domain concept in the Movie Theater API.

---

#### **Accounts Models**

These models handle user authentication, authorization, and related functionality.


#### **1. UserGroupModel**

Represents user groups in the application (e.g., USER, MODERATOR, ADMIN).

- **Table Name**: `user_groups`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each user group.
    - `name`: Enum value representing the group (`UserGroupEnum`).

- **Relationships**:
    - `users`: One-to-many relationship with `UserModel`.

- **Constraints**:
    - Unique constraint on `name`.


#### **2. UserModel**

Represents application users.

- **Table Name**: `users`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each user.
    - `email`: Email address of the user (unique).
    - `hashed_password`: Securely stored password hash.
    - `is_active`: Boolean indicating whether the user account is active.
    - `created_at`: Timestamp when the user was created.
    - `updated_at`: Timestamp when the user was last updated.
    - `group_id`: Foreign key linking to the `user_groups` table.

- **Relationships**:
    - `group`: Links to `UserGroupModel`.
    - `activation_token`: One-to-one relationship with `ActivationTokenModel`.
    - `password_reset_token`: One-to-one relationship with `PasswordResetTokenModel`.
    - `refresh_tokens`: One-to-many relationship with `RefreshTokenModel`.
    - `profile`: One-to-one relationship with `UserProfileModel`.


#### **3. UserProfileModel**

Represents additional information about a user (optional).

- **Table Name**: `user_profiles`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each profile.
    - `first_name`: User's first name.
    - `last_name`: User's last name.
    - `avatar`: Path to the user's avatar image.
    - `gender`: Enum value representing the user's gender (`GenderEnum`).
    - `date_of_birth`: User's date of birth.
    - `info`: Additional information about the user.
    - `user_id`: Foreign key linking to the `users` table.

- **Relationships**:
    - `user`: Links to `UserModel`.

- **Constraints**:
    - Unique constraint on `user_id`.


#### **4. TokenBaseModel**

Abstract base class for all token-based models.

- **Fields**:
    - `id` (Primary Key): Unique identifier for each token.
    - `token`: Securely generated token value.
    - `expires_at`: Expiration timestamp for the token.
    - `user_id`: Foreign key linking to the `users` table.


#### **5. ActivationTokenModel**

Represents tokens used for user account activation.

- **Table Name**: `activation_tokens`
- **Fields**:
    - Inherits all fields from `TokenBaseModel`.

- **Relationships**:
    - `user`: Links to `UserModel`.

- **Constraints**:
    - Unique constraint on `user_id`.


#### **6. PasswordResetTokenModel**

Represents tokens used for password reset.

- **Table Name**: `password_reset_tokens`
- **Fields**:
    - Inherits all fields from `TokenBaseModel`.

- **Relationships**:
    - `user`: Links to `UserModel`.

- **Constraints**:
    - Unique constraint on `user_id`.


#### **7. RefreshTokenModel**

Represents refresh tokens for user authentication.

- **Table Name**: `refresh_tokens`
- **Fields**:
    - Inherits all fields from `TokenBaseModel`.
    - `token`: Securely generated token value with an extended length.

- **Relationships**:
    - `user`: Links to `UserModel`.

- **Methods**:
    - `create`: Factory method to simplify the creation of new refresh tokens.


---

#### **Movie Models**

These models handle movies theater functionality.


#### **1. MovieModel**

Represents a movie in the database.

- **Table Name**: `movies`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each movie.
    - `name`: Name of the movie.
    - `date`: Release date of the movie.
    - `score`: Movie rating score (e.g., IMDb score).
    - `overview`: A short description or synopsis of the movie.
    - `status`: Production status of the movie (e.g., Released, In Production).
    - `budget`: The budget of the movie (stored as a decimal value).
    - `revenue`: The revenue generated by the movie.
    - `country_id`: Foreign key linking to the `countries` table.

- **Relationships**:
    - `country`: Links to the `CountryModel`.
    - `genres`: Many-to-many relationship with `GenreModel`.
    - `actors`: Many-to-many relationship with `ActorModel`.
    - `languages`: Many-to-many relationship with `LanguageModel`.

- **Constraints**:
    - Unique constraint on `name` and `date` to prevent duplicate entries.

#### **2. GenreModel**

Represents a genre (e.g., Action, Comedy).

- **Table Name**: `genres`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each genre.
    - `name`: Name of the genre (e.g., Action, Drama).

- **Relationships**:
    - `movies`: Many-to-many relationship with `MovieModel`.

#### **3. ActorModel**

Represents an actor in the database.

- **Table Name**: `actors`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each actor.
    - `name`: Name of the actor.

- **Relationships**:
    - `movies`: Many-to-many relationship with `MovieModel`.

#### **4. CountryModel**

Represents a country associated with a movie (e.g., production country).

- **Table Name**: `countries`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each country.
    - `code`: ISO 3166-1 alpha-3 country code (e.g., USA, FRA).
    - `name`: Full name of the country.

- **Relationships**:
    - `movies`: One-to-many relationship with `MovieModel`.

#### **5. LanguageModel**

Represents a language spoken in a movie.

- **Table Name**: `languages`
- **Fields**:
    - `id` (Primary Key): Unique identifier for each language.
    - `name`: Name of the language (e.g., English, French).

- **Relationships**:
    - `movies`: Many-to-many relationship with `MovieModel`.

#### **6. Association Tables**

Used to establish many-to-many relationships between entities.

- **`MoviesGenresModel`**:
    - Links `movies` and `genres`.
    - Fields: `movie_id`, `genre_id`.

- **`ActorsMoviesModel`**:
    - Links `movies` and `actors`.
    - Fields: `movie_id`, `actor_id`.

- **`MoviesLanguagesModel`**:
    - Links `movies` and `languages`.
    - Fields: `movie_id`, `language_id`.


### Task Description: Extending the Cinema Application

In this assignment, you are tasked with continuing the development of the cinema application. 
The `schemas/movies.py` and `routes/movies.py` files have already been provided as examples of implementation and do not require any changes. Your objective is to implement the required functionality by filling out the `schemas/accounts.py` and `routes/accounts.py` files.

These files will handle user-related operations, such as registration, authentication, and account management, while adhering to the structure and design demonstrated in the existing movie-related files.

#### Additional Notes and Considerations:

1. **SQLite and Timezone Handling**:
   - SQLite does not have built-in support for time zones. To ensure compatibility with SQLite during testing, especially for fields like `expires_at` in tokens, you need to manually adjust the timezone.
   - Example:
     ```python
     expires_at = cast(datetime, token_record.expires_at).replace(tzinfo=timezone.utc)
     ```
   - This ensures that the datetime object is timezone-aware and allows proper comparisons during tests.

2. **Mapped Annotations and `cast`**:
   - SQLAlchemy's `Mapped` type hint can sometimes cause IDE warnings or issues when accessing certain attributes. To avoid these, use Python's `cast` function to explicitly cast the value.
   - Example:
     ```python
     reset_token = PasswordResetTokenModel(user_id=cast(int, user.id))
     ```
   - This approach helps resolve type-related issues, ensuring compatibility with IDEs and type-checking tools like MyPy.

3. **Adhering to Test Requirements**:
   - Tests have been pre-written for the application, which means your implementation must align with their expected behavior. Make sure to review and follow the test scenarios carefully.
   - Handle edge cases, such as invalid tokens, expired tokens, and unregistered users, to ensure all tests pass successfully.

By following these guidelines and addressing the nuances of SQLite and `Mapped` annotations, your implementation will integrate seamlessly into the existing application and meet the expected functionality.
These files will handle user-related operations, such as registration, authentication, and account management, while adhering to the structure and design demonstrated in the existing movie-related files.

### Task: Implement User Registration Endpoint

Your task is to implement a **user registration endpoint** in the `routes/accounts.py` file. This endpoint allows new users to register by providing their email and password. It should handle potential errors and return the appropriate response based on the scenarios described below.

---

#### **Endpoint Details**

- **HTTP Method**: `POST`  
- **Path**: `/register/`

---

#### **Request Body**

The endpoint accepts the following request body:

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

---

#### **Response Structure**

If the request is successful, the endpoint returns the following JSON response:

```json
{
  "id": 1,
  "email": "user@example.com",
}
```

---

#### **Behavior**

1. **User Creation**:
    - The endpoint registers a new user and assigns them to the default user group (`UserGroupEnum.USER`).
    - The password is hashed before storing in the database.
    - A new activation token is created for the user, allowing them to activate their account later.

2. **Error Handling**:
    - **Conflict (409)**: If a user with the same email already exists, the endpoint returns a `409 Conflict` response with the message:  
      `"A user with this email {user_data.email} already exists."`
    - **Internal Server Error (500)**: If an unexpected error occurs during user creation, the endpoint returns a `500 Internal Server Error` response with the message:  
      `"An error occurred during user creation."`

3. **Data Validation**:
    - The email and password fields are validated using the `UserRegistrationRequestSchema` schema.
    - Invalid inputs (e.g., weak passwords, improperly formatted emails) will not pass validation.

---

#### **HTTP Responses**

- **201 Created**: User registered successfully.
- **409 Conflict**: A user with the same email already exists.
- **500 Internal Server Error**: An error occurred during user creation.

---

#### **Example Response for Errors**

- **409 Conflict**:
    ```json
    {
      "detail": "A user with this email test@example.com already exists."
    }
    ```

- **500 Internal Server Error**:
    ```json
    {
      "detail": "An error occurred during user creation."
    }
    ```

---

#### **Implementation Notes**

This task requires you to implement the registration logic in `routes/accounts.py`. Ensure that the following conditions are met:

1. **Database Checks**:
    - Before creating a user, the database must be checked for an existing email.

2. **Token Creation**:
    - Generate an activation token for every new user.

3. **Transaction Handling**:
    - Ensure proper transaction management. Roll back changes in case of an error.

4. **Validation and Testing**:
    - Validate the functionality against provided test cases, ensuring that all edge cases are handled.

### Task: Implement User Account Activation Endpoint

Your task is to implement an endpoint in the `routes/accounts.py` file that allows users to activate their accounts by providing a valid activation token and email. The required behavior and response structure are detailed below.

---

#### **Endpoint Details**

- **HTTP Method**: `POST`
- **Path**: `/activate/`

---

#### **Request Body**

The endpoint expects a JSON object with the following structure:

```json
{
  "email": "test@example.com",
  "token": "activation_token"
}
```

- **`email`** (string): The email address associated with the user's account.
- **`token`** (string): The activation token provided to the user.

---

#### **Response Structure**

- **Success Response (200)**:
    - If the token is valid and the user's account is successfully activated, the endpoint returns:
    ```json
    {
      "message": "User account activated successfully."
    }
    ```

---

#### **Behavior**

1. **Token Validation**:
    - The endpoint retrieves the activation token and verifies its validity.
    - The token must:
        - Belong to the specified user.
        - Not be expired.

2. **User Activation**:
    - If the token is valid, the endpoint sets the user's account status to active.
    - The activation token is deleted after successful activation.

3. **Error Handling**:
    - **400 Bad Request**:
        - If the token is invalid or expired, the response includes:
        ```json
        {
          "detail": "Invalid or expired activation token."
        }
        ```
        - If the user's account is already active, the response includes:
        ```json
        {
          "detail": "User account is already active."
        }
        ```

---

#### **HTTP Responses**

- **200 OK**: The user's account was successfully activated.
- **400 Bad Request**:
    - If the activation token is invalid or expired, or if the account is already active.

---

### Implementation Notes

1. **Database Interaction**:
    - Use the `ActivationTokenModel` table to retrieve and validate the token.
    - Set `is_active` to `True` for the user and delete the activation token after successful activation.

2. **Edge Cases**:
    - Handle cases where:
        - The token is not found or expired.
        - The user account is already active.

### Task: Implement Password Reset Token Request Endpoint

Your task is to implement an endpoint in the `routes/accounts.py` file that allows users to request a password reset token. The endpoint ensures that no sensitive user information is leaked while providing a mechanism to reset passwords securely. 

---

#### **Endpoint Details**

- **HTTP Method**: `POST`
- **Path**: `/password-reset/request/`

---

#### **Request Body**

The endpoint expects a JSON object with the following structure:

```json
{
  "email": "test@example.com"
}
```

- **`email`** (string): The email address associated with the user's account.

---

#### **Response Structure**

- **Success Response (200)**:
    - The endpoint always responds with:
    ```json
    {
      "message": "If you are registered, you will receive an email with instructions."
    }
    ```

---

#### **Behavior**

1. **User Validation**:
    - If a user with the provided email exists and is active:
        - Any existing password reset tokens for that user are invalidated.
        - A new password reset token is generated and stored in the database.
    - If the user does not exist or is inactive:
        - The same success message is returned to prevent leaking information about the user's existence.

2. **Token Invalidation**:
    - The endpoint deletes any existing password reset tokens for the user before creating a new one.

3. **Always Respond with Success**:
    - To prevent information leaks, the endpoint always responds with the same success message, regardless of whether the user exists or is active.

---

#### **HTTP Responses**

- **200 OK**: The request was successful. This response is always returned regardless of the user's existence or status.

---

### Implementation Notes

1. **Database Interaction**:
    - Use the `UserModel` table to verify the user's existence and active status.
    - Use the `PasswordResetTokenModel` table to manage password reset tokens:
        - Delete any existing tokens for the user.
        - Generate a new token and save it in the database.

2. **Security Considerations**:
    - Ensure no information about the user's existence or account status is leaked in the response.
    - Validate the email address format to ensure only valid requests are processed.

### Task: Implement Password Reset Completion Endpoint

Your task is to implement the password reset completion functionality in the `/reset-password/complete/` endpoint. This endpoint allows users to reset their password using a valid password reset token.

---

#### Endpoint Details

- **HTTP Method**: `POST`
- **Path**: `/reset-password/complete/`

---

#### Request Body

The request body must adhere to the following schema:

- **`email`** (string, required):
  - The email address of the user attempting to reset their password.

- **`token`** (string, required):
  - The password reset token received during the reset request process.

- **`password`** (string, required):
  - The new password for the user.

Example:

```json
{
  "email": "testuser@example.com",
  "token": "valid-reset-token",
  "password": "NewStrongPassword123!"
}
```

---

#### Behavior

1. **Token Validation**:
   - The system checks if a valid `PasswordResetTokenModel` exists for the provided email.
   - The token is verified against the stored record, and its expiration date is validated.

2. **Error Handling**:
   - If the email or token is invalid, or the token has expired, the system deletes the token (if it exists) and returns an error response with a `400 Bad Request` status code.
   - If the user does not exist or is inactive, an error response with a `400 Bad Request` status code is returned.

3. **Password Reset**:
   - Upon successful validation, the user's password is updated in the database.
   - The token is deleted after the password is reset to prevent reuse.

4. **Error Scenarios**:
   - If a database error occurs while updating the password, the transaction is rolled back, and a `500 Internal Server Error` is returned.

---

#### HTTP Responses

- **200 OK**: Password reset successfully.
  - **Example Response**:
    ```json
    {
      "message": "Password reset successfully."
    }
    ```

- **400 Bad Request**: The provided email, token, or password is invalid, or the token has expired.
  - **Examples**:
    - **Invalid Token**:
      ```json
      {
        "detail": "Invalid email or token."
      }
      ```
    - **Expired Token**:
      ```json
      {
        "detail": "Invalid email or token."
      }
      ```

- **500 Internal Server Error**: An unexpected error occurred while resetting the password.
  - **Example**:
    ```json
    {
      "detail": "An error occurred while resetting the password."
    }
    ```

---

#### Implementation Notes

1. Validate the token expiration using a timezone-aware comparison.
2. Ensure the password meets all validation requirements before updating.
3. Use proper database transaction handling to prevent partial updates.

This task requires careful attention to token validation and password handling to ensure the security and integrity of user data.

### Task: Implement User Login Endpoint

Your task is to implement an endpoint that authenticates a user based on their email and password, generates access and refresh tokens upon successful login, and stores the refresh token in the database. Follow the specifications below to ensure the endpoint works as expected.

---

#### **Endpoint Details**

- **HTTP Method**: `POST`
- **Path**: `/login/`

---

#### **Request Body**

The endpoint accepts the following JSON payload:

```json
{
  "email": "user@example.com",
  "password": "UserPassword123!"
}
```

- **`email`** (string): The email address of the user.
- **`password`** (string): The password associated with the user's account.

---

#### **Response**

The endpoint should return the following JSON response upon successful login:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

- **`access_token`**: A JWT used for accessing protected resources.
- **`refresh_token`**: A JWT used to refresh the access token.
- **`token_type`**: Specifies the type of token (`bearer`).

---

#### **Behavior**

1. **Authentication**:
   - Validate the user's email and password.
   - If the email or password is incorrect, return a `401 Unauthorized` error with the message `"Invalid email or password."`.

2. **Account Activation**:
   - If the user's account is not activated, return a `403 Forbidden` error with the message `"User account is not activated."`.

3. **Token Generation**:
   - Generate a new refresh token using the `jwt_manager.create_refresh_token` method.
   - Store the refresh token in the `RefreshTokenModel` table, associating it with the user.

4. **Error Handling**:
   - If an unexpected database error occurs during token storage, return a `500 Internal Server Error` with the message `"An error occurred while processing the request."`.

5. **Success**:
   - Return both the `access_token` and `refresh_token` in the response.

---

#### **Error Responses**

- **401 Unauthorized**:
  - Occurs when the email or password is invalid.
  - Example response:
    ```json
    {
      "detail": "Invalid email or password."
    }
    ```

- **403 Forbidden**:
  - Occurs when the user's account is not activated.
  - Example response:
    ```json
    {
      "detail": "User account is not activated."
    }
    ```

- **500 Internal Server Error**:
  - Occurs when there is an unexpected database error.
  - Example response:
    ```json
    {
      "detail": "An error occurred while processing the request."
    }
    ```

---

#### **Hints and Tips**

1. **JWT Manager**:
   - Use the `JWTAuthManagerInterface` to manage token creation and validation.
   - The `jwt_manager` dependency can be injected into the endpoint using:
     ```python
     jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager)
     ```

2. **Settings**:
   - Token-related settings, such as `SECRET_KEY_ACCESS`, `SECRET_KEY_REFRESH`, and `LOGIN_TIME_DAYS`, can be accessed via:
     ```python
     settings: BaseAppSettings = Depends(get_settings)
     ```

3. **Refresh Token Storage**:
   - Use the `RefreshTokenModel.create` method to create and store the refresh token in the database.

---

#### **Acceptance Criteria**

1. The endpoint successfully authenticates users with valid credentials and returns the correct response.
2. The endpoint handles all edge cases (e.g., invalid credentials, inactive account, database errors) and returns appropriate error messages.
3. The refresh token is correctly stored in the database, and the tokens are valid according to the provided settings.

### Task: Implement Access Token Refresh Endpoint

Your task is to implement an endpoint in the `routes/accounts.py` file that allows users to refresh their access token by providing a valid refresh token.

---

#### Endpoint Details

- **HTTP Method**: `POST`
- **Path**: `/api/v1/accounts/refresh/`

---

#### Request Body

The request body must include the refresh token in the following structure:

```json
{
  "refresh_token": "example_refresh_token"
}
```

---

#### Response Structure

Upon successful execution, the endpoint should return a new access token in the following format:

```json
{
  "access_token": "new_access_token"
}
```

---

#### Behavior

1. **Token Validation**:
   - The provided refresh token must be validated using the `JWTAuthManager.decode_refresh_token` method.
   - If the token is invalid or expired, return a `400 Bad Request` response with an appropriate error message.

2. **Refresh Token Existence**:
   - Check the database to ensure the provided refresh token exists in the `RefreshTokenModel` table.
   - If the token does not exist, return a `401 Unauthorized` response with the message: `"Refresh token not found."`

3. **User Validation**:
   - Use the `user_id` extracted from the refresh token to query the `UserModel` table.
   - If the user associated with the token does not exist, return a `404 Not Found` response with the message: `"User not found."`

4. **Access Token Generation**:
   - If all validations pass, generate a new access token using `JWTAuthManager.create_access_token`.
   - Return the new access token in the response.

---

#### HTTP Responses

- **200 OK**: Access token successfully refreshed.
  - Example response:
    ```json
    {
      "access_token": "new_access_token"
    }
    ```
- **400 Bad Request**: The provided refresh token is invalid or expired.
  - Example response:
    ```json
    {
      "detail": "Token has expired."
    }
    ```
- **401 Unauthorized**: The provided refresh token does not exist in the database.
  - Example response:
    ```json
    {
      "detail": "Refresh token not found."
    }
    ```
- **404 Not Found**: The user associated with the refresh token does not exist.
  - Example response:
    ```json
    {
      "detail": "User not found."
    }
    ```

---

#### Notes

1. **Dependency Injection**:
   - Use `jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager)` to access the JWT manager for decoding and creating tokens.
   - Use `db: Session = Depends(get_db)` for database interactions.

2. **Edge Cases**:
   - Handle tokens that are structurally valid but have been tampered with.
   - Ensure the `user_id` extracted from the token matches the user associated with the refresh token in the database.

---

### Tips and Guidance

If you’re unsure about the expected behavior or need clarification, **refer to the provided test suite**. Running the tests will:
- Show the expected logic and flow for each endpoint.
- Help you identify edge cases and handle errors correctly.
- Ensure your implementation aligns with the project's requirements.

To run the tests, use the following command in the project root directory:
```bash
pytest
```

The test results will indicate any discrepancies between your implementation and the expected behavior, providing clear guidance on how to fix them.
