import cloudinary as cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote

# from flask_babelex import Babel


app = Flask(__name__, template_folder='template')
app.secret_key = "!@#$%^&*()"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/maybaydb?charset=utf8mb4' % quote(
    'Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'
cloudinary.config(cloud_name='dbqaequqv',
                  api_key='741317942552615',
                  api_secret='L05czfd2tdEhRvbUy29A1vF8BZ4')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

gio_mua_toi_da = 12
gio_ban_toi_da = 4
thoi_gian_bay_toi_thieu = 1
san_bay_trung_gian_toi_da = 5
thoi_gian_dung_toi_da = 2
thoi_gian_dung_toi_thieu = 0.1

# babel = Babel(app=app)
# @babel.localeselector
# def load_locale():
#     return 'vi'
