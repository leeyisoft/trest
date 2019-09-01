#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
base handler
要获得中间件等特性需继承BaseHandler
"""

import tornado.locale
import tornado.web
from tornado.escape import xhtml_escape
from tornado.escape import json_encode
from raven.contrib.tornado import SentryMixin
from typing import Any

from .settings_manager import settings
from .exception import Http404
from .exception import JsonError
from .cache import close_caches


class BaseHandler(SentryMixin, tornado.web.RequestHandler):
    response_to_mq = False

    def get_user_locale(self):
        if settings.TRANSLATIONS_CONF.use_accept_language:
            user_locale = self.get_argument('lang', None)
            if user_locale in ['en', 'us','en_US', 'en-US']:
                return tornado.locale.get('en_US')
            elif user_locale in ['cn','zh_CN', 'zh-CN', 'zh-hans', 'zh-Hans-CN']:
                return tornado.locale.get('zh_CN')
            elif user_locale in ['ph','en_PH', 'en-PH']:
                # 英国 -菲律宾共和国
                return tornado.locale.get('en_PH')
            elif user_locale in ['id','id_ID', 'id-ID']:
                # 印尼 -印尼
                return tornado.locale.get('id_ID')
            elif user_locale in ['vi','vi_VN', 'vi-VN']:
                # 越南 -越南
                return tornado.locale.get('vi_VN')
            elif user_locale in ['tw','zh_TW', 'zh-TW']:
                return tornado.locale.get('zh_TW')
        # 默认中文
        return tornado.locale.get(settings.TRANSLATIONS_CONF.locale_default)

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        May be overridden by subclasses to add or modify values.

        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = super().get_template_namespace()
        namespace['lang'] = self.get_argument('lang', None)
        return namespace

    def error(self, msg='error', code=1, **args):
        self.set_status(200, msg)
        raise JsonError(code=code, msg=msg, **args)

    def success(self, msg='success', **args):
        self.set_status(200, msg)
        raise JsonError(code=0, msg=msg, **args)

class ErrorHandler(BaseHandler):

    def _autoload_html(self, uri_li):
        uri_li = [i for i in uri_li if i]
        tmpl = '/' . join(uri_li[1:])
        params = {}
        self.render(tmpl, **params)

    def prepare(self):
        super(ErrorHandler, self).prepare()
        uri_li = self.request.uri.split('?', 1)[0].split('/')
        if uri_li[-1].endswith('.html'):
            return self._autoload_html(uri_li)
        raise Http404()


if settings.MIDDLEWARE_CLASSES:
    from .mixins.middleware import MiddlewareHandlerMixin

    BaseHandler.__bases__ = (MiddlewareHandlerMixin,) + BaseHandler.__bases__
