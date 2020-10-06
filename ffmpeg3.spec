%global realname ffmpeg

#define _legacy_common_support 1
%global _lto_cflags %{nil}

%if 0%{?fedora} >= 25
# OpenCV 3.X has an overlinking issue - unsuitable for core libraries
# Reported as https://github.com/opencv/opencv/issues/7001
%global _without_opencv   1
%endif

%if 0%{?rhel}
%global _without_frei0r   1
%global _without_vpx      1
%bcond_without opencv
%else
%bcond_with opencv
%endif

# Globals for git repository
%global commit0 c289f4b6c9390d5b2b6388b0d82d40af62ea7ce2
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}


Summary:        Digital VCR and streaming server
Name:           ffmpeg3
Version:        3.4.2
Release:        18%{?dist}
%if 0%{?_with_amr:1}
License:        GPLv3+
%else
License:        GPLv2+
%endif
URL:            http://ffmpeg.org/
Source0:	https://git.ffmpeg.org/gitweb/ffmpeg.git/snapshot/%{commit0}.tar.gz#/%{realname}-%{shortcommit0}.tar.gz
# Backport of http://git.videolan.org/?p=ffmpeg.git;a=commitdiff;h=a606f27f4c610708fa96e35eed7b7537d3d8f712 thanks to Nicolas George
Source1:	ffmpeg3.sh
Source2:	ffmpeg3.conf
Patch1:		fs56089.patch
# forces the buffers to be flushed after a drain has completed. Thanks to jcowgill
Patch2:		buffer_flush.patch
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  bzip2-devel
%{?_with_faac:BuildRequires: faac-devel}
%{?_with_fdk_aac:BuildRequires: fdk-aac-devel}
%{?_with_flite:BuildRequires: flite-devel}
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
%{!?_without_frei0r:BuildRequires: frei0r-devel}
%{?_with_gme:BuildRequires: game-music-emu-devel}
BuildRequires:  gnutls-devel
BuildRequires:  gsm-devel
%{?_with_ilbc:BuildRequires: ilbc-devel}
BuildRequires:  lame-devel >= 3.98.3
%{!?_without_jack:BuildRequires: jack-audio-connection-kit-devel}
%{!?_without_ladspa:BuildRequires: ladspa-devel}
BuildRequires:  libass-devel
BuildRequires:  libbluray-devel
%{?_with_bs2b:BuildRequires: libbs2b-devel}
%{?_with_caca:BuildRequires: libcaca-devel}
%{!?_without_cdio:BuildRequires: libcdio-paranoia-devel}
%{?_with_chromaprint:BuildRequires: libchromaprint-devel}
#libcrystalhd is currently broken
%{?_with_crystalhd:BuildRequires: libcrystalhd-devel}
%if 0%{?_with_ieee1394}
BuildRequires:  libavc1394-devel
BuildRequires:  libdc1394-devel
BuildRequires:  libiec61883-devel
%endif
BuildRequires:  libgcrypt-devel
BuildRequires:  libGL-devel
BuildRequires:  libmodplug-devel
%{?_with_rtmp:BuildRequires: librtmp-devel}
%{?_with_smb:BuildRequires: libsmbclient-devel}
%{?_with_ssh:BuildRequires: libssh-devel}
BuildRequires:  libtheora-devel
BuildRequires:  libv4l-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
%{?!_without_vpx:BuildRequires: libvpx-devel >= 0.9.1}
%ifarch %{ix86} x86_64
BuildRequires:  libmfx-devel
BuildRequires:  libXvMC-devel
BuildRequires:  libva-devel >= 0.31.0
BuildRequires:  yasm
%endif
%{?_with_webp:BuildRequires: libwebp-devel}
%{?_with_netcdf:BuildRequires: netcdf-devel}
%{!?_without_nvenc:BuildRequires: nvenc-devel}
%{?_with_amr:BuildRequires: opencore-amr-devel vo-amrwbenc-devel}
%{!?_without_openal:BuildRequires: openal-soft-devel}
%if 0%{!?_without_opencl:1}
BuildRequires:  opencl-headers ocl-icd-devel
Recommends:     opencl-icd
%endif
%{!?_without_opencv:BuildRequires: opencv-devel}
BuildRequires:  openjpeg2-devel
BuildRequires:  openjpeg-devel
BuildRequires:  opus-devel
%{!?_without_pulse:BuildRequires: pulseaudio-libs-devel}
BuildRequires:  perl(Pod::Man)
%{?_with_rubberband:BuildRequires: rubberband-devel}
BuildRequires:  SDL2-devel
%{?_with_snappy:BuildRequires: snappy-devel}
BuildRequires:  soxr-devel
BuildRequires:  speex-devel
BuildRequires:  subversion
%{?_with_tesseract:BuildRequires: tesseract-devel}
#BuildRequires:  texi2html
BuildRequires:  texinfo
%{?_with_twolame:BuildRequires: twolame-devel}
%{?_with_wavpack:BuildRequires: wavpack-devel}
%{!?_without_x264:BuildRequires: x264-devel >= 0.159}
%{!?_without_x265:BuildRequires: x265-devel >= 3.3}
%{!?_without_xvid:BuildRequires: xvidcore-devel}
BuildRequires:  zlib-devel
%{?_with_zmq:BuildRequires: zeromq-devel}
%{?_with_zvbi:BuildRequires: zvbi-devel}
BuildRequires:  libxcb-devel libxcb
# New support
BuildRequires:	libdrm-devel
BuildRequires:	openh264-devel
BuildRequires:	kvazaar-devel >= 1.2.0
BuildRequires:	libmysofa-devel
BuildRequires:	shine-devel
BuildRequires:	vid.stab-devel
BuildRequires:	alsa-lib-devel
%if 0%{?fedora} >= 31
BuildRequires:  intel-mediasdk-devel
%else
BuildRequires:  libmfx-devel
%endif

%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%package        libs
Summary:        Libraries for %{name}
Supplements:	firefox <= 60

%description    libs
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains the libraries for %{name}

%package     -n libavdevice3
Summary:        Special devices muxing/demuxing library

%description -n libavdevice3
Libavdevice is a complementary library to libavf "libavformat". It provides
various "special" platform-specific muxers and demuxers, e.g. for grabbing
devices, audio capture and playback etc.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Requires:       libavdevice3%{_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libxcb

%description    devel
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}

%global ff_configure \
./configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir}/%{name} \\\
    --datadir=%{_datadir}/%{name} \\\
    --docdir=%{_docdir}/%{name} \\\
    --incdir=%{_includedir}/%{name} \\\
    --libdir=%{_libdir}/%{name} \\\
    --mandir=%{_mandir}/%{name} \\\
    --pkgconfigdir=%{_datadir}/pkgconfig \\\
    --arch=%{_target_cpu} \\\
    --optflags="%{optflags}" \\\
    --extra-ldflags="%{?__global_ldflags}" \\\
    %{?_with_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3} \\\
    --enable-bzlib \\\
    --enable-libdrm \\\
    %{?_with_chromaprint:--enable-chromaprint} \\\
    %{!?_with_crystalhd:--disable-crystalhd} \\\
    --enable-fontconfig \\\
    %{!?_without_frei0r:--enable-frei0r} \\\
    --enable-gcrypt \\\
    %{?_with_gmp:--enable-gmp --enable-version3} \\\
    --enable-gnutls \\\
    %{!?_without_ladspa:--enable-ladspa} \\\
    --enable-libass \\\
    --enable-libbluray \\\
    %{?_with_bs2b:--enable-libbs2b} \\\
    %{?_with_caca:--enable-libcaca} \\\
    %{!?_without_cdio:--enable-libcdio} \\\
    %{?_with_ieee1394:--enable-libdc1394 --enable-libiec61883} \\\
    %{?_with_faac:--enable-libfaac --enable-nonfree} \\\
    %{?_with_fdk_aac:--enable-libfdk-aac --enable-nonfree} \\\
    %{?_with_flite:--enable-libflite} \\\
    %{!?_without_jack:--enable-indev=jack} \\\
    --enable-libfreetype \\\
    --enable-libfribidi \\\
    %{?_with_gme:--enable-libgme} \\\
    --enable-libgsm \\\
    %{?_with_ilbc:--enable-libilbc} \\\
    --enable-libmp3lame \\\
    --enable-libkvazaar \\\
    %{?_with_netcdf:--enable-netcdf} \\\
    %{!?_without_nvenc:--enable-nvenc --extra-cflags="-I%{_includedir}/nvenc"} \\\
    %{!?_without_openal:--enable-openal} \\\
    %{!?_without_opencl:--enable-opencl} \\\
    %{!?_without_opencv:--enable-libopencv} \\\
    --enable-libopenh264 \\\
    --enable-libmysofa \\\
    --enable-libshine \\\
    --enable-libvidstab \\\
    --enable-libmfx \\\
    %{!?_without_opengl:--enable-opengl} \\\
    --enable-libopenjpeg \\\
    --enable-libopus \\\
    %{!?_without_pulse:--enable-libpulse} \\\
    %{?_with_rtmp:--enable-librtmp} \\\
    %{?_with_rubberband:--enable-librubberband} \\\
    %{?_with_smb:--enable-libsmbclient} \\\
    %{?_with_snappy:--enable-libsnappy} \\\
    --enable-libsoxr \\\
    --enable-libspeex \\\
    %{?_with_ssh:--enable-libssh} \\\
    %{?_with_tesseract:--enable-libtesseract} \\\
    --enable-libtheora \\\
    %{?_with_twolame:--enable-libtwolame} \\\
    --enable-libvorbis \\\
    --enable-libv4l2 \\\
    %{!?_without_vpx:--enable-libvpx} \\\
    %{?_with_webp:--enable-libwebp} \\\
    %{!?_without_x264:--enable-libx264} \\\
    %{!?_without_x265:--enable-libx265} \\\
    %{!?_without_xvid:--enable-libxvid} \\\
    %{?_with_zmq:--enable-libzmq} \\\
    %{?_with_zvbi:--enable-libzvbi} \\\
    --enable-avfilter \\\
    --enable-avresample \\\
    --enable-postproc \\\
    --enable-pthreads \\\
    --disable-static \\\
    --enable-shared \\\
    --enable-gpl \\\
    --disable-debug \\\
    --disable-stripping

#--enable-x11grab \\\
# was deleted as legacy
# https://www.ffmpeg.org/ffmpeg-devices.html#x11grab


%prep
%autosetup -n %{realname}-%{shortcommit0} -p1

# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
mkdir -p _doc/examples
cp -pr doc/examples/{*.c,Makefile,README} _doc/examples/

%build

%{ff_configure}\
    --shlibdir=%{_libdir}/%{name} \
%if 0%{?ffmpegsuffix:1}
    --build-suffix=%{ffmpegsuffix} \
    --disable-doc \
    --disable-ffmpeg --disable-ffplay --disable-ffprobe --disable-ffserver \
%else
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
%endif
%ifarch %{ix86} x86_64 ppc ppc64
    --enable-runtime-cpudetect \
%endif
%ifarch ppc
    --cpu=g3 \
    --enable-pic \
%endif
%ifarch ppc64
    --cpu=g5 \
    --enable-pic \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%else
    --enable-thumb \
%endif
%ifarch armv7hl armv7hnl
    --cpu=armv7-a \
    --enable-vfpv3 \
    --enable-thumb \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%ifarch armv7hl
    --disable-neon \
%endif
%endif
%endif

%make_build V=0 AM_DEFAULT_VERBOSITY=0
make documentation V=0
make alltools V=0 AM_DEFAULT_VERBOSITY=0

%install
%make_install V=0
rm -r %{buildroot}%{_datadir}/%{name}/examples
%if 0%{!?ffmpegsuffix:1}
install -pm755 tools/qt-faststart %{buildroot}/%{_bindir}/%{name}
%endif

# Install profile and ld.so.config files
install -Dm755 %{S:1} "%{buildroot}/etc/profile.d/ffmpeg3.sh"
install -Dm644 %{S:2} "%{buildroot}/etc/ld.so.conf.d/ffmpeg3.conf"

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post -n libavdevice3 -p /sbin/ldconfig

%postun -n libavdevice3 -p /sbin/ldconfig

%if 0%{!?ffmpegsuffix:1}
%files
%doc COPYING.* CREDITS README.md doc/ffserver.conf
%{_bindir}/%{name}/ffmpeg
%{_bindir}/%{name}/ffplay
%{_bindir}/%{name}/ffprobe
%{_bindir}/%{name}/ffserver
%{_bindir}/%{name}/qt-faststart
%{_mandir}/%{name}/man1/ffmpeg*.1*
%{_mandir}/%{name}/man1/ffplay*.1*
%{_mandir}/%{name}/man1/ffprobe*.1*
%{_mandir}/%{name}/man1/ffserver*.1*
%{_datadir}/%{name}
%{_sysconfdir}/profile.d/%{name}.sh
%endif

%files libs
%{_libdir}/%{name}/lib*.so.*
%exclude %{_libdir}/%{name}/libavdevice.so.*
%{_mandir}/%{name}/man3/lib*.3.gz
%exclude %{_mandir}/%{name}/man3/libavdevice.3*
%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%files -n libavdevice3
%{_libdir}/%{name}/libavdevice.so.*
%{_mandir}/%{name}/man3/libavdevice.3*

%files devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%doc _doc/examples
%doc %{_docdir}/%{name}/*.html
%{_includedir}/%{name}
%{_datadir}/pkgconfig/lib*.pc
%{_libdir}/%{name}/lib*.so

%changelog

* Mon Oct 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-18 
- Rebuilt 

* Sun Jul 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-17 
- Rebuilt for x264

* Wed Jun 03 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-16 
- Rebuilt for x265

* Mon Feb 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-15 
- Rebuilt for x265

* Wed Jan 01 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-14 
- Rebuilt for xvid

* Sun Dec 08 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-13 
- F31 Replaced libmfx by intel-mediasdk

* Sun Dec 01 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-12 
- Rebuilt for x265

* Fri Aug 02 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-11 
- Rebuilt for x265

* Tue Jul 16 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-10 
- Rebuilt 

* Sat Jun 22 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-9  
- Rebuilt for x265

* Wed Mar 13 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-8  
- Rebuilt for x264

* Sun Feb 17 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-7  
- Rebuilt for x265

* Fri Oct 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-6  
- Rebuilt for x265

* Mon Oct 08 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-5  
- Rebuilt for x264

* Sat Jun 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-4  
- Rebuilt for libass

* Fri Apr 27 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-3  
- Automatic Mass Rebuild

* Wed Apr 25 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-2  
- Fixed detection

* Wed Mar 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.4.2-1  
- Initial build
