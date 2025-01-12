import inspect
import os
import random
import socket
import sys
import time
from collections import deque
import re
import yagmail
import importlib
import requests
from logzero import logger
from adbutils import _AdbStreamConnection, AdbTimeout

path = None


def project_root_path():
    global path
    if path is None:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            path = os.path.dirname(__file__)
            print('running in a PyInstaller bundle')
            while True:
                if os.path.isdir(path + "/cv2"):
                    print(path)
                    return path
                else:
                    path = os.path.abspath(os.path.join(path, ".."))
        else:
            path = os.path.dirname(__file__)
            print('running in a normal Python process')
            while True:
                if os.path.isdir(path + "/module"):
                    print(path)
                    return path
                else:
                    path = os.path.abspath(os.path.join(path, ".."))
    else:
        return path


def recv_all(stream, chunk_size=4096) -> bytes:
    if isinstance(stream, _AdbStreamConnection):
        stream = stream.conn

    try:
        fragments = []
        while 1:
            chunk = stream.recv(chunk_size)
            if chunk:
                fragments.append(chunk)
            else:
                break
        return b''.join(fragments)
    except socket.timeout:
        raise AdbTimeout('adb read timeout')


def random_port(port_range):
    """ get a random port from port set """
    new_port = random.choice(list(range(*port_range)))
    if is_port_using(new_port):
        return random_port(port_range)
    else:
        return new_port


def is_port_using(port_num):
    """ if port is using by others, return True. else return False """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        result = s.connect_ex(('127.0.0.1', port_num))
        # if port is using, return code should be 0. (can be connected)
        return result == 0
    finally:
        s.close()


def random_time_str():
    return str(int(time.time_ns() / 1000))


# 截取从task...started 到task...finished的日志
def last_lines(filename):
    # 初始:0  匹配到end_pattern:0->1  匹配到start_pattern:1->2
    status = 0
    res_log = deque()
    start_pattern = '(.*?)task(.*?)started(.*?)'
    end_pattern = '(.*?)task(.*?)finished(.*?)'
    with open(filename, 'r', encoding='utf-8') as fb:
        dq = deque(fb)
        while dq:
            last_row = dq.pop()
            if status == 0:
                match_res = re.match(end_pattern, last_row)
                if match_res is not None:
                    status = 1
            if status == 1:
                match_res = re.match(start_pattern, last_row)
                if match_res is not None:
                    status = 2
            if status in (1, 2):
                res_log.appendleft(last_row)
            if status == 2:
                break
    return list(res_log)


def saveFileByList(file: str, lines: list, encoding='utf-8'):
    with open(file, 'w', encoding=encoding) as f:
        f.writelines(lines)
    logger.info("save file %s", file)


def save_last_lines(src_filename, dst_filename):
    res = last_lines(src_filename)
    saveFileByList(dst_filename, res)


def send(subject, contents, user, password, host, receiver, attachments=None):
    yag = yagmail.SMTP(user=user,
                       password=password,
                       host=host)
    yag.send(receiver, subject, contents, attachments)


def send_wechat(token, title, msg):
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    logger.info(url)
    r = requests.get(url=url)
    logger.info(r.text)


# 通过str 获取函数
# input module.dir1.dir2:function
def get_func_by_str(str_fc: str):
    module_name, function_name = tuple(str_fc.split(":"))
    file_name = module_name.split(".")[-1]
    moduleInstance = __import__(module_name, fromlist=(file_name,))
    fc = None
    try:
        fc = getattr(moduleInstance, function_name)
    except AttributeError as e:
        logger.error(e)
    finally:
        return fc


# 通过函数 获取注解
# input module.dir1.dir2:function
def get_announce_by_fc(fc, key):
    return fc.__annotations__.get(key)


# 通过函数str 获取注解
# input module.dir1.dir2:function
def get_announce_by_str(fc_name, key):
    value = None
    fc = get_func_by_str(fc_name)
    if fc is not None:
        value = get_announce_by_fc(fc, key)
    return value
