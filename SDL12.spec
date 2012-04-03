%define	fname	SDL

%define	build_plugins	0
%define	build_directfb	1
%define	build_ggi	1
%define	build_aalib	1

Summary:	Simple DirectMedia Layer
Name:		SDL12
Version:	1.2.15
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.libsdl.org/
Source0:	http://www.libsdl.org/release/%{fname}-%{version}.tar.gz
Patch0:		SDL-1.2.10-fixrpath.patch
Patch21:	SDL-1.2.14-anonymous-enums.patch
# (cg) 1.2.13-10mdv Use pulse output by default
Patch54:	SDL-1.2.14-dont-propagate-lpthread.patch
# (fc) 1.2.13-7mdv fix crash in pulseaudio backend when /proc is not mounted (Mdv bug #38220)
Patch57:	SDL-1.2.14-noproc.patch
# (misc) patch from fedora to solve ri-li crash ( mdv bug #45721 )
Patch58:	SDL-1.2.13-rh484362.patch 

# debian patches
Patch102:	060_disable_ipod.diff
Patch103:	205_x11_keysym_fix.diff
Patch104:	221_check_SDL_NOKBD_environment_variable.diff
Patch107:	310_fixmouseclicks

# libGL is required to enable glx support
BuildRequires:	libmesaglu-devel
BuildRequires:	nas-devel
BuildRequires:	chrpath
BuildRequires:	libpulseaudio-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	libxrandr-devel
BuildRequires:	zlib-devel
%ifarch %{ix86}
BuildRequires:	yasm
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
# just to get multiarch fix properly
BuildRequires:	rpm >= 5.3.10-0.20110422.2

%description
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

%define	lib_name_orig	lib%{fname}
%define	apiver	1.2
%define	major	0
%define	libname	%mklibname %{fname} %{apiver} %{major}
%define	devname	%mklibname %{fname} -d

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
%rename		%{fname}
%define	libold	%mklibname %{fname} 1.2
%rename		%{libold}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	pkgconfig(alsa)
# GL/GLU referenced in headers, but is dlopened so there are no autodeps:
Requires:	mesagl-devel
Requires:	mesaglu-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{fname}-devel = %{EVRD}
Provides:	%{name}%{apiver}-devel = %{version}-%{release}
%define	libold	%mklibname SDL %{fname} -d
%rename	libold

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%if %{build_plugins}
%if %{build_ggi}
%package -n	%{libname}-video-ggi
Summary:	GGI video support for SDL
Group:		System/Libraries

%description -n	%{libname}-video-ggi
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

This package provides GGI video support as a plugin to SDL.
%endif

%if %{build_directfb}
%package -n	%{libname}-video-directfb
Summary:	DirectFB video support for SDL
Group:		System/Libraries

%description -n	%{libname}-video-directfb
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

This package provides DirectFB video support as a plugin to SDL.
%endif
%endif

%prep
%setup -q -n %{fname}-%{version}
%patch0 -p1
%patch21 -p1 -b .enums~
%patch54 -p1 -b .no_lpthread~
%patch57 -p1 -b .noproc~
%patch58 -p1 -b .disable_SDL_revcpy~

iconv -f ISO-8859-1 -t UTF-8 CREDITS > CREDITS.tmp
touch -r CREDITS CREDITS.tmp
mv CREDITS.tmp CREDITS

%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch107 -p1

%build
./autogen.sh
export CFLAGS="%{optflags} -fPIC -funroll-loops -ffast-math -O3"
export CXXFLAGS="$CFLAGS"

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
%ifarch %{ix86} x86_64
		--enable-nasm \
%else
		--disable-nasm \
%endif
		--enable-assembly \
		--enable-sdl-dlopen \
		--enable-nas \
		--enable-nas-shared \
		--enable-pulseaudio \
		--enable-pulseaudio-shared \
		--enable-alsa \
		--enable-alsa-shared \
		--disable-arts \
		--disable-esd \
		--program-prefix= \
		--disable-rpath
%make

%install
%makeinstall_std

# remove unpackaged files
%if %{build_plugins}
rm -f %{buildroot}%{_libdir}/SDL/*.a
%endif

# --disable-rpath does not seem to work correctly
chrpath -d %{buildroot}%{_libdir}/libSDL.so

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/sdl-config

%files -n %{libname}
%doc README-SDL.txt CREDITS BUGS
%{_libdir}/libSDL-%{apiver}.so.%{major}*
%if %{build_plugins}
%dir %{_libdir}/SDL
%endif

%if %{build_plugins}

%if %{build_ggi}
%files -n %{libname}-video-ggi
%{_libdir}/SDL/video_ggi.*
%endif

%if %{build_directfb}
%files -n %{libname}-video-directfb
%{_libdir}/SDL/video_directfb.*
%endif

%endif

%files -n %{devname}
%doc README README-SDL.txt CREDITS BUGS WhatsNew docs.html
%doc docs/html/*.html
%{_bindir}/sdl-config
%{multiarch_bindir}/sdl-config
%{_libdir}/pkgconfig/sdl.pc
%{_libdir}/*a
%{_libdir}/*.so
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_datadir}/aclocal/*
%{_mandir}/*/*
