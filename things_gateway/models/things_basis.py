from odoo import models, fields
from uuid import uuid4

class ThingsBasis(models.AbstractModel):
    _name = 'things.basis'
    _description = 'Basis Model for a Things Gateway'

    # Machine ID identifies the linux machines (Gateway) uniquely
    hashed_machine_id = fields.Char(readonly = True)

    _sql_constraints = [ (  'hashed_machine_id_uniq',
                            'UNIQUE (hashed_machine_id)',
                            'Machine ID must be unique.') ]

    # manufacturingData
    firmwareAtShipment = fields.Char(readonly = True)
    productName = fields.Char("Type", readonly = True)
    productionDate = fields.Char(readonly = True)
    productionLocation = fields.Char(readonly = True)
    productionNumber = fields.Char(readonly = True)
    qualityInspector = fields.Char(readonly = True)

    #info not to be changed in Odoo
    firmwareVersion = fields.Char("Firmware Version", readonly = True)
    ipAddress = fields.Char("Local IP Address", readonly = True) # on the device "ownIpAddress"
    incrementalLog = fields.Text('Incremental Log', readonly = True)
    #linesOfIncrementalLog = fields

    #info to be changed in Odoo

    location = fields.Char('Location')
    ssh  = fields.Char() #enable, disable
    sshPassword = fields.Char()
    shouldGetFirmwareUpdate = fields.Boolean("Update Firmware",
            help = "when rebooted, the firmware will be updated")
    setRebootAt = fields.Datetime('Reboot Time',
            help = 'Time when the Terminal will be rebooted',
            default = None)
    shutdownTerminal = fields.Boolean("Shutdown",
            help = "Shutdown the Terminal immediately",
            default = False)


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