# This file is part of the party_device module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.modules.party.party import STATES, DEPENDS

__all__ = ['Party']


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    start_date = fields.Function(fields.Date('Start date'), 'get_date')
    end_date = fields.Function(fields.Date('End date'), 'get_date')
    delegacion = fields.Function(fields.Many2One('contract.device',
            'Delegacion'), 'get_delegacion')

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
