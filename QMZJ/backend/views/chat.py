from flask import Blueprint, request, jsonify
from zhipuai import ZhipuAI
from decorators import login_limit
from models.Message import Message, Conversation
from models.modelConfig import db
import uuid  # 生成唯一ID
from extensions import socketio
from flask_socketio import emit
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
import requests

BIGMODEL_API_KEY = "64661646507f4886af8bda4d2928e21b.RIQSS2ebNaX4yVAr"
BIGMODEL_APP_ID = "1923383444797325312"
BIGMODEL_BASE_URL = "https://open.bigmodel.cn/api/llm-application/open" # https://appcenter.bigmodel.cn/console/appcenter_v2/chat?share_code=joJv9n4c_-GMEaSsY4Ekq

chat_api = Blueprint("chat", __name__, url_prefix="/api/chat")

def create_conversation():
    url = f"{BIGMODEL_BASE_URL}/v2/application/{BIGMODEL_APP_ID}/conversation"
    headers = {"Authorization": f"Bearer {BIGMODEL_API_KEY}"}
    response = requests.post(url, headers=headers)
    return response.json()["data"]["conversation_id"]

def invoke_chat(conversation_id, user_message):
    url = f"{BIGMODEL_BASE_URL}/v3/application/invoke"
    headers = {
        "Authorization": f"{BIGMODEL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": BIGMODEL_APP_ID,
        "conversation_id": conversation_id,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input",
                        "value": user_message
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result["choices"][0]["messages"]["content"]["msg"]

def verify_jwt_token(token):
    try:
        decoded_token = decode_token(token)
        return decoded_token
    except Exception as e:
        return None

def get_history_by_ID(conversation_id=None, user_id=None):
    """
    根据 conversation_id 或 user_id 获取聊天记录
    """
    if conversation_id is None and user_id is not None:
        # 查询用户的所有对话
        conversations = Conversation.query.filter_by(user_id=user_id).all()
        conversation_history = [
            {
                "conversation_id": conv.id,
                "messages": [{"role": msg.role, "content": msg.content} for msg in Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp).all()]
            }
            for conv in conversations
        ]
    elif conversation_id is not None:
        # 查询特定对话的所有消息
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
        conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages]
    else:
        conversation_history = []

    return conversation_history

@socketio.on('chat')
def handle_chat(data):
    """
    处理 WebSocket 方式的聊天请求
    """
    # print("handle_chat")
    # try:
    token = data['token']
    if not token:
        return False
    user_id = verify_jwt_token(token)['sub']
    # print("user_id", user_id)
    user_message = data['userMessage']['content']
    conversation_id = data['userMessage']['conversation_id']

    # # 调用 ZhipuAI API
    # response = client.chat.completions.create(
    #     model="glm-4-plus",
    #     messages=conversation_history + [{"role": "user", "content": user_message}],
    #     stream=True,  # WebSocket 使用流式传输
    # )

    # ai_reply = ''.join(chunk.choices[0].delta.content for chunk in response)
    ai_reply = invoke_chat(conversation_id, user_message)

    # 记录消息
    user_message_record = Message(conversation_id=conversation_id, role='user', user_id=user_id, content=user_message)
    ai_message_record = Message(conversation_id=conversation_id, role='assistant', user_id=user_id, content=ai_reply)

    db.session.add(user_message_record)
    db.session.add(ai_message_record)
    db.session.commit()

    emit('chat_response', {'response': ai_reply, 'status': 'success'})

    # except Exception as e:
        # db.session.rollback()
        # emit('chat_response', {'error': str(e), 'status': 'fail'})

@chat_api.route('/history', methods=['POST'])
@login_limit
def get_history():
    """
    获取用户的历史对话
    """
    try:
        conversation_id = request.args.get('conversation_id', None)
        # print("conversation_id", conversation_id)
        user_id = get_jwt_identity()
        conversation = get_history_by_ID(conversation_id, user_id)
        return jsonify({'history': conversation, 'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'fail'}), 400

@chat_api.route('/conversations', methods=['GET'])
@login_limit
def get_conversations():
    """
    获取用户所有的会话
    """
    # print("get_conversations")
    # try:
    user_id = get_jwt_identity()
    # print("user_id", user_id)
    conversations = Conversation.query.filter_by(user_id=user_id, is_pet=False).order_by(Conversation.created_at.desc()).all()

    # print("conversations", conversations)

    conversation_list = [
        {
            'id': conv.id,
            'preview': Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp).first().content[:10] if Message.query.filter_by(conversation_id=conv.id).count() > 0 else '历史对话'
        }
        for conv in conversations
    ]
    return jsonify({'conversations': conversation_list, 'status': 'success'})

    # except Exception as e:
        # return jsonify({'error': str(e), 'status': 'fail'}), 400

@chat_api.route('/pet_chat', methods=['GET'])
@login_limit
def pet_chat():
    """
    获取用户和小精灵的会话
    """
    try:
        user_id = get_jwt_identity()
        # print("user_id", user_id)
        conversations = Conversation.query.filter_by(user_id=user_id, is_pet=True).order_by(Conversation.created_at.desc()).all()

        # print("conversations", conversations)

        conversation_list = [
            {
                'id': conv.id,
                'is_pet': conv.is_pet,
                'preview': Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp).first().content[:10] if Message.query.filter_by(conversation_id=conv.id).count() > 0 else '历史对话'
            }
            for conv in conversations
        ]
        return jsonify({'conversations': conversation_list, 'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'fail'}), 400

def create_bigmodel_conversation():
    url = f"{BIGMODEL_BASE_URL}/v2/application/{BIGMODEL_APP_ID}/conversation"
    headers = {
        "Authorization": f"Bearer {BIGMODEL_API_KEY}"
    }
    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    return resp.json()['data']['conversation_id']

@chat_api.route('/new_conversations', methods=['POST'])
@login_limit
def create_conversation():
    """
    创建新会话，并插入欢迎语
    """
    try:
        is_pet = request.json.get('is_pet', False)
        user_id = get_jwt_identity()

        # Step 1: 调用 bigmodel 平台创建新会话
        new_conversation_id = create_bigmodel_conversation()

        # Step 2: 本地数据库记录会话
        new_conversation = Conversation(id=new_conversation_id, user_id=user_id, is_pet=is_pet)
        db.session.add(new_conversation)

        # Step 3: 添加开场白消息
        welcome_text = (
            "欢迎来到齐民智鉴！这里是你探索古代农业知识的智能助手，"
            "无论你对耕作技术、农时节气还是古代农具有什么疑问，"
            "我都能为你提供详尽的解答。"
        )

        welcome_message = Message(
            conversation_id=new_conversation_id,
            user_id=user_id,
            role='assistant',
            content=welcome_text
        )
        db.session.add(welcome_message)

        # Step 4: 提交事务
        db.session.commit()

        return jsonify({
            'conversation_id': new_conversation_id,
            'opening_message': welcome_text,
            'status': 'success'
        })

    except Exception as e:
        print('create_conversation failed:', e)
        db.session.rollback()
        return jsonify({'error': str(e), 'status': 'fail'}), 400

@chat_api.route('/delete_conversation', methods=['DELETE'])
@login_limit
def delete_conversation():
    try:
        conversation_id = request.args.get('conversation_id')
        conversation = Conversation.query.filter_by(id=conversation_id).first()

        # print(conversation)
        # if conversation.is_pet == True:
        #     return jsonify({'status': 'error', 'message': '和小精灵的对话不能删除哦~'}), 500
        
        messages = Message.query.filter_by(conversation_id=conversation_id).all()
        for message in messages:
            db.session.delete(message)
        db.session.delete(conversation)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': '删除对话失败'}), 500
