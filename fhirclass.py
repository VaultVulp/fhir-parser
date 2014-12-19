#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FHIRClass(object):
    """ An element/resource that should become its own class.
    """
    
    known = {}
    
    @classmethod
    def for_element(cls, element):
        """ Returns an existing class or creates one for the given element.
        Returns a tuple with the class and a bool indicating creation.
        """
        assert element.represents_class
        class_name = element.name_if_class()
        if class_name in cls.known:
            return cls.known[class_name], False
        
        klass = cls(element)
        cls.known[class_name] = klass
        return klass, True
    
    @classmethod
    def with_name(cls, class_name):
        return cls.known.get(class_name)
    
    def __init__(self, element):
        assert element.represents_class
        self.path = element.path
        self.name = element.name_if_class()
        self.module = element.profile.spec.as_module_name(self.name)
        self.resource_name = element.name_of_resource()
        self.superclass = None
        self.superclass_name = element.superclass_name
        self.short = element.definition.short
        self.formal = element.definition.formal
        self.properties = []
    
    def add_property(self, prop):
        """ Add a property to the receiver.
        
        :param FHIRClassProperty prop: A FHIRClassProperty instance
        """
        assert isinstance(prop, FHIRClassProperty)
        
        # do we already have a property with this name?
        # if we do and it's a specific reference, make it a reference to a
        # generic resource
        for existing in self.properties:
            if existing.name == prop.name:
                if not existing.reference_to_profile:
                    print('Already have property "{}" on "{}", which is only allowed for references'.format(prop.name, self.name))
                
                existing.reference_to_profile = 'Resource'
                return
        
        self.properties.append(prop)
        self.properties = sorted(self.properties, key=lambda x: x.name)
    
    def property_for(self, prop_name):
        for prop in self.properties:
            if prop.name == prop_name:
                return prop
        return None
    
    def should_write(self):
        if self.superclass is not None:
            return True
        return True if len(self.properties) > 0 else False
    
    @property
    def has_nonoptional(self):
        for prop in self.properties:
            if prop.nonoptional:
                return True
        return False


class FHIRClassProperty(object):
    """ An element describing an instance property.
    """
    
    def __init__(self, element, type_obj, type_name=None):
        assert element and type_obj     # and must be instances of FHIRElement and FHIRElementType
        spec = element.profile.spec
        
        self.path = element.path
        if not type_name:
            type_name = type_obj.code
        name = element.definition.prop_name
        if '[x]' in name:
            name = name.replace('[x]', '{}{}'.format(type_name[:1].upper(), type_name[1:]))
        
        self.orig_name = name
        self.name = spec.safe_property_name(name)
        self.parent_name = element.parent_name
        self.class_name = spec.class_name_for_type(type_name)
        self.module_name = None             # should only be set if it's an external module (think Python)
        self.json_class = spec.json_class_for_class_name(self.class_name)
        self.is_native = spec.class_name_is_native(self.class_name)
        self.is_array = True if '*' == element.n_max else False
        self.nonoptional = True if element.n_min is not None and 0 != int(element.n_min) else False
        self.reference_to_profile = type_obj.profile
        self.reference_to_name = spec.class_name_for_profile(self.reference_to_profile)
        self.reference_to = None
        self.short = element.definition.short
