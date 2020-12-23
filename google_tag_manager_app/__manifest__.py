# -*- coding: utf-8 -*-
# Copyright 2019 oopo.io
{
    'name': 'Google Tag Manager',
    'category': 'Website',
    'summary': 'Enable Google Tag Manager in Odoo',
    'version': '13.0.0.0.2',
    'license': 'LGPL-3',
    'author': 'Oopo.io',
    'depends': [
        'website',
        'website_sale',
    ],
    'data': [
        'views/assets.xml',
        'views/layout.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': [
        'static/description/cover.png',
    ],
    'installable': True,
    'application': False,
    "price": 49,
    "currency": "EUR",
}
