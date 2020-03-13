from werkzeug.security import generate_password_hash, check_password_hash
# from flask_rbac import RoleMixin, UserMixin
from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    passwordHash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    @property
    def password(self):
        raise AttributeError("Error: Password is not readable attribute")

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def activate(self):
        self.isActive = True


# role_parents = db.Table(
#     role_parents,
# )


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic",
                            cascade="all, delete-orphan")
