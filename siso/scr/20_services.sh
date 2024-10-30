#!/bin/bash
[ "$#" -ne 1 ] && echo "Usage: $0 <rootfs_dir>" && exit 1
ROOTFS="$1"
[ ! -d ${ROOTFS} ] && echo "Error: ${ROOTFS} is not a directory" && exit 1
[ ! -f ${ROOTFS}/usr/bin/dpkg ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
[ ! -f ${ROOTFS}/usr/bin/apt-get ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
sudo chroot ${ROOTFS} /bin/bash <<- EOF
		export HOME=/root
		export LC_ALL=C
		systemctl enable NetworkManager
		systemctl enable systemd-timesyncd
		systemctl enable systemd-udevd
		systemctl set-default graphical.target
		systemctl enable sddm

EOF
