from odoo import api, models, fields


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    email_user_name = fields.Char("Email")
    email_password = fields.Char("Password")
    imap_server = fields.Char("IMAP Server")
    email_folder = fields.Selection(
        [("inbox", "Inbox")], 'Folder'
    )
