from fastapi import FastAPI , HTTPException
from app.schemas import  PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {
        "title": "Clean Code",
        "content": "Robert C. Martin explains how to write readable, maintainable, and professional code through practical principles and real-world examples."
    },
    2: {
        "title": "The Pragmatic Programmer",
        "content": "Andrew Hunt and David Thomas share timeless advice on craftsmanship, problem-solving, and continuous learning as a software engineer."
    },
    3: {
        "title": "Designing Data-Intensive Applications",
        "content": "Martin Kleppmann explores databases, distributed systems, scalability, and reliability in modern software architecture."
    },
    4: {
        "title": "Refactoring",
        "content": "Martin Fowler demonstrates how to improve existing code without changing its external behavior, making systems easier to understand and extend."
    },
    5: {
        "title": "Domain-Driven Design",
        "content": "Eric Evans introduces strategic and tactical design patterns for managing complex business domains."
    },
    6: {
        "title": "Working Effectively with Legacy Code",
        "content": "Michael Feathers provides techniques for safely modifying legacy systems by introducing tests and reducing technical debt."
    },
    7: {
        "title": "Accelerate",
        "content": "Nicole Forsgren, Jez Humble, and Gene Kim present research-backed practices that improve software delivery performance."
    },
    8: {
        "title": "Real-World Software Development",
        "content": "Raoul-Gabriel Urma and Richard Warburton teach modern Java, clean architecture, testing, and maintainable application design."
    },
    9: {
        "title": "Test-Driven Development: By Example",
        "content": "Kent Beck introduces TDD by demonstrating how writing tests first leads to better software design and confidence."
    },
    10: {
        "title": "Building Microservices",
        "content": "Sam Newman explains how to design, deploy, and maintain scalable microservice-based systems while avoiding common pitfalls."
    }
}


@app.get("/posts")
def get_all_post(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/post/{id}")
def get_post(id: int)-> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, details="Post not found")
    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post



