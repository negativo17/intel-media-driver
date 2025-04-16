%undefine       __cmake_in_source_build

Name:           intel-media-driver
Version:        25.2.0
Release:        1%{?dist}
Epoch:          1
Summary:        VA-API user mode driver for GEN based graphics hardware
License:        MIT and BSD-3-Clause
URL:            https://01.org/linuxmedia/vaapi

Source0:        https://github.com/intel/media-driver/archive/intel-media-%{version}.tar.gz
Source1:        %{name}.metainfo.xml
Source2:        %{name}.py
Source3:        %{name}.svg
Patch0:         %{name}-info.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib >= 0.6.3
BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libva) >= 1.0.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)
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
%ifarch %{ix86}
export CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
%endif

%cmake \
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
  -DRUN_TEST_SUITE=OFF

%cmake_build

%install
%cmake_install

# Install AppData and add modalias provides
install -pm 0644 -D %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
%{SOURCE2} . | xargs appstream-util add-provide %{buildroot}%{_metainfodir}/%{name}.metainfo.xml modalias
install -pm 0644 -D %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/%{name}.svg

%check
appstream-util validate --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

%files -n libva-intel-media-driver
%license LICENSE.md
%doc README.md
%{_libdir}/dri/iHD_drv_video.so
%{_metainfodir}/%{name}.metainfo.xml
%{_datadir}/pixmaps/%{name}.svg

%files -n libigfxcmrt
%license LICENSE.md
%{_libdir}/libigfxcmrt.so.*

%files -n libigfxcmrt-devel
%{_includedir}/igfxcmrt
%{_libdir}/libigfxcmrt.so
%{_libdir}/pkgconfig/igfxcmrt.pc

%changelog
* Wed Apr 16 2025 Simone Caronni <negativo17@gmail.com> - 1:25.2.0-1
- Update to 25.2.0.

* Tue Mar 18 2025 Simone Caronni <negativo17@gmail.com> - 1:25.1.3-1
- Update to 25.1.3.
- Trim changelog.

* Fri Dec 27 2024 Simone Caronni <negativo17@gmail.com> - 1:24.4.4-1
- Update to 24.4.4.

* Thu Nov 28 2024 Simone Caronni <negativo17@gmail.com> - 1:24.4.3-1
- Update to 24.4.3.

* Sun Sep 29 2024 Simone Caronni <negativo17@gmail.com> - 1:24.3.4-1
- Update to 24.3.4.

* Tue Sep 10 2024 Simone Caronni <negativo17@gmail.com> - 1:24.3.3-1
- Update to 24.3.3.

* Mon Aug 05 2024 Simone Caronni <negativo17@gmail.com> - 1:24.3.1-1
- Update to 24.3.1.

* Fri Jun 28 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.5-2
- Make sure there are no redirects in the Appstream metadata URLs.

* Tue Jun 25 2024 Simone Caronni <negativo17@gmail.com> - 1:24.2.5-1
- Update to 24.2.5.
- Add icon to AppData.

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
- Re-enable Meteor/Arrow Lake platforms in 32 bit builds.

* Thu Jan 25 2024 Simone Caronni <negativo17@gmail.com> - 24.1.1-1
- Update to 24.1.1.
