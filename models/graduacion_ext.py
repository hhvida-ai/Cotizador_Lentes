class OpticaGraduacion(models.Model):
    _inherit = 'optica.graduacion'


    # Suponiendo campos existentes: esfera_od, esfera_oi, cilindro_od, cilindro_oi, adicion
    serie_id = fields.Many2one('optica.series', string='Serie', compute='_compute_serie', store=True)
    serie_status = fields.Selection([('ok','Asignada'),('mixed','Mixta'),('out','Fuera de rango')], string='Estado Serie', compute='_compute_serie', store=True)


    @api.depends('esfera_od','esfera_oi','cilindro_od','cilindro_oi')
    def _compute_serie(self):
         Series = self.env['optica.series'].search([('active','=',True)])
        for rec in self:
            matches = []
            for s in Series:
                ok_od = s.matches(rec.esfera_od or 0.0, rec.cilindro_od or 0.0)
                ok_oi = s.matches(rec.esfera_oi or 0.0, rec.cilindro_oi or 0.0)
                if ok_od and ok_oi:
                    matches.append(s)
                if len(matches) == 1:
                    rec.serie_id = matches[0]
                    rec.serie_status = 'ok'
                elif len(matches) > 1:
                    rec.serie_id = matches[0]
                    rec.serie_status = 'mixed'
                else:
                    rec.serie_id = False
                    rec.serie_status = 'out'
