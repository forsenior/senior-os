#!/bin/bash
[ "$#" -ne 2 ] && echo "Usage: $0 <rootfs_dir> <image_dir>" && exit 1
ROOTFS="$1"
IMAGE_DIR="$2"
[ ! -d ${ROOTFS} ] && echo "Error: ${ROOTFS} is not a directory" && exit 1
[ ! -d ${IMAGE_DIR} ] && echo "Error: ${IMAGE_DIR} is not a directory" && exit 1
[ ! -f ${ROOTFS}/usr/bin/dpkg ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
[ ! -f ${ROOTFS}/usr/bin/apt-get ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1

sudo chroot ${ROOTFS} dpkg-query -W --showformat='${Package} ${Version}\n' | sudo tee ${IMAGE_DIR}/casper/filesystem.manifest
