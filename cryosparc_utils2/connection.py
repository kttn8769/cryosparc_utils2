import os
import json
from cryosparc.tools import CryoSPARC


def communicate_cryosparc(conf_file: str) -> CryoSPARC:
    """Establish communication with a cryoSPARC instance.

    Parameters
    ----------
    conf_file : str
        A json format config file defining following info: 'license', 'host', 'base_port', 'email', 'password'.

    Returns
    -------
    CryoSPARC
        cryosparc.tools.CryoSPARC class object
    """

    assert os.path.exists(conf_file), f"Config file {conf_file} does not exist."
    with open(conf_file) as f:
        conf = json.load(f)

    cs = CryoSPARC(
        license=conf["license"],
        host=conf["host"],
        base_port=conf["base_port"],
        email=conf["email"],
        password=conf["password"],
    )
    assert cs.test_connection(), "cs.test_connection() failed."

    return cs
