from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///rules.db')
Base = declarative_base()

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    rule_string = Column(String)
    ast = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_rule(rule_string, ast):
    new_rule = Rule(rule_string=rule_string, ast=str(ast))
    session.add(new_rule)
    session.commit()
