from models.DataTable import NongJu, NongShu, NongZuoWu, NongYeJiShu, NongYeWenHua
from models.modelConfig import db
from flask_jwt_extended import get_jwt_identity
from flask import Blueprint, request, jsonify
from decorators import login_limit

search_bp = Blueprint("search", __name__, url_prefix="/api/search")

# 获取全部农业数据（包括农具、农书、农作物、农业技术、农业文化）
@search_bp.route("/searchAll", methods=['GET'])
@login_limit
def search_all():
    data = {
        "NongJu": [item.to_dict() for item in NongJu.query.all()],
        "NongShu": [item.to_dict() for item in NongShu.query.all()],
        "NongZuoWu": [item.to_dict() for item in NongZuoWu.query.all()],
        "NongYeJiShu": [item.to_dict() for item in NongYeJiShu.query.all()],
        "NongYeWenHua": [item.to_dict() for item in NongYeWenHua.query.all()]
    }
    return jsonify(data), 200

# 带过滤条件的搜索接口
# 可通过查询参数指定 model（数据类型）、category（类别）、period（时期）和 location（地点）
# 如：/api/search/filter?model=nongju&category=农具&period=商周&location=中国
@search_bp.route("/filter", methods=['GET'])
@login_limit
def filter_search():
    # 根据请求参数决定查询哪个模型，默认查询 NongJu
    model_param = request.args.get("model", "nongju").lower()
    models = {
        "nongju": NongJu,
        "nongshu": NongShu,
        "nongzuowu": NongZuoWu,
        "nongyejishu": NongYeJiShu,
        "nongyewenhua": NongYeWenHua
    }
    model = models.get(model_param)
    if not model:
        return jsonify({"error": "Invalid model parameter. Valid options: nongju, nongshu, nongzuowu, nongyejishu, nongyewenhua."}), 400

    query = model.query

    # 公共过滤条件
    category = request.args.get('category')
    location = request.args.get('location')
    period = request.args.get('period')

    if category:
        query = query.filter_by(category=category)
    if location:
        query = query.filter(model.location.like(f"%{location}%"))
    if period:
        # 部分模型有 period 字段，NongShu 则使用 publish_date 作为时间过滤字段
        if hasattr(model, "period"):
            query = query.filter_by(period=period)
        elif model.__name__ == "NongShu":
            query = query.filter_by(publish_date=period)
        # 其他模型若无对应字段则忽略该过滤条件

    results = query.all()
    return jsonify({
        "results": [item.to_dict() for item in results]
    }), 200
