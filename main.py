from fastapi import FastAPI, status, HTTPException, Depends
from schema import PostCreate, PostResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from deps import create_db_and_table, get_db
from models import Post
from typing import List
from uuid import UUID

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/post", response_model=PostResponse)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    try:
        newPost = Post(
            title = post.title,
            content = post.content
        )
        db.add(newPost)
        await db.commit()
        await db.refresh(newPost)

        return newPost
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@app.get("/post", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Post))
    return res.scalars().all()

@app.put("/post/{id}", response_model=PostResponse)
async def update_post(id: UUID, newpost: PostCreate, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(select(Post).where(Post.id == id))
        post = res.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with entered ID")
        post.title = newpost.title
        post.content = newpost.content
        await db.commit()
        await db.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@app.delete("/post/{id}", response_model=PostResponse)
async def delete_post(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(select(Post).where(Post.id == id))
        post = res.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with entered ID")
        await db.delete(post)
        await db.commit()
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


# posts = []

# @app.get("/post", status_code=status.HTTP_200_OK)
# def get_post():
#     return posts

# @app.post("/post", status_code=status.HTTP_201_CREATED)
# def create_post(newPost: Post):
#     try:
#         for post in posts:
#             if post.id == newPost.id:
#                 raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="resource already exists")
#         posts.append(newPost)
#         return {"message": f"post created: {newPost}", "status": "created"}
#     except Exception as e:
#         return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error while creating the post{str(e)}")


# @app.put("/post/{id}", status_code= status.HTTP_200_OK)
# def update_post(id: int, updatedPost: Post):
#     try:
#         for index,post in enumerate(posts):
#             if post.id == id:
#                 posts[index] = updatedPost
#                 return {"message": f"post updated: {updatedPost}", "status": "updated"}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# @app.delete("/post/{id}", status_code= status.HTTP_200_OK)
# def delete_post(id: int):
#     try:
#         for index, post in enumerate(posts):
#             if post.id == id:
#                 deletedPost = posts.pop(index)
#                 return {"message": f"post deleted: {deletedPost}"}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")