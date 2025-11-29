from db.config import graph, CA_LIST, similar_words
from models.DataTable import NongJu, NongShu, NongZuoWu, NongYeJiShu, NongYeWenHua
import codecs
import os
import json
import base64
from sqlalchemy.exc import SQLAlchemyError

# 这一部分是查询模块实现
# 只查询直接相连的结点
def query(name):
    data = graph.run(
    "match(p)-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name,name)
    )
    data = list(data)
    if(len(data)==0):
        json_data={}
        return json_data
    return get_json_data(data)
# 深度查询关联的所有结点
def deep_query(name):
    try:
        cypher = """
        MATCH path = (root:Person {Name: '%s'})-[rels*]->(descendant)
        UNWIND rels as r
        RETURN DISTINCT startNode(r).Name as `p.Name`, r.relation as `r.relation`, endNode(r).Name as `n.Name`, 
            startNode(r).cate as `p.cate`, endNode(r).cate as `n.cate`
        """ % (name)
        data = graph.run(cypher)
        data = list(data)
        if len(data) == 0:
            json_data = {}
            return json_data
    except Exception as e:
        print("报错：", e)
    return get_json_data(data)

def query_by_map_table():
    """
    根据 mapTable 中的内容分别调用 query 进行查询，
    返回一个字典，键为 mapTable 的 key，值为 query 查询返回的字典数据
    """
    map_table = {
        'NongJu': '农具',
        'NongShu': '农书',
        'NongZuoWu': '农作物',
        'NongYeJiShu': '农业技术',
        'NongYeWenHua': '农业文化',
    }
    result = {}
    for key, value in map_table.items():
        result[key] = deep_query(value)
    return result

def query_all_relations():
    data = graph.run("match(p)-[r]->(n) return p.Name, n.Name, r.relation, p.cate, n.cate")
    data = list(data)
    return [get_json_data(data)]

def if_exist(name):
    result = graph.run("match(n:Person{Name:'%s'}) return n" % (name))
    exists = False  
    for _ in result:  
        exists = True  
        break
    return exists

def get_json_data(data):
    try:
        json_data={'data':[],"links":[]}
        d=[]
        
        for i in data:
            #print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
            d.append(i['p.Name']+"_"+i['p.cate'])
            d.append(i['n.Name']+"_"+i['n.cate'])
            d=list(set(d))
        name_dict={}
        count=0
        for j in d:
            j_array=j.split("_")
        
            data_item={}
            name_dict[j_array[0]]=count
            count+=1
            data_item['name']=j_array[0]
            data_item['category']=CA_LIST[j_array[1]]
            json_data['data'].append(data_item)
        for i in data:
    
            link_item = {}
            
            link_item['source'] = name_dict[i['p.Name']]
            
            link_item['target'] = name_dict[i['n.Name']]
            link_item['value'] = i['r.relation']
            json_data['links'].append(link_item)
    except Exception as e:
        print("报错：", e)

    return json_data

def find_image(last_name, folder_path="./Data/images"):
    # 遍历文件夹，匹配名称前缀
    for filename in os.listdir(folder_path):
        if filename.startswith(last_name + "."):
            return os.path.join(folder_path, filename)
    return None  # 未找到时返回默认图片

def get_profile(name, model_param):
    mapTable = {
        "农具": NongJu,
        "农书": NongShu,
        "农作物": NongZuoWu,      
        "农业技术": NongYeJiShu,
        "农业文化": NongYeWenHua,
    }
    
    model = mapTable.get(model_param)
    if model is None:
        print(f"错误：无效的模型参数 '{model_param}'")
        return None
    
    try:
        results = model.query.filter_by(name=name).all()
    except SQLAlchemyError as e:
        print(f"数据库查询失败: {e}")
        return None
    
    if not results:
        print(f"未找到名称 '{name}' 的记录")
        return None
    
    try:
        data = results[0].to_dict()
    except AttributeError:
        print("错误：模型未定义 to_dict() 方法")
        return None
    
    return data

def get_KGQA_answer(array, is_reverse, model_param="nongju"):
    data_array=[]
    exist = True
    if(len(array)<=1):
        data_array = array[0]
        single = 1
        str_profile = str(data_array)
        last_name = str(data_array)
        json_data = query(data_array)
        if(len(json_data)==0):
            exist = False
    else:
        single = 0
        for i in range(len(array)-2):
            if i==0:
                name=array[0]
            else:
                name=data_array[-1]['p.Name']
            if(is_reverse):
                data = graph.run(
                    "match(n:Person {Name:'%s'})-[r:%s]->(p) return n.Name, p.Name, r.relation, n.cate, p.cate" 
                    % (name, similar_words[array[i+1]])
                )
            else:
                data = graph.run(
                    "match(p)-[r:%s]->(n:Person {Name:'%s'}) return p.Name, n.Name, r.relation, p.cate, n.cate" 
                    % (similar_words[array[i+1]], name)
                )
            data = list(data)
            #print(data)
            data_array.extend(data)
            if(len(data_array)!=0):
                str_profile = str(data_array[-1]['p.Name'])
                last_name = str(data_array[-1]['p.Name'])
            else:
                exist = False

    if(exist):
        image_path = find_image(last_name)
        if image_path:
            with open(image_path, "rb") as image:
                base64_data = base64.b64encode(image.read())
                b=str(base64_data)
        else:
            with open("./Data/images/暂无图片.jpg", "rb") as image2:
                base64_data2 = base64.b64encode(image2.read())
                b=str(base64_data2)

    if(single == 1):
        if(exist):
            return [query(data_array), get_profile(str_profile,model_param), b.split("'")[1]]
        return [json_data, '', '']
    
    if(exist):
        return [get_json_data(data_array), get_profile(str_profile,model_param), b.split("'")[1]]
    else:
        return [{}, '', '']


def get_answer_profile(name):
    image_path = "./Data/images/{}.jpg".format(str(name))
    if os.path.exists(image_path):  
        with open(image_path, "rb") as image:
            base64_data = base64.b64encode(image.read())
            b=str(base64_data)
    else:
        with open("./Data/images/暂无图片.jpg", "rb") as image2:
            base64_data2 = base64.b64encode(image2.read())
            b=str(base64_data2)
    return [get_profile(str(name)), b.split("'")[1]]

