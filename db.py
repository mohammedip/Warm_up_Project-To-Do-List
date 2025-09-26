from sqlalchemy import create_engine,MetaData,insert,select,delete,values,update

connection_string = f"postgresql://postgres:124@localhost:5432/postgres"
engine = create_engine(connection_string)

metadata = MetaData()