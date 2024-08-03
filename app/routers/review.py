import statistics
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from sqlalchemy import select, insert, update
from app.models.review import Rating, Review
from app.schemas import CreateReview
from app.models import *
from app.routers.auth import get_current_user


router = APIRouter(prefix="/reviews", tags=["review"])


async def update_product_rating(db: Annotated[AsyncSession, Depends(get_db)],
                                product_id):
    all_reviews = await db.scalars(
        select(Rating).where(Rating.product_id == product_id)
    )
    await db.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(rating=statistics.mean(review.grade for review in all_reviews))
    )
    await db.commit()


@router.get("/")
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    if reviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no review"
        )
    return reviews.all()


@router.get("/{product_id}")
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_id: int):
    reviews = await db.scalars(select(Review).where(Review.product_id == product_id,
                                                    Review.is_active == True))
    if reviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no review"
        )
    return reviews.all()


@router.post("/add")
async def add_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    create_review: CreateReview,
    get_user: Annotated[dict, Depends(get_current_user)],
):
    if get_user:
        product = await db.scalar(
            select(Product).where(Product.id == create_review.product_id)
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with slug {repr(create_review.product_id)} not found" ',
            )
        await db.execute(
            insert(Rating).values(
                grade=create_review.rating,
                user_id=get_user["id"],
                product_id=product.id,
            )
        )
        rating = await db.scalar(
            select(Rating).where(
                Rating.product_id == product.id, Rating.user_id == get_user["id"]
            )
        )
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed on rating creation",
            )
        await db.execute(
            insert(Review).values(
                user_id=get_user["id"],
                product_id=product.id,
                rating_id=rating.id,
                comment=create_review.comment,
            )
        )
        await db.commit()
        await update_product_rating(db, product.id)
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )


@router.delete("/delete")
async def delete_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    review_id: int,
    get_user: Annotated[dict, Depends(get_current_user)],
):
    review_delete = await db.scalar(select(Review).where(Review.id == review_id))
    if review_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no review found"
        )
    if get_user.get("is_admin"):
        await db.execute(
            update(Review).where(Review.id == review_id).values(is_active=False)
        )
        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Review delete is successful",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )
