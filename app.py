from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    CORS(app)
    
    # Register learning blueprint
    from learning import learning_bp
    app.register_blueprint(learning_bp, url_prefix='/learning')
    
    # Register API blueprint
    from api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app