# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
import time
import json
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)
from . import helpers as h


class HrAttendance(models.Model):

    _inherit = "hr.attendance"


    check_in_source = fields.Char(  string="Source of the Check-In TimeStamp", 
                                    default=h.defaultClockingSource, 
                                    size=3,
                                    required=True)
    check_out_source = fields.Char( string="Source of the Check-Out TimeStamp", 
                                    default=h.defaultClockingSource, 
                                    size=3,
                                    required=True)

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we can have :
                * "open" attendance records (without check_out)
            But we must have:
                * no overlapping time slices with previous employee records
        """
        for attendance in self:
            # we take the latest attendance before our check_in time and check it doesn't overlap with ours
            last_attendance_before_check_in = self.env['hr.attendance'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('check_in', '<=', attendance.check_in),
                ('id', '!=', attendance.id),
            ], order='check_in desc', limit=1)
            if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
                raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                    'empl_name': attendance.employee_id.name,
                    'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(attendance.check_in))),
                })

            #   # if not attendance.check_out:
                #     # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
                #     no_check_out_attendances = self.env['hr.attendance'].search([
                #         ('employee_id', '=', attendance.employee_id.id),
                #         ('check_out', '=', False),
                #         ('id', '!=', attendance.id),
                #     ], order='check_in desc', limit=1)
                #     if no_check_out_attendances:
                #         raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
                #             'empl_name': attendance.employee_id.name,
                #             'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(no_check_out_attendances.check_in))),
                #         })
                # else:
                #     # we verify that the latest attendance with check_in time before our check_out time
                #     # is the same as the one before our check_in time computed before, otherwise it overlaps
                #     last_attendance_before_check_out = self.env['hr.attendance'].search([
                #         ('employee_id', '=', attendance.employee_id.id),
                #         ('check_in', '<', attendance.check_out),
                #         ('id', '!=', attendance.id),
                #     ], order='check_in desc', limit=1)
                #     if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
                #         raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                #             'empl_name': attendance.employee_id.name,
                #             'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(last_attendance_before_check_out.check_in))),
                #         })

    @api.multi
    def add_clocking(   self,
                        employee_id,
                        timestamp, 
                        checkin_or_checkout="not_defined", 
                        source=h.defaultClockingSource):
     
        helper = h.attendanceHelpers(self.env['hr.attendance'],
                                    employee_id, 
                                    timestamp, 
                                    checkin_or_checkout, 
                                    source)

        #helper.logging_at_the_beginning()
        
        if helper.warningMessage: return helper.warningMessage

        
        return "all OK"
        #return "Could not add the clocking."


    @api.multi
    def delete_clocking(self):
        _logger.info( 'this is info:'+WARNING+ 'Button DELETE_timestamp works like a charm'+ENDC)
        _logger.debug( 'this is debug debug')
        _logger.debug(OKBLUE+"self.context is:  %s "+ENDC, self.env.context ) 
