import re
import sys
from collections import namedtuple

from django.conf import settings
from django.http import HttpResponse
import django.utils.simplejson as json
from django.core.urlresolvers import RegexURLResolver

from django_js_utils.core import _patterns


def prepare_js_patterns():
    RE_KWARG = re.compile(r"(\(\?P<(.*?)>.*?\))") #Pattern for recognizing named parameters in urls
    RE_ARG = re.compile(r"(\(.*?\))") #Pattern for recognizing unnamed url parameters

    _Resolver = namedtuple('Resolver', ['urls', 'ns'])
    def Resolver():
        return _Resolver({}, {})


    def handle_url_module(resolver, module_name, prefix=""):
        """
        Load the module and output all of the patterns
        Recurse on the included modules
        """
        if isinstance(module_name, basestring):
            __import__(module_name)
            patterns = sys.modules[module_name].urlpatterns
        else:
            patterns = module_name

        have_patterns = False

        for pattern in patterns:
            if isinstance(pattern, RegexURLResolver) and pattern.urlconf_name:
                next_resolver = Resolver() if pattern.namespace else resolver
                if handle_url_module(next_resolver,
                    pattern.urlconf_name,
                    prefix=pattern.regex.pattern):
                    have_patterns = True
                    if pattern.namespace:
                        resolver.ns[pattern.namespace] = next_resolver
            elif pattern in _patterns:
                have_patterns = True
                full_url = prefix + pattern.regex.pattern
                for chr in ["^","$"]:
                    full_url = full_url.replace(chr, "")
                    #handle kwargs, args
                kwarg_matches = RE_KWARG.findall(full_url)
                for el in kwarg_matches:
                    #prepare the output for JS resolver
                    full_url = full_url.replace(el[0], "<%s>" % el[1])
                    #after processing all kwargs try args
                args_matches = RE_ARG.findall(full_url)
                for el in args_matches:
                    full_url = full_url.replace(el, "<>")#replace by a empty parameter name
                resolver.urls[pattern.name] = "/" + full_url

        return have_patterns

    js_patterns = Resolver()
    handle_url_module(js_patterns, settings.ROOT_URLCONF)
    return 'django_js_utils_urlconf = ' + json.dumps(js_patterns)

_js_patterns = prepare_js_patterns()


def jsurls(request):
    response = HttpResponse(mimetype='text/javascript')
    response.write(_js_patterns)
    return response

