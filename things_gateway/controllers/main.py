from odoo import http
import time
import logging
import json

_logger = logging.getLogger(__name__)

class ThingsGate(http.Controller):

    @http.route('/things/gates/create',
            type = 'json',
            auth = 'public',
            methods=['POST'],
            csrf = False)
    def RegisterNewGate(self, **kwargs):
        # create a new record things.gate
        # only if there is no things.gate
        # awaiting to be confirmed
        answer = {"error": None}
        try:
            data = http.request.jsonrequest

            #_logger.info(f'data: {data}')

            hashed_machine_id = data.get('hashed_machine_id', None)

            _logger.info(f'hashed_machine_id: {hashed_machine_id}')

            GatesModel = http.request.env['things.gate']

            # _logger.info("GatesModel Search same hashed_machine_id", GatesModel.sudo().search(
            #     [('confirmed', '=', False)]) )
            
            # if GatesModel.sudo().search(
            #     [('confirmed', '=', False)]):
            #     return {}
            # else:
            #     newGate = GatesModel.sudo().create({
            #             'confirmed' : False,
            #             'name' : name,
            #             'location' : location,            
            #     })
            #     newGateDict = newGate.sudo().read()[0]

        except Exception as e:
            _logger.info(f'the new gate request could not be dispatched - Exception {e}')
            answer["error"] = e
        return answer

    @http.route('/things/gates/incoming/<routeFrom>',
            type = 'json',
            auth ='public', csrf=False)    
    def messageFromGate(self, routeFrom, **kwargs):
        GatesModel = http.request.env['things.gate']
        response = {
            'gate route known'  :   'false',
            'type created'      :   'none',
            'route from'        :   'none',
            'route to'          :   'none',
            'error'             :   'none'
        }
        
        gateSending = GatesModel.sudo().search(
            [('route_from', '=', routeFrom)])
        if gateSending:
            response = {'gate route known': 'true'}
            
        return response