import datetime
import os
import sys

from flask import Flask, jsonify
import sqlalchemy as db
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_SERVER = os.getenv("database_server")
DATABASE_USER = os.getenv("database_user")
DATABASE_PASSWORD = os.getenv("database_password")
DAYS_TO_RETURN = os.getenv("days_to_return")

class Backups(Base):
    __tablename__ = "Backup.Model.BackupTaskSessions"

    id = Column(String, primary_key=True)
    creation_time = Column(DateTime)
    object_name = Column(Text)
    status = Column(Integer)
    reason = Column(Text)
    end_time = Column(DateTime)

    def __repr__(self):
        return '<Backup {}>'.format(self.id)

app = Flask(__name__)
engine = db.create_engine(
    'mssql+pyodbc://{}:{}@{}/VeeamBackup?driver=ODBC+Driver+13+for+SQL+Server'.format(
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_SERVER
    )
)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/backups')
def backup():
    date_filter = datetime.datetime.utcnow() - datetime.timedelta(days=int(DAYS_TO_RETURN))
    backups = session.query(Backups).order_by(Backups.creation_time).filter(Backups.creation_time > date_filter)
    session.close()
    out = []
    for backup in backups:
        out.append(
            {
                'id': backup.id,
                'creation_time': backup.creation_time,
                'object_name': backup.object_name,
                'status': backup.status,
                'reason': backup.reason,
                'end_time': backup.end_time
            }
        )
    return jsonify(out)

@app.route('/backups/<id>')
def backup_by_id(id):
    date_filter = datetime.datetime.utcnow() - datetime.timedelta(days=int(DAYS_TO_RETURN))
    backups = session.query(Backups).order_by(Backups.creation_time).filter(Backups.creation_time > date_filter).filter(Backups.object_name==id)
    session.close()
    out = []
    for backup in backups:
        out.append(
            {
                'id': backup.id,
                'creation_time': backup.creation_time,
                'object_name': backup.object_name,
                'status': backup.status,
                'reason': backup.reason,
                'end_time': backup.end_time
            }
        )
    return jsonify(out)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8888')
