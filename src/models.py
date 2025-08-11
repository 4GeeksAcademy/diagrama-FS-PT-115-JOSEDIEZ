from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    following: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.user_from_id]",
        back_populates="follower"
    )

    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.user_to_id]",
        back_populates="followed"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)

    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_from_id],
        back_populates="following"
    )

    followed: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_to_id],
        back_populates="followers"
    )

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    texto: Mapped[str] = mapped_column(nullable = False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey('post.id'), nullable = False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),nullable = False
    )    
