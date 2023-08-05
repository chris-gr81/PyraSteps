# PyraSteps

## Video-Demo:

https://www.youtube.com/watch?v=176hJmiBa34

## Description:

This project is a web application developed to manage and structure personal and private tasks based on Maslow's Hyrachy of Needs. The app was built with Flask, as well as Python and uses a SQL database to store tasks, their properties and ratings. The application has the following main functions:

- Function 1: Create a personal account, log in with this account and the possibility to delete the account completely.
- Function 2: Creation, completion and reactivation of tasks with different properties of scope and classification in Maslow's pyramid model.
- Function 3: An algorithm evaluates the tasks based on the properties with a scoring and presents them based on this in a processing order. In addition, there are various representations of tasks that are still  open and tasks that have been completed.

## Files and functions:

- app.py: The main application that contains the flask server and routing logic.
- support.py: The auxiliary files contains various functions used by the main application:
    - discarder(message): A function that returns a template "discard.html" with an error message passed. It is used to indicate an error to the user.
    - create_showtask(): A function that returns a sorted list of tasks based on data from the SQLite database. It also calculates a score for each task based on certain parameters.
    - score_calc(maslow, size, boost): A function that contains the algorithm for calculating the task score.
    - tab_name(maslow), maslow_word(maslow) and size_word(word): Functions that convert various numerical values from the database into words.
- database.db: The database of the app consisting of the tables users, tasks and scores.
- templates/: This folder contains the HTML templates used to rennder the web pages.
    - about.html: Includes explanations of the app and Maslow's theory
    - accdelete.html: Includes the account deletion form
    - discard.html: A HTML page to display the error messages.
    - history.html: A HTML page that displays the historical data. Includes the form for reactivating tasks.
    - index.html: Home page. Includes the welcome overview.
    - layout.html: A HTML page that contains the page layout. The navbar renders depending on whether a user is logged in or not. All other pages are rendered to this layout.
    - login.html: Includes the login form. If no user is logged in, this page is rendered automatically.
    - newtask.html: A HTML page that contains the form for entering new tasks.
    - register.html: A HTML page that contains the form to register an account.
    - showtask.html: A HTML page that displays the task overview. Includes the form to close and boost a task.

## Design decisions

In developing this web application, certain design decisions were made to improve usability and performance. Some of these decisions were:

- use of flask: flask was chosen as the web framework because it is easy to handle.
- use of bootstrap: bootstrap was chosen as a framework to create a responsive and proffesional looking design
- use of python: python was chosen as it interacts perfectly with flask
- use of sqlite3: sqlite3 was chosen as database because it is integrated with Python.

## Contributing

I welcome contributions to improve the web application. If you want to improve something, please create a pull request with a detailed description of the changes.

## Author

- Author: epicwinzer

## Contact

If you have any questions, problems or suggestions, you can contact me by e-mail: webmaster@midlifestudent.de