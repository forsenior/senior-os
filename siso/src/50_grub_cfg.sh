#!/bin/bash
[ "$#" -ne 3 ] && echo "Usage: $0 <image_dir> <name> <version>" && exit 1
IMAGE_DIR="$1"
NAME="$2"
VERSION="$3"

[ -z "${VERSION}" ] && echo "Error: no version specified" && exit 1
[ ! -d ${IMAGE_DIR} ] && echo "Error: ${IMAGE_DIR} is not a directory" && exit 1


	cat << EOF | sudo tee ${IMAGE_DIR}/boot/grub/grub.cfg
set default="0"
set timeout=10
menuentry "${NAME} ${VERSION} LTS" {
    set gfxpayload=keep
    linux /casper/vmlinuz boot=casper ---
    initrd /casper/initrd
}
EOF
