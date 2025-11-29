from py2neo import Graph, Node, Relationship,NodeMatcher
from config import graph
# 这里用来创建知识图谱，需要一份整理好的关系文档，relation.txt

graph.run("MATCH (n) DETACH DELETE n")
print("已清空原有图谱。")

with open("../Data/raw_data/dataRelation.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        rela_array=line.strip("\n").split(",")
        print(rela_array)
        graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
        graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
        graph.run(
            "MATCH(e: Person), (cc: Person) \
            WHERE e.Name='%s' AND cc.Name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])
        )

