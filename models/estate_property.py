# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from typing import DefaultDict
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
import logging

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate plans"
    _order = "name"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date(
        'Available From', default=lambda self: fields.date.today())
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden', )
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        store=True,
        default='new',
        required=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")

    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    seller = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    total = fields.Integer(string="Area", compute="_compute_total")
    best_price = fields.Float(string="Best Offer", compute="_best_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'A property selling price must be positive')

    ]

    #computing#

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _best_price(self):
        better_offer = 0
        for record in self:
            if record.offer_ids:
                better_offer = max(record.offer_ids.mapped('price'))
            record.best_price = better_offer

    @api.onchange('garden')
    def _onchange_garden_(self):
        for record in self:
            if record.garden == True:
                record.garden_orientation = 'north'
                record.garden_area = 10

            else:
                record.garden_orientation = ''
                record.garden_area = 0

    @api.constrains('selling_price')
    def _check_price_(self):
        for record in self:
             #if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1: (another method)
             if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError(
                    "The selling price cannot be lower than 90 percent of the expected price.")

    # Action buttons

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                message = f"{record.name} is a canceled and cannot be sold "
                _logger.warning(message)
                raise UserError(message)
            else:
                record.state = "sold"

        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                message = f"{record.name} is Sold property and cannot be canceled."
                raise UserError(message)
            else:
                record.state = "canceled"

        return True


# for offer in record.offer_ids:
        #     if offer.price > better_offer_price:
        #         better_offer_price = offer.price
        # record.best_price = better_offer_price
