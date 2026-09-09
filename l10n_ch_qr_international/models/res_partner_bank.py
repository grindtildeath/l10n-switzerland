# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    def _get_error_messages_for_qr(self, qr_method, debtor_partner, currency):
        res = super()._get_error_messages_for_qr(qr_method, debtor_partner, currency)
        if (
            res
            and qr_method == "ch_qr"
            and debtor_partner.country_id.code not in ("CH", "LI")
            and debtor_partner.commercial_partner_id.force_swiss_qr_invoice
        ):
            # As super function is returning all the errors reasons in a single string
            #  we need to split that string using what's used to join the reasons.
            # Then we can check if there's any other error than the one for partners
            #  not located in Switzerland or Liechtenstein
            # If we have any other error, return the result from super call instead
            #  of trying to remove string that was already translated, with a note
            #  about what this module already allows
            qr_errors_nbr = len(res.split("\r\n")) - 2
            if qr_errors_nbr > 0:
                return res + _(
                    "\r\nNote: limitation on partner not in Switzerland can be ignored"
                    " as partner is already configured to receive QR invoice."
                )
            return None
        return res
