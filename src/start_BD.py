from src.post.posts import create_tables, insert_post
from src.user.users import insert_user


def start():
    create_tables()
    insert_user()
    insert_post()


start()