class OpticaSeries(models.Model):
  _name = 'serie.lentes'
  _description = 'Series de micas por rango de esfera y cilindro'


  name = fields.Char(required=True)
  sphere_min = fields.Float(string='Esfera mín')
  sphere_max = fields.Float(string='Esfera máx')
  cyl_min = fields.Float(string='Cilindro mín')
  cyl_max = fields.Float(string='Cilindro máx')
  active = fields.Boolean(default=True)
  note = fields.Text()


  def matches(self, sphere, cyl):
      if sphere is None or cyl is None:
          return False
      try:
          # Comparación simple entre rangos
          if sphere < self.sphere_min or sphere > self.sphere_max:
              return False
          if cyl < self.cyl_min or cyl > self.cyl_max:
              return False
           return True
      except Exception:
          return False
