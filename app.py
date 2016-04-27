"""Singleton module so everything can get a handle to the Flask app"""
import flask

app = None

def init(*args, **kwargs):
  global app

  app = flask.Flask(*args, **kwargs)

