from odoo import models, fields
from uuid import uuid4

class ThingsBasis(models.AbstractModel):
    _name = 'things.basis'
    _description = 'description'

    name = fields.Char('Name')
    location = fields.Char('Location')
    confirmed = fields.Boolean(
        'Confirmed?',
        default = False)
    serial_number = fields.Char(
        string='Serial Number',
        default = generate_default_serial_number)
    
    _sql_constraints = [ (  'serial_number_uniq',
                            'UNIQUE (serial_number)',
                            'Serial Number must be unique.') ]

    def generate_route(self):
        return self.env['things.route'].create({}).route
    
    def generate_default_serial_number(self):
        result = str(fields.Datetime.now())
        result = result.replace(" ","").replace(":","").replace("-","")
        result= "serial number not provided - " + result
        return result

    route_to =fields.Char(
        string = 'route to thing/gate',
        help = 'route for outgoing data from the database to the thing/gate',
        default = generate_route,
        store = True,
        compute_sudo = False,
        readonly = True
        )
        
    route_from =fields.Char(
        string = 'route from thing/gate',
        help = 'route for incoming data from the thing/gate to the database',
        default = generate_route,
        store = True,
        compute_sudo = False,
        readonly = True
        )

    can_receive = fields.Boolean(
        'can process/needs data from the database',
        default = True)

    can_send = fields.Boolean(
        'can send data to the database',
        default = True)