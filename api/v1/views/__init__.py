from flask import Blueprint

classes = {'documents':'Document', 'students':'Student', "courses":'Course', 'departments':'Department'}
app_views = Blueprint('views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.documents import *
from api.v1.views.courses import *
from api.v1.views.students import *
from api.v1.views.departments import *
from api.v1.views.auth import *
