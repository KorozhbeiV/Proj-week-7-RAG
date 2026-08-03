from loguru import logger

logger.add(
    "/Users/getapple/Documents/Py_Projects/Proj week 7 RAG/logs/proj.log",
    level='DEBUG',
    rotation='10 MB',
    retention='7 days',
    format='{time:DD.MM.YYYY HH:mm:ss} | {level} | {module}:{function} | {message}'
)
