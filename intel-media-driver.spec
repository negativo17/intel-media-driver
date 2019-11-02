Name:           intel-media-driver
Version:        19.3.1
Release:        1%{?dist}
Summary:        VA-API user mode driver for GEN based graphics hardware
License:        MIT and BSD
URL:            https://github.com/intel/media-driver

Source0:        %{url}/archive/intel-media-%{version}.tar.gz
Source1:        %{name}.metainfo.xml
Patch0:		https://salsa.debian.org/multimedia-team/intel-media-driver/raw/master/debian/patches/0002-Remove-settings-based-on-ARCH.patch

BuildRequires:  cmake >= 3.5
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib >= 0.6.3
BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libcmrt)
BuildRequires:  pkgconfig(libva) >= 1.0.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)

%description
The Intel(R) Media Driver for VAAPI is a new VA-API (Video Acceleration API)
user mode driver supporting hardware accelerated decoding, encoding, and video
post processing for GEN based graphics hardware.

%prep
%autosetup -p1 -n media-driver-intel-media-%{version}

# rpmlint fixes
find . -name "*.cpp" -exec chmod 644 {} \;
chmod -x README.md LICENSE.md

%build
mkdir build
pushd build
%cmake \
  -DBUILD_CMRTLIB=OFF \
  -DENABLE_NONFREE_KERNELS=ON \
  -DINSTALL_DRIVER_SYSCONF=ON \
  -DMEDIA_RUN_TEST_SUITE=OFF \
  -DRUN_TEST_SUITE=OFF \
  ..

%make_build V=1

popd

%install
pushd build
%make_install
popd

# Install AppData and add modalias provides
mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_metainfodir}

%files
%license LICENSE.md
%doc README.md
%config(noreplace) %{_sysconfdir}/profile.d/intel-media.sh
%{_libdir}/dri/iHD_drv_video.so
%{_metainfodir}/%{name}.metainfo.xml

%changelog
* Fri Nov 01 2019 Simone Caronni <negativo17@gmail.com> - 19.3.1-1
- First build.
