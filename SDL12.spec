%define	fname	SDL
%define	api	1.2
%define	major	0
%define	libname	%mklibname %{fname} %{api} %{major}
%define	devname	%mklibname %{fname} -d
%define _disable_lto 1

%define	build_plugins	0
%define	build_directfb	0
%define	build_ggi	0
%define	build_aalib	1

Summary:	Simple DirectMedia Layer
Name:		SDL12
Version:	1.2.70
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/libsdl-org/sdl12-compat
Source0:	https://github.com/libsdl-org/sdl12-compat/archive/refs/tags/release-%{version}.tar.gz

BuildRequires:	chrpath
%ifnarch %{riscv}
BuildRequires:	nas-devel
%endif
BuildRequires:	pkgconfig(sdl2)
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
BuildSystem:	cmake

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

%install -a
# For better compatibility with "real" SDL1
ln -s sdl12_compat.pc %{buildroot}%{_libdir}/pkgconfig/sdl.pc

%files -n %{libname}
%{_libdir}/libSDL-%{api}.so.*
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
%{_bindir}/sdl-config
%{_libdir}/pkgconfig/sdl12_compat.pc
%{_libdir}/pkgconfig/sdl.pc
%{_libdir}/*.so
%{_libdir}/libSDLmain.a
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_datadir}/aclocal/*
