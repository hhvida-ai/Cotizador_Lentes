{
    "name": "Óptica - Cotizador de Lentes",
    "version": "17.0.1.0.0",
    "summary": "Series de micas, precios por serie y wizard de cotización basado en graduación",
    "category": "Custom/Optica",
    "author": "PeeWee"
    "license": "LGPL-3",
    "depends": ["base", "product", "sale_management", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/optica_series_views.xml",
        "views/product_template_inherit_views.xml",
        "views/graduacion_inherit_views.xml",
        "views/cotizador_wizard_views.xml",
        "views/menus.xml",
],
    "installable": True,    
    "application": False,
}
