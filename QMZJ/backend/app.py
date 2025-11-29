from flask import Flask, jsonify,request,session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from werkzeug.datastructures import Headers
from models import *
from models.modelConfig import db
from config import Config
from datetime import timedelta
from decorators import login_limit
from flask_socketio import SocketIO
from extensions import jwt, socketio
from datetime import timedelta


def create_app():

    # dir_path_base='../frontend/'
    # app = Flask(__name__, static_folder=dir_path_base+'src/assets', template_folder = dir_path_base+"src/components")  
    app = Flask(__name__, static_folder='static')  
    app.config.from_object(Config)
    CORS(app,supports_credentials=True) # 解决跨域服务问题

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)  # 设置 Token 有效期2小时

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    jwt.init_app(app)

    from views.forum import comments
    from views.index import index
    from views.qa import qa
    from views.usercenter import usercenter
    from views.chat import chat_api
    from views.map import maps
    from views.search import search_bp
    from views.timeline import timeline

    app.register_blueprint(search_bp)
    app.register_blueprint(index)
    app.register_blueprint(comments)
    app.register_blueprint(qa)
    app.register_blueprint(usercenter)
    app.register_blueprint(chat_api)
    app.register_blueprint(maps)
    app.register_blueprint(timeline)

    @app.before_request
    def load_token():
        headers = Headers(request.headers)
        headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
        headers.add('Access-Control-Allow-Credentials', 'true')
        token = request.cookies.get('access_token')
        if token:
            headers['Authorization'] = f'Bearer {token}'
            request.headers = headers

    return app

app = create_app()

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000)  # 监听所有网络接口
    # app.run(host='0.0.0.0', port=5000)