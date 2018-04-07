# -*- coding: utf-8 -*-
import logging

class Module(object):
    """
    モジュール
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', logging.getLogger(__name__))

    def predict(self, **kwargs):
        raise self.ModuleMethodNotImplementedError()

    class ModuleMethodNotImplementedError(NotImplementedError):
        def __init__(self, message=None):
            """
            例外メッセージを設定する。
            """
            if not message:
                message = 'このメソッドはサブクラスのメソッドによって上書きされる必要があります。'
            self.message = message

        def __str__(self):
            return self.message
