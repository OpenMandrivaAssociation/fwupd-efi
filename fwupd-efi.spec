%define _empty_manifest_terminate_build 0

%define devname %mklibname %{name} -d

Group:		System/Kernel and hardware
Summary:	Firmware update EFI binaries
Name:		fwupd-efi
Version:	1.1
Release:	3
License:	LGPLv2+
URL:		https://github.com/fwupd/fwupd-efi
Source0:	http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
Patch0:		0001-meson-using-local-copy-ldscript-when-local-copy-crt0.patch
# these are the only architectures supporting UEFI UpdateCapsule
ExclusiveArch:	%{efi}
BuildRequires:	meson
BuildRequires:	gnu-efi
BuildRequires:	efi-srpm-macros

%description
fwupd is a project to allow updating device firmware, and this package provides
the EFI binary that is used for updating using UpdateCapsule.

%package -n %{devname}
Summary:	Header files from %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%prep
%autosetup -p1

%build
%meson \
    -Defi_sbat_distro_id="%{efi_vendor}" \
    -Defi_sbat_distro_summary="%{distribution}" \
    -Defi_sbat_distro_pkgname="%{name}" \
    -Defi_sbat_distro_version="%{version}-%{release}" \
    -Defi_sbat_distro_url="%{disturl}"

%meson_build

%install
%meson_install

%files
%doc README.md AUTHORS
%license COPYING
%{_libexecdir}/fwupd/efi/*.efi

%files -n %{devname}
%{_libdir}/pkgconfig/fwupd-efi.pc
