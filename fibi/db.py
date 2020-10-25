from sqlalchemy import Column, String

from fibi.main import Base


class User(Base):
    __tablename__ = 'user'
    fitbit_user_id = Column(String, primary_key=True)
    access_token = Column(String)
    refresh_token = Column(String)

    def __repr__(self):
        return "<User('%d', '%s')>" % (self.fitbit_user_id, self.name)
