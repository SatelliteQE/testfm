from testfm.content import Content
from testfm.log import logger


def test_positive_content_migrate(ansible_module, setup_yum_content):
    """Verify that pulp2 to pulp3 content migration subcommands work properly.

    :id: 71836e91-3bfa-4867-ac6f-16f29cf37d52

    :setup:
        1. foreman-maintain should be installed.
        2. Yum content synced via fixture.

    :steps:
        1. Run prep-6.10-upgrade
        2. Migrate content to Pulp 3
        3. Check migration statistics
        4. Reset the migration data
        5. Check migration statistics again

    :expectedresults: Successful run.

    :CaseImportance: High
    """
    contacted = ansible_module.command("foreman-maintain prep-6.10-upgrade")
    assert contacted.values()[0]["rc"] == 0

    contacted = ansible_module.command(Content.prepare())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0

    contacted = ansible_module.command(Content.migration_stats())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
        assert "Migrated/Total RPMs: 32/32" in result["stdout"]

    contacted = ansible_module.command(Content.migration_reset())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0

    contacted = ansible_module.command(Content.migration_stats())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
        assert "Migrated/Total RPMs: 0/32" in result["stdout"]
