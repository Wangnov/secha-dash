# 找色差小游戏
# secha-dash

## 项目描述
本项目是一个基于Dash框架的Web应用程序，旨在帮助用户通过识别颜色差异来测试视觉感知能力。游戏界面包含多个方块，其中一个方块的颜色与其他方块略有不同。用户需要通过点击不同的方块来识别出颜色差异。
项目基于Dash框架构建，使用了[fac](https://fac.feffery.tech)和[fuc](https://fuc.feffery.tech)组件库，并提供了快速编写Dash CSS的[实用工具库](https://github.com/CNFeffery/feffery-dash-utils)。
本项目是对[找色差小游戏](https://www.shj.work/tools/secha/)的仿写

## Project Description
This project is a web application based on the Dash framework, aiming to help users test their visual perception ability through color difference recognition. The game interface contains several blocks, and one block has a slightly different color from the others. The user needs to click different blocks to identify the color difference.
The project is based on the Dash framework, and uses the [fac](https://fac.feffery.tech) and [fuc](https://fuc.feffery.tech) component libraries, and provides a [utility library](https://github.com/CNFeffery/feffery-dash-utils) for writing Dash CSS quickly.
This project is a reproduction of the [The Color!](https://www.shj.work/tools/secha/).

## 功能特性
- **颜色差异识别**：用户需要在多个颜色相似的方块中识别出颜色略有不同的方块。
- **动态生成**：每次游戏开始时，方块的颜色和位置都会随机生成。随着关卡推进，难度会越来越高。
- **用户交互**：用户可以通过点击方块来选择他们认为颜色不同的方块。

## Features
- **Color Difference Recognition**: The user needs to identify the block with a slightly different color from multiple blocks with similar colors.
- **Dynamic Generation**: The blocks' colors and positions will be randomly generated every time the game starts. As the level progresses, the difficulty will increase.
- **User Interaction**: The user can select the block they think is different by clicking on it.

## 技术栈
- **Dash**：用于构建Web应用程序的Python框架。
- **feffery_antd_components**：用于Dash的Ant Design组件库。
- **feffery_utils_components**：用于Dash的实用组件库。
- **feffery_dash_utils**：用于快速编写Dash css的实用工具库。

## Technology Stack
- **Dash**: A Python framework for building web applications.
- **feffery_antd_components**: A component library for the Dash framework based on Ant Design.
- **feffery_utils_components**: A component library for the Dash framework based on utility components.
- **feffery_dash_utils**: A utility library for writing Dash CSS quickly.


## 安装与运行 Installation and Running
1. **克隆仓库 Clone the repository**：
   ```bash
   git clone https://github.com/Wangnov/secha-dash.git
   cd secha-dash
   ```

2. **安装依赖 Install dependencies**：
   ```bash
   pip install -r requirements.txt
   pip install feffery_antd_components --pre -U
   pip install feffery_utils_components --pre -U
   pip install feffery_dash_utils --pre -U
   ```


3. **运行项目 Run the project**：
   ```bash
   python app.py
   ```

## 部署(可选的)
**部署到pythonanywhere**
- 创建一个pythonanywhere账号（免费）
- 上传项目到pythonanywhere
- 创建虚拟环境，并安装依赖
- 新建一个web服务，并设置项目路径和虚拟环境路径
- 修改WSGI configuration file为以下内容（自行替换路径）：
```python
import sys

# add your project directory to the sys.path
project_home = u'/home/yourname/secha-dash'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app import app
application = app.server
```
- Reload pythonanywhere web服务
- 打开浏览器，输入pythonanywhere web服务的域名，即可访问游戏

## Deployment (Optional)
**Deploy to pythonanywhere**
- Create a pythonanywhere account (free)
- Upload the project to pythonanywhere
- Create a virtual environment and install dependencies
- Create a web service and set the project path and virtual environment path
- Modify the WSGI configuration file to the following content (replace the path with your own):
```python
import sys

# add your project directory to the sys.path
project_home = u'/home/yourname/secha-dash'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app import app
application = app.server
```
- Reload the pythonanywhere web service
- Open the browser, enter the domain of the pythonanywhere web service, and you can access the game.


## 许可证 License
[MIT](https://github.com/Wangnov/secha-dash/blob/main/LICENSE) © Wangnov

