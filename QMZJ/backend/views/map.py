from models.DataTable import NongJu, NongShu, NongZuoWu, NongYeJiShu, NongYeWenHua
from models.User import User
from models.modelConfig import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, session, jsonify
from decorators import login_limit
import math
from collections import defaultdict
import random

maps = Blueprint("maps", __name__, url_prefix="/api/map")
def apply_jitter(markers):
    try:
        grouped = defaultdict(list)
        for m in markers:
            if m.lng is None or m.lat is None:
                # print(f"跳过无坐标点：{m.name} (id={m.id})")
                continue
            key = f"{round(m.lng, 6)}_{round(m.lat, 6)}"
            grouped[key].append(m)

        jitter_offset = 1
        for group in grouped.values():
            if len(group) > 1:
                for i, m in enumerate(group):
                    angle = 2 * math.pi * i / len(group)
                    r =0.1 + 0.9 * random.random()  # 半径 jitter：控制在 [0.0004, 0.0006] 范围内
                    dx = math.cos(angle) * r
                    dy = math.sin(angle) * r
                    m.lng += dx
                    m.lat += dy

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("jitter 处理出错：", e)

# 返回全部地图数据点
@maps.route("/markersAll", methods=['GET'])
@login_limit
def markers_all():
    # 分别获取每类数据
    markers_nongju = NongJu.query.all()
    markers_nongshu = NongShu.query.all()
    markers_nongzuowu = NongZuoWu.query.all()
    markers_nongyijishu = NongYeJiShu.query.all()
    markers_nongyiwenhua = NongYeWenHua.query.all()

    # 对每类数据分别 jitter，确保直接修改原列表
    apply_jitter(markers_nongju)
    apply_jitter(markers_nongshu)
    apply_jitter(markers_nongzuowu)
    apply_jitter(markers_nongyijishu)
    apply_jitter(markers_nongyiwenhua)

    # 最后按原格式 jsonify 返回
    return jsonify({
        'NongJu': [m.to_dict() for m in markers_nongju],
        'NongShu': [m.to_dict() for m in markers_nongshu],
        'NongZuoWu': [m.to_dict() for m in markers_nongzuowu],
        'NongYeJiShu': [m.to_dict() for m in markers_nongyijishu],
        'NongYeWenHua': [m.to_dict() for m in markers_nongyiwenhua]
    }), 200
