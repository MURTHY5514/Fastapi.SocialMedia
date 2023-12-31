from .. import models, schemas, oauth2
from fastapi import status, FastAPI, Response, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


# getting all posts


@router.get("/", response_model=List[schemas.PostResponse])
# @router.get("/", response_model=List[schemas.PostOut])
async def get_post(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# creating a post
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # it will store back the added post to new_post
    return new_post


# getting a individual post
@router.get("/{id}", response_model=schemas.PostResponse)
# @router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = (
    #     db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    #     .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #     .group_by(models.Post.id)
    #     .filter(models.Post.id == id)
    #     .first()
    # )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with  id: {id} not found",
        )
    return post


# delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with id: {id} not found",
        )

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with id: {id} not found",
        )
    if updated_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
