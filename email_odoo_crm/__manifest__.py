{
    'name': 'ODOO Email CRM',
    'version': '1.0.0',
    'category': 'CRM/CRM',
    'author': 'ODOO Email.',
    'sequence': 1,
    'summary': 'Email Fetch into the ODOO from Gmail',
    'description': 'Email Fetch in ODOOO',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
