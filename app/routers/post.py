from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import model, schemas, oauth2
from ..database import get_db, engine
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)

model.Base.metadata.create_all(bind=engine)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db), limit: int = 5, skip: int = 0, search: Optional [str] = ""):
    # print(f"Fetching posts for user_id: {user_id}")
    posts = db.query(model.Post).filter (model.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(model.Post).filter(model.Post.user_id == user_id).all()
    return posts    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = model.Post(**post.dict(), user_id=user_id)
    # new_post = model.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#get on individual post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user) ): #path parameter 
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation")
   
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_query  = db.query(model.Post).filter(model.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} not found")
    
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation")
    
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()