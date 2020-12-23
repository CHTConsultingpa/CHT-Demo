# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    additional_price = fields.Float(
        "Additional Price",
        help="Amount that will be added into the sale price")

    def _compute_product_price_extra(self):
        super(ProductProduct, self)._compute_product_price_extra()
        for product in self:
            product.price_extra += product.additional_price
