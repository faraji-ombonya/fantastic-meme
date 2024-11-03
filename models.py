from typing import List, Optional
from sqlalchemy import JSON, String, DateTime, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(unique=True)
    content: Mapped[dict] = mapped_column(JSON)
    source: Mapped[str]
    is_posted: Mapped[bool] = mapped_column(default=False)
    
    
engine = create_engine("sqlite:///sqlite.db")

Base.metadata.create_all(engine)


class PostManager():
    def __init__(self) -> None:
        pass

    def create(*args, **kwargs) -> Post:
        with Session(engine) as session:
            post = Post(
                slug = kwargs.get("slug"),
                content = kwargs.get("content"),
                source = kwargs.get("source"),
            )
            session.add(post)
            session.commit()
            return post
        
    def get_post(self, id: int) -> Post:
        """Get post by id."""
        with Session(engine) as session:
            stmt = select(Post).where(Post.id == id)
            post = session.scalars(stmt).one()
            return post
        
    def get_post_by_slug(self, slug: str) -> Post:
        """Get post by slug."""
        with Session(engine) as session:
            stmt = select(Post).where(Post.slug == slug)
            post = session.scalars(stmt).one()
            return post
        
    def get_pending_posts(self, source: str) -> list[Post]:
        """Get pending posts from a specified source."""
        with Session(engine) as session:
            stmt = (
                select(Post)
                .where(Post.is_posted == False)
                .where(Post.source == source)
            )
            posts = session.scalars(stmt).all()
            return posts

    def bulk_create(self, posts: list[Post]) -> None:
        """Create posts in bulk."""
        with Session(engine) as session:
            new_posts: list[Post] = []
            for post in posts:
                # Check if the post exists.
                stmt = select(Post).where(Post.slug == post.slug)
                exists = session.scalar(stmt)

                # If it exists, go to the next post.
                if exists:
                    continue

                # Otherwise add to new posts list.
                new_posts.append(post)

            # Then do a bulk insert.
            session.add_all(new_posts)
            session.commit()

    def mark_as_posted(self, post_id):
        """Mark a post as posted."""
        with Session(engine) as session:
            stmt = select(Post).where(Post.id == post_id)
            post = session.scalars(stmt).one()
            post.is_posted = True
            session.commit()
