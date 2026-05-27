# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        compute='_compute_poa_report_partner_id',
        help='Compatibility alias for POA DOCX templates rendered directly from a client.',
    )
    poa_permission_ids = fields.Many2many(
        comodel_name='poa.permission',
        relation='poa_permission_res_partner_rel',
        column1='partner_id',
        column2='permission_id',
        string=_('POA Permissions / Authorities'),
        help=_('Select the authorities this client is authorized for.'),
    )

    def _compute_poa_report_partner_id(self):
        for partner in self:
            partner.partner_id = partner

    def action_open_poa_download_wizard(self):
        self.ensure_one()
        action = self.env.ref(
            'legal_practice_management_poa.action_legal_poa_download_wizard'
        ).read()[0]
        action['context'] = {
            **self.env.context,
            'default_partner_id': self.id,
        }
        return action

