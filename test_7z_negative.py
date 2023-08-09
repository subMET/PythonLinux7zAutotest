from sshcheckers import ssh_checkout_negative
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)

folder_out = data["folder_badarx"]
folder_ext = data["folder_ext"]


def test_step1():
    # test1
    assert ssh_checkout_negative(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; 7z e badarx.{} -o{} -y".format(folder_out, data["format"], folder_ext), "ERROR"), "Test4 Fail"


def test_step2():
    # test2
    assert ssh_checkout_negative(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; 7z t badarx.{}".format(folder_out, data["format"]), "ERROR"), "Test5 Fail"
