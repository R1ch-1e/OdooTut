# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
  
from odoo import fields, models


class EstatePropertyTags(models.Model):
  _name="estate.property.tags"
  _description="Real estate tags"

  name=fields.Char("Name")
  
  
