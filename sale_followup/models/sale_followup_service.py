# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class SaleFollowupService(models.Model):
    _name = 'sale.followup.service'
    _description = 'Process Sale Followup'

    @api.model
    def run_sale_followup_update(self):
        partners = self.env['res.partner'].search([
            ('sale_followup_setting', '!=', 'False'),
            ('sale_followup_setting', '!=', 'no_followup')])
        partners.process_sale_followup()
