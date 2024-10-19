# database.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlite3
import json
from datetime import datetime
from ast_builder import create_ast

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    rule_name = Column(String)  # Rule name
    rule_string = Column(String)  # Original rule string
    ast = Column(Text)  # AST stored as text
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp for creation

# Set up database connection
engine = create_engine('sqlite:///rules.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Function to save a rule
def save_rule(rule_string, ast):
    """Save the rule and its AST to the database."""
    conn = sqlite3.connect('rules.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist with the correct schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT,
            rule_string TEXT NOT NULL,
            ast TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    ''')

    # Convert AST to JSON format before saving
    ast_json = json.dumps(ast.to_dict())

    # Insert rule and its AST
    cursor.execute('''
        INSERT INTO rules (rule_name, rule_string, ast, created_at)
        VALUES (?, ?, ?, ?)
    ''', (None, rule_string, ast_json, datetime.now()))

    conn.commit()
    conn.close()

# Function to modify an existing rule
def modify_rule(rule_id, new_rule_string):
    """
    Modifies an existing rule in the database by rule ID.
    """
    rule = session.query(Rule).filter_by(id=rule_id).first()
    if rule:
        rule.rule_string = new_rule_string
        rule.ast = str(create_ast(new_rule_string))  # Regenerate AST for new rule
        session.commit()
        return rule
    return None
