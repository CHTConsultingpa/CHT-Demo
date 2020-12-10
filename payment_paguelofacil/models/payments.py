# -*- coding: utf-8 -*-
import logging
import pprint
import json
from odoo.http import request
from odoo.exceptions import UserError,Warning
from datetime import timedelta, date, datetime, time
import requests
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

from .. vendor.PaguelofacilPaymentsSDK import PaguelofacilPaymentsSDK

class PaguelofacilPaymentsAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('paguelofacil_payments', 'Paguelofacil Payments')])
    paguelofacil_access_key = fields.Char(string='Código Web')
    paguelofacil_secret_key = fields.Char(string='Secret Key')
    environment = fields.Char()

    def paguelofacil_payments_form_generate_values(self, values):
        self.ensure_one()
        paguelofacil_tx_values = dict(values)
        self.environment = self.state
        paguelofacil_tx_values.update({
            "environment" 	        : self.environment,
            "customer_first_name" 	: values.get('partner_first_name'),
            "customer_last_name"  	: values.get('partner_last_name'),
            "customer_email"  		: values.get('partner_email'),
            "customer_phone" 		: values.get('partner_phone'),
            "customer_city"         : values.get('partner_city') or '',
            "customer_address"      : values.get('partner_address') or '',
            "customer_postal_code"  : values.get('partner_zip') or '',
            'amount'                : values.get('amount') or '',
            'currency'              : 'EUR',
        })

        return paguelofacil_tx_values

    def paguelofacil_payments_get_form_action_url(self):
        self.ensure_one()
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')  + '/payment/paguelofacil_payments/redirect'

class PaymentTransactionPaguelofacilPayments(models.Model):
    _inherit = 'payment.transaction'
    
    def compose_callback_url(self, reference, is_notification):
        return '{}/payment/paguelofacil_payments/callback?merchant_reference={}{}'.format(
            self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            reference,
            '&is_notification=1' if is_notification else ''
        )

    def get_redirect_url(self, values):

        ''' 
        Use payment data from transaction to create redirect url 
        with Paguelofacil Payments SDK
        '''
        payment_data = {
            'amount':                values.get('amount'),
            "merchant_reference"   : self.reference,
            "customer_first_name"  : values.get('customer_first_name'), 
            "customer_last_name"   : values.get('customer_last_name'), 
            "customer_email"       : values.get('customer_email'), 
            "customer_phone"       : values.get('customer_phone'),
            "customer_city"        : values.get('customer_city'),
            "customer_address"     : values.get('customer_address'),
            "customer_postal_code" : values.get('customer_postal_code'),
            'amount'               : values.get('amount'),
            'currency'             : values.get('currency'),
            'merchant_return_url'  : self.compose_callback_url(self.reference, False),
            'merchant_notification_url'  : self.compose_callback_url(self.reference, True),
        }

        sdk = PaguelofacilPaymentsSDK(
            self.acquirer_id.paguelofacil_access_key,
            self.acquirer_id.paguelofacil_secret_key,
            'sandbox' if self.acquirer_id.environment == 'test' else 'production'
        )

        sdk.payment_data = payment_data
        _logger.info(self.acquirer_id.paguelofacil_secret_key)

        return sdk.get_payment_url()
    
    def paguelofacil_payments_callback(self, values):
        ''' Validate Paguelofacil Payments status. '''
        _logger.info('\nValidating Paguelofacil Payments - Order:{}'.format(values.get('merchant_reference')))
        
        former_tx_state = self.state

        redirect_url = '/shop/payment'

        # if not values.get('CCLW'):
        #     return redirect_url
        #
        # payment_info = PaguelofacilPaymentsSDK.decode_payment_token(
        #     values.get('CCLW'),
        #     self.acquirer_id.paguelofacil_access_key
        # )
        #
        # if not payment_info:
        #     return redirect_url
        var = True
        # if (values.get('Estado') == 'Denegado') or (values.get('Estado') == 'Denegada'):
        #     self._set_transaction_error(json.dumps(values))

        if var:
            # redirect_url = 'http://localhost:8071/payment/process/' # TODO: Remove localhost
            redirect_url = '/payment/process'

            # mark a new state for the transaction
            self._set_transaction_done()
            self.write({
                'state': 'done',
                'date': fields.Datetime.now(),
                'state_message': '',
            })
            if self.state == 'done' and self.state != former_tx_state:
                _logger.info('Validated Paguelofacil Payments for tx %s: set as done' % (self.reference))

                # actually write to DB that transaction is done (webhook)
                self._post_process_after_done()
        
        return redirect_url

