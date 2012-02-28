var django_js_utils = {};

django_js_utils.urls = function(){

    function _get_path(name, kwargs, resolver)
    {
        var path = resolver[name] || false;

        if (!path)
        {
            throw('URL not found for view: ' + name);
        }

        var _path = path;

        var key;
        for (key in kwargs)
        {
            if (kwargs.hasOwnProperty(key)) {
                if (!path.match('<' + key +'>'))
                {
                    throw(key + ' does not exist in ' + _path);
                }
                path = path.replace('<' + key +'>', kwargs[key]);
            }
        }

        var re = new RegExp('<[a-zA-Z0-9-_]{1,}>', 'g');
        var missing_args = path.match(re);
        if (missing_args)
        {
            throw('Missing arguments (' + missing_args.join(", ") + ') for url ' + _path);
        }

        return path;

    }

    return {
        resolve: function(name, kwargs, resolver) {
            if (!resolver)
            {
                resolver = django_js_utils_urlconf || {};
            }

            return _get_path(name, kwargs, resolver);
        }
    };

}();
