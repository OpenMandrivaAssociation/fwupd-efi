#global debug_package %{nil}
%define _empty_manifest_terminate_build 0

%define devname	%mklibname %{name} -d

Group:     System/Kernel and hardware
Summary:   Firmware update EFI binaries
Name:      fwupd-efi
Version:   1.1
Release:   1
License:   LGPLv2+
URL:       https://github.com/fwupd/fwupd-efi
Source0:   http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz


BuildRequires: meson
BuildRequires: gnu-efi
BuildRequires: pesign
BuildRequires: pkgconfig(nss)

%description
fwupd is a project to allow updating device firmware, and this package provides
the EFI binary that is used for updating using UpdateCapsule.

package -n %{devname}
Summary:	Header files from %{name}
Group:		Development/C
Requires: %{name} = %{EVRD}
Provides:	%{name}-devel = %{version}-%{release}

%prep
%autosetup -p1

%build

%meson \
    -Defi_sbat_distro_id="OpenMandriva" \
    -Defi_sbat_distro_summary="OpenMandriva Lx" \
    -Defi_sbat_distro_pkgname="%{name}" \
    -Defi_sbat_distro_version="%{version}-%{release}" \
    -Defi_sbat_distro_url="https://github.com/OpenMandrivaAssociation/%{name}"

%meson_build

%install
%meson_install


# sign fwupd.efi loader
%ifarch x86_64
%global efiarch x64
%endif
%ifarch aarch64
%global efiarch aa64
%endif
%global fwup_efi_fn $RPM_BUILD_ROOT%{_libexecdir}/fwupd/efi/fwupd%{efiarch}.efi
%pesign -s -i %{fwup_efi_fn} -o %{fwup_efi_fn}.tmp
%define __pesign_client_cert fwupd-signer
%pesign -s -i %{fwup_efi_fn}.tmp -o %{fwup_efi_fn}.signed
rm -vf %{fwup_efi_fn}.tmp

%files
%doc README.md AUTHORS
%license COPYING
%{_libexecdir}/fwupd/efi/*.efi
%{_libexecdir}/fwupd/efi/*.efi.signed

%files -n %{devname}
%{_libdir}/pkgconfig/fwupd-efi.pc
