from odoo import models, fields
from odoo.exceptions import UserError

class GateConfirmWizard(models.TransientModel):
    _name = 'gate.confirm.wizard'
    _description = 'description'

    def confirm_new_gate(self):
        self.ensure_one()
        gate = self.env['things.gate'].sudo().search(
            [('confirmed', '=', False)])
        if gate:
            gate.write({
                'confirmed' : True,
                })
            action =  gate.get_formview_action()
            return action
        else:
            raise UserError('There is no Gate '
                            'awaiting to be confirmed')
            