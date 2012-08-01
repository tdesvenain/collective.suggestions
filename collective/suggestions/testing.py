from plone.testing import z2

from plone.app.testing import *
import collective.suggestions

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=collective.suggestions,
                                additional_z2_products=[],
                                gs_profile_id='collective.suggestions:default',
                                name="collective.suggestions:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.suggestions:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.suggestions:Functional")

