# This file is part of the party_device module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import party


def register():
    Pool.register(
        party.Party,
        module='party_device', type_='model')
