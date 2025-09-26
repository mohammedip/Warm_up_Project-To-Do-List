from sqlalchemy import Table,Column,Integer,String
from db import metadata

tasks = Table('tasks' ,
                    metadata ,
                    Column('id' , Integer , primary_key=True,autoincrement=True),
                    Column('description' , String(255), nullable=False),
                    Column('priorite' , String(50) ,default="Medium"),
                    Column('statut' , String(50), default="To do")
                   )