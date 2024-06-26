from flask import Flask, render_template
import os, logging

from app.extensions import db
from flask_wtf.csrf import CSRFProtect

PATH = os.path.dirname(os.path.abspath(__file__))

# Configure the logging object
logging.basicConfig(
    filename=os.path.join(PATH, '../logs/app.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

LOGGER = logging.getLogger(__name__)

def init_app(configure='config.DevConfig'):
    '''
    Initializes the flask application
    NOTE: Configured for development

    Parameter(s):
        configure (default='config.DevConfig'): app environment configuration

    Output(s):
        app (Object): flask application object
    '''
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(configure)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    CSRFProtect(app)

    from app.models.flashcard_model import view_all_categories

    # Custom page not found
    @app.errorhandler(404)
    def page_not_found(e):
        '''
        Builds and returns an html page that displays the categories and the number of questions in 
        each category.

        Parameter(s): None

        Output(s):
            a built html page that displays the categories and their count
        '''
        # Query database for all categories and their counts
        categories = view_all_categories()

        return render_template('404.html', nav_id="home-page", categories=categories), 404

    with app.app_context():
        # NOTE: Include routes and custom modules here
        from . import utils

        from app.main import bp as main_bp
        from app.manage import bp as manage_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(manage_bp, url_prefix='/manage')
        app.register_error_handler(404, page_not_found)

    return app