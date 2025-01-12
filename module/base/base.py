from logzero import logger
import _thread
import os
import time
from module.base.ocr import OcrHandler
from module.base.template import Template
from module.base.decorator import singleton
import module.utils.core_utils
from module.base.watcher import Watcher


@singleton
class Base(Template, OcrHandler, Watcher):
    def __init__(self):
        super().__init__()
        logger.info("class Base __init__")
        self.init_dir()
        # self.init_close_alerter()

    def init_dir(self):
        root = self.project_path
        dic_path = root + '/cache/'
        if not os.path.exists(dic_path):
            os.makedirs(dic_path)
        dic_path = root + '/screenshots/'
        if not os.path.exists(dic_path):
            os.makedirs(dic_path)

    def close_alert(self):
        import module.step.common_step
        while True:
            time.sleep(3)
            if self.isLive():
                module.step.common_step.CommonStep.close_alert()

    def init_close_alerter(self):
        _thread.start_new_thread(self.close_alert, ())

    def send(self, subject, contents, attachments=None):
        if self.enable_mail:
            user = self.user
            password = self.password
            host = self.host
            receiver = self.receiver
            logger.info("send email to %s", receiver)
            module.utils.core_utils.send(subject, contents, user, password, host, receiver, attachments)

    def send_wechat(self, subject, contents):
        if self.enable_pushplus:
            token = self.pushplus_token
            module.utils.core_utils.send_wechat(token, subject, contents)


base = Base()
