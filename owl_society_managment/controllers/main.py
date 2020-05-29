# -*- coding: utf-8 -*-
from datetime import date

from odoo import http, SUPERUSER_ID
from odoo.http import request
import json
import base64


class OwlController(http.Controller):

    def getUserType(self):
        userType = None
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('owl_society_managment.society_secratery_group_admin'):
            userType = "secretary"
        elif request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            userType = "member"
        else:
            userType = "treasurer"
        return userType

    @http.route(['/my', '/my/home'], type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        userType = self.getUserType()
        return http.request.render("owl_society_managment.menu_item", {'userType': userType})

    @http.route('/society_create', type='http', auth="public", csrf=False)
    def society_form(self, **post):
        return http.request.render("owl_society_managment.society_form")

    @http.route('/member_create', type='http', auth="public", csrf=False)
    def member_register(self, **post):
        userType = self.getUserType()
        return http.request.render("owl_society_managment.member_register", {'userType': userType})

    @http.route('/complaint_create', type='http', auth="public", csrf=False)
    def complaint_register(self, **post):
        userType = self.getUserType()
        return http.request.render("owl_society_managment.complaint_register", {'userType': userType})

    @http.route('/event_create', type='http', auth="public", csrf=False)
    def event_register(self, **post):
        userType = self.getUserType()
        return http.request.render("owl_society_managment.event_register", {'userType': userType})

    @http.route('/balance_create', type='http', auth="public", csrf=False)
    def balance_register(self, **post):
        return http.request.render("owl_society_managment.balance_register")

    @http.route('/jounral_create', type='http', auth="public", csrf=False)
    def jounral_register(self, **post):
        return http.request.render("owl_society_managment.jounral_register")

    @http.route('/account_create', type='http', auth="public", csrf=False)
    def account_register(self, **post):
        return http.request.render("owl_society_managment.account_register")

    @http.route('/society', auth="public", type="json", csrf=False)
    def society_register_form(self, **kw):
        currencys = request.env['res.currency'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n 111111', currencys)
        return currencys

    @http.route('/society/form/', auth="public", type="json", csrf=False)
    def society_register(self, **post):
        currencys = request.env['res.currency'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n\n\n', post)
        # groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        groups_id_name = [(6, 0, [request.env.ref('owl_society_managment.society_secratery_group_admin').id])]
        currency = request.env['res.currency'].sudo().search([('id', '=', post.get('currency'))], limit=1)
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
            'member_type': 'secretary',
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name
        })
        # request.env['helpdesk.team'].sudo().create({
        #     'name': post.get('name'),
        #     'company_id': company.id,
        #         })
        return currencys

    @http.route('/get_member_data', auth="user", type="json", csrf=False)
    def get_member(self, offset=0, limit=0):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        members = request.env['res.users'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'email', 'member_type'])
        print('\n\n\n\n\n\n 111111', members)
        userType = self.getUserType()
        return (members, userType)

    @http.route('/member/form', auth="user", type="json", csrf=False)
    def member_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        products = request.env['product.template'].sudo().search([('company_id', '=', user.company_id.id)])
        print('\n\n\n\n\n\n\n\n33333333', user)
        print('\n\n\n\n\n\n\n\n44444444', kw)
        member_type = kw.get('member_type')
        if member_type == 'treasurer':
            groups_id_name = [(6, 0, [request.env.ref('owl_society_managment.society_treasurer_group_admin').id])]
        else:
            groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        partner = request.env['res.partner'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
        })
        user = request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': kw.get('email'),
            'password': kw.get('name'),
            'member_type': kw.get('member_type'),
            'groups_id': groups_id_name
        })
        sale = request.env['sale.order'].sudo().create({
                    'partner_id': partner.id,
                    'state': 'sale',
                    'user_id': user.id,
                    'invoice_status': 'no',
                    'company_id': user.company_id.id,
                })
        print('\n\n\n\n\n\n\n\n\n555555555555', sale)
        for i in products:
            sale_order = request.env['sale.order.line'].sudo().create({
                        'order_id': sale.id,
                        'product_id': i.id,
                        'name': i.name,
                        'price_total': int(i.list_price),
                        'price_unit': int(i.list_price),
                    })
            print('\n\n\n\n\n666666', sale_order)
        return self.get_member()

    @http.route('/get_Product_data', auth="user", type="json", csrf=False)
    def get_product(self, **post):
        subscriptions = request.env['sale.subscription.template'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n 111111', subscriptions)
        return subscriptions

    @http.route('/services/form', auth="user", type="json", csrf=False)
    def services_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n', kw)
        # file = open(kw.get('image_1920'), 'rb')base64.encodestring(file.read()),base64.encodebytes
        # print('\n\n\n\n\n\n\n\n22222', file)
        prod = request.env['product.template'].sudo().create([{
                    'name': kw.get('name'),
                    'purchase_ok': kw.get('purchase_ok'),
                    'sale_ok': kw.get('sale_ok'),
                    'rent_ok': kw.get('rent_ok'),
                    'type': kw.get('type'),
                    'standard_price': kw.get('standard_price'),
                    'list_price': kw.get('list_price'),
                    'image_1920': base64.encodebytes(kw.get('image_1920')),
                    'company_id': user.company_id.id
                    }])
        print('\n\n\n\n\n\n\n\n\n50000', prod.id)
        # request.env['rental.pricing'].sudo().create([{
        #             'duration': kw.get('duration'),
        #             'unit': kw.get('unit'),
        #             'price': kw.get('price'),
        #             'product_template_id': prod.id,
        #             }])
        # return http.request.render("owl_society_managment.demo_template")
        # return http.local_redirect('/owl_demo')
        return {"prod": prod}

    @http.route('/get_complaint_data', auth="user", type="json", csrf=False)
    def get_complaint(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        members = request.env['res.users'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'email'])
        complaints = request.env['helpdesk.ticket'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'partner_name', 'stage_id'])
        print('\n\n\n\n\n\n 111111', complaints)
        userType = self.getUserType()
        return (complaints, userType, members)

    @http.route('/complaint/form', auth="user", type="json", csrf=False)
    def complaint_form(self, **kw):
        print('\n\n\n\n\n\n\n22222222', kw)
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n\n333333', user, '\n\n\n\n\n44444', user.company_id)
        team = request.env['helpdesk.team'].sudo().search([('company_id', '=', user.company_id)])
        complaint = request.env['helpdesk.ticket'].sudo().create([{
                'name': kw.get('name'),
                'partner_name': user.partner_id.name,
                'partner_email': user.partner_id.email,
                'team_id': team.id,
                'company_id': user.company_id.id,
                }])
        print('\n\n\n\n\n\n\n6666666', complaint.company_id)
        # return http.request.render("owl_society_managment.member_register")
        # return http.local_redirect('/owl_demo')
        return self.get_complaint()

    @http.route('/get_event_data', auth="user", type="json", csrf=False)
    def get_event(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        events = request.env['event.event'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'date_begin', 'date_end', 'note'])
        print('\n\n\n\n\n\n 111111', events)
        # userType = self.getUserType()
        print('\n\n\n\n\n\n\n\n\n**********', user.member_type)
        return (events, user.member_type)

    @http.route('/event/form', auth="user", type="json", csrf=False)
    def event_form(self, **kw):
        # events = request.env['event.event'].sudo().search([('company_id', '=', request.session.uid)])

        def deactive(self):
            record = self.env['event.event'].sudo().search([])
            for i in record:
                if i.date_end < date.today():
                    i.active = False
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
        return self.get_event()
        # return {"am": am}

    @http.route('/get_Parnter_data', auth="user", type="json", csrf=False)
    def get_partner(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        partners = request.env['res.partner'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        accounts = request.env['account.account'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        jounrals = request.env['account.journal'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        # jounrals = request.env['account.journal'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        return (partners, accounts, jounrals)

    @http.route('/balance/form', auth="user", type="json", csrf=False)
    def balance_form(self, **kw):
        print('\n\n\n\n\n\n\n000000', kw)
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        # partners = request.env['res.partner'].sudo().search([('id', '=', kw.get('partner_id'))])
        # print('\n\n\n\n\n\n\n\n222222222', partners.id)
        # accounts = request.env['account.account'].sudo().search([('id', '=', kw.get('destination_account_id'))])
        # print('\n\n\n\n\n\n\n\n55555555555555', accounts.id)
        method = request.env['account.payment.method'].sudo().search([('payment_type', '=', kw.get('payment_type'))], limit=1)
        # print('\n\n\n\n\n\n\n\n\n\n\n111111', method.id)
        currency = request.env['account.journal'].sudo().search([('id', '=', kw.get('journal_id'))], limit=1)
        vals = {
                'move_type': 'entry',
                'journal_id': currency.id,
                'partner_id': int(kw.get('partner_id')),
                'company_id': user.company_id.id,
        }
        print('\n\n\n\n\n\n 88888888888', vals)
        move = request.env['account.move'].with_user(SUPERUSER_ID).create([{
                'move_type': 'entry',
                'journal_id': currency.id,
                'partner_id': int(kw.get('partner_id')),
                'company_id': user.company_id.id,
            }])
        print('\n\n\n\n\n\n\n\n\n\n\n\n777777', move.id)
        payment = request.env['account.payment'].sudo().create([{
                'move_id': move.id,
                'payment_type': kw.get('payment_type'),
                'partner_type': kw.get('partner_type'),
                'amount': kw.get('amount'),
                'partner_id': int(kw.get('partner_id')),
                'date': date.today(),
                'destination_account_id': int(kw.get('destination_account_id')),
                'payment_method_id': method.id,
                }])
        print('\n\n\n\n\n\n\n\n\n\n4444444', payment)
        # return http.request.render("owl_society_managment.demo_template")
        return {'currency': currency}

    @http.route('/jounral/form', auth="user", type="json", csrf=False)
    def jounral_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n\n\n1111111111', kw)
        request.env['account.journal'].sudo().create([{
                'name': kw.get('name'),
                'type': kw.get('type'),
                'code': kw.get('code'),
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')

    @http.route('/get_account_data', auth="user", type="json", csrf=False)
    def get_account_data(self, **post):
        accounts = request.env['account.account.type'].sudo().search_read([], ['id', 'name'])
        return accounts

    @http.route('/account/form', auth="user", type="json", csrf=False)
    def account_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        # accounts = request.env['account.account.type'].sudo().search([('name', '=', kw.get('user_type_id'))])
        # print('\n\n\n\n\n\n\n\n\n', accounts)
        request.env['account.account'].sudo().create([{
                'name': kw.get('name'),
                'user_type_id': int(kw.get('user_type_id')),
                'code': kw.get('code'),
                'company_id': user.company_id.id,
                'reconcile': 'TRUE',
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')

    @http.route('/my_order', type='http', auth="public", csrf=False)
    def owl_demos(self, **post):
        return http.request.render("owl_society_managment.orders_template")

    @http.route('/get_order_details', type='json', auth="public", csrf=False)
    def get_partners(self, **post):
        users = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        if users.member_type == "member":
            domain = [
                ('partner_id', '=', request.env.user.partner_id.id),
                ('state', 'in', ['sale', 'done'])
            ]
        else:
            domain = [
                ('company_id', '=', request.env.user.company_id.id),
                ('state', 'in', ['sale', 'done'])
            ]
        return request.env['sale.order'].sudo().search_read(domain, ['id', 'name', 'date_order', 'amount_total'])

    @http.route('/get_data/', type='http', auth="public", csrf=False)
    def owl_details(self, **post):
        return http.request.render("owl_demo.detail_template")

    @http.route('/order_detail', type='json', auth="public", csrf=False)
    def order_data(self, **kw):
        order = request.env['sale.order'].sudo().search([('id', '=', kw.get('order_id'))])
        order_detail = order.order_line.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty', 'product_id'])
        products = {}
        # for line in order.order_line:
        #     products[line.id] = line.product_id.image_1920
        sale_detail = order.read(['name', 'date_order'])
        partner_detail = order.partner_id.read(['id', 'name', 'street', 'city', 'zip'])
        return {'details': order_detail, 'order': sale_detail, 'partner': partner_detail, 'products': products}
