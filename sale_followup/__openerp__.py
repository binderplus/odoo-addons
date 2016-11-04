# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Followup",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://www.binderplus.com.ar/",
    "author": "Iván Todorovich <ivan.todorovich@gmail.com>, BINDERPLUS S.R.L.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        "crm"
    ],
    "data": [
        "security/sale_followup.xml",
        "views/res_partner_view.xml",
        "views/service_sale_followup.xml",
    ]
}
