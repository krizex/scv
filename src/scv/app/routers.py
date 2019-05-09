from .app import app
from .views import display_sales_data


@app.route('/')
@app.route('/index')
def index():
    return display_sales_data()
