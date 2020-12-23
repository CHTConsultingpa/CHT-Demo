odoo.define('google_tag_manager.gtm', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;
    
    var timeout;
    
    publicWidget.registry.addToCartGTM = publicWidget.Widget.extend({
        selector: '#product_details',
        events: {
            'click #add_to_cart': '_onClick',
        },
        _onClick: function (evt) {
            var $tgt = $(evt.currentTarget);
            dataLayer.push({
                'event': 'addToCart',
                'ecommerce': {
                    'currencyCode': $tgt.data('currency'),
                    'add': {
                        'products': [{
                            'name': $tgt.data('name'),
                            'id': $tgt.data('code'),
                            'price': $tgt.data('price'),
                            'brand': $tgt.data('company'),
                            'category': $tgt.data('category'),
                            'position': $tgt.data('pid'),
                            'quantity': 1
                        }]
                    }
                },
            });
        },
    });
    publicWidget.registry.productLinkClickGTM = publicWidget.Widget.extend({
        selector: '.oe_product_cart',
        events: {
            'click .oe_product_image_link': '_onClick',
            'click .oe_product_name_link': '_onClick',
        },
        _onClick: function (evt) {
            var $tgt = $(evt.currentTarget);
            dataLayer.push({
                'event': 'productClick',
                'ecommerce': {
                    'click': {
                        'products': [{
                            'name': $tgt.data('name'),
                            'id': $tgt.data('code'),
                            'price': $tgt.data('price'),
                            'brand': $tgt.data('company'),
                            'category': $tgt.data('category'),
                            'position': $tgt.data('pid'),
                            'list': 'Search Results',
                            'quantity': 1
                        }]
                    }
                },
            });
        },
    });
    publicWidget.registry.removeFromCartGTM = publicWidget.Widget.extend({
        selector: '.js_cart_lines',
        events: {
            'click .js_delete_product': '_onClick',
        },
        _onClick: function (evt) {
            var $tgt = $(evt.currentTarget);
            dataLayer.push({
                'event': 'removeFromCart',
                'ecommerce': {
                    'remove': {
                        'products': [{
                            'name': $tgt.data('name'),
                            'id': $tgt.data('code'),
                            'price': $tgt.data('price'),
                            'brand': $tgt.data('company'),
                            'category': $tgt.data('category'),
                            'position': $tgt.data('pid'),
                            'quantity': 1,
                        }]
                    }
                },
            });
        },
    });
});
