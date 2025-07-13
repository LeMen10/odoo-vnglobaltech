from odoo import http
from odoo.http import request


class VnextProductController(http.Controller):
    @http.route("/<slug>", type="http", auth="public", website=True)
    def custom_product_page(self, slug, **kwargs):
        product = (
            request.env["product.template"]
            .sudo()
            .search([("custom_slug", "=", slug)], limit=1)
        )
        if not product or not product.website_published:
            return request.not_found()

        return request.render(
            "product_custom.vnext_custom_product_template",
            {
                "product": product,
                "main_object": product,
            },
        )
