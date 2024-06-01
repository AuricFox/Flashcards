from flask import Flask, render_template
import os, logging

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

    Parameter(s):
        configure (default='config.DevConfig'): app environment configuration

    Output(s):
        app (Object): flask application object
    '''
    app = Flask(__name__, instance_relative_config=False)
    # Configured for development
    app.config.from_object(configure)

    # Custom page not found
    def page_not_found(error):
        '''
        Builds and returns an html page that displays the categories and the number of questions in 
        each category.

        Parameter(s): None

        Output(s):
            a built html page that displays the categories and their count
        '''
        # Query database for all categories and their counts
        categories = database.view_allcategories()

        return render_template('404.html', nav_id="home-page", categories=categories), 404

    with app.app_context():
        # NOTE: Include routes and custom modules here
        from . import database, utils

        from app.main import bp as main_bp
        from app.manage import bp as manage_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(manage_bp, url_prefix='/manage')
        app.register_error_handler(404, page_not_found)

    return app