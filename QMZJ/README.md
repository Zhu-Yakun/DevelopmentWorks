# QMZJ
**齐民智鉴——古代农学数据可视化平台**

## 本地安装运行方式
以下提供**Windows操作系统**中的安装运行方式  
在我们提供的“源代码”文件夹中，有着“frontend”（前端代码）、“backend”（后端代码）以及README.md（使用说明）文件
在安装本系统之前请确保所用的电脑已经正确安装了2.2系统软硬件平台中所提及的对应版本的软件并且硬件设备达到基本要求，包括Python3.9、NodeJs、MySQL和Neo4j
建议使用VScode打开“源代码”文件夹

### 前端
1. 在控制台或者终端中打开源代码文件夹作为工作目录
2. 切换到frontend目录：cd frontend
3. 安装前端所需要的依赖：npm install  （建议以管理员权限启动终端，避免因权限不足而报错）
4. 运行前端npm run dev，应当可以看到前端代码正确运行
### 数据库
确保已经正确安装了对应版本的MySQL和Neo4j数据库
1. 打开终端控制台
2. 运行mysql -u root -p，回车跳过输入密码（如果已经注册过密码则输入密码），进入mysql>
3. 创建数据库QMZJ：create database QMZJ;
4. 打开新的终端控制台
5. 运行neo4j.bat console（要保持终端一直打开）或者neo4j.bat start
6. 打开浏览器，访问http://localhost:7474/ ，进入Neo4j数据库页面，默认用户名和密码均为neo4j，登录
7. 可以自行修改Neo4j数据库密码
8. 打开源文件/backend，进入config.py文件，修改SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/QMZJ'，password填写你的MySQL数据库的密码
9. 打开源文件/backend/db文件夹，进入config.py，修改graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j"))，默认的账号和密码均为neo4j
### 后端
1. 在控制台或者终端中打开源代码文件夹作为工作目录
2. 切换到backend目录：cd backend
3. 确保已经安装了Python3.9，并创建一个Python3.9的环境  
  a. 如果只安装了Python3.9，python3.9 -m venv myenv，即可创建一个名为“myenv”的python3.9虚拟环境，然后运行cd myenv/Scripts，输入activate并回车，激活虚拟环境  
  b. 如果安装了Anaconda，可以打开conda终端使用conda create -n myenv python=3.9，即可创建一个名为“myenv”的python3.9虚拟环境，然后运行conda activate myenv激活虚拟环境
4. 在虚拟环境下打开“源代码/backend”作为工作目录，运行pip install -r requirements.txt，安装所需要的Python库
5. 运行python create_table.py创建MySQL数据库表
6. 切换到db目录：cd db
7. 运行python create_graph.py创建Neo4j知识图谱
8. 回到backend目录，cd ..
9. 运行python app.py启动后端

以上完成后在浏览器中输入http://localhost:8080 ，即可看到网站内容，实现本地运行

## 使用运行说明
完成上述系统安装的步骤之后，若后续重新运行项目，则只需要完成以下步骤：
1. 启动数据库：首先确保MySQL数据库和Neo4j数据库已经启动，并且对应的用户名和密码已经在backend/config.py和backend/db/config.py中进行配置，具体如下：  
  a. 启动MySQL：在终端中输入net start mysql  
  b. 启动Neo4j：在终端中输入neo4j.bat console（需要一直保持终端打开）或者neo4j.bat start  
2. 启动后端：在控制台或者终端中打开源代码文件夹作为工作目录，切换到backend目录：cd backend，运行python app.py
3. 启动前端：在控制台或者终端中打开源代码文件夹作为工作目录，切换到frontend目录：cd frontend，运行npm run dev

以上完成后在浏览器中输入http://localhost:8080 ，即可看到网站内容，实现本地运行
