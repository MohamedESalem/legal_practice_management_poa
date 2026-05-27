# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class LegalPoaDownloadWizard(models.TransientModel):
    _name = 'legal.poa.download.wizard'
    _description = 'POA Download Wizard'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
        readonly=True,
    )
    poa_template_id = fields.Many2one(
        comodel_name='docx.report.config',
        string='POA Template',
        required=True,
        domain=[
            ('state', '=', 'published'),
            ('model_id.model', '=', 'res.partner'),
            ('action_report_id', '!=', False),
        ],
    )

    def action_download_poa(self):
        self.ensure_one()

        template = self.poa_template_id
        if (
            not template
            or template.state != 'published'
            or template.model_id.model != 'res.partner'
            or not template.action_report_id
        ):
            raise UserError(
                _(
                    'Please select a published POA template configured for clients.'
                )
            )

        action = template.action_report_id.report_action(self.partner_id)
        action['close_on_report_download'] = True
        return action
