from odoo import models, fields, api
import unicodedata
import re


class ProductTemplate(models.Model):
    _inherit = "product.template"

    custom_slug = fields.Char("Custom URL Slug", required=False, index=True)
    external_url = fields.Char("External Purchase URL")

    @api.model
    def create(self, vals):
        if not vals.get("custom_slug") and vals.get("name"):
            vals["custom_slug"] = self._generate_unique_slug(vals["name"])
        return super().create(vals)

    def write(self, vals):
        if "custom_slug" in vals and vals["custom_slug"]:
            vals["custom_slug"] = self._generate_unique_slug(
                vals["custom_slug"], self.id
            )
        return super().write(vals)

    def _generate_unique_slug(self, name, exclude_id=None):
        slug_base = self._slugify(name)
        slug = slug_base
        i = 1
        Product = self.env["product.template"].sudo()
        while Product.search(
            [("custom_slug", "=", slug)]
            + ([("id", "!=", exclude_id)] if exclude_id else []),
            limit=1,
        ):
            i += 1
            slug = f"{slug_base}-{i}"
        return slug

    def _slugify(self, text):
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[\s_-]+", "-", text)
    
    def _compute_website_url(self):
        super()._compute_website_url()
        for product in self:
            if product.custom_slug:
                product.website_url = '/%s' % product.custom_slug
