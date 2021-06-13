from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String , Integer, Float, ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import CHAR, VARCHAR

Base = declarative_base()

# main code starts here

class UserInput(Base):
    __tablename__ = "userinputs"
    
    id = Column(Integer, primary_key= True)
    patient_id= Column(Integer)
    patient_name= Column(VARCHAR)
    age = Column(Integer)
    location = Column(String)

    def __repr__(self) -> str:
        return f'{self.patient_name}({self.age})'
    
    def __str__(self) -> str:
        return f'{self.patient_name}({self.age})'

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('userinputs.id')) 
    spiral_img_path = Column(String)
    wave_img_path = Column(String)
    predict_date = Column(DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f'{self.patient_name}({self.age})'





if __name__ == "__main__":
    engine = create_engine('sqlite:///project_db.sqlite3')
    Base.metadata.create_all(engine)