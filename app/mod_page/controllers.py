from flask import Flask, Blueprint, request, render_template, flash, session, redirect, url_for

from app.controllers import missing_session, go_home, go_dashboard, get_field

from app.mod_page.forms import CreateAndUpdateForm
from app.mod_page.resource_forms import CreateAndUpdateResourceForm
from app.mod_page.models import Page, PageResource


mod_page = Blueprint('page', __name__, url_prefix='/page')


@app.route('/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def page():
    if missing_session() or not request.values.get('seq'): go_home()

    page_form = CreateAndUpdateForm()

    if request.values.get('id'):
        page = Page.lookup_id(request.values.get('id'))

        resource_form = CreateAndUpdateResourceForm()

        if page_form.validate_on_submit():
            page.name =
        elif request.method == 'DELETE':
        else:
            page_form.sequence.data = req.values.get('seq')
            
    else:
        if page_form.validate_on_submit() and request.args.get('course_id') and request.args.get('unit_id'):
            page = Page(
                course_id=request.args.get('course_id'),
                unit_id=request.args.get('unit_id'),
                name=page_form.name.data,
                text_content=page_form.text_content.data,
                sequence=page_form.sequence.data
            )

            page.save()
        else:
            go_dashboard()
