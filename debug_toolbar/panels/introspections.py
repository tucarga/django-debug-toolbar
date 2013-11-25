from debug_toolbar.panels import DebugPanel


class ContextIntrospectionPanel(DebugPanel):

    name = 'Context Introspection'
    template = 'debug_toolbar/panels/introspection.html'
    has_content = True

    def nav_title(self, *args, **kwargs):
        return 'Context Introspection'

    def title(self, *args, **kwargs):
        return 'Context Variables'

    def process_response(self, request, response):
        data = response.context_data.copy()
        data.pop('view')
        objects = []
        for key, value in data.items():
            obj = {'name': key,
                   'type': str(type(value)),
                   'attributes': get_attributes(value),
                   }
            objects.append(obj)

        self.record_stats({
            'objects': objects,
        })


def get_attribute_type(attribute, obj):
    if attribute == 'objects':
        return 'Manager'
    attribute_type = type(getattr(obj, attribute)).__name__
    return attribute_type


def get_attributes(obj):
    attribute_list = []
    attributes = dir(obj)
    attributes = filter_attributes(attributes)
    for attribute in attributes:
        attribute_list.append({'name': attribute,
                               'type': get_attribute_type(attribute, obj)})
    return attribute_list


def filter_attributes(attributes):
    attributes = [attribute for attribute in attributes if not attribute.startswith('_')]
    attributes = [attribute for attribute in attributes if not attribute[0].isupper()]
    return attributes
