from django.core.urlresolvers import RegexURLPattern

_patterns = set()

def expose_to_js(pattern):
    if issubclass(pattern.__class__, RegexURLPattern):
        if pattern.name:
            _patterns.add(pattern)
    return pattern