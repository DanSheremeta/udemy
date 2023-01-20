# IMDB API Clone With DRF

A REST api written in Django

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```bash
        $ pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/DanSheremeta/udemy.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd watchmate
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ python -m venv env
            $ venv/Scripts/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ python manage.py runserver
    ```
    You can now access the file api service on your browser by using
    ```
        http://localhost:8000/
    ```
    
## All end-points:

<b>1. Admin Access</b>
<ul>
    <li>Admin Section: http://127.0.0.1:8000/dashboard/</li>
</ul>
<br>

<b>2. Accounts</b>
<ul>
    <li>Registration: http://127.0.0.1:8000/api/account/register/</li>
    <li>Login: http://127.0.0.1:8000/api/account/login/</li>
    <li>Logout: http://127.0.0.1:8000/api/account/logout/</li>
</ul>
<br>

<b>3. Stream Platforms</b>
<ul>
    <li>Create Element & Access List: http://127.0.0.1:8000/api/watch/stream/</li>
    <li>Access, Update & Destroy Individual Element: http://127.0.0.1:8000/api/watch/stream/&lt;int:streamplatform_id&gt;/</li>

</ul>
<br>

<b>4. Watch List</b>
<ul>
    <li>Create & Access List: http://127.0.0.1:8000/api/watch/</li>
    <li>Access, Update & Destroy Individual Element: http://127.0.0.1:8000/api/watch/&lt;int:movie_id&gt;/</li>
</ul>
<br>

<b>5. Reviews</b>
<ul>
    <li>Create Review For Specific Movie: http://127.0.0.1:8000/api/watch/&lt;int:movie_id&gt;/reviews/create/</li>
    <li>List Of All Reviews For Specific Movie: http://127.0.0.1:8000/api/watch/&lt;int:movie_id&gt;/reviews/</li>
    <li>Access, Update & Destroy Individual Review: http://127.0.0.1:8000/api/watch/reviews/&lt;int:review_id&gt;/</li>
</ul>
<br>

<b>6. User Review</b>
<ul>
    <li>Access All Reviews For Specific User: http://127.0.0.1:8000/api/watch/user-reviews/?username=example</li>
</ul>
<br>
