# Integration Testing Framework

## Problem statement

ITF solves target abstraction for testing environments. Instead of writing a separate test script for each target environment, you can write one test and run it across multiple targets.

Examples of target environments:

- Docker containers for fast, lightweight testing (Developer's environment)
- QEMU virtual machines for emulated hardware (CI/CD pipelines)
- Real hardware for production validation (Hardware-in-loop)

Without ITF, testing the same feature across Docker and real hardware or QEMU often requires different scripts because the APIs and commands differ between environments.

## How does ITF achieve this?

ITF provides a unified Target interface. Instead of calling environment-specific commands, the test code interacts with a generic target object. We write test logic once in Python/pytest, and ITF routes the execution to Docker, QEMU, or real hardware seamlessly.

### 1. The Unified Target Interface

Target object provides a standard set of methods that every target implementation supports:

```python
target.execute(cmd)
target.upload(src, dst)
target.download(src, dst)
target.restart()
```

### 2. Capability-Based Adaptation

Not all targets support the same features. A minimal Docker container might not have SSH, while a QEMU VM does. Instead of hardcoding assumptions, ITF uses a capability system:

```python
from score.itf.plugins.core import requires_capabilities

# This test ONLY runs if the target supports 'exec'
@requires_capabilities("exec")
def test_basic_command(target):
    exit_code, output = target.execute("uname -a")
    assert exit_code == 0


# This test ONLY runs if target has BOTH ssh AND sftp
@requires_capabilities("ssh", "sftp")
def test_file_transfer_over_ssh(target):
    with target.ssh() as ssh:
        ssh.execute_command("touch /tmp/test.txt")
```

### How this solves portability

- When running against Docker: the first test runs, and the second test is automatically skipped because there is no SSH server.
- When running against QEMU: both tests run.
- You maintain a single test file for multiple environments without `if/else` checks for the environment.

### 3. Plugin-Driven Target Selection

The actual target type is not hardcoded in the test. It is selected at runtime via Bazel configuration:

```python
# Same test file, different BUILD targets
py_itf_test(
    name = "test_feature_docker",
    srcs = ["test_feature.py"],
    args = ["--docker-image=ubuntu:24.04"],
    plugins = ["@score_itf//score/itf/plugins:docker_plugin"],
)

py_itf_test(
    name = "test_feature_qemu",
    srcs = ["test_feature.py"],
    args = ["--qemu-rootfs=$(location //images:rootfs)"],
    plugins = ["@score_itf//score/itf/plugins:qemu_plugin"],
)
```

The `plugins` parameter tells ITF which target implementation to instantiate. The test file itself remains agnostic to the target environment.

### 4. Debugging & Telemetry Problem
When an test crashes or misbehaves, we rely on specific industry standards debugging tools like DLT (Diagnostic Log and Trace) and need to extract .dlt file and core dumps from the crashed processes. Extracting these from a running QEMU VM or a physical ECU usually requires custom bash scripts. ITF provides dedicated, target-agnostic plugins for automotive debugging:

- dlt plugin: Captures and analyzes DLT messages natively within the Python test.
- core_dump plugin: Automatically extracts core dumps from targets that support exec and file_transfer, regardless of whether the target is QEMU or real hardware.

## How to build & run test
