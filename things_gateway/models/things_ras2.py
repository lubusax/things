from odoo import models, fields
from uuid import uuid4
from odoo.addons.base.models.res_partner import _tz_get


class ThingsRAS2(models.Model):
    _name = 'things.ras2'
    _description = 'Model for the RFID Attendance Terminal'


  # Factory Settings ########################################################
    firmwareAtShipment = fields.Char(readonly = True)
    productName = fields.Char("Type", readonly = True)
    productionDate = fields.Char(readonly = True)
    productionLocation = fields.Char(readonly = True)
    productionNumber = fields.Char(readonly = True)
    qualityInspector = fields.Char(readonly = True)
    SSIDreset = fields.Char(readonly = True)

    # Machine ID identifies the linux machines (Gateway) uniquely
    hashed_machine_id = fields.Char(readonly = True)

    _sql_constraints = [ (  'hashed_machine_id_uniq',
                            'UNIQUE (hashed_machine_id)',
                            'Machine ID must be unique.') ]
    
    https = fields.Boolean(readonly = True)
    odoo_host = fields.Char(readonly = True)
    odoo_port = fields.Char(readonly = True)
    odooConnectedAtLeastOnce = fields.Boolean(readonly = True)
    odooUrlTemplate = fields.Char(readonly = True) ###################### to deprecate
    fileForMessages = fields.Char(readonly = True) ###################### to deprecate
    teminalSetupManagement = fields.Char(readonly = True) # "remotely, on Odoo" "locally, on the terminal"#### to deprecate


  # RAS2 Device Setup ##############################################################
    hasCompletedSetup =  fields.Boolean(readonly = True)
    admin_id = fields.Char(readonly = True) ############################# to deprecate
    db = fields.Char(readonly = True) ################################### to deprecate
    user_name = fields.Char(readonly = True) ############################ to deprecate
    user_password = fields.Char(readonly = True)# ####################### to deprecate
    timezone = fields.Char("timezone in +xx:xx"
        ,readonly = True) # "+01:00" ################ to deprecate  # to be substituted by "tz"


  # UPDATED_FROM_ODOO_ONLY_ON_START ###############################################

    #>>>>>>>>>>>> terminalIDinOdoo is the id ####################################

    RASxxx = fields.Char(readonly = True)

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

    version_things_module_in_Odoo = fields.Char(readonly = True)  

    ownIpAddress = fields.Char("Local IP Address", readonly = True)


  # UPDATED_FROM_ODOO_ON_ROUTINE_CALLS #####################################
    #  can be changed anytime when connected to Odoo through routine calls
    ssh =  fields.Boolean()
    showEmployeeName = fields.Boolean()
    sshPassword = fields.Char()
    language = fields.Char()
    tz = fields.Selection(
        _tz_get, string='Timezone', required=True,
        default=lambda self: self._context.get('tz') or self.env.user.tz or 'Europe/Madrid',
        help="In which timezone the Device will display time.")
    time_format = fields.Selection(
        [("12 hour","12 hour"),("24 hour","24 hour")],
        string='12 or 24-hour',
        required=True,
        default= "12 hour",
        help="am/pm or 00:00 to 23:59")
    timeoutToCheckAttendance = fields.Float()  
    periodEvaluateReachability = fields.Float()  
    periodDisplayClock = fields.Float()   
    timeToDisplayResultAfterClocking = fields.Float()  
    location = fields.Char('Location')
    shouldGetFirmwareUpdate = fields.Boolean("Update Firmware",
        help = "when rebooted, the firmware will be updated")
    setRebootAt = fields.Datetime('Reboot Time',
        help = 'Time when the Terminal will be rebooted',
        default = None)
    shutdownTerminal = fields.Boolean("Shutdown",
        help = "Shutdown the Terminal immediately",
        default = False)
    isRemoteOdooControlAvailable = fields.Boolean(readonly = True)  
    gitBranch = fields.Char()
    gitCommit = fields.Char()
    gitRemote = fields.Char()
    doFactoryReset = fields.Boolean()
    updateAvailable = fields.Boolean(readonly = True)
    lastConnectionOdooTerminal = fields.Datetime('Last Connection',
        help = "Timestamp of the last successful connection between the Device and Odoo",
        default = None,
        readonly = True)
    timeoutToGetOdooUID = fields.Float() ############################ to deprecate


  # UPDATED_FROM_DEVICE: Updates are done through the Firmware #############################
    installedPythonModules = fields.Char("Installed Python Modules in the Terminal", readonly = True)
    firmwareVersion = fields.Char("Firmware Version", readonly = True)  
    lastFirmwareUpdateTime = fields.Datetime('Last Firmware Update',
      help = 'Last Update of the Firmware of the Terminal',
      default = None, readonly = True)
    lastTimeTerminalStarted = fields.Datetime('Last Time Device Started',
      default = None, readonly = True)
    updateFailedCount = fields.Integer("How Many Times the last Firmware Update Failed", readonly = True)
    incrementalLog = fields.Text('Last Log Entries', readonly = True)

    


    
