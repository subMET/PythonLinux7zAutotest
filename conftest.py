import random
import string
import subprocess
import pytest
import yaml
from datetime import datetime
from sshcheckers import ssh_checkout_positive, upload_files

with open("config.yaml") as f:
    data = yaml.safe_load(f)


folder_in = data["folder_in"]
folder_out = data["folder_out"]
folder_ext = data["folder_ext"]
folder_badarx = data["folder_badarx"]


@pytest.fixture()
def make_folders():
    return ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "mkdir {} {} {} {}".format(folder_in, folder_out, folder_ext, folder_badarx), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "rm -rf {}/* {}/* {}/* {}/*".format(folder_in, folder_out, folder_ext, folder_badarx), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; dd if=/dev/urandom of={} bs=1M count=1 "
                                 "iflag=fullblock".format(folder_in, filename), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; mkdir {}".format(folder_in, subfoldername), ""):
        return None, None
    if not ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 "
                                 "iflag=fullblock".format(folder_in, subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture(autouse=True)
def log():
    yield
    with open("/proc/loadavg", mode='r') as load:
        for item in load:
            load_txt = item
    record = " ".join((datetime.now().strftime("%Y-%b-%d %H-%M-%S"),str(data["count"]),str(data["size"]),load_txt))
    with open("stat.txt",mode='a') as log:
        log.write(record)

@pytest.fixture(scope="session")
def deploy():
    res = []
    upload_files(data["host"], data["user"], str(data["passwd"]), "tests/p7zip-full.deb",
                 "/home/{}/p7zip-full.deb".format(data["user"]))
    res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]), "echo '{}' | sudo -S dpkg -i "
                                     "/home/{}/p7zip-full.deb".format(str(data["passwd"]), data["user"]),
                                     "Настраивается пакет"))
    res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                     "echo '{}' | sudo -S dpkg -s p7zip-full".format(str(data["passwd"])),
                                     "Status: install ok installed"))
    assert all(res)