# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PoaPermission(models.Model):
    _name = 'poa.permission'
    _description = 'POA Permission'
    _order = 'name_en, id'
    _rec_name = 'name_en'

    # Short bilingual names (new fields)
    name_en = fields.Char(string=_('Permission Name (EN)'), required=False, translate=False)
    name_ar = fields.Char(string=_('Permission Name (AR)'), required=False, translate=False)

    # Long bilingual descriptions (renamed from former name fields)
    description_en = fields.Char(string=_('Permission Description (EN)'), required=True, translate=False, oldname='name_en')
    description_ar = fields.Char(string=_('Permission Description (AR)'), required=True, translate=False, oldname='name_ar')

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='poa_permission_res_partner_rel',
        column1='permission_id',
        column2='partner_id',
        string=_('Clients'),
    )

    _sql_constraints = [
        ('name_en_unique', 'unique(name_en)', 'English permission name must be unique.'),
        ('name_ar_unique', 'unique(name_ar)', 'Arabic permission name must be unique.'),
    ]

    @api.constrains('description_en', 'description_ar')
    def _check_descriptions_not_empty(self):
        for rec in self:
            if not rec.description_en or not rec.description_ar:
                raise ValidationError(_('Both English and Arabic permission descriptions are required.'))


    def name_get(self):
        """Return a language-aware display name.

        - Arabic UI (lang startswith 'ar'): show name_ar
        - Otherwise: show name_en
        Fallback to the other name if one is missing; finally to record id.
        Vectorized, no extra queries.
        """
        # Prefer session/context language; fallback to user's language
        lang = (self.env.context.get('lang') or self.env.user.lang or '').lower()
        is_arabic = lang.startswith('ar')
        result = []
        for record in self:
            # Prefer short names; fallback to descriptions; finally id
            name_ar = (record.name_ar or record.description_ar or '').strip()
            name_en = (record.name_en or record.description_en or '').strip()
            if is_arabic:
                display = name_ar or name_en or str(record.id)
            else:
                display = name_en or name_ar or str(record.id)
            result.append((record.id, display))
        return result

    @api.depends_context('lang')
    @api.depends('name_en', 'name_ar', 'description_en', 'description_ar')
    def _compute_display_name(self):
        """Ensure display_name follows the same localization as name_get.
        This helps widgets relying on display_name cache the correct label.
        """
        lang = (self.env.context.get('lang') or self.env.user.lang or '').lower()
        is_arabic = lang.startswith('ar')
        for record in self:
            name_ar = (record.name_ar or record.description_ar or '').strip()
            name_en = (record.name_en or record.description_en or '').strip()
            if is_arabic:
                record.display_name = name_ar or name_en or str(record.id)
            else:
                record.display_name = name_en or name_ar or str(record.id)

