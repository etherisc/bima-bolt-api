import connexion
import six

from openapi_server import util
from server_impl.controllers_impl import TestController_impl


def test_setup_post(tenant, env=None):  # noqa: E501
    """test_setup_post

    Creates/resets test setup (WARNING - request will delete/reset data on systemtest db/bucket).&lt;br&gt; &lt;ol&gt; &lt;li&gt;ensures existence of tenant (acre, systemtest)&lt;/li&gt; &lt;li&gt;ensures existence of correct tenant config&lt;/li&gt; &lt;li&gt;ensures existence of season data with id &#39;systemtest&#39; &lt;/li&gt; &lt;li&gt;ensures existence of bucket acre-systemtest with folder 2021-1-systemtest &lt;li&gt;ensures s3 folder contianing the necessary test files (and nothing else)&lt;/li&gt; &lt;li&gt;drops all mongodb collections that will be recreated by the systemtest)&lt;/li&gt; &lt;/ol&gt; # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: None
    """
    return TestController_impl.test_setup_post(tenant, env)


def test_systemtest_post(target_date, tenant, env=None):  # noqa: E501
    """test_systemtest_post

    Run system test (WARNING - request will delete/reset data on systemtest db/bucket). &lt;ol&gt; &lt;li&gt;sets system to defined state by executing endpoint &#39;/test/setup&#39;&lt;/li&gt; &lt;li&gt;runs test by executing endpoint &#39;calculations&#39;&lt;/li&gt; &lt;li&gt;compiles test outcome and provides feeback in mongodb collection &#39;systemtest&#39;&lt;/li&gt; &lt;/ol&gt; # noqa: E501

    :param target_date: The target date for the loss calculation (rainfall data assumed to be available up to this date)
    :type target_date: str
    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: None
    """
    return TestController_impl.test_systemtest_post(target_date, tenant, env)
