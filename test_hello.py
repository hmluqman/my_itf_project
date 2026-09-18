def test_hello_qemu(target):
    """Runs a command on a QEMU/Docker target."""

    exit_code, output = target.execute("echo 'Hello from my standalone test!'")

    assert exit_code == 0
    assert b"Hello from my standalone test!" in output