%define _empty_manifest_terminate_build 0

%define devname %mklibname %{name} -d

Group:		System/Kernel and hardware
Summary:	Firmware update EFI binaries
Name:		fwupd-efi
Version:	1.4
Release:	1
License:	LGPLv2+
URL:		https://github.com/fwupd/fwupd-efi
Source0:	http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz

# these are the only architectures supporting UEFI UpdateCapsule
ExclusiveArch:	%{efi}
BuildRequires:	meson
BuildRequires:	gnu-efi
BuildRequires:	efi-srpm-macros
BuildRequires:	gcc
BuildRequires:	binutils

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
    -Defi-cc="gcc" \
    -Defi-ld="ld.bfd" \
    -Defi-libdir="%{_libdir}" \
    -Defi-ldsdir="%{_libdir}/gnuefi" \
    -Defi-includedir="%{_includedir}/efi" \
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
