---
date: 2024-06-04T16:02:51.453539
author: AutoGPT <info@agpt.co>
---

# TODO lists

This should be an API that receives peoples TODO lists and store them for the users, they should be able to retreive them from the database

**Features**

- **Create TODO List** Allows users to create new TODO lists by providing a name and optionally a description. This helps in organizing tasks.

- **Add Task to TODO List** Enables users to add tasks to the TODO lists. Each task can have details like title, due date, priority, and notes.

- **Retrieve TODO Lists** Allows users to fetch and view all their TODO lists. They can select a specific list to view and interact with the tasks it contains.

- **Update Task** Gives users the ability to update the details of tasks in their TODO lists such as changing the due date, title, or adding additional notes.

- **Delete Task** Enables the deletion of tasks from the TODO list. Users can select tasks they no longer need and remove them.

- **User Authentication** Requires users to sign up and log in to access their TODO lists. This ensures that only authorized users can view and manage their data.

- **Audit Log** Maintains a log of all changes made to TODO lists and tasks, providing a history of actions performed by the user.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'TODO lists'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
