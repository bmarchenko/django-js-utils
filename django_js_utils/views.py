# -*- coding: utf-8 -*-

import re
import sys

from django.conf import settings
from django.core.urlresolvers import RegexURLResolver
from django.http import HttpResponse
from django.utils import simplejson as json

from django_js_utils.core import _patterns


def prepare_response(urlconf=settings.ROOT_URLCONF):
    RE_KWARG = re.compile(r"(\(\?P<(.*?)>.*?\))")  # Pattern for recognizing named parameters in urls
    RE_ARG = re.compile(r"(\(.*?\))")  # Pattern for recognizing unnamed url parameters

    js_patterns = {}

    def handle_url_module(module_name, prefix="", view_prefix=""):
        """
        Load the module and output all of the patterns
        Recurse on the included modules
        """
        if isinstance(module_name, basestring):
            __import__(module_name)
            patterns = sys.modules[module_name].urlpatterns
        else:
            patterns = module_name

        for pattern in patterns:
            if isinstance(pattern, RegexURLResolver) and pattern.urlconf_name:
                ns = pattern.namespace
                handle_url_module(
                    pattern.urlconf_name,
                    prefix=pattern.regex.pattern,
                    view_prefix='%s%s:' % (view_prefix, ns) if ns else view_prefix
                )
            elif pattern in _patterns:
                full_url = prefix + pattern.regex.pattern
                for chr in ["^", "$"]:
                    full_url = full_url.replace(chr, "")
                    #handle kwargs, args
                kwarg_matches = RE_KWARG.findall(full_url)

                for el in kwarg_matches:
                    #prepare the output for JS resolver
                    full_url = full_url.replace(el[0], "<%s>" % el[1])
                    #after processing all kwargs try args
                args_matches = RE_ARG.findall(full_url)
                for el in args_matches:
                    full_url = full_url.replace(el, "<>")  # replace by a empty parameter name
                js_patterns[view_prefix + pattern.name] = "/" + full_url

    handle_url_module(urlconf)
    return 'django_js_utils_urlconf = ' + json.dumps(js_patterns)

_urlconfs = {
    settings.ROOT_URLCONF: prepare_response()
}


def jsurls(request):
    urlconf = settings.ROOT_URLCONF

    if hasattr(request, 'urlconf'):
        urlconf = request.urlconf
    if urlconf not in _urlconfs:
        _urlconfs[urlconf] = prepare_response(urlconf)

    response = HttpResponse(mimetype='text/javascript')
    response.write(_urlconfs.get(urlconf))
    return response
