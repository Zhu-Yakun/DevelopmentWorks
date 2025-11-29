import csv  

# CSV文件路径  
csv_file_path = [
    './raw_data/NongShu.csv',
    './raw_data/NongYeJiShu.csv',
    './raw_data/NongYeWenHua.csv',
    './raw_data/NongJu.csv',
    './raw_data/NongZuoWu.csv',
]

# 读取CSV文件  

with open(csv_file_path[4], 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # 按sub_cate分组存储name（自动去重）
    sub_cate_map = {}
    # 按cate和sub_cate分组去重
    cate_map = {}
    
    for row in reader:
        name = row.get("名称", "")
        cate = row.get("所属类别", "")
        sub_cate = row.get("2级类别", "")
        
        print(f"{sub_cate},{name},包括,{sub_cate},{sub_cate}")
        # 处理cate,sub_cate分组去重
        key = (cate, sub_cate)
        if key not in cate_map:
            cate_map[key] = True

    # 输出 cate,sub_cate（去重）
    print("\n")
    for (cate, sub_cate), _ in cate_map.items():
        print(f"{cate},{sub_cate},包括,{cate},{sub_cate}")