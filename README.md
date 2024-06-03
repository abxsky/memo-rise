Note:
Le projet n'est pas dockeriser, pour run le backend il faut:
python, pipenv ou miconda:
aprés avoir clone, fork ou telecharger depuis un terminal shell run les commandes suivante:

Backend:
//dans le dossier root(backend/memorise_server/)
1 pipenv install
2 pipenv shell
3 python manage.py makemigrations
4 python manage.py migrate
5 python manage.py runserver 8000

voici la liste des APIs disponibles:
    "books": "http://127.0.0.1:8000/store/books/",
    "categories": "http://127.0.0.1:8000/store/categories/",
    "carts": "http://127.0.0.1:8000/store/carts/",
    "customers": "http://127.0.0.1:8000/store/customers/",
    "orders": "http://127.0.0.1:8000/store/orders/"
    "users": "http://127.0.0.1:8000/auth/users/"
    "user": "http://127.0.0.1:8000/auth/users/me"
    
vous ne pourrez pas accedez tous les routes car certains on besoin d'une permission adminr/staff ou une authintification.
Pour acceder a l'espace admin : http://127.0.0.1:8000/admin/
id : admin
mdp : admin

Frontend:
il faut avoir dart et flutter sdk d'installer et dans le root du dossier 'frontend/memorise_client' run les commandes:
1 flutter config --enable-web
2 flutter run -d chrome



