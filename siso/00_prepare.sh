#!/bin/bash
[ "$#" -lt 2 ] && echo "Usage: $0 <rootfs_dir> <packages>" && exit 1
ROOTFS=$1
shift
PREPARE_PACKAGES="$@"
[ ! -d ${ROOTFS} ] && echo "Error: ${ROOTFS} is not a directory" && exit 1
[ -z "${PREPARE_PACKAGES}" ] && echo "Error: no packages specified" && exit 1
[ ! -f ${ROOTFS}/usr/bin/dpkg ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
[ ! -f ${ROOTFS}/usr/bin/apt-get ] && echo "Error: ${ROOTFS} is not a chroot" && exit 1
sudo chroot ${ROOTFS} /bin/bash <<- EOF
		export HOME=/root
		export LC_ALL=C
		echo "senioros-live" > /etc/hostname
		if grep -q universe /etc/apt/sources.list; then
			echo "Universe already enabled"
		else
			sed -i 's/main/main universe multiverse restricted/' /etc/apt/sources.list
		fi
		apt-get update || exit 1
		apt-get install --yes dbus || exit 1
		dbus-uuidgen > /var/lib/dbus/machine-id || exit 1
		dpkg-divert --local --rename --add /sbin/initctl || exit 1
		ln -s /bin/true /sbin/initctl || true
		apt-get upgrade --yes || exit 1
		apt-get install --yes casper discover laptop-detect os-prober initramfs-tools || exit 1
                if grep -q "# export" /etc/casper.conf; then
                        sed -i 's/# export/export/' /etc/casper.conf
                fi
		apt-get install --yes linux-generic --no-install-recommends || exit 1
		apt-get install --yes ${PREPARE_PACKAGES} || exit 1
		touch /.prepare
EOF
