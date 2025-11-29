from gevent import monkey
monkey.patch_all()

from app import app
from extensions import socketio

if __name__ == "__main__":
    # app.run(debug = True)  # debug = True
    # socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000)  # 监听所有网络接口
