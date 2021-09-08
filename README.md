# Creating a Forum

the following project is Percepto Home Assignment.
The following are some data about the task:

## Programming Assignment

In this assignment you are asked to build a simple forum server. Please choose any framework you desire and for the client side choose angular/react/vue.js

### Required Features

- The forum server will contain an option to create a user.
- All the forum messages will be on the same page, no need to create forum topics
- Each user will be able to post a new thread, comment on each thread.
- Each user will be able the see all the threads and all the comments
- The client side needs to be able to display the message content, time of message and the participant who sent it.
- Each user will be able to delete his threads or comments
- You need to implement a basic client side application that will be able to send and receive messages. - Please notice! a basic working implementation is good enough, don’t waste your time on design.
- You should be able to set a user as superuser (directly in DB no ui needed), which can delete any message or thread

### Other requirements:

- The data should be saved in a relational database of your choice, please add a dump file for base structure if needed.
- Think about scale issues and how you would have solved them.
- Please make sure your code is clean and readable
- Bonus - update the forum live via websocket

## Installation

1. Clone the repository into a local directory
2. Create a virtual environment using
   - Linux and MacOS: `python3 -m venv virtual_environment_name`
   - Windows: `py -m venv venv virtual_environment_name`
3. Activate the virtual environment:
   - Linux and MacOS: `source virtual_environment_name/bin/activate`
   - Windows: `.\virtual_environment_name\Scripts\activate`
4. To Deactivate the virtual environment, Run `deactivate`
5. Run `pip install -r requirements.txt` to install all dependencies

## Run Application

use flask to run the application:
`flask run`

## DB Management

I have use SQLite3 as my DB for this project. if you would like to add any changes and overview the DB you should use SQLite3 CLI:

1. Install sqlite3 over your Windows/Mac/Linux OS.
   For more info, Use the following [link](https://www.servermania.com/kb/articles/install-sqlite/).
2. use sqlite3 cli to get access to the database:
   `sqlite3 forum.db`
3. to get access and see the database tables:
   `.tables`
