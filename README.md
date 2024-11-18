# Bachelor's Thesis Project
<h3>Design and development of a backend infrastructure for A/B testing of recommendation models</h3>

#
<h3>Overall information</h3>
<i>Author:</i> Francesco Falcone<br/>
<i>University:</i> Politecnico di Bari<br/>
<i>Department:</i> Dipartimento di Ingegneria Elettrica e dell'Informazione<br/>
<i>Course:</i> Ingegneria Informatica e dell’Automazione<br/>
<i>Subject:</i> Ingegneria del Software e Fondamenti Web<br/>
<i>Supervisor:</i> Prof. Ing. Antonio Ferrara<br/>
<i>Academic year:</i> 2023-2024<br/>

#
<h3>Instructions</h3>
<p>Run <strong>python manage.py runserver</strong> to start the server.</p>
<p>Run <strong>python training_scheduler.py</strong> in a separate tab to start the training scheduler, which trains the models every day at 00:00.</p>
<p>Make a GET request to <strong><i>/api</i></strong> in order to get the list of all the available API paths.</p>
<p>When using unsafe methods (POST, PUT, PATCH, DELETE) and authentication credentials are required, you also have to provide the <strong>CSRF Token</strong> sent in a cookie after the login.</p>