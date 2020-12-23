# -*- coding: utf-8 -*-
{
    'name': 'Product Additional Price',
    'version': '1.0',
    'category': 'Product',
    "license": "OPL-1",
    'description': """
        Allow you to input additional sale price into the variant
    """,
    'author': 'Felix',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        "views/product_product_view.xml"
    ],

    'test': [],
    'demo': [],
    'qweb': [
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'active': True,
    'application': False,
}
