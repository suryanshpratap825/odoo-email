from odoo import api, models, fields


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    email_user_name = fields.Char("Email")
    email_password = fields.Char("Password")
