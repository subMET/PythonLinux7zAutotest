from sshcheckers import ssh_checkout_positive
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)

folder_in = "{}/file".format(data["working_folder"])
folder_out = "{}/out".format(data["working_folder"])
folder_ext = "{}/ext".format(data["working_folder"])


def test_step1(deploy, make_folders, clear_folders, make_files):
    # test1
    res1 = ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; 7z a {}/arx1 -t{}".format(folder_in, folder_out, data["format"]),
                                 "Everything is Ok"), "Test1 Fail"
    res2 = ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "ls {}".format(folder_out), "arx.{}".format(data["format"])), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                     "cd {}; 7z a {}/arx1 -t{}".format(folder_in, folder_out, data["format"]),
                                     "Everything is Ok"))
    res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                     "cd {}; 7z e arx1.{} -o{} -y".format(folder_out, data["format"], folder_ext),
                                     "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                         "ls {}".format(folder_ext), ""))
    assert all(res)


def test_step3():
    # test3
    assert ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; 7z t {}/arx1.{}".format(folder_in, folder_out, data["format"]),
                                 "Everything is Ok"), "Test1 Fail"


def test_step4(make_folders, clear_folders, make_files):
    # test4
    assert ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "cd {}; 7z u {}/arx1.{}".format(folder_in, folder_out, data["format"]),
                                 "Everything is Ok"), "Test1 Fail"


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                     "cd {}; 7z a {}/arx1 -t{}".format(folder_in, folder_out, data["format"]),
                                     "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                         "cd {}; 7z l arx1.{}".format(folder_out, data["format"]), item))
    assert all(res)


def test_step6():
    assert ssh_checkout_positive(data["host"], data["user"], str(data["passwd"]),
                                 "7z d {}/arx1.{}".format(folder_out, data["format"]), "Everything is Ok"), "Test1 Fail"
