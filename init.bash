cd ~/UGV-backend;

source venv/Scripts/activate;
 
python3 manage.py runserver 0.0.0.0:8000 &

python3 DatabaseSync/getSignal.py