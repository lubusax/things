{
    'name': "Things RAS - RFID Attendance",
    'summary': "Connect your Things RAS RFID Attendance with Odoo",       
    'description': """Receive RFID Attendance Clockings directly in Odoo.
        Manage your Thins RAS RFID Terminal from Odoo. """,

    'version': '12.0.2.0.210211', # update controllers.main.ThingsRasGate
    'category': 'Things',
    'website': "https://thingsintouch.com",
    'images': [
        'static/description/icon.png',
    ],
    'author': "thingsintouch.com",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,    
    'depends': ['base'],
    'data': [
        'security/things_ras_rfid_attendance.xml',
        'security/ir.model.access.csv',
        'views/things_menus.xml',
        'views/things_gate.xml',
        'views/things_ras2.xml'
    ],
# 'demo': ['demo.xml'],
}