from fastapi import FastAPI, Depends
from src.user.routers import router as router_user
from src.post.routers import router as router_post

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))



app = FastAPI(title='Pastebin')

app.include_router(router_user)
app.include_router(router_post)


