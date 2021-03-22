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
    timezone = fields.Char("timezone in +xx:xx") # "+01:00"
    periodDisplayClock = fields.Float() 
    periodEvaluateReachability = fields.Float()
    timeToDisplayResultAfterClocking = fields.Float()
    timeoutToCheckAttendance = fields.Float()
    timeoutToGetOdooUID = fields.Float()
    hour12or24 = fields.Selection(
        [("12 hour","12 hour"),("24 hour","24 hour")],
        string='12 or 24-hour',
        required=True,
        default= "12 hour",
        help="am/pm or 00:00 to 23:59")