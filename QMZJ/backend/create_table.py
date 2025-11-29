import csv
import models.User  
import models.Comments
import models.Message
from models.DataTable import NongJu, NongShu, NongZuoWu, NongYeJiShu, NongYeWenHua
from models.Knowledge import KnowledgePair, ListItem
from app import db, app
import re


# CSV文件路径
csv_file_path = [
    './Data/raw_data/NongShu.csv',
    './Data/raw_data/NongYeWenHua.csv',
    './Data/raw_data/NongYeJiShu.csv',
    './Data/raw_data/NongJu.csv',
    './Data/raw_data/NongZuoWu.csv',
    './Data/raw_data/QianNianHuiXiang.csv',
]
if_add = True               # 是否要读取cvs文件导入数据
if_create_table = True      # 是否要重新创建数据库表

with app.app_context():
    if if_create_table:
        db.drop_all()
        db.create_all()
        # NongJu.init()
        # NongShu.init()
        # NongZuoWu.init()
        # NongYeJiShu.init()
        # NongYeWenHua.init()
        # KnowledgePair.init()

    if if_add:
        # 读取CSV文件并插入数据到数据库
        
        # 农书
        with open(csv_file_path[0], 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                # 解析经纬度（添加异常处理）
                try:
                    # 检查字段是否存在且非空
                    if row.get('经纬度') and ',' in row['经纬度']:
                        lng, lat = map(float, row['经纬度'].split(','))
                    else:
                        lng, lat = None, None
                except (ValueError, KeyError):
                    lng, lat = None, None
                
                # 创建NongShu实例并插入数据
                new_nongshu = NongShu(
                    name=row['名称'],
                    category=row['所属类别'],
                    sub_category=row['2级类别'],
                    description=row['主要用途'],
                    author=row['创作者'],
                    publish_date=row['出现时期'],
                    significance=row['意义'],
                    ancient_reference='',
                    location=row['作者故乡'],
                    lng=lng,
                    lat=lat
                )
                # print(new_nongshu)
                # 将数据添加到会话
                db.session.add(new_nongshu)

            # 提交数据库更改
            db.session.commit()
        # 农业文化
        with open(csv_file_path[1], 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                # 解析经纬度（添加异常处理）
                try:
                    # 检查字段是否存在且非空
                    if row.get('经纬度') and ',' in row['经纬度']:
                        lng, lat = map(float, row['经纬度'].split(','))
                    else:
                        lng, lat = None, None
                except (ValueError, KeyError):
                    lng, lat = None, None
                
                # 创建NongShu实例并插入数据
                new_nongyewenhua = NongYeWenHua(
                    name=row['名称'],
                    category=row['所属类别'],
                    sub_category=row['2级类别'],
                    description=row['文化解读'],
                    period=row['出现时间'],
                    significance=row['主要意义'],
                    widespread=row['传播范围'],
                    location=row['诞生地点'],
                    ancient_reference='',
                    lng=lng,
                    lat=lat
                )
                # print(new_nongyewenhua)
                # 将数据添加到会话
                db.session.add(new_nongyewenhua)

            # 提交数据库更改
            db.session.commit()
        # 农业技术
        with open(csv_file_path[2], 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                # 解析经纬度（添加异常处理）
                try:
                    # 检查字段是否存在且非空
                    if row.get('经纬度') and ',' in row['经纬度']:
                        lng, lat = map(float, row['经纬度'].split(','))
                    else:
                        lng, lat = None, None
                except (ValueError, KeyError):
                    lng, lat = None, None
                
                # 创建NongShu实例并插入数据
                new_nongyejishu = NongYeJiShu(
                    name=row['名称'],
                    category=row['所属类别'],
                    sub_category=row['2级类别'],
                    description='',
                    period=row['时间'],
                    significance=row['重要意义'],
                    main_usage=row['主要作用'],
                    location=row['发源地'],
                    ancient_reference='',
                    lng=lng,
                    lat=lat
                )
                # print(new_nongyejishu)
                # 将数据添加到会话
                db.session.add(new_nongyejishu)

            # 提交数据库更改
            db.session.commit()
        
        # 农具
        with open(csv_file_path[3], 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                # 解析经纬度（添加异常处理）
                try:
                    # 检查字段是否存在且非空
                    if row.get('经纬度') and ',' in row['经纬度']:
                        lng, lat = map(float, row['经纬度'].split(','))
                    else:
                        lng, lat = None, None
                except (ValueError, KeyError):
                    lng, lat = None, None
                
                # 创建NongJu实例并插入数据
                new_nongju = NongJu(
                    name=row['名称'],
                    category=row['所属类别'],
                    sub_category=row['2级类别'],
                    alias=row['别称'],
                    description=row['概述'],
                    creator=row['创作者'],
                    period=row['出现时期'],
                    significance='',
                    ancient_reference=row['古籍记载'],
                    location=row['人为地点'],
                    main_usage=row['主要用途'],
                    region=row['出现/主要使用地点'],
                    lng=lng,
                    lat=lat
                )
                # print(new_nongshu)
                # 将数据添加到会话
                db.session.add(new_nongju)

            # 提交数据库更改
            db.session.commit()

        # 农作物
        with open(csv_file_path[4], 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                # 解析经纬度（添加异常处理）
                try:
                    # 检查字段是否存在且非空
                    if row.get('经纬度') and ',' in row['经纬度']:
                        lng, lat = map(float, row['经纬度'].split(','))
                    else:
                        lng, lat = None, None
                except (ValueError, KeyError):
                    lng, lat = None, None
                
                # 创建NongZuoWu实例并插入数据
                new_nongzuowu = NongZuoWu(
                    name=row['名称'],
                    category=row['所属类别'],
                    sub_category=row['2级类别'],
                    description='',
                    origin=row['原产地'],
                    ancient_reference='',
                    location=row['人为地点'],
                    main_usage=row['主要用途'],
                    nutri_value=row['营养价值'],
                    econo_value=row['经济价值'],
                    grow_env=row['生长环境'],
                    plant_area=row['种植地带'],
                    lng=lng,
                    lat=lat
                )
                # print(new_nongshu)
                # 将数据添加到会话
                db.session.add(new_nongzuowu)

            # 提交数据库更改
            db.session.commit()
        
        # 千年回响
        with open(csv_file_path[5], 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                list = []

                # 遍历每一行的member列
                member_str = row["member"]
                
                # print("member_str", member_str)
                # 使用正则表达式提取所有[]包裹的组
                groups = re.findall(r"\['(.*?)',\s*'(.*?)',\s*(\d+),\s*'(.*?)'\]", member_str)

                # print("groups", groups)
                
                for group in groups:
                    # 验证数据完整性
                    if len(group) != 4:
                        print(f"格式错误的数据组: {group}")
                        continue
                        
                    # 解包数据并处理year类型
                    try:
                        title, description, year, img = group
                        # print(f'数据：{title}, {description}, {year}, {img}')
                        list.append(
                            ListItem(
                                title = title.strip("'"),
                                description = description.strip("'"),
                                year = year,
                                img = img.strip("'"),
                            )
                        )
                    except ValueError as e:
                        print(f"数据类型转换错误: {e} | 数据组: {group}")


                # 创建KnowledgePair实例并插入数据
                new_knowledge = KnowledgePair(
                    ancient_title=row['ancient_title'],
                    ancient_description=row['ancient_description'],
                    ancient_year=row['ancient_year'],
                    ancient_img=row['ancient_img'],
                    modern_title=row['modern_title'],
                    modern_description=row['modern_description'],
                    modern_year=row['modern_year'],
                    modern_img=row['modern_img'],
                    list_items = list,
                )
                # 将数据添加到会话
                db.session.add(new_knowledge)

            # 提交数据库更改
            db.session.commit()
