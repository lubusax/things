from odoo import http, fields
import time
import logging
import json

_logger = logging.getLogger(__name__)

factory_settings = [
  "firmwareAtShipment",
  "productName",
  "productionDate",
  "productionLocation",
  "productionNumber",
  "qualityInspector",
  "SSIDreset",
  "hashed_machine_id"]

defined_on_device_setup = [
  "https",
  "odoo_host",
  "odoo_port",
  "odooConnectedAtLeastOnce",
  "odooUrlTemplate",
  "hasCompletedSetup"]

defined_on_ack_from_odoo = [
  "terminalIDinOdoo",
  "RASxxx",
  "routefromDeviceToOdoo",
  "routefromOdooToDevice",
  "version_things_module_in_Odoo",
  "ownIpAddress"]

updated_continuously_from_odoo = [
  "ssh",
  "showEmployeeName",
  "sshPassword",
  "language",
  "tz",
  "time_format",
  "timeoutToCheckAttendance",
  "periodEvaluateReachability",
  "periodDisplayClock",
  "timeToDisplayResultAfterClocking",
  "location",
  "shouldGetFirmwareUpdate",
  "setRebootAt",
  'shutdownTerminal',
  "isRemoteOdooControlAvailable",
  "gitBranch",
  "gitCommit",
  "gitRemote",
  "doFactoryReset",
  "updateAvailable",
  "timestampLastConnection"]

defined_on_ack_from_device = [
  "installedPythonModules",
  "firmwareVersion",
  "lastFirmwareUpdateTime",
  "lastTimeTerminalStarted",
  "updateFailedCount"]

all_keys = factory_settings + defined_on_device_setup + \
    defined_on_ack_from_device + updated_continuously_from_odoo + \
    defined_on_ack_from_device

keys_defined_in_device = factory_settings + \
    defined_on_device_setup + defined_on_ack_from_device

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
        def get_data_to_transfer(listOfkeys):
            data_to_transfer ={}
            for o in listOfkeys:
                data_to_transfer[o] = data.get(o)
            data_to_transfer['timestampLastConnection'] = fields.Datetime.now()          
            return data_to_transfer

        answer = {"error": None}
        try:
            data = http.request.jsonrequest
            #_logger.info(f'data: {data}')
            hashed_machine_id = data.get('hashed_machine_id', None)
            _logger.info(f'hashed_machine_id: {hashed_machine_id}')

            Ras2Model = http.request.env['things.ras2']

            ras2_machine_in_database = Ras2Model.sudo().search(
                 [('hashed_machine_id', '=', hashed_machine_id)])
            
            if ras2_machine_in_database:
                ras2_to_be_acknowledged = ras2_machine_in_database
                ras2_to_be_acknowledged.sudo().write(
                    get_data_to_transfer(keys_defined_in_device))
            else:
                ras2_to_be_acknowledged = Ras2Model.sudo().create(
                    get_data_to_transfer(keys_defined_in_device))

            ras2_Dict = ras2_to_be_acknowledged.sudo().read()[0]

            for p in all_keys:
                answer[p] = ras2_Dict.get(p)

        except Exception as e:
            _logger.info(f'the new gate request could not be dispatched - Exception {e}')
            answer["error"] = e
        _logger.info(f'answer to request to acknowledge RAS: {answer} ')
        return answer

    def resetSettings(self,routeFrom, answer):
        try:
            Ras2Model = http.request.env['things.ras2']
            ras2_in_database = Ras2Model.sudo().search(
                [('routefromDeviceToOdoo', '=', routeFrom)])
            
            if ras2_in_database:
                ras2_in_database.sudo().write({
                    'setRebootAt' : None,
                    'shutdownTerminal' : False,
                    'shouldGetFirmwareUpdate': False                
                })
            else:
                answer["error"] = "This should never occur. Method resetSettings"
                _logger.info(f'resetSettings RAS - Error: {answer["error"]} ')
        except Exception as e:
            _logger.info(f'resetSettings RAS - Exception {e}')
            answer["error"] = e

        _logger.info(f'resetSettings RAS: {answer} ')
        return answer

    @http.route('/things/gates/ras/incoming/<routeFrom>',
            type = 'json',
            auth = 'public',
            methods=['POST'],
            csrf = False)
    def messageFromGate(self, routeFrom, **kwargs):
        answer = {"error": None}
        try:
            data = http.request.jsonrequest
            productName = data.get('productName', None)
            question = data.get('question', None)

            if productName == "RAS2" and question == "Reset":
                answer = self.resetSettings(routeFrom, answer)
        except Exception as e:
            _logger.info(f'Message from Odoo To Gate could not be dispatched - Exception {e}')
            answer["error"] = e

        return answer

    def answerRas2routineQuestion(self,routeTo, data, answer):
        try:
            Ras2Model = http.request.env['things.ras2']
            ras2_in_database = Ras2Model.sudo().search(
                [('routefromOdooToDevice', '=', routeTo)])
            
            if ras2_in_database:
                incrementalLog_received = data.get('incrementalLog')
                ras2_Dict = ras2_in_database.sudo().read()[0]
                incrementalLog_stored = ras2_Dict['incrementalLog'] or " "
                log_length = len(incrementalLog_stored)
                _logger.info(f'Length of incremental log in storage {log_length} ')
                if log_length > 10000:
                    incrementalLog_capped = incrementalLog_stored[3000:]
                else:
                    incrementalLog_capped = incrementalLog_stored
                incrementalLog_received_str = ""
                for l in incrementalLog_received:
                    incrementalLog_received_str += l +"\n"
                _logger.info(f'incrementalLog_received_str {incrementalLog_received_str} ')
                new_inc_log = incrementalLog_capped + incrementalLog_received_str
                ras2_in_database.sudo().write({
                        'incrementalLog' : new_inc_log,
                        'timestampLastConnection': fields.Datetime.now()               
                })

                list_of_params_to_include_in_answer = [ \
                    "setRebootAt",
                    'shouldGetFirmwareUpdate',
                    'location',
                    'shutdownTerminal',
                    'tz',
                    'hour12or24']
                for p in list_of_params_to_include_in_answer:
                    answer[p] = ras2_Dict.get(p)
            else:
                answer["error"] = "This should never occur. Method answerRasroutineQuestion"
                _logger.info(f'Routine Question RAS - Error: {answer["error"]} ')
        except Exception as e:
            _logger.info(f'Routine Question RAS - Exception {e}')
            answer["error"] = e

        _logger.info(f'answer to routine Question RAS: {answer} ')
        return answer

    @http.route('/things/gates/ras/outgoing/<routeTo>',
            type = 'json',
            auth = 'public',
            methods=['POST'],
            csrf = False)    
    def messageToGate(self, routeTo, **kwargs):
        answer = {"error": None}
        try:
            data = http.request.jsonrequest
            productName = data.get('productName', None)
            question = data.get('question', None)

            if productName == "RAS2" and question == "Routine":
                answer = self.answerRas2routineQuestion(routeTo, data, answer)
        except Exception as e:
            _logger.info(f'Message from Odoo To Gate could not be dispatched - Exception {e}')
            answer["error"] = e

        return answer
