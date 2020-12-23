# -*- coding: utf-8 -*-
# Copyright 2019 Oopo.io
from odoo import fields, models


class Website(models.Model):

    _inherit = 'website'
    google_tag_manager_key = fields.Char()
