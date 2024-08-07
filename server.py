import dash
import re
from flask import Flask


def modify_url(original_url):
    # 先替换所有"/@"，针对/@babel这类情况
    original_url = original_url.replace("/@", "^&*")
    # 找到第一个"@"后第一个"/"的定位
    index = original_url.index("/", original_url.index("@"))
    # 替换为"/"
    modified_url = original_url.replace("@", "/", 1)
    # 在index位置插入"files/"
    modified_url = modified_url[: index + 1] + "files/" + modified_url[index + 1 :]

    # 替换"/@"回来，替换域名
    modified_url = modified_url.replace(
        "https://unpkg.com", "https://registry.npmmirror.com"
    ).replace("^&*", "/@")

    return modified_url


class CustomDash(dash.Dash):
    def interpolate_index(self, **kwargs):
        scripts = kwargs.pop("scripts")

        # 提取scripts部分符合条件的外部js资源
        external_scripts = re.findall('(<script src="http.*?"></script>)', scripts)

        # 将原有的script标签内容替换为带备用地址错误切换的版本
        for external_script in external_scripts:
            scripts = scripts.replace(
                external_script,
                """<script src="{}" onerror='this.remove(); let fallbackScript = document.createElement("script"); fallbackScript.src = "{}"; document.querySelector("head").prepend(fallbackScript);'></script>""".format(
                    modify_url(re.findall('"(.*?)"', external_script)[0]),
                    re.findall('"(.*?)"', external_script)[0],
                ),
            )

        scripts = (
            """<script>
window.onerror = async function(message, source, lineno, colno, error) {
    if (message.includes('is not defined') !== -1) {
        await waitForModules();
    }
}

async function waitForModules() {
    const requiredModules = [
        'DashRenderer',
        'dash_html_components',
        'dash_core_components',
        'feffery_antd_components',
        'feffery_utils_components',
        'feffery_markdown_components',
        'feffery_antd_charts',
    ];

    while (!areModulesDefined(requiredModules)) {
        await delay(100); // 延迟100毫秒
    }

    // 变量已定义，触发事件
    var renderer = new DashRenderer();
}

function areModulesDefined(modules) {
    return modules.every(module => window[module]);
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
</script>
"""
            + scripts
        )

        return super(CustomDash, self).interpolate_index(scripts=scripts, **kwargs)


server = Flask(__name__)

app = CustomDash(
    __name__,
    compress=True,
    suppress_callback_exceptions=True,
    update_title=None,
    server=server,
    serve_locally=False,
)
app.server.config["COMPRESS_ALGORITHM"] = "br"
app.server.config["COMPRESS_BR_LEVEL"] = 9

app.title = "找色差小游戏"
server = app.server
