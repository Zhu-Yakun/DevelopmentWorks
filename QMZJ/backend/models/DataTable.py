from models.modelConfig import db

# 农具 农书 农作物 农业技术 农业文化

# 定义一个公共的抽象基类
class BaseAgricultural(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True, comment="名称")
    category = db.Column(db.String(255), nullable=False, comment="类别")
    sub_category = db.Column(db.String(255), nullable=False, comment="二级类别")
    description = db.Column(db.Text, nullable=False, comment="描述")
    ancient_reference = db.Column(db.Text, nullable=False, comment="古籍记载")
    location = db.Column(db.String(255), nullable=False, comment="地点")
    lng = db.Column(db.Float, nullable=True, comment="经度")
    lat = db.Column(db.Float, nullable=True, comment="纬度")

    def common_to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'sub_category': self.sub_category,
            'description': self.description,
            'ancient_reference': self.ancient_reference,
            'location': self.location,
            'lng': self.lng,
            'lat': self.lat
        }


# 农具表
class NongJu(BaseAgricultural):
    period = db.Column(db.String(255), nullable=False, comment="出现时期")
    creator = db.Column(db.String(255), nullable=False, comment="创作者")
    main_usage = db.Column(db.Text, nullable=False, comment="主要用途")
    alias = db.Column(db.String(255), nullable=True, comment="别称（可空）")
    significance = db.Column(db.Text, nullable=False, comment="意义")
    region = db.Column(db.String(255), nullable=False, comment="出现/主要使用地区")
    
    def to_dict(self):
        data = self.common_to_dict()
        data.update({
            'period': self.period,
            'creator': self.creator,
            'main_usage': self.main_usage,
            'alias': self.alias,
            'significance': self.significance,
            'region': self.region,
        })
        return data
    
    @staticmethod
    def init():
        test_data_list = [
            {"name": "犁", "category": "农具", "sub_category": "整地农具", "description": "用于翻土整地", 
             "period": "商周", "creator": "不详", "main_usage": "翻土", "alias": "耕犁", 
             "significance": "提高耕作效率", "ancient_reference": "《考工记》", 
             "location": "北京;东城区", "lng": 116.4074, "lat": 39.9042},
            {"name": "镰刀", "category": "农具", "sub_category": "收获农具", "description": "用于收割庄稼", 
             "period": "汉代", "creator": "农民", "main_usage": "收割庄稼", "alias": "收割刀", 
             "significance": "加快收割速度", "ancient_reference": "《齐民要术》", 
             "location": "中国", "lng": 118.7969, "lat": 32.0603},
            {"name": "筒车", "category": "农具", "sub_category": "运输农具", "description": "用于运输农产品", 
             "period": "汉代", "creator": "农民", "main_usage": "运输农产品", "alias": "车筒", 
             "significance": "提高运输效率", "ancient_reference": "《齐民要术》", 
             "location": "中国", "lng": 118.7969, "lat": 32.0603}
        ]
        for test_data in test_data_list:
            new_data = NongJu(**test_data)
            db.session.add(new_data)
        db.session.commit()


# 农书表
class NongShu(BaseAgricultural):
    author = db.Column(db.String(255), nullable=False, comment="作者")
    publish_date = db.Column(db.String(255), nullable=False, comment="出版日期或成书时期")
    significance = db.Column(db.Text, nullable=False, comment="农书的意义")
    
    def to_dict(self):
        data = self.common_to_dict()
        data.update({
            'author': self.author,
            'publish_date': self.publish_date,
            'significance': self.significance,
        })
        return data

    @staticmethod
    def init():
        test_data_list = [
            {
                "name": "齐民要术", 
                "category": "农书", "sub_category": "综合类", "description": "记载农业生产技术的古籍。",
                "author": "贾思勰", "publish_date": "北魏", "significance": "奠定农业技术基础。",
                "ancient_reference": "《齐民要术》", "location": "河南;洛阳市", "lng": 112.434, "lat": 34.663
            },
            {
                "name": "农政全书", 
                "category": "农书", "sub_category": "综合类", "description": "论述农业生产与技术的著作。",
                "author": "徐光启", "publish_date": "明末", "significance": "推动中西农学交流。",
                "ancient_reference": "《农政全书》", "location": "南京", "lng": 118.7969, "lat": 32.0603
            }
        ]
        for data in test_data_list:
            new_data = NongShu(**data)
            db.session.add(new_data)
        db.session.commit()


# 农作物表
class NongZuoWu(BaseAgricultural):
    origin = db.Column(db.String(255), nullable=False, comment="起源或出现时期")
    main_usage = db.Column(db.Text, nullable=False, comment="主要用途")
    nutri_value = db.Column(db.Text, nullable=False, comment="营养价值")
    econo_value = db.Column(db.Text, nullable=False, comment="经济价值")
    grow_env = db.Column(db.Text, nullable=False, comment="生长环境")
    plant_area = db.Column(db.Text, nullable=False, comment="种植地带")

    def to_dict(self):
        data = self.common_to_dict()
        data.update({
            'origin': self.origin,
            'main_usage': self.main_usage,
            'nutri_value': self.nutri_value,
            'econo_value': self.econo_value,
            'grow_env': self.grow_env,
            'plant_area': self.plant_area,
        })
        return data

    @staticmethod
    def init():
        test_data_list = [
            {
                "name": "稻米", 
                "category": "农作物", "sub_category": "粮食作物", "description": "主食作物，水稻。",
                "origin": "古代", "main_usage": "作为主食", "alias": "水稻", 
                "significance": "保障粮食安全的重要作物。",
                "ancient_reference": "《齐民要术》", "location": "长江流域",
                "lng": 120.1551, "lat": 30.2741
            },
            {
                "name": "小麦", 
                "category": "农作物", "sub_category": "粮食作物", "description": "主要粮食作物，小麦。",
                "origin": "古代", "main_usage": "作为主食", "alias": None, 
                "significance": "重要的粮食来源。",
                "ancient_reference": "《农政全书》", "location": "河南;郑州市",
                "lng": 113.6254, "lat": 34.7466
            }
        ]
        for data in test_data_list:
            new_data = NongZuoWu(**data)
            db.session.add(new_data)
        db.session.commit()


# 农业技术表
class NongYeJiShu(BaseAgricultural):
    # inventor = db.Column(db.String(255), nullable=False, comment="发明者或推广者")
    period = db.Column(db.String(255), nullable=False, comment="时期")
    main_usage = db.Column(db.Text, nullable=False, comment="主要用途")
    significance = db.Column(db.Text, nullable=False, comment="技术意义")
    
    def to_dict(self):
        data = self.common_to_dict()
        data.update({
            # 'inventor': self.inventor,
            'period': self.period,
            'main_usage': self.main_usage,
            'significance': self.significance,
        })
        return data

    @staticmethod
    def init():
        test_data_list = [
            {
                "name": "梯田耕作", 
                "category": "农业技术", "sub_category": "耕作技术", "description": "在山坡上修建梯田以便耕作。",
                "inventor": "古代农民", "period": "汉代", 
                "main_usage": "适应山区地形耕作", "significance": "提高山区农业利用率",
                "ancient_reference": "《农书》", "location": "云南", "lng": 102.7123, "lat": 25.0453
            },
            {
                "name": "灌溉技术", 
                "category": "农业技术", "sub_category": "水利技术", "description": "利用水渠和水车对农田进行灌溉。",
                "inventor": "古代工程师", "period": "秦汉", 
                "main_usage": "提高农田产量", "significance": "奠定农业发展的基础",
                "ancient_reference": "《齐民要术》", "location": "陕西", "lng": 108.9398, "lat": 34.3416
            }
        ]
        for data in test_data_list:
            new_data = NongYeJiShu(**data)
            db.session.add(new_data)
        db.session.commit()


# 农业文化表
class NongYeWenHua(BaseAgricultural):
    period = db.Column(db.String(255), nullable=False, comment="时期")
    significance = db.Column(db.Text, nullable=False, comment="文化意义")
    widespread = db.Column(db.Text, nullable=False, comment="文化传播")

    def to_dict(self):
        data = self.common_to_dict()
        data.update({
            'period': self.period,
            'significance': self.significance,
            'widespread': self.widespread,
        })
        return data

    @staticmethod
    def init():
        test_data_list = [
            {
                "name": "农耕文化节", 
                "category": "农业文化", "sub_category": "节日", "description": "庆祝丰收与祭祀土地神的传统节日。",
                "period": "明清", "significance": "传承农耕文化精神与乡土情怀。",
                "ancient_reference": "《农政全书》", "location": "江苏", "lng": 118.7674, "lat": 32.0415
            },
            {
                "name": "田园诗", 
                "category": "农业文化", "sub_category": "文学", "description": "以田园风光和农耕生活为题材的诗歌文化。",
                "period": "唐宋", "significance": "反映农村生活与自然和谐共生的理念。",
                "ancient_reference": "《乐府诗集》", "location": "江南", "lng": 120.1551, "lat": 30.2741
            }
        ]
        for data in test_data_list:
            new_data = NongYeWenHua(**data)
            db.session.add(new_data)
        db.session.commit()
