from flask import Blueprint, request, jsonify
from db.query_graph import query,get_KGQA_answer,get_answer_profile,query_all_relations,query_by_map_table
# from KGQA.ltp import get_target_array
from decorators import login_limit


qa = Blueprint("qa", __name__, url_prefix="/api/qa")


#问答
@qa.route('/get_profile',methods=['GET','POST'])
@login_limit
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    if not json_data:
        return jsonify({'error': 'No such character'}),404
    return jsonify(json_data)

@qa.route('/KGQA_answer', methods=['GET'])
@login_limit
def KGQA_answer():
    question = request.args.get('name')
    target_array = str(question)
    is_reverse = False
    json_data = get_KGQA_answer(target_array,is_reverse)
    if not json_data:
        return jsonify({'error': 'No answer'}),404
    return jsonify(json_data)
    
@qa.route('/search_name', methods=['GET', 'POST'])
@login_limit
def search_name():
    name = request.args.get('name')
    model_param = request.args.get('model_param')
    json_data=get_KGQA_answer([str(name)], False, model_param)
    if not json_data:
        return jsonify({'error': 'No answer'}),404
    return jsonify(json_data)

@qa.route('/all_relations',methods=['get'])
@login_limit
def allRelations():
    json_data = query_all_relations()
    if not json_data:
        return jsonify({'error': 'No relations'}),404  
    return jsonify(json_data)

@qa.route('/all_relations_by_cate',methods=['get'])
@login_limit
def allRelationsByCate():
    json_data = query_by_map_table()
    if not json_data:
        return jsonify({'error': 'No relations'}),404  
    return jsonify(json_data)