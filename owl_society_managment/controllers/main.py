# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import base64


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_society_managment.demo_template")

    @http.route('/society_create', type='http', auth="public", csrf=False)
    def society_form(self, **post):
        return http.request.render("owl_society_managment.society_form")

    @http.route('/member_create', type='http', auth="public", csrf=False)
    def member_register(self, **post):
        return http.request.render("owl_society_managment.member_register")

    @http.route('/complaint_create', type='http', auth="public", csrf=False)
    def complaint_register(self, **post):
        return http.request.render("owl_society_managment.complaint_register")

    @http.route('/event_create', type='http', auth="public", csrf=False)
    def event_register(self, **post):
        return http.request.render("owl_society_managment.event_register")

    @http.route('/society', auth="public", type="json", csrf=False)
    def society_register_form(self, **kw):
        currencys = request.env['res.currency'].sudo().search([]).mapped('name')
        print('\n\n\n\n\n\n 111111', currencys)
        return currencys

    @http.route('/society/form/', auth="public", type="json", csrf=False)
    def society_register(self, **post):
        print('\n\n\n\n\n\n\n\n', post)
        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        currency_code = post.get('currency')
        currency = request.env['res.currency'].sudo().search([('name', '=', currency_code)], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'commercial_company_name': post.get('name')
        })
        company = request.env['res.company'].sudo().create({
            'name': post.get('name'),
            'partner_id': partner.id,
            'currency_id': currency.id
        })
        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('email'),
            'password': post.get('name'),
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name
        })
        return http.local_redirect('/web/login')

    @http.route('/member/form', auth="user", type="json", csrf=False)
    def member_form(self, **kw):
        u = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n33333333', u)
        print('\n\n\n\n\n\n\n\n44444444', kw)
        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        partner = request.env['res.partner'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email')
        })
        user = request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': kw.get('email'),
            'password': kw.get('name'),
            'groups_id': groups_id_name
        })
        return {"user": user}

    @http.route('/get_Product_data', auth="user", type="json", csrf=False)
    def get_product(self, **post):
        subscriptions = request.env['sale.subscription.template'].sudo().search([]).mapped('name')
        print('\n\n\n\n\n\n 111111', subscriptions)
        return subscriptions

    @http.route('/services/form', auth="user", type="json", csrf=False)
    def services_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n', kw)
        file = open(kw.get('image_1920'), 'rb')
        print('\n\n\n\n\n\n\n\n22222', file)
        am = request.env['product.product'].sudo().create([{
                    'name': kw.get('name'),
                    'purchase_ok': kw.get('purchase_ok'),
                    'sale_ok': kw.get('sale_ok'),
                    'type': kw.get('type'),
                    'standard_price': kw.get('standard_price'),
                    'list_price': kw.get('list_price'),
                    'image_1920': base64.encodestring(file.read()),
                    'company_id': user.company_id.id
                    }])
        # return http.request.render("owl_society_managment.demo_template")
        # return http.local_redirect('/owl_demo')
        return {"am": am}

    @http.route('/complaint/form', auth="user", type="json", csrf=False)
    def complaint_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        request.env['helpdesk.ticket'].sudo().create([{
                'name': kw.get('name'),
                'partner_name': user.partner_id.name,
                'partner_email': user.partner_id.email,
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')
        # return {"am": am}

    @http.route('/event/form', auth="user", type="json", csrf=False)
    def event_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n000000', kw)
        request.env['event.event'].sudo().create([{
                'name': kw.get('name'),
                'date_begin': kw.get('date_begin'),
                'date_end': kw.get('date_end'),
                'date_tz':  'Asia/Kolkata',
                'note': kw.get('note'),
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')
        # return {"am": am}
