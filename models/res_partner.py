# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    poa_permission_ids = fields.Many2many(
        comodel_name='poa.permission',
        relation='poa_permission_res_partner_rel',
        column1='partner_id',
        column2='permission_id',
        string=_('POA Permissions / Authorities'),
        help=_('Select the authorities this client is authorized for.'),
    )


