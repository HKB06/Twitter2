from .auth import router as auth_router
from .tweet import router as tweet_router
from .bookmark import router as bookmark_router
from .comment import router as comment_router


# Liste des routers
routers = [auth_router, tweet_router, bookmark_router, comment_router]
