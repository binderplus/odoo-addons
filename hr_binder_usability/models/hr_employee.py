# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    start_date = fields.Date(
        'Start Date',
        help='The date the employee started working at this firm!.',
        default=fields.Date.today)

    start_date_real = fields.Date(
        'Real Start Date',
        help='The real date the employee started working at this firm, off the record.',
        default=fields.Date.today)

    end_date = fields.Date(
        'End Date',
        help='The date the employeed left this firm')

    end_reason = fields.Char(
        'End Reason',
        help='Why did the employee left the firm.')

    union_id = fields.Many2one(
        'hr.union',
        string='Union',
        help='The union where this employee is registered')

    union_category_id = fields.Many2one(
        'hr.union.category',
        string='Union Category')

    union_is_affiliated = fields.Boolean(
        'Affiliated to Union?',
        help='Check if the employee is affiliated to the union')

    state = fields.Selection([
        ('draft',    'Draft'),
        ('hired',    'Hired'),
        ('resigned', 'Resigned'),
        ('fired',    'Fired'),
        ('retired',  'Retired')],
        string='State',
        help='The status of this employee',
        default='draft',
        required=True)
