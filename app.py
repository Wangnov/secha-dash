from dash import html
from feffery_dash_utils.style_utils import style
from dash.dependencies import Input, Output
import feffery_antd_components as fac
import feffery_utils_components as fuc
from server import app
import views
import views.game


app.layout = html.Div(
    [
        # 调整组件颜色和背景色
        fuc.FefferyStyle(
            rawStyle=""".ant-typography {color: white}
                body {background: linear-gradient(45deg, #c37b8f, #7c2b42);}
                .ant-btn {background: #c37b8f; box-shadow: 0 2px 0 rgb(255 5 97 / 10%)} 
                .ant-btn:hover {background: #7c2b42!important;}
                .ant-modal-content {background: linear-gradient(45deg, #c37b8f, #7c2b42);}
                .ant-message-notice-content {background: rgb(0 0 0 / 30%)!important; color: rgb(255 255 255 / 90%);}"""
        ),
        # 应用自动动画
        fuc.FefferyAutoAnimate(
            [
                fac.AntdSpace(
                    [
                        fac.AntdTitle(
                            "找色差小游戏",
                            level=2,
                            style=style(margin=0, color="white"),
                        )
                    ],
                    id="header",
                    align="center",
                    style=style(height=64, width="100%", justifyContent="center"),
                ),
                fac.AntdSpace(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdTitle(
                                    "眼睛色差辨识度测试！",
                                    level=4,
                                    style=style(margin=0, color="white"),
                                ),
                                fac.AntdTitle(
                                    "The Color!",
                                    level=4,
                                    style=style(margin="0 0 3rem 0", color="white"),
                                ),
                                fac.AntdText("找出所有色块里颜色不同的一个"),
                                fac.AntdText(
                                    "Click on the tile that has a different color"
                                ),
                            ],
                            direction="vertical",
                            align="center",
                            style=style(
                                justifyContent="center",
                            ),
                        ),
                        fac.AntdButton(
                            "开始测试",
                            type="primary",
                            id="start-button",
                            size="large",
                            style=style(width="10rem"),
                        ),
                    ],
                    id="main-body",
                    direction="vertical",
                    align="center",
                    style=style(
                        height="calc(100vh - 128px)",
                        width="100%",
                        justifyContent="space-around",
                    ),
                ),
                fac.AntdSpace(
                    [],  # 未使用
                    id="footer",
                    align="center",
                    style=style(height=64, width="100%", justifyContent="center"),
                ),
            ],
            id="main",
            style=style(
                height="100vh",
                width="100vw",
            ),
        ),
    ]
)


# 进入游戏页面
@app.callback(
    Output("main", "children"),
    Input("start-button", "nClicks"),
    prevent_initial_call=True,
)
def callback_func(c):
    return views.game.content()


if __name__ == "__main__":
    app.run()
