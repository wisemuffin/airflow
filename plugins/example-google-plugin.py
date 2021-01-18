# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_appbuilder import expose, BaseView as AppBuilderBaseView

# Importing base classes that we need to derive
from airflow.hooks.base import BaseHook
from airflow.models.baseoperator import BaseOperatorLink
from airflow.providers.amazon.aws.transfers.gcs_to_s3 import GCSToS3Operator

# Will show up in Connections screen in a future version


class PluginHook(BaseHook):
    pass

# Will show up under airflow.macros.test_plugin.plugin_macro
# and in templates through {{ macros.test_plugin.plugin_macro }}


def plugin_macro():
    pass


# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "test_plugin", __name__,
    # registers airflow/plugins/templates as a Jinja template folder
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/test_plugin')

# Creating a flask appbuilder BaseView


class TestAppBuilderBaseView(AppBuilderBaseView):
    default_view = "test"

    @expose("/")
    def test(self):
        return self.render("test_plugin/test.html", content="Hello galaxy!")


v_appbuilder_view = TestAppBuilderBaseView()
v_appbuilder_package = {"name": "Test View",
                        "category": "Test Plugin",
                        "view": v_appbuilder_view}

# Creating a flask appbuilder Menu Item
appbuilder_mitem = {"name": "Google",
                    "category": "Search",
                    "category_icon": "fa-th",
                    "href": "https://www.google.com"}

# A global operator extra link that redirect you to
# task logs stored in S3


class GoogleLink(BaseOperatorLink):
    name = "Google"

    def get_link(self, operator, dttm):
        return "https://www.google.com"

# A list of operator extra links to override or add operator links
# to existing Airflow Operators.
# These extra links will be available on the task page in form of
# buttons.


class S3LogLink(BaseOperatorLink):
    name = 'S3'
    operators = [GCSToS3Operator]

    def get_link(self, operator, dttm):
        return 'https://s3.amazonaws.com/airflow-logs/{dag_id}/{task_id}/{execution_date}'.format(
            dag_id=operator.dag_id,
            task_id=operator.task_id,
            execution_date=dttm,
        )


# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "test_plugin"
    hooks = [PluginHook]
    macros = [plugin_macro]
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package]
    appbuilder_menu_items = [appbuilder_mitem]
    global_operator_extra_links = [GoogleLink(), ]
    operator_extra_links = [S3LogLink(), ]
