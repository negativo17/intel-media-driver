Name:           intel-media-driver
Version:        23.3.4
Release:        1%{?dist}
Summary:        VA-API user mode driver for GEN based graphics hardware
License:        MIT and BSD-3-Clause
URL:            https://01.org/linuxmedia/vaapi

Source0:        https://github.com/intel/media-driver/archive/intel-media-%{version}.tar.gz
Source1:        %{name}.metainfo.xml
Source2:        %{name}.py

BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libva) >= 1.0.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)

BuildRequires:  cmake3 >= 3.5
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib >= 0.6.3
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

%files
%license LICENSE.md
%doc README.md
%{_libdir}/dri/iHD_drv_video.so
%{_libdir}/libigfxcmrt.so.*

%files devel
%{_includedir}/igfxcmrt
%{_libdir}/libigfxcmrt.so
%{_libdir}/pkgconfig/igfxcmrt.pc

%changelog
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
