"""
Database connections in microservices usually attempt to initialise a
a connection, keep it alive, and use it in the application. This a bit
different when using Flask and SQLite.

Python and Flask have a totally different approach in terms of threading and
databases:

- Flask uses thread-local objects internally so that you don’t have to pass
  objects around from function to function within a request in order to stay
  threadsafe.
- sqlite3, the default module for SQLite, does not support multithreading.
  Older SQLite versions had issues with sharing connections between threads.
  That’s why the Python module disallows sharing connections and cursors
  between threads. If you still try to do so, you will get an exception at
  runtime.

It is possible to disable the threading, using the option `check_same_thread`
to False. However, the sqlite3 module is not threadsafe and Flask also does not
get along with it so well.

We will enable the write-ahead mode in SQLite and we will initalise a different
connection per thread that we will hold in a global object in the thread so it
can be reused in the same thread.
"""
from flask import Flask, jsonify
from poc.db import init_db, close_db
from poc.todo.controller import bp as todo_bp

# Initialise our app.
app = Flask(__name__)

# Initialise the database module. We will register it in the context so it is
# available globally for the thread.
app.teardown_appcontext(close_db)
app.cli.add_command(init_db)

# Register the blueprints
app.register_blueprint(todo_bp)


@app.errorhandler(404)
def not_found(error):
    return (jsonify({'error': 'not_found'}), 404,
            {'ContentType': 'application/json'})
