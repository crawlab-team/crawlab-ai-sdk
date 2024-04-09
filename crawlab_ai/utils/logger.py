import logging

# 创建logger
logger = logging.getLogger("crawlab_ai")
logger.setLevel(logging.INFO)

# 创建handler，用于将日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
console_handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(console_handler)
