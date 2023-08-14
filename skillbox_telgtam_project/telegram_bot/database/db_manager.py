from sqlalchemy.orm import Session
from .models import User, Search, session
from datetime import datetime


class DBManager:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, user_id: int, username: str, lastname: str, firstname: str):
        user = User(id=user_id, username=username, lastname=lastname, firstname=firstname)
        self.session.add(user)
        self.session.commit()

    def get_user_by_id(self, user_id: str):
        return self.session.query(User).filter_by(id=user_id).first()

    def add_search_result(self, user_id: int, title: str, price: float, promotion_price: float, url: str, image):
        search = Search(title=title, price=float(price), promotion_price=promotion_price, date=datetime.utcnow(),
                        user_id=user_id, url=url, image_url=image)
        self.session.add(search)
        self.session.commit()

    def get_search_results_by_user(self, user_id: int):
        return self.session.query(Search).filter_by(user_id=user_id).all()


db_manager = DBManager(session=session)
