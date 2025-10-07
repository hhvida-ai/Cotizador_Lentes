from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    lens_type = fields.Selection([
      ('monofocal','Monofocal'),
      ('bifocal','Bifocal'),
      ('progresivo','Progresivo'),
      ('blended','Blended'),
      ('otros','Otros')
      ], string='Tipo de lente', default='monofocal')


    serie_price_ids = fields.One2many('optica.product.serie.price', 'product_tmpl_id', string='Precios por serie')


    class OpticaProductSeriePrice(models.Model):
      _name = 'optica.product.serie.price'
      _description = 'Precio del producto por serie'


    product_tmpl_id = fields.Many2one('product.template', 'Producto', required=True, ondelete='cascade')
    series_id = fields.Many2one('optica.series', 'Serie', required=True)
    price = fields.Monetary('Precio', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
