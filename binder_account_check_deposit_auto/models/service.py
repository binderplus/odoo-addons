# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class CheckDepositService(models.Model):
    _name = 'account_check_deposit_auto.service'
    _description = 'Check Deposit Service'

    @api.model
    def run_check_deposit_service(self):
        checks = self.env['account.check'].search([
        	('type', '=', 'third_check'),
        	('state', '=', 'holding'),
        	('journal_id.name', '=', 'Cheques de Terceros en Banco Galicia CIG'),
            ('payment_date', '<=', fields.Date.today())])
        active_ids = [check.id for check in checks]
        # continue only if there are checks
        if not checks:
            return
        # check company_ids, all checks have to be of the same company
        company_ids = [x.company_id.id for x in checks]
        if len(set(company_ids)) > 1:
            raise Warning(_('All checks must be from the same company!'))
        company_id = checks[0].company_id
        # hardcoded journal (and account)
        deposit_journal = self.env['account.journal'].search([
        	('name', '=', 'Banco (Galicia)')])
        # check company again, checks' company should be the same as the deposit_journal/account
        if company_id.id != deposit_journal.company_id.id:
            raise Warning(_('This automated action will only work for BINDERPLUS S.R.L.'))
        # do wizard
        wizard = self.env['account.check.action'].create({
        	'action_type': 'deposit',
        	'date': fields.Date.today(),
        	'journal_id': deposit_journal.id,
        	'account_id': deposit_journal.default_debit_account_id.id,
            'company_id': company_id.id,
        	})
        # confirm
        wizard.with_context({'active_ids':active_ids}).action_confirm()

