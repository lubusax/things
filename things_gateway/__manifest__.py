{
    'name': "Things Gateway",
    'summary': "Connect Odoo to your sensors and devices",       
    'description': """Receive and send data
        from/to your sensors and devices.
        Manage your Things Gateways that guide the data between your sensors/devices and Odoo. """,

    'version': '12.0.1.0.210211',
    'category': 'Things',
    'website': "http://www.thingsintouch.com",
    'images': [
        'static/description/icon.png',
    ],
    'author': "thingsintouch.com",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,    
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/things_menus.xml',
        'views/things_gate.xml',
        'views/popup_wizard.xml',
    ],
# 'demo': ['demo.xml'],
}