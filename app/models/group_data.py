from ..database import db

class Group_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    lessons = db.Column(db.LargeBinary)
    def __repr__(self):
        return f"<group {self.id}>"