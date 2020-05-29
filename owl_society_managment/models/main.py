from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    member_type = fields.Selection([
        ('treasurer', 'Treasurer'),
        ('member', 'Member'),
        ('secretary', 'Secretary'),
    ])
