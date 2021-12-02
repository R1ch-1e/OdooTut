# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
  

from odoo import fields, models


class EstatePropertyType(models.Model):
  _name="estate.property.type"
  _description="Real estate types"
  _order = 'name'

  name=fields.Char("Name")
  sequence = fields.Integer('Sequence', default=1,
   help="Used to order stages. Lower is better.")
  
  property_ids = fields.One2many("estate.property", "property_type_id")


  _sql_constraints = [
     ('name_offer_check', 'UNIQUE(name)',
     'A property type name must be unique')

     ]



  