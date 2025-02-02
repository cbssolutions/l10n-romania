# Copyright (C) 2022 NextERP Romania SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"
    _log_access = False

    create_date = fields.Datetime("Created on", index=True, readonly=True)
    create_uid = fields.Many2one("res.users", "Created by", index=True, readonly=True)
    write_date = fields.Datetime("Last Updated on", index=True, readonly=True)
    write_uid = fields.Many2one(
        "res.users", "Last Updated by", index=True, readonly=True
    )
    date_done = fields.Datetime(
        readonly=True,
        help="This is the date when this recod was created. Original create_date is writen"
        " at reception by module nexterp_stock_date",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            val_date = fields.datetime.now()
            if values.get("stock_move_id"):
                move = self.env["stock.move"].browse(values["stock_move_id"])
                val_date = move.get_move_date()
            values.update(
                {
                    "create_uid": self._uid,
                    "create_date": val_date,
                    "write_uid": self._uid,
                    "write_date": val_date,
                    "date_done": fields.datetime.now(),
                }
            )
        return super().create(vals_list)

    def write(self, vals):
        if not vals.get("write_uid"):
            vals["write_uid"] = self._uid
        if not vals.get("write_date"):
            vals["write_date"] = fields.datetime.now()
        return super().write(vals)
