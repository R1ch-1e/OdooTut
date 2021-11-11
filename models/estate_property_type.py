# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
  

from odoo import fields, models


class EstatePropertyType(models.Model):
  _name="estate.property.type"
  _description="Real estate types"

  name=fields.Char("Name")
  sequence = fields.Integer('Sequence', default=1,
   help="Used to order stages. Lower is better.")
