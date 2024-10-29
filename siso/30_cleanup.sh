#!/bin/bash
[ "$#" -ne 1 ] && echo "Usage: $0 <rootfs_dir>" && exit 1
ROOTFS="$1"
[ ! -d ${ROOTFS} ] && echo "Error: ${ROOTFS} is not a directory" && exit 1
[ ! -f ${ROOTFS}/usr/bin/dpkg ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
[ ! -f ${ROOTFS}/usr/bin/apt-get ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1

sudo chroot ${ROOTFS} /bin/bash <<- EOF
		export HOME=/root
		export LC_ALL=C
		rm /var/lib/dbus/machine-id
		rm /sbin/initctl
		dpkg-divert --rename --remove /sbin/initctl
		apt-get clean
		rm -rf /tmp/*
		rm -rf /var/tmp/*
		rm -rf /var/log/*
		rm -rf /var/cache/*
		rm -rf /.prepare
                id -u ubuntu &>/dev/null || /sbin/useradd -m -G sudo -s/bin/bash ubuntu
                echo "ubuntu:ubuntu" | /sbin/chpasswd
EOF
