from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randint 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"title of post1", "content":"content of post1", "id":1},{"title":"title of post2", "content":"content of post2", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

#path operation function -- route 
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randint(1,10000)
    my_posts.append(post_dict)
    return {"data":post_dict}

#get on individual post
@app.get("/posts/{id}")
def get_post(id: int): #path parameter 
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} not found")
    print(post)
    return{"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            my_posts.remove(p)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} not found")

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for p in my_posts:
        if p['id'] == id:
            p['title'] = post.title
            p['content'] = post.content
            return {"data": p}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} not found")