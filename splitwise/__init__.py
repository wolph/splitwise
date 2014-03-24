__all__ = [
    'app',
    'views',
]

# Import and initialize the app before anything else gets imported to prevent
# circular imports. DO NOT MOVE OTHER IMPORTS BEFORE THIS!
from splitwise import application
app = application.get_app()

from splitwise import views

