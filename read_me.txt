1- Kindly, add MySQL Tables to your database schema
you will find them in the MySQL folder

Notes about the database: 
- publications_tab table has the same values that publications_tab_2018 
which both are vectorized from 2018.xlsx file 
thats why i have created the strategy of getting the value the four years and save them in 4 tables
instead of loading them each time you run the project which will impact very very much time "can reach 1 hour for 1 query" 

- candidate table stores the results the we got from SciBert2 model and paths for plots 
Please don't change any of that 

- plots path is /static/img/ keep it as it is anywhere you see  


2- install requirements through 
pip install -r requirements.txt

3- Change path in model.py
model = gensim.models.KeyedVectors.load_word2vec_format(datapath(path), binary=False)

4- Change password and port in mysql_manager.py
PASSWORD = ""
PORT = ""

5- Change image_path in main.py to \static\img full path

6- in app.py 
- change mysql config to your configuration

7- HTML files have been changed, please update them

Notes 
- you have 2 folders SciBERT and MatchJobSystem 
- all updated files exist in MatchJobSystem which you will need to add them in there for run the website
- some updated files for the SciBERT project are added there where you can test the model sperately from the website

once you follow all instructions you can run the model, for any issue please refer to me.