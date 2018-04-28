# Project review

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

Udacity Full Stack Web Developer Nanodegree program

[Project 4. Flask Item Catalog App](https://github.com/br3ndonland/udacity-fsnd-p4-flask-catalog)

Brendon Smith

br3ndonland

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Reviewer summary](#reviewer-summary)
  - [Fantastic Effort](#fantastic-effort)
- [Code review](#code-review)

## Reviewer summary

### Fantastic Effort

>I really commend you for this project. You have demonstrated great skills, and proven your knowledge in Python, flask and SQLAlchemy.
>
>- Your code is simple to understand and neat.
>- Your use of python docstring is fantastic.
>- Your README file is informative enough to run your application, and excellently written.
>
>You are definitely on the right track. Please take out time to check the Code review for more improvements where necessary.
>
>Wishing you the best in future projects.
>Kind regards :thumbsup:

## Code review

**My project was accepted without required revisions.**

- *[application.py](application.py)*
  - Lines 1-9
    - >**Awesome** Excellent use of python docstrings. It is good to personalise each file, to create distinctiveness. :thumbsup:
  - Lines 10-28
    - >**Awesome** Import module is well formatted.
  - Lines 29-85
    - >**Awesome** Fantastic! JSON is good because It’s lightweight and compact for sending data compared to XML, making it great for mobile apps. It is extremely easy to work with in some languages such as PHP, Python and especially JavaScript.
  - Lines 86-277
    - >**Awesome** Good idea saving the user's state to the database. This will help maintain the user state, and make authentication and authorization easy to handle.
  - Lines 278-297
    - >**Awesome** Helper functions are good because they make your programs easier to read by giving descriptive names to computations. They also let you reuse computations, just as with functions in general.
  - Lines 298-315

    ```python
    @app.route('/add-category', methods=['GET', 'POST'])
    def add_category():
        """App route function to create categories with POST requests."""
        # Verify user login. If not, redirect to login page.
        login_status = None
        if 'email' in login_session:
            login_status = True
        else:
            flash('Please log in.')
            return redirect(url_for('login'))
    ```

    - >**Suggestion** Brilliant idea checking for user login status prior to adding a new category to the database. However, there is another way this can be implemented with less codes:

    ```python
    if "username" not in login_session:
        flash("Please log in")
        return redirect(url_for('login'))
    ```

    - **My response:** This is less code here, but it's more difficult to validate the login session, especially in the HTML templates. The way I have it now, I simply have to type `{% if login_status %}` in the template before any item I only want to be shown on log in.

  - Lines 316-328
    - >**Awesome** Nice! validating input is very important because it streamlines user's activity within a scope of operation, which maintains the integrity of your application.
  - Lines 329-386
    - >**Awesome** Great! Authorization Check is good because it identifies what resources the user can be given during this session. Thus, authorization is sometimes seen as both the preliminary setting up of permissions by a system administrator and the actual checking of the permission values that have been set up when a user is getting access.

  - Lines 387-441
    - >**Awesome** :thumbsup:
  - Lines 442-445

    ```python
        session.delete(category)
    for item in category_items:
        session.delete(item)
    session.commit()
    ```

    - >**Awesome** You have done a very good job here. Many people forget to remove items whenever the parent data associated with that item is deleted. By implementing this line of code, you are protecting the integrity of your application, and ensure that there are no residue data, which may lead to application leak.
  - Lines 446-693
    - >**Awesome** Overall, a very good job well done.
- *[database_data.py](database_data.py)*
  - Lines 40-42 (user data prompt)
    - >**Awesome** :blush: I like this feature.
- *[database_setup.py](database_setup.py)*
  - Overall comment
    - >**Awesome** You have successfully created a valid Entity-Relationship model and each column has meaningful name and proper data type.
- *[README.md](README.md)*
  - Overall comment
    - >**Awesome** This is an *excellent* README. It is detailed enough to guide the user on how to run your application. :clap: