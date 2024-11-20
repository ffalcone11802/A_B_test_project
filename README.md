# Design and development of a backend infrastructure for A/B testing of recommendation models
<h3>Bachelor's Thesis Project</h3>

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
<h3>Configuration</h3>
<p>Create your <strong>PostgreSQL</strong> database (minimum required version == 14.0).</p>
<p>Create your <strong>TMDB</strong> app.</p>
<p>Create the <strong>.env</strong> file in <i>A_B_test_project</i> and put in it your Django SECRET_KEY, your TMDB API_KEY and your PostgreSQL database connection params.</p>
<p>Create a <strong>superuser</strong> in order to manage the app from the admin panel.</p>
<p>Run <strong>python manage.py import_users</strong> and <strong>python manage.py import_ratings</strong> in order to import users and initial ratings into the database.</p>
<p>Put in <i>config_files/A_B_test_config.yml</i> Elliot models you want to use:
<ul>
    <li>only models based on Collaborative Filtering or the unpersonalized ones are allowed.</li>
    <li>the last one will be set as the default one, and it will not be used for the test, so be sure to put at least three of them.</li>
</ul>


#
<h3>Usage</h3>
<p>Run <strong>python manage.py runserver</strong> to start the server and train the models.</p>
<p>Run <strong>python training_scheduler.py</strong> in a separate tab to start the training scheduler, which trains the models every day at 00:00.</p>
<p>Make a GET request to <i>/api</i> in order to get the list of all the available API paths.</p>
<p>When using unsafe methods (POST, PUT, PATCH, DELETE) and authentication credentials are required, you also have to provide the <strong>CSRF Token</strong> sent in a cookie after the login.</p>