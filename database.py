# -*- coding: utf8 -*-
from pymongo import MongoClient

#initialisation du client et de la BDD
client = MongoClient()
database = client.blogware_db

#"création" des divers bases de données

articles = database.articles
admin_logins = database.admin_logins

