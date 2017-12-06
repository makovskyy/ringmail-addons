from odoo import models, fields, api
import random
import base64

def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(20))

class Domain(models.Model):
    _name = 'ringmail_reg.domain'

    name = fields.Char(string='Domain Name', required=True)
    state = fields.Selection([
        ('draft', 'Not Confirmed'),
        ('done', 'Confirmed'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
    txt_record = fields.Char(string='TXT record', readonly=True)
    page = fields.Binary(string="HTML page", readonly=True)
    page_fname = fields.Char(string="File name")

    @api.multi
    def confirm_domain(self):
        self.state = 'done'


    @api.model
    def create(self, vals):
        token = random_token()
        vals['txt_record'] = 'ringmail-domain-verify='+token
        vals['page_fname'] = 'ringmail_'+token+'.html'
        vals['page'] = base64.encodebytes(str.encode(vals['txt_record']))
        return super(Domain, self).create(vals)

