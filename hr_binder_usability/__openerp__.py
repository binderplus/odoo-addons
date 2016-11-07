# -*- coding: utf-8 -*-
# Copyright 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "BINDERPLUS HR Usability",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://www.binderplus.com.ar/",
    "author": "Iván Todorovich <ivan.todorovich@gmail.com>, BINDERPLUS S.R.L.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee.xml",
        "views/hr_union.xml",
    ]
}
