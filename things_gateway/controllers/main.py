from odoo import http
import time
import logging
import json

_logger = logging.getLogger(__name__)

class ThingsRas2Gate(http.Controller):

    @http.route('/things/gates/ras2/create',
            type = 'json',
            auth = 'public',
            methods=['POST'],
            csrf = False)
    def RegisterNewRas2Gate(self, **kwargs):
        # create a new record things.gate
        # only if there is no things.gate
        # awaiting to be confirmed
        answer = {"error": None}
        try:
            data = http.request.jsonrequest

            #_logger.info(f'data: {data}')

            hashed_machine_id = data.get('hashed_machine_id', None)
            md = data.get('manufacturingData', {})

            _logger.info(f'hashed_machine_id: {hashed_machine_id}')

            Ras2Model = http.request.env['things.ras2']

            _logger.info("Ras2Model Search same hashed_machine_id", Ras2Model.sudo().search(
                 [('hashed_machine_id', '=', hashed_machine_id)]) )
            
            if Ras2Model.sudo().search(
                 [('hashed_machine_id', '=', hashed_machine_id)]):
                answer["error"] = "Ras2 Gateway with same hashed machine id already registered"
                return answer
            else:
                newRas2 = Ras2Model.sudo().create({
                        'hashed_machine_id' : hashed_machine_id,
                        'firmwareAtShipment' : md.get('firmwareAtShipment'),
                        'productName' : md.get('productName'),
                        'productionDate' : md.get('productionDate'),
                        'productionLocation' : md.get('productionLocation'),
                        'productionNumber' : md.get('productionNumber'),
                        'qualityInspector' : md.get('qualityInspector'),                        
                        'firmwareVersion' : data.get('firmwareVersion'),
                        'ipAddress' : data.get('ownIpAddress'),
                        'location' : data.get('location'), 
                        'ssh' : data.get('ssh'), 
                        'sshPassword' : data.get('sshPassword'),
                        'language' : data.get('language'), 
                        'showEmployeeName' : data.get('showEmployeeName'), 
                        'terminalSetupManagement' : data.get('terminalSetupManagement'), 
                        'timezone' : data.get('timezone'), 
                        'periodDisplayClock' : data.get('periodDisplayClock'), 
                        'periodEvaluateReachability' : data.get('periodEvaluateReachability'), 
                        'timeToDisplayResultAfterClocking' : data.get('timeToDisplayResultAfterClocking'), 
                        'timeoutToCheckAttendance' : data.get('timeoutToCheckAttendance'), 
                        'timeoutToGetOdooUID' : data.get('timeoutToGetOdooUID')                 
                })
                newRas2Dict = newRas2.sudo().read()[0]
                list_of_params_to_include_in_answer = ['id', 'routefromOdooToDevice', 'routefromDeviceToOdoo']
                for p in list_of_params_to_include_in_answer:
                   answer[p]=newRas2Dict.get(p)
        except Exception as e:
            _logger.info('the new gate request could not be dispatched - Exception', e)
            answer["error"] = e
        _logger.info('answer to request to register RAS2: ', answer)
        return answer

    @http.route('/things/gates/ras2/incoming/<routeFrom>',
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