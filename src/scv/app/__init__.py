#!/usr/bin/env python
from .app import app
from . import routers
from .models import db

db.init_app(app)

