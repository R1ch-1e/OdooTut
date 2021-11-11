# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from typing import DefaultDict
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate plans"
    _order = "id"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date(
        'Available From', default=lambda self:fields.date.today())
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, store=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean('Active', default=True)
    status = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        store=True,
        default='new',
        required=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    seller= fields.Many2one("res.users", string="Sales Person", default=lambda self:self.env.user)
    buyer= fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids= fields.One2many("estate.property.offer", "property_id", string="Offers")
  
 



    