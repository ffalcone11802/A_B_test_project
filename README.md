# Bachelor's Thesis Project

<h3>Overall information</h3>
<i>Title:</i> Design and development of a backend infrastructure for A/B testing of recommendation models<br/>
<i>Author:</i> Francesco Falcone<br/>
<i>Course:</i> Ingegneria Informatica e dell’Automazione (D.M. 270)<br/>
<i>Subject:</i> Ingegneria del Software e Fondamenti Web<br/>
<i>Supervisor:</i> Prof. Ing. Antonio Ferrara
<i>Academic year:</i> 2023-2024<br/>

<h3>Instructions</h3>
<p>Run <strong>python manage.py runserver</strong> to start the server.</p>
<p>Run <strong>python training_scheduler.py</strong> in a separate tab to start the training scheduler, which trains the models every day at 00:00.</p>
<p>Make a GET request to <strong><i>/api</i></strong> in order to get the list of all the available API paths.</p>
<p>When using unsafe methods (POST, PUT, PATCH, DELETE) and authentication credentials are required, you have to also provide the <strong>CSRF Token</strong> sent in a cookie after the login.</p>