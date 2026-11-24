"""
gunicorn_config.py – Gunicorn configuration for StudyTrack.
Starts the APScheduler when the app is preloaded.
"""

import os

# Bind to the app port
bind = "0.0.0.0:8085"

# Single worker to avoid duplicate scheduler jobs
workers = 1
threads = 2

# Preload the app so the scheduler starts once
preload_app = True

# Access log
accesslog = "-"
errorlog = "-"
loglevel = "info"


def on_starting(server):
    """Called just before the master process is initialized."""
    pass


def post_fork(server, worker):
    """Called after a worker has been forked – start the scheduler here."""
    from app import app
    from scheduler import init_scheduler
    init_scheduler(app)
