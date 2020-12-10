# -*- coding: utf-8 -*-

import json
import logging

import pprint
import werkzeug
from werkzeug import urls
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)

class PaguelofacilPaymentsControllers(http.Controller):

    @http.route(['/payment/paguelofacil_payments/redirect'], auth='public', csrf=False)
    def redirect_to_paguelofacil(self, **post):
        ''' Redirect to Paguelofacil Payments '''

        cr, context, env = http.request.cr, http.request.context, http.request.env

        tx = None
        if post.get('invoice_num'):
            tx = env['payment.transaction'].sudo().search([('reference', '=', post['invoice_num'])])
        if not tx:
            raise werkzeug.exceptions.NotFound()

        response = tx.get_redirect_url(post) #este es el URL que se envia
        return werkzeug.utils.redirect(response)

    def paguelofacil_payments_callback(self, post):
        ''' Validate Paguelofacil application status '''
        
        cr, context, env = http.request.cr, http.request.context, http.request.env

        if post:
            request.env['payment.transaction'].sudo().form_feedback(post, 'authorize')
        tx = None
        if post.get('merchant_reference'):
            tx = env['payment.transaction'].sudo().search([('reference', '=', post['merchant_reference'])])
        if not tx:
            raise werkzeug.exceptions.NotFound()

        redirect_url = tx.paguelofacil_payments_callback(post)


        # tx_ids_list = self.get_payment_transaction_ids()
        # _logger.info('Verificando tx_ids_list %s:' % (tx_ids_list))
        # payment_transaction_ids = request.env['payment.transaction'].sudo().browse(tx_ids_list).exists()
        # _logger.info('Verificando payment_transaction_ids %s:' % (payment_transaction_ids))
        # if not payment_transaction_ids:
        #     list = []
        #     list.append(tx.id)
        #     request.session["__payment_tx_ids__"] = list
        #     _logger.info('Forzando ID list %s:' % (list))
        return werkzeug.utils.redirect(redirect_url)

    # @staticmethod
    # def get_payment_transaction_ids():
    #     # return the ids and not the recordset, since we might need to
    #     # sudo the browse to access all the record
    #     # I prefer to let the controller chose when to access to payment.transaction using sudo
    #     return request.session.get("__payment_tx_ids__", [])

    @http.route(['/payment/paguelofacil_payments/callback'], type='http', auth='public', csrf=False)
    def handle_paguelofacil_payments_callback_http(self, **post):
        return self.paguelofacil_payments_callback(post)
