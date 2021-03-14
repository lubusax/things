from odoo import models, fields

class ThingsRAS2(models.Model):
    _name = 'things.ras2'
    _inherit = ['things.basis']

    #terminalIDinOdoo is the id

    #info to be changed in Odoo
    language = fields.Char()
    showEmployeeName  = fields.Char()# "yes", "no"
    terminalSetupManagement  = fields.Char()# "remotely, on Odoo" "locally, on the terminal"

    #time settings
    timezone = fields.Char() # "+01:00"
    periodDisplayClock = fields.Float() 
    periodEvaluateReachability = fields.Float()
    timeToDisplayResultAfterClocking = fields.Float()
    timeoutToCheckAttendance = fields.Float()
    timeoutToGetOdooUID = fields.Float()    