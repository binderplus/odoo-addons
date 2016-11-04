# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        if res:
            # notify the live leads that we have an order
            leads = self.env['crm.lead'].sudo().search([
                ('type', '=', 'opportunity'),
                ('stage_id.fold', '!=', 'True'),
                ('partner_id', 'child_of', self.commercial_partner_id.id)])
            for lead in leads:
                # notify partners that are users with base.group_user group
                notify_partners = lead.message_follower_ids.filtered(
                    lambda p: p.user_ids.filtered(
                        lambda u: u.has_group('base.group_user')))
                notify_partners = [(4, p.id) for p in notify_partners]
                lead.sudo().message_post(
                    partner_ids=notify_partners,
                    body='<span>%(cname)s ha confirmado un pedido</span>'
                    '<div> &nbsp; &nbsp; • <b>Órden de Ventas</b>: '
                    '<a href="#id=%(id)d&model=sale.order">%(name)s</a></div>'
                    '<div> &nbsp; &nbsp; • <b>Importe sin Impuestos</b>: '
                    '%(amount_untaxed)f</div>'
                    % {
                        'cname': self.partner_id.display_name,
                        'id': self.id,
                        'name': self.name,
                        'amount_untaxed': self.amount_untaxed
                    })
        return res
