from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules


from apps import db,admin

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