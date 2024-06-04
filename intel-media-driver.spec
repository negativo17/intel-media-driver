Name:           intel-media-driver
Version:        24.2.4
Release:        1%{?dist}
Epoch:          1
Summary:        VA-API user mode driver for GEN based graphics hardware
License:        MIT and BSD-3-Clause
URL:            https://01.org/linuxmedia/vaapi

Source0:        https://github.com/intel/media-driver/archive/intel-media-%{version}.tar.gz
Source1:        %{name}.metainfo.xml
Source2:        %{name}.py
Patch0:         %{name}-info.patch

BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libva) >= 1.0.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)

BuildRequires:  cmake3 >= 3.5
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib >= 0.6.3
BuildRequires:  python3

%description
The Intel Media Driver for VAAPI is a new VA-API (Video Acceleration API) user
mode driver supporting hardware accelerated decoding, encoding, and video post
processing for GEN based graphics hardware.

%package -n     libva-intel-media-driver
Summary:        VA-API user mode driver for GEN based graphics hardware
Requires:       libva%{?_isa}
Obsoletes:      cmrt < %{epoch}:%{version}-%{release}
Provides:       cmrt = %{epoch}:%{version}-%{release}
Obsoletes:      intel-media-driver < %{epoch}:%{version}-%{release}
Provides:       intel-media-driver%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       bundled(cmrt)

%description -n libva-intel-media-driver
The Intel Media Driver for VAAPI is a new VA-API (Video Acceleration API) user
mode driver supporting hardware accelerated decoding, encoding, and video post
processing for GEN based graphics hardware.

%package -n     libigfxcmrt
Summary:        Library to load own GPU kernels on render engine via Intel media driver.
Requires:       libva-intel-media-driver%{?_isa} = %{epoch}:%{version}-%{release}

%description -n libigfxcmrt
libigfxcmrt is a runtime library needed when user wants to execute their own GPU
kernels on render engine. It calls Intel media driver to load the kernels and
allocate the resources. It provides a set of APIs for user to call directly from
application.

%package -n     libigfxcmrt-devel
Summary:        Development files for libigfxcmrt
Requires:       libigfxcmrt%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig

%description -n libigfxcmrt-devel
The libigfxcmrt-devel package contains libraries and header files for developing
applications that use libigfxcmrt.

%prep
%autosetup -p1 -n media-driver-intel-media-%{version}

# rpmlint fixes
find . -name "*.cpp" -o -name "*.md" -o -name "*.txt" -o -name "*.h" -o -name "*.cmake" -exec chmod 644 {} \;

%build
mkdir build
pushd build

%ifarch %{ix86}
export CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
%endif

. /opt/rh/devtoolset-9/enable

%cmake3 \
%ifarch %{ix86}
  -DARCH:STRING=32 \
%endif
  -DBUILD_CMRTLIB=ON \
  -DENABLE_KERNELS=ON \
  -DENABLE_NONFREE_KERNELS=ON \
  -DENABLE_PRODUCTION_KMD=ON \
  -DINSTALL_DRIVER_SYSCONF=OFF \
  -DMEDIA_BUILD_FATAL_WARNINGS=OFF \
  -DMEDIA_RUN_TEST_SUITE=OFF \
  -DRUN_TEST_SUITE=OFF \
  ..

%cmake3_build

popd

%install
pushd build
%cmake3_install
popd

%{?ldconfig_scriptlets}

%files -n libva-intel-media-driver
%license LICENSE.md
%doc README.md
%{_libdir}/dri/iHD_drv_video.so

%files -n libigfxcmrt
%license LICENSE.md
%{_libdir}/libigfxcmrt.so.*

%files -n libigfxcmrt-devel
%{_includedir}/igfxcmrt
%{_libdir}/libigfxcmrt.so
%{_libdir}/pkgconfig/igfxcmrt.pc

%changelog
* Tue Jun 04 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.4-1
- Update to 24.2.4.

* Thu May 23 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.3-1
- Update to 24.2.3.
- Print if it's a Free Kernel or Full Feature build in the information string.

* Sat May 04 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.2-1
- Update to 24.2.2.

* Tue Apr 23 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.1-1
- Update to 24.2.1.

* Mon Apr 15 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.0-1
- Update to 24.2.0.

* Mon Apr 15 2024 Simone Caronni <negativo17@gmail.com> - 1:24.1.5-1
- Rename to match with Fedora's packages.
- Trim changelog.

* Wed Mar 20 2024 Simone Caronni <negativo17@gmail.com> - 24.1.5-1
- Update to 24.1.5.

* Mon Feb 19 2024 Simone Caronni <negativo17@gmail.com> - 24.1.3-1
- Update to 24.1.3.

* Thu Jan 25 2024 Simone Caronni <negativo17@gmail.com> - 24.1.1-1
- Update to 24.1.1.

* Thu Dec 14 2023 Simone Caronni <negativo17@gmail.com> - 23.4.3-1
- Update to 23.4.3.
- Enable Meteor/Arrow Lake platforms in 32 bit builds.

* Fri Nov 03 2023 Simone Caronni <negativo17@gmail.com> - 23.3.5-1
- Update to 23.3.5.
- Disable Meteor/Arrow Lake platforms in 32 bit builds.

* Mon Oct 02 2023 Simone Caronni <negativo17@gmail.com> - 23.3.4-1
- Update to 23.3.4.

* Tue Aug 08 2023 Simone Caronni <negativo17@gmail.com> - 23.3.1-1
- Update to 23.3.1.

* Mon Jul 17 2023 Simone Caronni <negativo17@gmail.com> - 23.3.0-1
- Update to 23.3.0.

* Tue May 23 2023 Simone Caronni <negativo17@gmail.com> - 23.2.2-1
- Update to 23.2.2.

* Wed Apr 19 2023 Simone Caronni <negativo17@gmail.com> - 23.2.0-1
- Update to 23.2.0.

* Thu Apr 13 2023 Simone Caronni <negativo17@gmail.com> - 23.1.6-1
- Update to 23.1.6.

* Sat Mar 11 2023 Simone Caronni <negativo17@gmail.com> - 23.1.3-1
- Update to 23.1.3.

* Fri Feb 24 2023 Simone Caronni <negativo17@gmail.com> - 23.1.2-1
- Update to 23.1.2.

* Fri Feb 10 2023 Simone Caronni <negativo17@gmail.com> - 23.1.1-1
- Update to 23.1.1.

* Mon Jan 30 2023 Simone Caronni <negativo17@gmail.com> - 23.1.0-1
- Update to 23.1.0.

* Sun Dec 04 2022 Simone Caronni <negativo17@gmail.com> - 22.6.4-1
- Update to 22.6.4.

* Fri Nov 18 2022 Simone Caronni <negativo17@gmail.com> - 22.6.3-1
- Update to 22.6.3.

* Mon Oct 24 2022 Simone Caronni <negativo17@gmail.com> - 22.6.0-1
- Update to 22.6.0.

* Tue Oct 04 2022 Simone Caronni <negativo17@gmail.com> - 22.5.4-1
- Update to 22.5.4.

* Wed Aug 24 2022 Simone Caronni <negativo17@gmail.com> - 22.5.3-1
- Update to 22.5.3.

* Wed Aug 17 2022 Simone Caronni <negativo17@gmail.com> - 22.5.2-1
- Update to 22.5.2.

* Tue Aug 09 2022 Simone Caronni <negativo17@gmail.com> - 22.5.1-1
- Update to 22.5.1.

* Thu Jul 21 2022 Simone Caronni <negativo17@gmail.com> - 22.5.0-1
- Update to 22.5.0.

* Mon Jul 04 2022 Simone Caronni <negativo17@gmail.com> - 22.4.4-1
- Update to 22.4.4.

* Thu Jun 09 2022 Simone Caronni <negativo17@gmail.com> - 22.4.3-1
- Update to 22.4.3.

* Wed May 25 2022 Simone Caronni <negativo17@gmail.com> - 22.4.2-1
- Update to 22.4.2.

* Tue Apr 26 2022 Simone Caronni <negativo17@gmail.com> - 22.4.0-1
- Update to 22.4.0.

* Tue Apr 05 2022 Simone Caronni <negativo17@gmail.com> - 22.3.1-2
- Split configuration for the different branches.

* Sun Apr 03 2022 Simone Caronni <negativo17@gmail.com> - 22.3.1-1
- Update to 22.3.1.
- Rework SPEC file.

* Sat Mar 19 2022 Simone Caronni <negativo17@gmail.com> - 22.3.0-1
- Update to 22.3.0.

* Sun Mar 13 2022 Simone Caronni <negativo17@gmail.com> - 22.2.2-1
- Update to 22.2.2.

* Thu Mar 03 2022 Simone Caronni <negativo17@gmail.com> - 22.2.1-1
- Update to 22.2.1.

* Sat Feb 12 2022 Simone Caronni <negativo17@gmail.com> - 22.2.0-1
- Update to 22.2.0.

* Sat Feb 12 2022 Simone Caronni <negativo17@gmail.com> - 22.1.1-2
- Add depdendency on libva.

* Thu Feb 03 2022 Simone Caronni <negativo17@gmail.com> - 22.1.1-1
- Update to 22.1.1.
