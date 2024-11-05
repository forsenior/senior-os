#!/bin/bash
[ "$#" -lt 2 ] && echo "Usage: $0 <rootfs_dir> <packages>" && exit 1
ROOTFS=$1
shift
PACKAGES=$@
[ ! -d ${ROOTFS} ] && echo "Error: ${ROOTFS} is not a directory" && exit 1
[ ! -f ${ROOTFS}/usr/bin/dpkg ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
[ ! -f ${ROOTFS}/usr/bin/apt-get ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
[ ! -f ${ROOTFS}/usr/bin/dpkg ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1

sudo chroot ${ROOTFS} /bin/bash <<- EOF
		export HOME=/root
		export LC_ALL=C
		apt-get install --yes ${PACKAGES} --no-install-recommends || exit 1
EOF
