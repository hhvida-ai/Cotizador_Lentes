from odoo import models, fields, api


class CotizadorWizard(models.TransientModel):
    _name = 'cotizador.wizard'
    _description = 'Wizard para crear cotizaciones de lentes desde graduación'


    partner_id = fields.Many2one('res.partner', string='Paciente', required=True)
    graduacion_id = fields.Many2one('optica.graduacion', string='Graduación')
    line_ids = fields.One2many('cotizador.wizard.line','wizard_id', string='Líneas')


    @api.onchange('partner_id')
    def _onchange_partner(self):
        if not self.partner_id:
            return
            graduacion = self.env['optica.graduacion'].search([('patient_id','=',self.partner_id.id)], order='create_date desc', limit=1)
        if graduacion:
            self.graduacion_id = graduacion.id


      def action_create_quotation(self):
          SaleOrder = self.env['sale.order']
          order = SaleOrder.create({
              'partner_id': self.partner_id.id,
              'note': 'Cotización generada desde Cotizador de Lentes',
          })
          for line in self.line_ids:
              order.order_line.create({
                  'order_id': order.id,
                  'product_id': line.product_id.id,
                  'name': line.product_id.display_name,
                  'product_uom_qty': line.qty,
                  'price_unit': line.price,
              })
          return {
                  'type': 'ir.actions.act_window',
                  'res_model': 'sale.order',
                  'view_mode': 'form',
                  'res_id': order.id,
          }


    class CotizadorWizardLine(models.TransientModel):
        _name = 'cotizador.wizard.line'


        wizard_id = fields.Many2one('cotizador.wizard', string='Wizard', required=True, ondelete='cascade')
        product_id = fields.Many2one('product.product', string='Producto', required=True)
        qty = fields.Float('Cantidad', default=1.0)
        price = fields.Monetary('Precio', currency_field='currency_id')
        currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)


        @api.onchange('product_id','wizard_id')
        def _onchange_product(self):
            if not self.product_id or not self.wizard_id or not self.wizard_id.graduacion_id:
              return
            grad = self.wizard_id.graduacion_id
            add = getattr(grad,'adicion', False) or getattr(grad,'add', False)
            allowed = True
            if not allowed:
                self.product_id = False
                self.price = 0.0
                return {'warning': {'title': 'Producto no permitido', 'message': 'El tipo de lente no es compatible con la graduación.'}}


            serie = grad.serie_id
            if serie:
                pps = self.env['optica.product.serie.price'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('series_id','=',serie.id)], limit=1)
            if pps:
                self.price = pps.price
                return  
        self.price = self.product_id.lst_price
