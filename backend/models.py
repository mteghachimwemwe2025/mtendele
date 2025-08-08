from flask_login import UserMixin
from backend.extensions import db
from datetime import datetime,date

session = db.session  # Optional shortcut


# ------------------- USERS -------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    reg_number = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def get_id(self):
        return self.reg_number

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_lecturer(self):
        return self.role == 'teacher'

    @property
    def is_admin(self):
        return self.role == 'admin'


# ------------------- ACTIVITIES -------------------
class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)

    program = db.relationship('Program', backref=db.backref('activities', lazy=True))


# ------------------- CATEGORIES -------------------
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# ------------------- PROGRAMS -------------------
class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)


# ------------------- NEWS -------------------
class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    category = db.relationship('Category', backref=db.backref('news', lazy=True))


# ------------------- MESSAGES -------------------
class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('unread', 'read', 'replied'), default='unread', nullable=False)

class Sermon(db.Model):
    __tablename__ = 'sermon'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    speaker = db.Column(db.String(255))
    date = db.Column(db.String(50))
    scripture = db.Column(db.String(255))
    description = db.Column(db.Text)
    media = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    image = db.Column(db.String(255))
    youtube_url = db.Column(db.String(255), default="N/A")
    
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=True)  # 🆕 Link to Series

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "speaker": self.speaker,
            "date": self.date,
            "scripture": self.scripture,
            "description": self.description,
            "media": self.media,
            "notes": self.notes,
            "image": self.image,
            "youtube_url": self.youtube_url or "N/A",
            "series_id": self.series_id,
        }

class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    # Relationship: one series has many sermons
    sermons = db.relationship("Sermon", backref="series", lazy=True)

class ResourceCategory(db.Model):
    __tablename__ = 'resource_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    resources = db.relationship('Resource', backref='category', cascade='all, delete-orphan')

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('resource_categories.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(255), nullable=True)  # file path or URL
    date = db.Column(db.Date, default=date.today, nullable=True)
class Ministry(db.Model):
    __tablename__ = 'ministries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ministry_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    meeting_time = db.Column(db.String(50), nullable=True)
    meeting_days = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Ministry {self.ministry_name}>"
class Testimony(db.Model):
    __tablename__ = 'testimonies'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    approve = db.Column(db.Enum('yes', 'no'), nullable=True)
    time = db.Column(db.Time, nullable=True)
    date = db.Column(db.Date, nullable=True)