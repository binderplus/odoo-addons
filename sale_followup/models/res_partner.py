# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    sale_followup_setting = fields.Selection([
        ('no_followup',		'Sin seguimiento'),
        ('1m',				'Una venta por mes'),
        ('15m',				'Una venta cada mes y medio'),
        ('2m',				'Una venta cada dos meses'),
        ('3m',				'Una venta cada tres meses'),
        ('6m',				'Una venta cada seis meses'),
        ('1y',				'Una venta cada un año')],
        string='Seguimiento',
        help='Se crearán Oportunidades de venta.')

    sale_followup_lead = fields.Many2one(
        'crm.lead',
        string='Oportunidad de Seguimiento',
        readonly=True)

    last_sale_date = fields.Date(
        'Fecha de la Última Venta',
        help='Fecha de la última venta confirmada.',
        compute='_compute_last_sale_date',
        store=True)

    # sale_followup_suspend_until_date = fields.Date(
    #    'Suspender seguimiento hasta',
    #    help='Suspende el seguimiento automático hasta la fecha establecida.')

    @api.one
    @api.depends('sale_order_ids')
    def _compute_last_sale_date(self):
        # TODO:
        # Improve this with read_group or something like that
        # to avoid some overhead at module install
        last_order = self.env['sale.order'].sudo().search([
            ('state', '!=', 'cancel'),
            ('commercial_partner_id', '=', self.commercial_partner_id.id)],
            limit=1,
            order='date_order DESC')
        if last_order:
            self.last_sale_date = last_order.date_order

    def _sale_followup_create_lead(self):
        last_sale_date = self.last_sale_date or 'Nunca'
        lead_obj = self.env['crm.lead']
        if self.sale_followup_lead:
            if self.sale_followup_lead.stage_id.fold is True:
                # lead is closed, we should get a new one
                self.sale_followup_lead = False
        if not self.sale_followup_lead:
            # try to get an open lead and convert it to followup
            lead = lead_obj.sudo().search([
                ('type', '=', 'opportunity'),
                ('stage_id.fold', '!=', 'True'),
                ('partner_id', 'child_of', self.commercial_partner_id.id)],
                limit=1,
                order='date_open DESC')
            if lead:
                self.sale_followup_lead = lead
            else:
                # create a new lead to track this followup
                followers = self.env.ref('sale_followup.group_manager').users
                followers = [(4, p.partner_id.id) for p in followers]
                lead = self.sale_followup_lead = lead_obj.sudo().create({
                    'type': 'opportunity',
                    'name': 'Pedido de %s' % self.commercial_partner_id.name,
                    'partner_id': self.id,
                    'message_follower_ids': followers,
                    'description':
                        'Se ha creado esta oportunidad porque '
                        'el cliente no compra desde: %s' % last_sale_date
                })
            # notify partners that belong to our company
            notify = self.sale_followup_lead.message_follower_ids.filtered(
                lambda p: p.user_ids.filtered(
                    lambda u: u.has_group('base.group_user')))
            notify = [(4, p.id) for p in notify]
            # post a message in the chatter
            self.sale_followup_lead.sudo().message_post(
                partner_ids=notify,
                body='<div> &nbsp; &nbsp; • '
                '<b>Última compra del cliente</b>: %s</div>' % last_sale_date)

    @api.one
    def process_sale_followup(self):
        future_days = {
            '1m': 30,
            '15m': 45,
            '2m': 60,
            '3m': 90,
            '6m': 180,
            '1y': 360
        }.get(self.sale_followup_setting, False)
        if not future_days:
            # no followup or invalid followup setting
            return
        if not self.last_sale_date:
            # no last sale records, immediate action required
            self._sale_followup_create_lead()
            return
        last_sale_date = datetime.strptime(self.last_sale_date, '%Y-%m-%d')
        expected_date = last_sale_date + timedelta(days=future_days)
        now = datetime.now()
        if now >= expected_date:
            # we are due for another sale
            self._sale_followup_create_lead()
