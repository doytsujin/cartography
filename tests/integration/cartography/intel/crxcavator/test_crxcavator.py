import cartography.intel.crxcavator.crxcavator
import tests.data.crxcavator.crxcavator


TEST_UPDATE_TAG = 123456789


def _ensure_local_neo4j_has_test_extensions_data(neo4j_session):
    cartography.intel.crxcavator.crxcavator.load_extensions(
        tests.data.crxcavator.crxcavator.TRANSFORMED_EXTENSIONS_DATA,
        neo4j_session,
        TEST_UPDATE_TAG
    )


def _ensure_local_neo4j_has_test_user_extensions_data(neo4j_session):
    cartography.intel.crxcavator.crxcavator.load_user_extensions(
        tests.data.crxcavator.crxcavator.TRANSFORMED_USER_DATA,
        tests.data.crxcavator.crxcavator.TRANSFORMED_USER_EXTENSION_DATA,
        neo4j_session,
        TEST_UPDATE_TAG
    )


def test_transform_and_load_extensions(neo4j_session):
    """
    Test that we can correctly transform and load ChromeExtension nodes to Neo4j.
    """
    extension_res = tests.data.crxcavator.crxcavator.REPORT_RESPONSE
    extension_list = cartography.intel.crxcavator.crxcavator.transform_extensions(extension_res)
    cartography.intel.crxcavator.crxcavator.load_extensions(
        extension_list,
        neo4j_session,
        TEST_UPDATE_TAG)

    query = """
    MATCH(ext:ChromeExtension{id:{ExtensionId}})
    RETURN
    ext.id,
    ext.extension_id,
    ext.version,
    ext.risk_total,
    ext.risk_metadata,
    ext.address,
    ext.email,
    ext.icon,
    ext.crxcavator_last_updated,
    ext.name,
    ext.offered_by,
    ext.permissions_warnings,
    ext.privacy_policy,
    ext.rating,
    ext.rating_users,
    ext.short_description,
    ext.size,
    ext.support_site,
    ext.users,
    ext.website,
    ext.type,
    ext.price,
    ext.report_link
    """
    expected_extension_id = 'f06981cbc72a3c6e2e9e736cbdaef4865a4571bc|1.0'
    nodes = neo4j_session.run(
        query,
        ExtensionId=expected_extension_id
    )
    actual_nodes = list([(
        n['ext.id'],
        n['ext.extension_id'],
        n['ext.version'],
        n['ext.risk_total'],
        n['ext.risk_metadata'],
        n['ext.address'],
        n['ext.email'],
        n['ext.icon'],
        n['ext.crxcavator_last_updated'],
        n['ext.name'],
        n['ext.offered_by'],
        n['ext.permissions_warnings'],
        n['ext.privacy_policy'],
        n['ext.rating'],
        n['ext.rating_users'],
        n['ext.short_description'],
        n['ext.size'],
        n['ext.support_site'],
        n['ext.users'],
        n['ext.website'],
        n['ext.type'],
        n['ext.price'],
        n['ext.report_link']
    ) for n in nodes])
    expected_nodes = list([
        (expected_extension_id,
         'f06981cbc72a3c6e2e9e736cbdaef4865a4571bc',
         '1.0',
         437,
         '{}',
         '',
         '',
         'https://lh3.googleusercontent.com/fake',
         '2016-02-22',
         'CartographyIntegrationTest',
         '',
         ['Your data on all websites'],
         '',
         4.6778846,
         208,
         'fake extension for Cartography integration testing',
         '13.95KiB',
         '',
         38241,
         '',
         'Extension',
         '',
         'https://crxcavator.io/report/f06981cbc72a3c6e2e9e736cbdaef4865a4571bc/1.0'
         )
    ])
    assert actual_nodes == expected_nodes


def test_transform_and_load_user_extensions(neo4j_session):
    """
    Ensure we can transform and load users and extension mapping.
    """
    users_res = tests.data.crxcavator.crxcavator.USER_RESPONSE
    type(users_res)
    users_list, user_extensions_list = cartography.intel.crxcavator.crxcavator.transform_user_extensions(users_res)
    cartography.intel.crxcavator.crxcavator.load_user_extensions(
        users_list,
        user_extensions_list,
        neo4j_session,
        TEST_UPDATE_TAG)

    query = """
    MATCH(user:GSuiteUser{id:{UserId}})
    RETURN user.id, user.email
    """
    expected_user_id = 'user@example.com'
    nodes = neo4j_session.run(query, UserId=expected_user_id)

    actual_nodes = list([(
        n['user.id'],
        n['user.email']
    ) for n in nodes])

    expected_nodes = list([
        ('user@example.com',
         'user@example.com')
    ])
    assert actual_nodes == expected_nodes


def test_user_to_extension(neo4j_session):
    """
    Ensure that users are connected to extensions.
    """
    _ensure_local_neo4j_has_test_extensions_data(neo4j_session)
    _ensure_local_neo4j_has_test_user_extensions_data(neo4j_session)
    query = """
    MATCH(user:GSuiteUser)-[:INSTALLS]->(ext:ChromeExtension{id:{ExtensionId}})
    RETURN user.id, ext.id, ext.name
    """
    expected_extension_id = 'f06981cbc72a3c6e2e9e736cbdaef4865a4571bc|1.0'
    nodes = neo4j_session.run(
        query,
        ExtensionId=expected_extension_id
    )
    actual_nodes = set([(
        n['user.id'],
        n['ext.id'],
        n['ext.name'],
    ) for n in nodes])

    expected_nodes = set([
        ('user@example.com',
         'f06981cbc72a3c6e2e9e736cbdaef4865a4571bc|1.0',
         'CartographyIntegrationTest'
         )
    ])
    assert actual_nodes == expected_nodes
