"""This module contains helper code used by :mod:`tests` module"""
from dynaconf import Dynaconf
from dynaconf import Validator

settings = Dynaconf(
    envvar_prefix="TESTFM",
    core_loaders=["YAML"],
    settings_file=["conf/testfm.yaml"],
    preload=["conf/*.yaml"],
    includes=["conf/testfm.local.yaml"],
    envless_mode=True,
    lowercase_read=True,
    load_dotenv=True,
    validators=[
        Validator(
            "subscription.rhn_username",
            "subscription.rhn_password",
            "subscription.fm_rhn_poolid",
            "subscription.dogfood_org",
            "subscription.dogfood_activationkey",
            "subscription.capsule_dogfood_activationkey",
            "subscription.dogfood_url",
            must_exist=True,
        )
    ],
)
