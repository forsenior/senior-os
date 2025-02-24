#!/bin/bash
ISO=$1
SIZE=512

get_size() {
	return $(expr $(du -s $ISO | awk '{print $1}') / 512)
}

expand_iso() {
	dd status=progress if=/dev/zero bs=512 count=$(expr ${SIZE} / 512)M >> $ISO
}

create_part() {
	(
	echo n
	echo p
	echo
	echo
	echo
	echo p
	echo w
	) | fdisk $ISO
}

create_filesystem() {
	PART=$(fdisk -l $ISO | tail -n 1)
	START=$(expr $(echo $PART | awk '{print $2}') \* 512)
	END=$(expr $(echo $PART | awk '{print $3}') \* 512)

	ld=$(losetup -f)
	losetup -o $START --sizelimit $END $ld $ISO
	mkfs -t ext4 -L senioros-persist $ld
	losetup -d $ld
}

usage() {
	echo "Usage: $0 <iso>" >&2
	exit 1
}

[[ $# -ne 1 ]] && usage

[[ "$(file -ib $ISO)" != "application/x-iso9660-image; charset=binary" ]] && echo "File is not valid application/x-iso9660-image" >&2 && usage 

[[ "$(id -u)" -ne 0 ]] && echo "Script must me run as root" >&2 && usage

expand_iso
create_part
create_filesystem
