load("@score_itf//:defs.bzl", "py_itf_test")
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_load")
load("@score_rules_imagefs//rules/linux:ext4.bzl", "ext4")

py_itf_test(
    name = "hello_standalone",
    srcs = ["test_hello.py"],
    args = [
        # Point to your local QEMU image path
        "--qemu-config=$(location @os_images//ubuntu_x86_64:qemu_config)",
        "--qemu-rootfs=$(location @os_images//ubuntu_x86_64:image)",
        "--qemu-disk=$(location @score_itf//test/resources:qemu_disk_image)",
        
    ],
    data = [
        "@os_images//ubuntu_x86_64:image",
        "@os_images//ubuntu_x86_64:qemu_config",
        "@score_itf//test/resources:qemu_disk_image",
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