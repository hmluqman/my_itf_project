# test_hello.py
from score.itf.plugins.core import requires_capabilities


@requires_capabilities("exec")
def test_uname(target):
    """
    Verify we can execute a command on any target that supports 'exec'.
    Works on both Docker (native exec API) and QEMU (via SSH).
    """
    exit_code, output = target.execute("uname -a")
    assert exit_code == 0
    assert b"Linux" in output


@requires_capabilities("ssh")
def test_ssh_command(target):
    """
    Verify SSH connectivity. Only runs on targets with SSH capability.
    - QEMU: SSH is available by default.
    - Docker: Only works if the image has an SSH server (e.g., linuxserver/openssh-server).
    """
    with target.ssh(username="root", password="") as ssh:
        exit_code, stdout, stderr = ssh.execute_command_output("echo hello")
        assert exit_code == 0
        assert "hello" in stdout[0]


@requires_capabilities("file_transfer")
def test_file_transfer(target):
    """
    Verify file upload/download. 
    - QEMU: uses SFTP via target.sftp()
    - Docker: uses Docker API via target.upload()/download()
    """
    # Write a local test file
    with open("test_upload.txt", "w") as f:
        f.write("ITF test payload\n")

    # Upload using the generic API
    target.upload("test_upload.txt", "/tmp/test_upload.txt")

    # Download it back to verify
    target.download("/tmp/test_upload.txt", "downloads/test_download.txt")

    with open("downloads/test_download.txt", "r") as f:
        assert "ITF test payload" in f.read()


@requires_capabilities("exec")
def test_kernel_version(target):
    """
    A simple assertion on the kernel version output.
    """
    exit_code, output = target.execute("cat /proc/version")
    assert exit_code == 0
    assert len(output) > 0
    assert b"Linux" in output
