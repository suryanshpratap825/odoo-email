from odoo import api, models, fields
import imaplib
import email
from email.header import decode_header


class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"

    msgnumn_binary = fields.Char("Msgumn ID")

    def generate_name(self, message):
        if message.is_multipart():
            # If the email has multiple parts (e.g., text, HTML, attachments)
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    body = part.get_payload(decode=True).decode(part.get_content_charset())
                    print(body)
                    return body
        else:
            # If the email is not multipart (e.g., plain text email)
            body = message.get_payload(decode=True).decode(message.get_content_charset())
            print(body)
            return body

    def decode_subject(self, subject):
        decoded_subject = ""
        for part, charset in decode_header(subject):
            if isinstance(part, bytes):
                decoded_subject += part.decode(charset or 'utf-8')
            else:
                decoded_subject += part
        return decoded_subject

    def create_lead(self, message, msgnumn):
        self.create({
            'name': self.decode_subject(message.get('Subject')),
            'email_from': message.get('From'),
            'type': 'opportunity',
            'msgnumn_binary': str(msgnumn, 'utf-8'),
            'description': self.generate_name(message)
        })

    def _get_emails(self):
        get_user_id = self.env['res.users'].search([])
        imap = imaplib.IMAP4_SSL(get_user_id.imap_server)
        imap.login(get_user_id.email_user_name, get_user_id.email_password)

        imap.select(get_user_id.email_folder)

        _ok, msgnumns = imap.search(None, "UNSEEN")

        for msgnumn in msgnumns[0].split()[1: 10]:
            _, data = imap.fetch(msgnumn, "(RFC822)")

            message = email.message_from_bytes(data[0][1])
            self.create_lead(message, msgnumn)

        imap.close()

    def write(self, vals):
        result = super(CrmLeadInherit, self).write(vals)
        if vals.get('stage_id') and vals.get('stage_id') == self.env.ref('crm.stage_lead4').id:
            get_user_id = self.env['res.users'].search([])
            imap = imaplib.IMAP4_SSL(get_user_id.imap_server)
            imap.login(get_user_id.email_user_name, get_user_id.email_password)
            imap.select(get_user_id.email_folder)
            imap.store(self.msgnumn_binary.encode('utf-8'), '+FLAGS', '\\Seen')
            imap.close()
        return result
