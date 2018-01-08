# This file is part of the party_device module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.modules.party.party import STATES, DEPENDS
import math

__all__ = ['Party']


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    start_date = fields.Function(fields.Date('Start date'), 'get_date')
    end_date = fields.Function(fields.Date('End date'), 'get_date')
    delegacion = fields.Function(fields.Many2One('contract.device',
            'Delegacion'), 'get_delegacion')
    partner_active = fields.Function(fields.Boolean('Partner active'), 'get_partner_active')

    def get_date(self, name):
        Contract = Pool().get('contract')
        contracts = Contract.search([('party', '=', self)])
        dates = []
        for contract in contracts:
            if name == 'start_date':
                dates.append(contract.start_date)
            else:
                dates.append(contract.end_date)
        if dates and name == 'start_date':
            return min(dates)
        elif dates and name == 'end_date':
                return max(dates)
        else:
            return None

    def get_delegacion(self, name):
        Contract = Pool().get('contract')
        contracts = Contract.search([('party', '=', self)])
        for contract in contracts:
            return contract.contract_device.id
        return None

    def get_partner_active(self, name):
        pool = Pool()
        Date = pool.get('ir.date')
        Contract = Pool().get('contract')
        contracts = Contract.search([('party', '=', self),
                                     ('state', '=', 'confirmed'),])
        partner_active = False
        for contract in contracts:
            if (contract.start_date <= Date.today() and
                (contract.end_date is None or contract.end_date >= Date.today())):

                InvoiceLine = pool.get('account.invoice.line')
                # Search for consumption lines in posted invoices
                invoice_lines = InvoiceLine.search([('party', '=', self),
                                                    ('invoice.state', '=', 'posted'),
                                                    ('origin', 'like', 'contract.consumption%' )])
                partner_active = True
                unpaid_months = 0
                for invoice_line in invoice_lines:
                    consumption = invoice_line.origin
                    diff_period = consumption.end_period_date - consumption.init_period_date
                    # Calculate consumption period months unpaid
                    diff_period_months = diff_period.days / float(30)
                    # Sum unpaid months to counter
                    unpaid_months += math.ceil(diff_period_months)
                # Set partner_active to false if there is more than 3 months unpaid
                if unpaid_months >= 3:
                    partner_active = False

        return partner_active
