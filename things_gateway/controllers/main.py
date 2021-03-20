from odoo import http
import time
import logging
import json

_logger = logging.getLogger(__name__)

class ThingsRasGate(http.Controller):

    @http.route('/things/gates/ras/version',
            type = 'json',
            auth = 'public',
            methods=['POST'],
            csrf = False)
    def ModuleVersion(self, **kwargs):
        answer = {"error": None}
        try:
            data = http.request.jsonrequest
            _logger.info(f'data: {data}') ##############

            question = data.get('question', None)
            if "Please" in question:
                answer["version"]= "12.0.1" # version of this things module as in __manifest__.py
            else:
                answer["error"]="Wrong question"
                answer["version"]= None
                _logger.error('someone is asking the wrong question (Get Module Version of ThingsRasGate Class)')
        except Exception as e:
            _logger.info(f'Get Module Version of ThingsRasGate Class - Exception {e}')
            answer["error"] = e
        _logger.info(f'answer to Get Module Version of ThingsRasGate Class: {answer}') ################
        return answer

    @http.route('/things/gates/ras/ack',
            type = 'json',
            auth = 'public',
            methods=['POST'],
            csrf = False)
    def AcknowdledgeRasGate(self, **kwargs):
        # create a new record things.ras2
        # or return if existing 

        answer = {"error": None}
        try:
            data = http.request.jsonrequest
            #_logger.info(f'data: {data}')
            hashed_machine_id = data.get('hashed_machine_id', None)
            md = data.get('manufacturingData', {})

            _logger.info(f'hashed_machine_id: {hashed_machine_id}')

            Ras2Model = http.request.env['things.ras2']

            ras2_machine_in_database = Ras2Model.sudo().search(
                 [('hashed_machine_id', '=', hashed_machine_id)])
            
            if ras2_machine_in_database:
                # "Ras Gateway with same hashed machine id already registered"
                ras2_to_be_acknowledged = ras2_machine_in_database
                ras2_to_be_acknowledged.sudo().write({
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
            else:
                ras2_to_be_acknowledged = Ras2Model.sudo().create({
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

            ras2_Dict = ras2_to_be_acknowledged.sudo().read()[0]

            list_of_params_to_include_in_answer = ['id',
                'routefromOdooToDevice',
                'routefromDeviceToOdoo',
                'shouldGetFirmwareUpdate']
            for p in list_of_params_to_include_in_answer:
                answer[p] = ras2_Dict.get(p)

        except Exception as e:
            _logger.info(f'the new gate request could not be dispatched - Exception {e}')
            answer["error"] = e
        _logger.info(f'answer to request to register RAS: {answer} ')
        return answer

    @http.route('/things/gates/ras/incoming/<routeFrom>',
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

    @http.route('/things/gates/ras/outgoing/<routeTo>',
            type = 'json',
            auth ='public', csrf=False)    
    def messageToGate(self, routeFrom, **kwargs):
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