NAME=SeniorOS
VERSION=24.04
ROOTFS=rootfs
ARCH=amd64
MIRROR=https://cz.archive.ubuntu.com/ubuntu/
RELEASE=noble
PREPARE_PACKAGES=dbus sudo casper discover laptop-detect os-prober grub-common grub-efi-amd64-signed shim-signed mtools binutils net-tools wireless-tools wpagui locales plymouth plymouth-themes network-manager systemd-resolved systemd-timesyncd
PACKAGES=sddm kde-plasma-desktop
BASEISO_URL=https://cdimage.ubuntu.com/ubuntu-mini-iso/noble/daily-live/current/noble-mini-iso-amd64.iso
IMAGEDIR=image

.PHONY: dirs init prepare packages mount umount services cleanup vmlinuz manifest grub squashfs iso all clean cleanall cleaniso baseiso

all: iso

clean: cleaniso
	@echo "Cleaning up..."
	@$(MAKE) umount
	@sudo rm -rf $(IMAGEDIR)
	@echo "Done."

cleanall: clean
	@echo "Cleaning up rootfs..."
	@$(MAKE) umount
	@sudo rm -rf $(ROOTFS)
	@echo "Done."

cleansquash:
	@echo "Cleaning squashfs..."
	@sudo rm -rf $(IMAGEDIR)/casper/filesystem.*
	@echo "Done."
cleaniso:
	@echo "Cleaning up iso..."
	@$(MAKE) umount
	@sudo rm -f $(NAME)-$(VERSION).iso
	@echo "Done."

dirs:
	@echo "Creating dirs..."
ifeq (,$(wildcard $(ROOTFS)))
	@sudo mkdir -p $(ROOTFS)
	@echo "Created $(ROOTFS) dir."
else
	@echo "$(ROOTFS) dir exists. Skipping..."
endif
ifeq (,$(wildcard $(IMAGEDIR)))
	@sudo mkdir -p $(IMAGEDIR)/{casper,boot/grub}
	@echo "Created $(IMAGEDIR) dir."
else
	@echo "$(IMAGEDIR) dir exists. Skipping..."
endif
	@echo "Done."

init: dirs
ifeq (,$(wildcard $(ROOTFS)/bin/bash))
	@echo "Creating new rootfs..."
	@sudo debootstrap --arch=$(ARCH) --variant=minbase --include=iproute2,iputils-ping,net-tools,openssh-server,systemd $(RELEASE) $(ROOTFS) $(MIRROR)
	@echo "Done."
else
	@echo "Rootfs exists. Skipping..."
endif

mount:
ifeq (,$(wildcard $(ROOTFS)/proc/cpuinfo))
	@echo "Mounting filesystems"
	@sudo mount --bind /dev $(ROOTFS)/dev
	@sudo mount --bind /sys $(ROOTFS)/sys
	@sudo mount --bind /proc $(ROOTFS)/proc
	@sudo mount --bind /dev/pts $(ROOTFS)/dev/pts
	@echo "Done."
else
	@echo "Filesystems are already mounted. Skipping..."
endif

umount:
	@echo "Unmounting filesystems"
	@sudo umount $(ROOTFS)/dev/pts || true
	@sudo umount $(ROOTFS)/proc || true
	@sudo umount $(ROOTFS)/sys || true
	@sudo umount $(ROOTFS)/dev || true
	@echo "Done."

prepare: init
ifeq (,$(wildcard $(ROOTFS)/.prepare))
	@$(MAKE) mount
	@echo "Preparing rootfs..."
	@./00_prepare.sh $(ROOTFS) $(PREPARE_PACKAGES)
	@$(MAKE) umount
	@echo "Done."
else
	@echo "Rootfs is already prepared. Skipping..."
endif

packages: prepare
	@echo "Installing packages..."
	@$(MAKE) mount
	@./10_packages.sh $(ROOTFS) $(PACKAGES)
	@$(MAKE) umount
	@echo "Done."

services: packages
	@$(MAKE) mount
	@echo "Configuring services..."
	@./20_services.sh $(ROOTFS)
	@$(MAKE) umount
	@echo "Done."

cleanup: services
	@$(MAKE) mount
	@echo "Cleaning up rootfs..."
	@./30_cleanup.sh $(ROOTFS)
	@$(MAKE) umount
	@echo "Done."

kernel: cleanup
	@echo "Copying kernel and initrd..."
	@sudo cp $(ROOTFS)/boot/$(shell ls $(ROOTFS)/boot | grep vmlinuz | head -n 1) image/casper/vmlinuz
	@sudo cp $(ROOTFS)/boot/$(shell ls $(ROOTFS)/boot | grep initrd.img | head -n 1) image/casper/initrd
	@echo "Done."

manifest: cleanup
	@echo "Generating manifest..."
	@./40_manifest.sh $(ROOTFS) $(IMAGEDIR)
	@echo "Done."

grub: dirs
	@echo "Generating grub files..."
	@./50_grub_cfg.sh "$(IMAGEDIR)" "$(NAME)" "$(VERSION)"
	@echo "Done."

squashfs: cleanup cleansquash
	@$(MAKE) umount
	@echo "Creating squashfs..."
	@sudo mksquashfs $(ROOTFS) $(IMAGEDIR)/casper/filesystem.squashfs -e boot
	@printf $(sudo du -sx --block-size=1 $(ROOTFS) | cut -f1) | sudo tee $(IMAGEDIR)/casper/filesystem.size
	@echo "Done."

baseiso:
ifeq (,$(wildcard base.iso))
	@echo "Downloading base iso..."
	@wget -O base.iso $(BASEISO_URL)
	@echo "Done."
else
	@echo "Base iso exists. Skipping..."
endif

iso: squashfs manifest kernel grub baseiso cleaniso
	@echo "Setting permissions..."
	@sudo chown -R root:root $(IMAGEDIR)
	@sudo chmod -R u+w $(IMAGEDIR)
	@sudo chmod -R +r $(IMAGEDIR)
	@echo "Creating iso..."
	@sudo xorriso -indev base.iso -outdev $(NAME)-$(VERSION).iso -rm /casper/vmlinuz /casper/initrd -- -map $(IMAGEDIR) / -boot_image any replay -compliance no_emul_toc -padding included
	@echo "Done."
