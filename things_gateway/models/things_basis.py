from odoo import models, fields
from uuid import uuid4

class ThingsBasis(models.AbstractModel):
    _name = 'things.basis'
    _description = 'Basis Model for a Things Gateway'

    # Machine ID identifies the linux machines (Gateway) uniquely
    hashed_machine_id = fields.Char()

    _sql_constraints = [ (  'hashed_machine_id_uniq',
                            'UNIQUE (hashed_machine_id)',
                            'Machine ID must be unique.') ]

    # manufacturingData
    firmwareAtShipment = fields.Char()
    productName = fields.Char()
    productionDate = fields.Char()
    productionLocation = fields.Char()
    productionNumber = fields.Char()
    qualityInspector = fields.Char()

    #info not to be changed in Odoo
    firmwareVersion = fields.Char()
    ipAddress = fields.Char() # on the device "ownIpAddress"

    #info to be changed in Odoo

    location = fields.Char('Location')
    ssh  = fields.Char() #enable, disable
    sshPassword = fields.Char()


    def generate_route(self):
        return self.env['things.route'].create({}).route

    routefromOdooToDevice =fields.Char(
        string = 'route from Odoo To Device',
        help = 'route for outgoing data from the database to the thing/gate',
        default = generate_route,
        store = True,
        compute_sudo = False,
        readonly = True
        )
        
    routefromDeviceToOdoo =fields.Char(
        string = 'route from Device To Odoo',
        help = 'route for incoming data from the thing/gate to the database',
        default = generate_route,
        store = True,
        compute_sudo = False,
        readonly = True
        )

    # can_receive = fields.Boolean(
    #     'can process/needs data from the database',
    #     default = True)

    # can_send = fields.Boolean(
    #     'can send data to the database',
    #     default = True)