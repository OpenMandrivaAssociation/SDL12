%define	fname	SDL
%define	name	SDL12
%define	version	1.2.13
%define rel	1
%define	lib_name_orig	lib%{fname}
%define	lib_major	1.2
%define	lib_name	%mklibname %{fname} %{lib_major}

%if %{mdkversion} >= 1010
%define build_plugins	0
%define build_directfb	1
%define build_ggi	1
%define	build_aalib	1
%else
%define build_plugins	0
%define build_directfb	0
%define build_ggi	0
%define	build_aalib	0
%endif

Summary:	Simple DirectMedia Layer
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Source0:	http://www.libsdl.org/release/%{fname}-%{version}.tar.gz
Patch0:		SDL-1.2.10-fixrpath.patch
Patch1:		SDL-1.2.10-libtool.patch
Patch3:		SDL-1.2.10-fix-libtoolize.patch
Patch4:		SDL-1.2.13-libdir.patch
Patch21:	SDL-1.2.10-anonymous-enums.patch
Patch31:	SDL-1.2.10-lock-keys.patch
Patch38:	SDL-1.2.9-missing-mmx-blit.patch
Patch39:	SDL-1.2.10-propagate-pic-to-nasm.patch
Patch41:	SDL-1.2.10-nasm-include.patch
Patch50:	SDL-1.2.10-byteorder.patch
Patch51:	SDL-1.2.13-preferalsa.patch
Patch52:	SDL-1.2.12-pagesize.patch
Patch53:	SDL-1.2.12-disable_yasm.patch
Patch54:	SDL-1.2.11-dont-propagate-lpthread.patch
License:	LGPL
Group:		System/Libraries
URL:		http://www.libsdl.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	arts-devel
# libGL is required to enable glx support
BuildRequires:	libmesaglu-devel
BuildRequires:	esound-devel
BuildRequires:	nas-devel
BuildRequires:	chrpath
BuildRequires:	libpulseaudio-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif
%if %{build_plugins}
BuildRequires:	libtool-devel
%endif
%if %{build_directfb}
BuildRequires:	DirectFB-devel >= 1.0.0
%endif
%if %{build_ggi}
BuildRequires:	libggi-devel
%endif
%if %{build_aalib}
BuildRequires:	aalib-devel
%endif

%description
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

%package -n	%{lib_name}-video-ggi
Summary:	GGI video support for SDL
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description -n	%{lib_name}-video-ggi
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

This package provides GGI video support as a plugin to SDL.

%package -n	%{lib_name}-video-directfb
Summary:	DirectFB video support for SDL
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description -n	%{lib_name}-video-directfb
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

This package provides DirectFB video support as a plugin to SDL.

%package -n	%{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{lib_name_orig} = %{version}-%{release}
Obsoletes:	SDL
Provides:	SDL

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{lib_name}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version} libalsa-devel >= 0.9.0
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	SDL-devel, SDL%{lib_major}-devel
Obsoletes:	SDL-devel

%description -n	%{lib_name}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q -n %{fname}-%{version}
%patch0 -p1
%patch1 -p1 -b .libtool
%patch3 -p1 -b .libtoolize
%patch4 -p1 -b .libdir
%patch21 -p1 -b .enums
%patch31 -p1 -b .lock
%patch38 -p1 -b .mmx_blit
%patch39 -p1 -b .nasm_pic
%patch41 -p1 -b .nasm_include
%patch50 -p1 -b .byteorder
%patch51 -p1 -b .alsa
%patch52 -p1 -b .pagesize
%patch53 -p1 -b .no_yasm
%patch54 -p1 -b .no_lpthread

%build
./autogen.sh

export CFLAGS="%{optflags} -fPIC -O3"
export CXXFLAGS="%{optflags} -fPIC -O3"

%configure2_5x	--enable-video-opengl \
		--disable-video-svga \
%if %{build_ggi}
		--enable-video-ggi \
%if %{build_plugins}
		--enable-video-ggi-plugin \
%endif
%endif
%if %{build_directfb}
		--enable-video-directfb \
%if %{build_plugins}
		--enable-video-directfb-plugin \
%endif
%endif
%if %{build_aalib}
		--enable-video-aalib \
%if %{build_plugins}
		--enable-video-aalib-plugin \
%endif
%endif
%ifarch %{ix86}
		--enable-nasm \
%else
		--disable-nasm \
%endif
		--disable-debug \
		--enable-dlopen \
		--enable-sdl-dlopen \
		--enable-arts \
		--enable-arts-shared \
		--enable-esd \
		--enable-esd-shared \
		--enable-nas \
		--enable-pulseaudio-shared \
		--enable-alsa \
		--program-prefix= \
		--disable-rpath
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# remove unpackaged files
%if %{build_plugins}
rm -f $RPM_BUILD_ROOT%{_libdir}/SDL/*.a
%endif

# --disable-rpath does not seem to work correctly
chrpath -d %{buildroot}%{_libdir}/libSDL.so

#multiarch
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/sdl-config

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{lib_name}
%defattr(-,root,root)
%doc README-SDL.txt COPYING CREDITS BUGS
%{_libdir}/libSDL-%{lib_major}.so.*
%if %{build_plugins}
%dir %{_libdir}/SDL
%endif

%if %{build_plugins}
%if %{build_ggi}
%files -n %{lib_name}-video-ggi
%defattr(-,root,root)
%{_libdir}/SDL/video_ggi.*
%endif

%if %{build_directfb}
%files -n %{lib_name}-video-directfb
%defattr(-,root,root)
%{_libdir}/SDL/video_directfb.*
%endif
%endif

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc README README-SDL.txt COPYING CREDITS BUGS WhatsNew docs.html
%doc docs/html/*.html
%{_bindir}/sdl-config
%multiarch %{multiarch_bindir}/sdl-config
%{_libdir}/pkgconfig/sdl.pc
%{_libdir}/*a
%{_libdir}/*.so
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_datadir}/aclocal/*
%{_mandir}/*/*


