%undefine       __cmake_in_source_build

Name:           intel-media-driver
Version:        22.3.1
Release:        2%{?dist}
Summary:        VA-API user mode driver for GEN based graphics hardware
License:        MIT and BSD-3-Clause
URL:            https://01.org/linuxmedia/vaapi

Source0:        https://github.com/intel/media-driver/archive/intel-media-%{version}.tar.gz
Source1:        %{name}.metainfo.xml
Source2:        %{name}.py

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib >= 0.6.3
BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libva) >= 1.0.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3

Requires:       libva%{?_isa}
Obsoletes:      cmrt < %{version}-%{release}
Provides:       cmrt = %{version}-%{release}
Provides:       bundled(cmrt)

%description
The Intel Media Driver for VAAPI is a new VA-API (Video Acceleration API) user
mode driver supporting hardware accelerated decoding, encoding, and video post
processing for GEN based graphics hardware.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains development files for the Intel Media Driver for VAAPI.

%prep
%autosetup -p1 -n media-driver-intel-media-%{version}

# rpmlint fixes
find . -name "*.cpp" -o -name "*.md" -o -name "*.txt" -o -name "*.h" -o -name "*.cmake" -exec chmod 644 {} \;

sed -e "/-Werror=address/d" -i media_driver/cmake/linux/media_compile_flags_linux.cmake

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

%check
appstream-util validate --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

%files
%license LICENSE.md
%doc README.md
%{_libdir}/dri/iHD_drv_video.so
%{_libdir}/libigfxcmrt.so.*
%{_metainfodir}/%{name}.metainfo.xml

%files devel
%{_includedir}/igfxcmrt
%{_libdir}/libigfxcmrt.so
%{_libdir}/pkgconfig/igfxcmrt.pc

%changelog
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

* Mon Dec 27 2021 Simone Caronni <negativo17@gmail.com> - 21.4.3-1
- Update to 21.4.3.

* Mon Oct 25 2021 Simone Caronni <negativo17@gmail.com> - 21.3.5-1
- Update to Intel Media Driver 2021Q3 Release.

* Sat Sep 04 2021 Simone Caronni <negativo17@gmail.com> - 21.3.3-1
- Update to 21.3.3.

* Sun Aug 15 2021 Simone Caronni <negativo17@gmail.com> - 21.3.1-1
- Update to 21.3.1.

* Wed Jun 23 2021 Simone Caronni <negativo17@gmail.com> - 21.2.2-1
- Update to 21.2.2.
- Fix build on CentOS/RHEL 8.

* Fri May 28 2021 Simone Caronni <negativo17@gmail.com> - 21.2.1-1
- Update to 21.2.1.

* Wed Apr 14 2021 Simone Caronni <negativo17@gmail.com> - 21.1.3-3
- Enable DG1/SG1 preliminary support.

* Wed Apr 14 2021 Simone Caronni <negativo17@gmail.com> - 21.1.3-2
- Generate PCI vendor data for PackageKit, rework AppStream metadata.
- Fix license.

* Sun Apr 04 2021 Simone Caronni <negativo17@gmail.com> - 21.1.3-1
- Update to 2021Q1 Release.

* Sun Mar 14 2021 Simone Caronni <negativo17@gmail.com> - 21.1.2-1
- Update to 21.1.2.

* Mon Mar 01 2021 Simone Caronni <negativo17@gmail.com> - 21.1.1-1
- Update to 21.1.1.

* Tue Jan  5 2021 Simone Caronni <negativo17@gmail.com> - 20.4.5-1
- Update to Intel Media Driver 2020Q4 Release.

* Tue Dec 08 2020 Simone Caronni <negativo17@gmail.com> - 20.4.3-1
- Update to 20.4.3.

* Fri Dec 04 2020 Simone Caronni <negativo17@gmail.com> - 20.4.2-1
- Update to 20.4.2.

* Fri Oct 30 2020 Simone Caronni <negativo17@gmail.com> - 20.3.0-1
- Update to 2020Q3 Release.

* Mon May 25 2020 Simone Caronni <negativo17@gmail.com> - 20.1.1-4
- Do not install environment variables forcing driver, let it autodetect along
  with intel-vaapi-driver.

* Tue May 19 2020 Simone Caronni <negativo17@gmail.com> - 20.1.1-3
- Fix macro invocation for CentOS/RHEL 7.

* Tue May 05 2020 Simone Caronni <negativo17@gmail.com> - 20.1.1-2
- Update SPEC file for CentOS/RHEL 7.

* Sun Apr 26 2020 Simone Caronni <negativo17@gmail.com> - 20.1.1-1
- Update to 2020 Q1 Release.

* Fri Nov 01 2019 Simone Caronni <negativo17@gmail.com> - 19.3.1-1
- First build.
