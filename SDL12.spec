%define	fname	SDL
%define	api	1.2
%define	major	0
%define	libname	%mklibname %{fname} %{api} %{major}
%define	devname	%mklibname %{fname} -d

%define	build_plugins	0
%define	build_directfb	1
%define	build_ggi	0
%define	build_aalib	1

Summary:	Simple DirectMedia Layer
Name:		SDL12
Version:	1.2.15
Release:	18
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.libsdl.org/
Source0:	http://www.libsdl.org/release/%{fname}-%{version}.tar.gz
Patch0:		SDL-1.2.10-fixrpath.patch
Patch1:		SDL-1.2.14-anonymous-enums.patch
# (cg) 1.2.13-10mdv Use pulse output by default
Patch2:		SDL-1.2.14-dont-propagate-lpthread.patch
# (fc) 1.2.13-7mdv fix crash in pulseaudio backend when /proc is not mounted (Mdv bug #38220)
Patch3:		SDL-1.2.14-noproc.patch
# (misc) patch from fedora to solve ri-li crash ( mdv bug #45721 )
Patch4:		SDL-1.2.13-rh484362.patch 
# (MD) from fedora
Patch5:		SDL-1.2.15-const_XData32.patch

# debian patches
Patch102:	060_disable_ipod.diff
Patch103:	205_x11_keysym_fix.diff
# needs to be updated or dropped
#Patch104:	221_check_SDL_NOKBD_environment_variable.diff
Patch107:	310_fixmouseclicks

BuildRequires:	chrpath
BuildRequires:	nas-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(zlib)
%ifarch %{ix86}
BuildRequires:	yasm
%endif
%if %{build_plugins}
BuildRequires:	libltdl-devel
%endif
%if %{build_directfb}
BuildRequires:	pkgconfig(directfb)
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

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
%rename		%{fname}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

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
%setup -qn %{fname}-%{version}
%apply_patches

iconv -f ISO-8859-1 -t UTF-8 CREDITS > CREDITS.tmp
touch -r CREDITS CREDITS.tmp
mv CREDITS.tmp CREDITS

./autogen.sh

%build
export CFLAGS="%{optflags} -fPIC -funroll-loops -ffast-math -O3"
export CXXFLAGS="$CFLAGS"
%configure \
	--enable-video-opengl \
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
	--program-prefix=

%make

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/*.a

# --disable-rpath does not seem to work correctly
chrpath -d %{buildroot}%{_libdir}/libSDL.so

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/sdl-config

%files -n %{libname}
%doc README-SDL.txt CREDITS BUGS
%{_libdir}/libSDL-%{api}.so.%{major}*
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
%{_libdir}/*.so
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_datadir}/aclocal/*
%{_mandir}/*/*

