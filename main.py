from fastapi import FastAPI, status, HTTPException
from schema import Post

app = FastAPI()

posts = []

@app.get("/post", status_code=status.HTTP_200_OK)
def get_post():
    return posts

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(newPost: Post):
    try:
        for post in posts:
            if post.id == newPost.id:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="resource already exists")
        posts.append(newPost)
        return {"message": f"post created: {newPost}", "status": "created"}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error while creating the post{str(e)}")


@app.put("/post/{id}", status_code= status.HTTP_200_OK)
def update_post(id: int, updatedPost: Post):
    try:
        for index,post in enumerate(posts):
            if post.id == id:
                posts[index] = updatedPost
                return {"message": f"post updated: {updatedPost}", "status": "updated"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.delete("/post/{id}", status_code= status.HTTP_200_OK)
def delete_post(id: int):
    try:
        for index, post in enumerate(posts):
            if post.id == id:
                deletedPost = posts.pop(index)
                return {"message": f"post deleted: {deletedPost}"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

