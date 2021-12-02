# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from typing import DefaultDict
from odoo import fields, models, api
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"
    _order = 'price'

    price = fields.Float("Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True, string='Buyers')
    property_id = fields.Many2one("estate.property", required=True)
    validity= fields.Integer("Validity", default=7)
    date_deadline=fields.Date(compute="_date_deadline_", inverse="_inverse_total", default=lambda self:fields.date.today())
    
    api.depends('validity', 'date_deadline')
    def _date_deadline_(self):
        for record in self:
            create_date = date.today()
            print(f'create_date={create_date}')
            record.date_deadline = create_date + timedelta(days=record.validity)
            
    
    def _inverse_total(self):
        for record in self:
            create_date = date.today()
            record.date_deadline= create_date - timedelta(days=record.validity)


   
    

 #action buttons 

    def button_accept_offer(self):
        for record in self:
            for offers in record.property_id.offer_ids:
                offers.status='refused'
            
            
            record.status = 'accepted'
            print('Accepted.')
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer accepted'


        return True
    

    def button_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        
        return True

 





class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Real Estate Offers"




