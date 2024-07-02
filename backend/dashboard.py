from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools_stats.modules import DashboardChart, get_active_graph
from django.utils.translation import gettext_lazy as _

class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Applications',
            exclude='django.contrib.*'
        ))

        self.children.append(modules.ModelList(
            title='Administration',
            models='django.contrib.*'
        ))

        # Add custom stats dashboard
        self.children.append(modules.AppList(
            _('Dashboard Stats Settings'),
            models=('admin_tools_stats.*', ),
        ))

        # Copy following code into your custom dashboard
        # append following code after recent actions module or
        # a link list module for "quick links"
        if context['request'].user.has_perm('admin_tools_stats.view_dashboardstats'):
                graph_list = get_active_graph()
        else:
                graph_list = []

        for i in graph_list:
            kwargs = {}
            kwargs['require_chart_jscss'] = True
            kwargs['graph_key'] = i.graph_key

            for key in context['request'].POST:
                if key.startswith('select_box_'):
                    kwargs[key] = context['request'].POST[key]

            self.children.append(DashboardChart(**kwargs))

class CustomAppIndexDashboard(AppIndexDashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Models',
            include='*'
        ))

        self.children.append(modules.RecentActions(
            title='Recent Actions',
            include_list=('my_app1.*', 'my_app2.*'),
        ))
