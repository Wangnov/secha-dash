import random
import feffery_antd_components as fac
from dash import html
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from server import app
import dash
from dash.dependencies import Input, Output, State


def content():
    # 初始化放置4个方块，确保pass-button作为Input可用
    box_num = 2

    init_color, init_color_rgb = get_color(255 - calculate_d(0))
    diff_color, diff_color_rgb = get_lv_color(init_color, calculate_d(0))

    diff_col_index = random.randint(0, box_num - 1)
    diff_row_index = random.randint(0, box_num - 1)

    init_boxes = [
        fac.AntdRow(
            [
                fac.AntdCol(
                    fuc.FefferyDiv(
                        id="pass-button"
                        if row == diff_row_index and col == diff_col_index
                        else f"{row}-{col}",
                        style=style(
                            width="calc(100% - 10px)",
                            height="calc(100% - 10px)",
                            border="5px solid #ddd",
                            borderRadius=10,
                            aspectRatio="1",
                            background=init_color_rgb
                            if row != diff_row_index or col != diff_col_index
                            else diff_color_rgb,
                        ),
                    ),
                    flex="1",
                )
                for col in range(box_num)
            ],
            style=style(height=f"calc(80vw / {box_num})", width="80vw"),
        )
        for row in range(box_num)
    ]

    return [
        fac.AntdSpace(
            [
                fac.AntdCompact(
                    [
                        fac.AntdText(
                            "过关：",
                            style=style(fontSize=16, marginLeft=5,
                                        fontWeight="bold"),
                        ),
                        fac.AntdText(
                            "0", id="rank", style=style(fontSize=16, fontWeight="bold")
                        ),
                    ]
                ),
                html.Div(
                    [
                        fuc.FefferyWindowSize(id="window-size"),
                        html.Div(id='message-box'),
                        html.Div(
                            fuc.FefferyCountDown(
                                id="count-down",
                                # delay控制游戏总时长
                                delay=60,
                            ),
                            id="count-down-container",
                        ),
                        fac.AntdText(
                            "60",
                            id="count-down-text",
                            style=style(fontSize=24, fontWeight="bold"),
                        ),
                        fac.AntdModal(
                            fac.AntdTitle(
                                "游戏暂停", level=3, style=style(color="white")
                            ),
                            id="pause-modal",
                            maskStyle=style(
                                # 防止暂停偷窥
                                background="linear-gradient(45deg, #c37b8f, #7c2b42)",
                            ),
                            bodyStyle=style(
                                display="flex",
                                justifyContent="center",
                                alignItems="center",
                            ),
                        ),
                    ]
                ),
                fac.AntdButton(
                    "暂停",
                    size="large",
                    type="primary",
                    id="pause-button",
                    style=style(margin=5, borderRadius=20),
                ),
            ],
            id="header",
            align="center",
            style=style(
                height=64,
                width="100%",
                justifyContent="space-between",
            ),
        ),
        html.Div(
            init_boxes,
            id="main-body",
            style=style(
                height="calc(100vh - 128px)",
                width="100%",
                display="flex",
                alignItems="center",
                flexDirection="column",
                paddingTop=20,
            ),
        ),
        fac.AntdSpace([], id="footer", style=style(height=64)),
    ]


# 点击到pass-button后进入下一关，更新方块颜色和难度
@app.callback(
    [Output("main-body", "children"), Output("rank", "children")],
    Input("pass-button", "nClicks"),
    State("rank", "children"),
    prevent_initial_call=True,
)
def callback_func(nClicks, rank):
    if nClicks is not None:
        box_num = get_box_num(rank)

        # 防止rgb数值在增量后超过255
        init_color, init_color_rgb = get_color(255 - calculate_d(rank))
        diff_color, diff_color_rgb = get_lv_color(
            init_color, calculate_d(rank))

        diff_col_index = random.randint(0, box_num - 1)
        diff_row_index = random.randint(0, box_num - 1)

        # 根据方块数调整border大小
        if box_num < 4:
            border = 5
        elif 4 <= box_num < 7:
            border = 4
        elif 7 <= box_num < 10:
            border = 3
        else:
            border = 2

        return [
            fac.AntdRow(
                [
                    fac.AntdCol(
                        fuc.FefferyDiv(
                            # 设置pass-button的id和其他方块id（可将其他方块id设为字典用ALL匹配回调进行其他操作）
                            id="pass-button"
                            if row == diff_row_index and col == diff_col_index
                            else f"{row}-{col}",
                            style=style(
                                width=f"calc(100% - {border*2}px)",
                                height=f"calc(100% - {border*2}px)",
                                border=f"{border}px solid #ddd",
                                borderRadius=10,
                                aspectRatio="1",
                                # 设置方块颜色和pass-button方块颜色
                                background=init_color_rgb
                                if row != diff_row_index or col != diff_col_index
                                else diff_color_rgb,
                            ),
                        ),
                        flex="1",
                    )
                    for col in range(box_num)
                ],
                style=style(height=f"calc(80vw / {box_num})", width="80vw"),
            )
            for row in range(box_num)
        ], f"{int(rank) + 1}"  # 左上角通关数+1
    return dash.no_update


# 窗口尺寸比例提示
@app.callback(
    Output("message-box", "children"),
    [
        Input("window-size", "_width"),
        Input("window-size", "_height"),
    ]
)
def window_size_callback(width, height):
    if width / height > 1:
        return fac.AntdMessage(
            content='为了更好的游戏体验，建议调整浏览器窗口比例为竖屏',
            type='info',
            maxCount=1,
            icon='antd-info-circle',
)
    return dash.no_update

# 倒计时输出


@app.callback(
    Output("count-down-text", "children"),
    Input("count-down", "countdown"),
    prevent_initial_call=True,
)
def count_down_callback(countdown):
    return countdown


# 暂停按钮点击后弹出modal
@app.callback(
    Output("pause-modal", "visible"),
    Input("pause-button", "nClicks"),
    prevent_initial_call=True,
)
def pause_modal_callback(nClicks):
    return True


# 暂停按钮点击后倒计时暂停
@app.callback(
    Output("count-down-container", "children"),
    Input("pause-button", "nClicks"),
    prevent_initial_call=True,
)
def pause_count_down_callback(nClicks):
    return None


# modal关闭后倒计时继续
@app.callback(
    Output("count-down-container", "children", allow_duplicate=True),
    Input("pause-modal", "closeCounts"),
    State("count-down-text", "children"),
    prevent_initial_call=True,
)
def resume_count_down_callback(closeCounts, children):
    return (
        fuc.FefferyCountDown(
            id="count-down",
            delay=int(children),
        ),
    )


# count_down结束后游戏结束
@app.callback(
    [
        Output("main-body", "children", allow_duplicate=True),
        Output("header", "children", allow_duplicate=True),
    ],
    Input("count-down", "countdown"),
    State("rank", "children"),
    prevent_initial_call=True,
)
def game_over_callback(countdown, rank):
    if countdown == 0:
        level = int(rank)
        text, icon = get_game_over_text(level)
        return [
            fac.AntdTitle("游戏结束！", style=style(color="white")),
            fac.AntdResult(
                title=fac.AntdTitle(f"{level}关", style=style(color="white")),
                subTitle=fac.AntdTitle(text, type="secondary"),
                icon=fac.AntdIcon(icon=icon, style=style(
                    fontSize=48, color="white")),
                style=style(
                    width="80vw",
                    marginTop=20,
                    marginBottom=20,
                ),
            ),
            html.Div(
                [
                    fac.AntdButton(
                        "再玩一次",
                        id="restart-button",
                        type="primary",
                        size="large",
                        clickExecuteJsString="window.location.reload()",
                        style=style(width="10rem"),
                    ),
                ],
                style=style(
                    display="flex",
                    justifyContent="center",
                    marginTop=20,
                ),
            ),
            fac.AntdDivider(),
            fac.AntdText(
                "游戏提示：这款游戏最好使用手机、平板等屏幕颜色比较准确的设备，否则屏幕的好坏会直接影响你的发挥水平。不信的话，在你手机上试一试，得分一定会大幅度提高。",
                style=style(padding=30),
            ),
        ], None
    return dash.no_update


def get_game_over_text(level):
    """
    根据过关数生成评价文本
    :param level: 过关数
    :return: 评价文本, 图标
    """
    lvT = [
        "基本上是瞎子！",
        "相当于鼴鼠的视力！",
        "低于大部分人的水平",
        "接近正常人的水平",
        "达到了正常人的水平",
        "超过大部分人的水平",
        "优秀级水平",
        "可以去“最强大脑”了",
        "对色差具有超凡的能力！作弊？？",
    ]
    lvI = [
        "antd-ellipsis",
        "antd-ellipsis",
        "antd-ellipsis",
        "antd-robot",
        "antd-robot",
        "antd-robot",
        "antd-like",
        "antd-like",
        "antd-question",
    ]
    index = 0 if level <= 10 else (level - 10) // 5
    text = lvT[index] if index < len(lvT) else lvT[-1]
    icon = lvI[index] if index < len(lvI) else lvI[-1]

    return text, icon


def get_color(max_value):
    """
    生成一个随机颜色
    :param max_value: RGB的最大值
    :return: 颜色数组和颜色字符串
    """
    color = [random.randint(0, max_value) for _ in range(3)]
    color_str = f"rgb({','.join(map(str, color))})"
    return color, color_str


def get_lv_color(color, delta):
    """
    根据颜色和增量计算相近的颜色
    :param color: 原始颜色数组
    :param delta: 增量
    :return: 新的颜色数组和颜色字符串
    """
    new_color = [c + delta for c in color]
    new_color_str = f"rgb({','.join(map(str, new_color))})"
    return new_color, new_color_str


# 根据关卡数计算颜色偏移量
def calculate_d(i):
    # 每关降低5的偏移量，20关后降低到最小偏移量4，用于控制游戏难度
    return max(100 - int(i) * 5, 4)


def get_box_num(rank):
    # 定义一个包含不同关卡数对应方块数量的列表
    box_num_list = [3, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8]
    # 如果等级超出列表范围则返回9
    return box_num_list[int(rank)] if int(rank) < len(box_num_list) else 9
