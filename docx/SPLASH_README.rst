==============================================
Scrapy & JavaScript integration through Splash
==============================================

.. image:: https://img.shields.io/pypi/v/scrapy-splash.svg
   :target: https://pypi.python.org/pypi/scrapy-splash
   :alt: PyPI Version

.. image:: https://travis-ci.org/scrapy-plugins/scrapy-splash.svg?branch=master
   :target: http://travis-ci.org/scrapy-plugins/scrapy-splash
   :alt: Build Status

.. image:: http://codecov.io/github/scrapy-plugins/scrapy-splash/coverage.svg?branch=master
   :target: http://codecov.io/github/scrapy-plugins/scrapy-splash?branch=master
   :alt: Code Coverage

This library provides Scrapy_ and JavaScript integration using Splash_.
The license is BSD 3-clause.

.. _Scrapy: https://github.com/scrapy/scrapy
.. _Splash: https://github.com/scrapinghub/splash

Installation
============

Install scrapy-splash using pip::

    $ pip install scrapy-splash

Scrapy-Splash uses Splash_ HTTP API, so you also need a Splash instance.
Usually to install & run Splash, something like this is enough::

    $ docker run -p 8050:8050 scrapinghub/splash

Check Splash `install docs`_ for more info.

.. _install docs: http://splash.readthedocs.org/en/latest/install.html


Configuration
=============

1. Add the Splash server address to ``settings.py`` of your Scrapy project
   like this::

      SPLASH_URL = 'http://192.168.59.103:8050'

2. Enable the Splash middleware by adding it to ``DOWNLOADER_MIDDLEWARES``
   in your ``settings.py`` file and changing HttpCompressionMiddleware
   priority::

      DOWNLOADER_MIDDLEWARES = {
          'scrapy_splash.SplashCookiesMiddleware': 723,
          'scrapy_splash.SplashMiddleware': 725,
          'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
      }

   Order `723` is just before `HttpProxyMiddleware` (750) in default
   scrapy settings.

   HttpCompressionMiddleware priority should be changed in order to allow
   advanced response processing; see https://github.com/scrapy/scrapy/issues/1895
   for details.

3. Enable ``SplashDeduplicateArgsMiddleware`` by adding it to
   ``SPIDER_MIDDLEWARES`` in your ``settings.py``::

      SPIDER_MIDDLEWARES = {
          'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
      }

   This middleware is needed to support ``cache_args`` feature; it allows
   to save disk space by not storing duplicate Splash arguments multiple
   times in a disk request queue. If Splash 2.1+ is used the middleware
   also allows to save network traffic by not sending these duplicate
   arguments to Splash server multiple times.

4. Set a custom ``DUPEFILTER_CLASS``::

      DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

5. If you use Scrapy HTTP cache then a custom cache storage backend
   is required. scrapy-splash provides a subclass of
   ``scrapy.contrib.httpcache.FilesystemCacheStorage``::

      HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

   If you use other cache storage then it is necesary to subclass it and
   replace all ``scrapy.util.request.request_fingerprint`` calls with
   ``scrapy_splash.splash_request_fingerprint``.

.. note::

    Steps (4) and (5) are necessary because Scrapy doesn't provide a way
    to override request fingerprints calculation algorithm globally; this
    could change in future.


There are also some additional options available.
Put them into your ``settings.py`` if you want to change the defaults:

* ``SPLASH_COOKIES_DEBUG`` is ``False`` by default.
  Set to ``True`` to enable debugging cookies in the ``SplashCookiesMiddleware``.
  This option is similar to ``COOKIES_DEBUG``
  for the built-in scarpy cookies middleware: it logs sent and received cookies
  for all requests.
* ``SPLASH_LOG_400`` is ``True`` by default - it instructs to log all 400 errors
  from Splash. They are important because they show errors occurred
  when executing the Splash script. Set it to ``False`` to disable this logging.
* ``SPLASH_SLOT_POLICY`` is ``scrapy_splash.SlotPolicy.PER_DOMAIN`` (as object, not just a string) by default.
  It specifies how concurrency & politeness are maintained for Splash requests,
  and specify the default value for ``slot_policy`` argument for
  ``SplashRequest``, which is described below.


Usage
=====

Requests
--------

The easiest way to render requests with Splash is to
use ``scrapy_splash.SplashRequest``::

    yield SplashRequest(url, self.parse_result,
        args={
            # optional; parameters passed to Splash HTTP API
            'wait': 0.5,

            # 'url' is prefilled from request url
            # 'http_method' is set to 'POST' for POST requests
            # 'body' is set to request body for POST requests
        },
        endpoint='render.json', # optional; default is render.html
        splash_url='<url>',     # optional; overrides SPLASH_URL
        slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
    )

Alternatively, you can use regular scrapy.Request and
``'splash'`` Request `meta` key::

    yield scrapy.Request(url, self.parse_result, meta={
        'splash': {
            'args': {
                # set rendering arguments here
                'html': 1,
                'png': 1,

                # 'url' is prefilled from request url
                # 'http_method' is set to 'POST' for POST requests
                # 'body' is set to request body for POST requests
            },

            # optional parameters
            'endpoint': 'render.json',  # optional; default is render.json
            'splash_url': '<url>',      # optional; overrides SPLASH_URL
            'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
            'splash_headers': {},       # optional; a dict with headers sent to Splash
            'dont_process_response': True, # optional, default is False
            'dont_send_headers': True,  # optional, default is False
            'magic_response': False,    # optional, default is True
        }
    })

Use ``request.meta['splash']`` API in middlewares or when scrapy.Request
subclasses are used (there is also ``SplashFormRequest`` described below).
For example, ``meta['splash']`` allows to create a middleware which enables
Splash for all outgoing requests by default.

``SplashRequest`` is a convenient utility to fill ``request.meta['splash']``;
it should be easier to use in most cases. For each ``request.meta['splash']``
key there is a corresponding ``SplashRequest`` keyword argument: for example,
to set ``meta['splash']['args']`` use ``SplashRequest(..., args=myargs)``.

* ``meta['splash']['args']`` contains arguments sent to Splash.
  scrapy-splash adds some default keys/values to ``args``:

  * 'url' is set to request.url;
  * 'http_method' is set to 'POST' for POST requests;
  * 'body' is set to to request.body for POST requests.

  You can override default values by setting them explicitly.

  Note that by default Scrapy escapes URL fragments using AJAX escaping scheme.
  If you want to pass a URL with a fragment to Splash then set ``url``
  in ``args`` dict manually. This is handled automatically if you use
  ``SplashRequest``, but you need to keep that in mind if you use raw
  ``meta['splash']`` API.

  Splash 1.8+ is required to handle POST requests; in earlier Splash versions
  'http_method' and 'body' arguments are ignored. If you work with ``/execute``
  endpoint and want to