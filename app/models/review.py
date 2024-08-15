import datetime
from sqlalchemy import Boolean, Date, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.backend.db import Base
from app.models.products import Product
from app.models.user import User


class Rating(Base):
    """
    id: Числовое поле, являющееся первичным ключом.
    grade: Числовое поле оценки товара.
    user_id: Поле связи с таблицей пользователей.
    product_id: Поле связи с таблицей товара.
    is_active: Булево поле, по умолчанию True.
    """
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grade: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    reviews: Mapped[list["Review"]] = relationship(back_populates="rating")
    product: Mapped["Product"] = relationship(back_populates="ratings")


class Review(Base):
    """
    id: Числовое поле, являющееся первичным ключом.
    user_id: Поле связи с таблицей пользователей.
    product_id: Поле связи с таблицей товара.
    rating_id: Поле связи с таблицей рейтинга
    comment: Текстовое поле отзыва о товаре.
    comment_date: Поле даты отзыва, по умолчанию заполняется автоматически.
    is_active: Булево поле, по умолчанию True.
    """

    __tablename__ = "review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    rating_id: Mapped[int] = mapped_column(Integer, ForeignKey('rating.id'))
    comment: Mapped[str] = mapped_column(String)
    comment_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.datetime.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    product: Mapped["Product"] = relationship(back_populates="reviews")
    rating: Mapped["Rating"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")
