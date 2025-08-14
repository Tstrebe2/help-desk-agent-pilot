from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine

def create_db_toolkit(db_path, llm):
    engine = create_engine(f"sqlite:///{db_path}")
    db = SQLDatabase(engine)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return toolkit