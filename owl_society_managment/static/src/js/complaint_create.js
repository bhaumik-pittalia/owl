odoo.define('owl_society_managment.complaint_create', function (require) {
    "use strict";

    debugger
    const rpc = require('web.rpc');
    // const member = require('owl_society_managment.my_member_create_component');
    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlComplaintCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
        });
    }
        async willStart() {
            this.complaint = await this.getComplaint();
        }

        async getComplaint () {
            const complaints = await rpc.query({ route: "/get_complaint_data"})
            return complaints;
        }
        get complaints ()  {
            debugger
            return this.complaint;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.complaint = await rpc.query({ route: "/complaint/form", 
                params:{name: this.state.name,
                }});
            this.render(true);
          
        }

        // AddMemberForm(ev) {
        //     if (ev.target.dataset.mode == 'showAddMemberForm') {
        //         const OwlMemberCreateInstance = new OwlMemberCreate();
        //         OwlMemberCreateInstance.mount($('.my_member_create_component')[0]);
        //         this.destroy();
        //     } else {
        //         this.render(true);
        //     }
        // }

        static template = xml`<div>
        <div>
            <div>
            <div class="card-body">
            <t t-if="complaints[1] == 'member'">
            <div>
                <form method="post">
                    <div  class="form-group">
                        <label>Complaint name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
            </t>
            <div class="container py-5">
                        <table class="table">
                            <thead>
                                <tr>
                                  <th scope="col">Complaint</th>
                                  <th scope="col">Member Name</th>
                                  <th scope="col">Stage</th>
                                  <th scope="col">Action</th>
                                </tr>
                            </thead>  
                            <t t-foreach="complaints[0]" t-as="complaint">
                                <tr>
                                    <td><t t-esc="complaint.name"/></td>
                                    <td><t t-esc="complaint.partner_name"/></td>
                                    <td><t t-esc="complaint.stage_id[1]"/></td>
                                    
                                    <td>
                                        <t t-if="complaint.stage_id[1] == 'New'">
                                            <a class="btn btn-primary" t-on-click="_onClickLink">In Progress</a>
                                        </t>
                                        <t t-if="complaint.stage_id[1] == 'In Progress'">
                                            <a class="btn btn-primary" t-on-click="_onClickLink">solved</a>
                                        </t>
                                    </td>
                                    
                                </tr>
                            </t>
                        </table>
                   </div>
                </div>
            </div>
        </div>
        </div>
        `;
    }
    

    // function setup() {
    //     const OwlComplaintCreateInstance = new OwlComplaintCreate();
    //     OwlComplaintCreateInstance.mount($('.my_complaint_create_component')[0]);
    // }
    // // if ($('.my_complaint_create_component').length) {
    // whenReady(setup);
    // }
    // return {OwlComplaintCreate :OwlComplaintCreate, OwlMemberCreate : OwlMemberCreate};
    return OwlComplaintCreate
});