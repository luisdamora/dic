dic
===

Dependency Injection Container for Python 3+ influenced partially by Autofac_. dic aims to be a tiny "out of the way" framework to help
realise IoC via dependency injection. dic uses Python 3 annotations to provide hints for the components that should be injected.

|version| |build| |docs|

Documentation
=============
dic documentation is available via `Read the Docs`_.

Install
=======
dic is available via pip:
 ::

    pip install dic

Features
========
Currently, dic supports:

1. Constructor injection for classes
2. Factory and Lazy relationships
3. Registration via:
    1. Constructor matching for a registered class
    2. Custom callback
    3. Pre-created instances
4. Lifetime scopes:
    1. Instance per dependency
    2. Single instance
    
Quick Example
=============
A quick example on how to use dic:
 ::

    import dic

    class SimpleThing(object):
        def say(self, message):
            print(message)

    class RequiresThing(object):
        def __init__(self, thing: SimpleThing):
            self.thing = thing

        def say(self, message):
            self.thing.say(message)

    # build the container
    builder = dic.container.ContainerBuilder()

    builder.register_class(SimpleThing)
    builder.register_class(RequiresThing, component_scope=dic.scope.SingleInstance)

    container = builder.build()

    # use the container

    # Note there'll only be one of these due to SingleInstance scoping during build
    x = container.resolve(RequiresThing)
    x.say("my message")

Relationships
=============
dic supports basic relationships:

1. `dic.rel.Lazy` - don't create the dependency until it's first used
2. `dic.rel.Factory` - the component wants to create other components. Lifetime scopes are respected. Supports custom arguments.

Using a factory:
 ::

    import dic

    class SimpleThing(object):
        def __init__(self, special_argument):
            self.special_argument = special_argument

    class BuildsThings(object):
        def __init__(self, thing_factory: dic.rel.Factory(SimpleThing)):
            self.thing_factory = thing_factory

        def build_me_a_thing(self):
            # builds a new thing using the injected factory
            # Note that custom arguments can be provided here
            self.thing_factory(special_argument="My super special argument")

    # build the container
    builder = dic.container.ContainerBuilder()

    builder.register_class(SimpleThing)
    builder.register_class(BuildsThing)

    container = builder.build()

    # use the container

    x = container.resolve(BuildsThing)

    # use it
    thing = x.build_me_a_thing()
    # ...


FAQ
===

1. Is dic thread-safe?

 Yes. `dic.rel.Lazy` and `dic.container.Container.resolve()` are thread-safe. As a result, do not store the component_context given to `register_callback` callbacks,
 as thread-safety is enforced at the container.resolve() level.

2. Can I define my own scopes?

 Yes. Derive a scope from `dic.scope.Scope`. Scopes can be used to provide lifetime for a calling thread, for example
 
Similar Projects
================
There's some similar dependency injection containers for python (not mentioning Spring for Python!?) that take different approaches:
 
1. `injector`_ 

2. `Bottle Dependency Injection`_


.. _Autofac: http://autofac.org/
.. _`Read the Docs`: http://dic.readthedocs.org/
.. _`Bottle Dependency Injection`: https://github.com/bottlepy/bottle-inject
.. _`injector`: https://github.com/alecthomas/injector
.. |version| image:: https://pypip.in/version/dic/badge.svg?text=version
    :target: https://pypi.python.org/pypi/dic
.. |docs| image:: https://readthedocs.org/projects/dic/badge/?version=latest
    :target: https://readthedocs.org/projects/dic/
.. |build| image:: https://travis-ci.org/zsims/dic.svg?branch=master
    :target: https://travis-ci.org/zsims/dic
