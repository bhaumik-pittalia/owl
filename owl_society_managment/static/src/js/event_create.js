odoo.define('owl_society_managment.event_create', function (require) {
    "use strict";

    const rpc = require('web.rpc');
    // const Menu = require('owl_society_managment.menu');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlEventCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            note:"",
            date_begin:"",
            date_end:"",
        });
    }
        async willStart() {
            this.event = await this.getEvent();
        }

        async getEvent () {
            const events = await rpc.query({ route : "/get_event_data"})
            return events;
        }
        get events ()  {
            debugger
            return this.event;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.event = await rpc.query({ route: "/event/form", 
                params:{name: this.state.name,
                    note: this.state.note,
                    date_begin: this.state.date_begin,
                    date_end: this.state.date_end,
                }});
            // window.location.href = "/member_create"
            this.render(true);
          
        }


        static template = xml`<div>
        <div>
            <t t-if="events[1] == 'secretary'">
            <div>
                <form method="post">
                    <div class="form-group">
                        <label>Event name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Note</label>
                        <textarea rows="4" cols="50" name='note' t-model="state.note" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Start Date</label>
                        <input type="date" name="date_begin" t-model="state.date_begin" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>End Date</label>
                        <input type="date" name="date_end" t-model="state.date_end" class="form-control"/>
                    </div>
                <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
            </t>
            <div class="card-columns">
                <t t-foreach="events[0]" t-as="event">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title"><t t-esc='event.name'/></h5>
                            <p class="card-text"> Start Date:<t t-esc='event.date_begin'/></p>
                            <p class="card-text">End Date:<t t-esc='event.date_end'/></p>
                            <p class="card-text">Details:<t t-esc='event.note'/></p>
                        </div>
                    </div>
                </t>
            </div>
        </div>
        </div>
       
        `;
         // static components = {Menu};
    }

    // function setup() {
    //     const OwlEventCreateInstance = new OwlEventCreate();
    //     OwlEventCreateInstance.mount($('.my_event_create_component')[0]);
    // }

    // whenReady(setup);

    return OwlEventCreate;
});