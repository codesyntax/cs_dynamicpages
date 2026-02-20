from plone.behavior.registration import (
    lookup_behavior_registration,
    BehaviorRegistrationNotFound,
)
from plone.restapi.serializer.schema import _check_permission


class Manager:

    def __init__(self, context):
        self.context = context

    def get_template_registry(self):
        """get the nearest item in the containment chain that implements the relevant
        behavior. Implementation taken from
        plone.restapi.services.inherit.get.InheritedBehaviorExpander
        """
        try:
            registration = lookup_behavior_registration("cs_dynamicpages.templates")
            closest = next(
                (
                    obj
                    for obj in self.context.aq_chain
                    if registration.marker.providedBy(obj)
                    and _check_permission("View", self, obj)
                ),
                None,
            )
            return closest or None

        except BehaviorRegistrationNotFound:
            return None

    def get_templates(self):
        """get all registered templates"""
        registry = self.get_template_registry()
        if registry is not None:
            return registry.templates.get("templates", [])

        return []

    def get_template(self, uid):
        """get template by name"""
        registry = self.get_template_registry()
        if registry is not None:
            for template in registry.templates.get("templates", []):
                if template.get("uid") == uid:
                    return template.get("uid", [])

        return None

    def append_template(self, template):
        """append a new template to the registry"""
        registry = self.get_template_registry()
        templates = registry.templates.get("templates", [])
        templates.append(template)
        self.save_templates(templates)

    def save_templates(self, templates):
        """save all new templates i the registry"""
        registry = self.get_template_registry()
        registry.templates = {"templates": templates}

    def delete_template(self, uid):
        """delete a given template from the registry"""
        templates = self.get_templates()
        new_templates = [
            template for template in templates if template.get("uid") != uid
        ]
        if len(templates) > len(new_templates):
            self.save_templates(new_templates)
            return True
        return False
