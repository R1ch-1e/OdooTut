# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
  
from odoo import fields, models


class EstatePropertyTags(models.Model):
  _name="estate.property.tags"
  _description="Real estate tags"
  _order = 'name'

  name=fields.Char("Name")
  color=fields.Integer()
  
  _sql_constraints = [
     ('name_offer_check', 'UNIQUE(name)',
     'A property tag name must be unique')

     ]
