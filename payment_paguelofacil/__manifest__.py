# -*- coding: utf-8 -*-
{
    'name': "Paguelo Facil",
    'category': 'eCommerce',
    'license': 'LGPL-3',
    'summary': 'Pagos por PagueloFacil',
    'author': "3mit",
    'description': '''
    ''',
    'depends': [
        'payment'
    ],
    'data': [
        'views/payment_views.xml',
        'views/payment_paguelofacil_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'demo': [
        'demo.xml'
    ],
    'images': [
    ],
    'installable': True,
}
