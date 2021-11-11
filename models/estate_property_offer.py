# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"

    price = fields.Float("Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True, string='Buyers')
    property_id = fields.Many2one("estate.property", required=True)

class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Real Estate Offers"


