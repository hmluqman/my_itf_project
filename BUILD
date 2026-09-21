load("@score_itf//:defs.bzl", "py_itf_test")

#load("@rules_oci//oci:defs.bzl", "oci_image", "oci_load")
#load("@score_rules_imagefs//rules/linux:ext4.bzl", "ext4")

py_itf_test(
    name = "hello_standalone",
    srcs = ["test_hello.py"],
    args = [
        # Point to your local QEMU image path
        "--qemu-config=$(location qemu_config.json)",
        "--qemu-image=$(location @os_images//ubuntu_x86_64:image)",
    ],
    data = [
        "@os_images//ubuntu_x86_64:image",
        "qemu_config.json",
    ],
    plugins = ["@score_itf//score/itf/plugins:qemu_plugin"],
    tags = [
        "manual",
    ],
    target_compatible_with = ["@platforms//os:linux"],
)

py_itf_test(
    name = "hello_docker_standalone",
    srcs = [
        "test_hello.py"
    ],
    args = [
        "--docker-image=ubuntu:24.04"
    ],
    plugins = [
        "@score_itf//score/itf/plugins:docker_plugin"
    ],
    target_compatible_with = ["@platforms//os:linux"],
)