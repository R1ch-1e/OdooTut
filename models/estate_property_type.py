# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
  

from odoo import fields, models,api


class EstatePropertyType(models.Model):
  _name="estate.property.type"
  _description="Real estate types"
  _order = 'name'

  name=fields.Char("Name")
  sequence = fields.Integer('Sequence', default=1,
   help="Used to order stages. Lower is better.")
  offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
  
  #offer_count=fields.Integer(compute='_compute_total') 

  offer_count = fields.Integer('Offer Counts', compute='_count_offer')
  
  property_ids = fields.One2many("estate.property", "property_type_id")

  
  @api.depends('offer_ids')
  def _count_offer(self):
    for record in self:
      record.offer_count = len(record.offer_ids)




  _sql_constraints = [
     ('name_offer_check', 'UNIQUE(name)',
     'A property type name must be unique')

     ]



  