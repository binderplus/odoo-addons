# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api


class HrUnion(models.Model):
    _name = 'hr.union'

    name = fields.Char(required=True)
    union_category_ids = fields.One2many(
        'hr.union.category',
        'union_id',
        string='Categories')


class HrUnionCategory(models.Model):
    _name = 'hr.union.category'

    name = fields.Char(required=True)
    description = fields.Text()
    union_id = fields.Many2one(
        'hr.union',
        string='Union',
        required=True)
