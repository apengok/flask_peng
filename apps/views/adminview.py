import os
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

import flask_admin as admin
from flask_admin.form import RenderTemplateWidget
from flask_admin.model.form import InlineFormAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.contrib.sqla.fields import InlineModelFormList

from apps import db,admin
from apps.models import UserImage

from wtforms import fields
from werkzeug import secure_filename
from flask import current_app,request,render_template

# Customized admin interface
class CustomView(ModelView):
    list_template = 'admin/blog_list.html'
    #create_template = 'admin/blog_create.html'
    edit_template = 'admin/blog_edit.html'


class UserAdmin(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name', 'email')

class PostBlogModelView(ModelView):

    

    # can_delete = False  # disable model deletion
    # page_size = 50  # the number of entries to display on the list view
    
    # column_exclude_list = ['comments','timestamp']
    
    # column_searchable_list = ('headline',)
    # column_filters = ('category', 'headline','body')
    
    #form_create_rules = ('category', 'tags','comments','headline','body','timestamp','timestamp','author')
    
    
    
    #form_create_rules = [
        # Header and four fields. Email field will go above phone field.
        #rules.FieldSet(('headline', 'body', ), 'Blog'),
        # Separate header and few fields
        #rules.Header('Author'),
        #rules.Field('author'),
        # String is resolved to form field, so there's no need to explicitly use `rules.Field`
        #'country',
        # Show macro from Flask-Admin lib.html (it is included with 'lib' prefix)
        #rules.Container('admin/rule_dm.wrap', rules.Field('timestamp'))
    #]

    # Use same rule set for edit page
    #form_edit_rules = form_create_rules

    
    # form_args = {
        # 'headline':{
            # 'label':'Title'
        # },
        # 'body':{
            # 'label':'Blog Html'
        # }
    # }
    #add additional args
    # form_widget_args = {
        # 'body': {
            # 'rows': 10,
            # 'style': 'color: black',
            # 'id':'editor1'
        # }
    # }
    
    form_create_rules = (
        rules.FieldSet(('headline', 'body', 'timestamp'), 'Blogsr rel'),
        #rules.FieldSet(('category', 'tags', 'comments'), 'Permission'),
    )
    
    create_template = 'blog_create.html'

    
# This widget uses custom template for inline field list
class CustomInlineFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super(CustomInlineFieldListWidget,self).__init__('field_list.html')
        
# This InlineModelFormList will use our custom widget and hide row controls
class CustomInlineModelFormList(InlineModelFormList):
    widget = CustomInlineFieldListWidget()
    
    def display_row_controls(self,field):
        return False
        
# Create custom InlineModelConverter and tell it to use our InlineModelFormList
class CustomInlineModelConverter(InlineModelConverter):
    inline_field_list_type = CustomInlineModelFormList
    
class InlineModelForm(InlineFormAdmin):
    form_excluded_columns = ('path',)
    
    form_label = 'Image'
    
    def __init__(self):
        return super(InlineModelForm,self).__init__(UserImage)
        
    def postprocess_form(self,form_class):
        form_class.upload = fields.FileField('Image')
        return form_class
        
    def on_model_change(self,form,model):
        file_data = request.files.get(form.upload.name)
        
        if file_data:
            model.path = secure_filename(file_data.filename)
            file_data.save(os.path.join(current_app.config['IMAGE_UPLOADS_DIR'],model.path))
            
class UserAdmin(ModelView):
    inline_model_form_converter = CustomInlineModelConverter
    
    inline_models = (InlineModelForm(),)

# class CustomModelView(ModelView):
    # def edit_form(self, obj):
        # return CustomModelForm(obj=obj)

# def filtering_function():
   # return app.db.query(CustomModel).filter_by(field_to_filter=my_criteria)

# from wtforms.form import Form
# class CustomModelForm(Form):
    # field_to_filter = QuerySelectField(query_factory=filtering_function)    
    
# admin.add_view(PostBlogModelView(BlogPost, db.session))
# admin.add_view(ModelView(Category, db.session))