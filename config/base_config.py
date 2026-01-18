# 基础配置
PLATFORM = "xhs"  # 平台，xhs | zhihu | xhy
KEYWORDS = "咖啡,美式"  # 关键词搜索配置，以英文逗号分隔
LOGIN_TYPE = "qrcode"  # qrcode or phone or cookie
COOKIES = ""
CRAWLER_TYPE = (
    "search"  # 爬取类型，search(关键词搜索) | detail(帖子详情)| creator(创作者主页数据)
)
# 是否开启 IP 代理
ENABLE_IP_PROXY = False

# 代理IP池数量
IP_PROXY_POOL_COUNT = 2

# 代理IP提供商名称
IP_PROXY_PROVIDER_NAME = "kuaidaili"  # kuaidaili | wandouhttp

# 设置为True不会打开浏览器（无头浏览器）
# 设置False会打开一个浏览器
# 小红书如果一直扫码登录不通过，打开浏览器手动过一下滑动验证码
# 抖音如果一直提示失败，打开浏览器看下是否扫码登录之后出现了手机号验证，如果出现了手动过一下再试。
HEADLESS = False

# 是否保存登录状态
SAVE_LOGIN_STATE = True

# ==================== CDP (Chrome DevTools Protocol) 配置 ====================
# 是否启用CDP模式 - 使用用户现有的Chrome/Edge浏览器进行爬取，提供更好的反检测能力
# 启用后将自动检测并启动用户的Chrome/Edge浏览器，通过CDP协议进行控制
# 这种方式使用真实的浏览器环境，包括用户的扩展、Cookie和设置，大大降低被检测的风险
ENABLE_CDP_MODE = True

# CDP调试端口，用于与浏览器通信
# 如果端口被占用，系统会自动尝试下一个可用端口
CDP_DEBUG_PORT = 9222

# 自定义浏览器路径（可选）
# 如果为空，系统会自动检测Chrome/Edge的安装路径
# Windows示例: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# macOS示例: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CUSTOM_BROWSER_PATH = ""

# CDP模式下是否启用无头模式
# 注意：即使设置为True，某些反检测功能在无头模式下可能效果不佳
CDP_HEADLESS = False

# 浏览器启动超时时间（秒）
BROWSER_LAUNCH_TIMEOUT = 60

# 是否在程序结束时自动关闭浏览器
# 设置为False可以保持浏览器运行，便于调试
AUTO_CLOSE_BROWSER = True

# 数据保存类型选项配置,支持五种类型：csv、db、json、sqlite、excel, 最好保存到DB，有排重的功能。
SAVE_DATA_OPTION = "json"  # csv or db or json or sqlite or excel

# 用户浏览器缓存的浏览器文件配置
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# 爬取开始页数 默认从第一页开始
START_PAGE = 1

# 爬取视频/帖子的数量控制
CRAWLER_MAX_NOTES_COUNT = 15

# 并发爬虫数量控制
MAX_CONCURRENCY_NUM = 1

# 是否开启爬媒体模式（包含图片或视频资源），默认不开启爬媒体
ENABLE_GET_MEIDAS = False

# 是否开启爬评论模式, 默认开启爬评论
ENABLE_GET_COMMENTS = True

# 爬取一级评论的数量控制(单视频/帖子)
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 10

# 是否开启爬二级评论模式, 默认不开启爬二级评论
# 老版本项目使用了 db, 则需参考 schema/tables.sql line 287 增加表字段
ENABLE_GET_SUB_COMMENTS = False

# 词云相关
# 是否开启生成评论词云图
ENABLE_GET_WORDCLOUD = False
# 自定义词语及其分组
# 添加规则：xx:yy 其中xx为自定义添加的词组，yy为将xx该词组分到的组名。
CUSTOM_WORDS = {
    "高频词": "专业术语",  # 示例自定义词
    "美式": "咖啡类型",
    "拿铁": "咖啡类型",
    "卡布奇诺": "咖啡类型",
    "摩卡": "咖啡类型",
    "意式浓缩": "咖啡类型",
    "单品咖啡": "咖啡类型",
    "冷萃": "咖啡类型",
    "冰滴": "咖啡类型",
    "爱尔兰咖啡": "咖啡类型",
    "维也纳咖啡": "咖啡类型"
}

# 停用(禁用)词文件路径
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"

# 中文字体文件路径
FONT_PATH = "./docs/STZHONGS.TTF"

# 爬取间隔时间（原有配置，保留向后兼容）
CRAWLER_MAX_SLEEP_SEC = 2

# ==================== 模拟人工行为配置 ====================
# 是否启用模拟人工行为
# 启用后将使用随机延迟和多种行为模拟策略，提高爬取稳定性
ENABLE_HUMAN_BEHAVIOR = True

# 基础延迟区间 (秒) - 用于一般操作
CRAWLER_MIN_SLEEP_SEC = 1.5
CRAWLER_MAX_SLEEP_SEC_NEW = 3.0

# 页面浏览延迟区间 (秒) - 模拟阅读时间，翻页等操作使用
PAGE_VIEW_MIN_SEC = 2.0
PAGE_VIEW_MAX_SEC = 5.0

# 操作间隔延迟区间 (秒) - 模拟鼠标点击、滚动等操作
ACTION_INTERVAL_MIN_SEC = 0.5
ACTION_INTERVAL_MAX_SEC = 1.5

# 会话休息配置 - 长时间运行后的休息间隔
SESSION_BREAK_INTERVAL = 30  # 每执行30次操作后休息一次
SESSION_BREAK_MIN_SEC = 10.0  # 休息最小时长（秒）
SESSION_BREAK_MAX_SEC = 30.0  # 休息最大时长（秒）

# 评论爬取延迟区间 (秒) - 爬取评论时的延迟
COMMENT_CRAWL_MIN_SEC = 1.0
COMMENT_CRAWL_MAX_SEC = 2.5

from .xhs_config import *
from .zhihu_config import *
