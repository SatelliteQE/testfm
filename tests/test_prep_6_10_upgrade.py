from testfm.log import logger


def test_positive_prep_6_10_upgrade(ansible_module):
    """Runs content directory preparation for pulp3 migration.

    :id: 46531c4a-2276-4ccd-aed7-92c53d1ad267

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Create /var/lib/pulp/content directory with root owner and 0000 mode
        2. Run foreman-maintain prep-6.10-upgrade

    :expectedresults: Owner group and mode should be changed.

    :CaseImportance: High
    """
    ansible_module.file(path="/var/lib/pulp/content", state="directory", group="root", mode="0000")

    contacted = ansible_module.command("foreman-maintain prep-6.10-upgrade")
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0

    contacted = ansible_module.stat(path="/var/lib/pulp/content")
    assert contacted.values()[0]["stat"]["gr_name"] == "pulp"
    assert contacted.values()[0]["stat"]["mode"] == "2070"
