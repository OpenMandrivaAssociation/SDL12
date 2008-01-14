%define	fname	SDL
%define	name	SDL12
%define	version	1.2.13
%define rel	2
%define	lib_name_orig	lib%{fname}
%define apiver 1.2
%define	major 0
%define	libname	%mklibname %{fname} %{apiver} %{major}
%define develname %mklibname %{fname} -d

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
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.libsdl.org/
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
Patch51:	SDL-1.2.13-preferpulsealsa.patch
Patch52:	SDL-1.2.12-pagesize.patch
Patch53:	SDL-1.2.12-disable_yasm.patch
Patch54:	SDL-1.2.11-dont-propagate-lpthread.patch
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

%package -n %{libname}-video-ggi
Summary:	GGI video support for SDL
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-video-ggi
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

This package provides GGI video support as a plugin to SDL.

%package -n %{libname}-video-directfb
Summary:	DirectFB video support for SDL
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-video-directfb
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

This package provides DirectFB video support as a plugin to SDL.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{lib_name_orig} = %{version}-%{release}
Obsoletes:	SDL
Provides:	SDL
Obsoletes:	%mklibname SDL 1.2
Provides:	%mklibname SDL 1.2

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	libalsa-devel >= 0.9.0
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	SDL-devel
Provides:	SDL%{apiver}-devel
Obsoletes:	%mklibname SDL 1.2 -d
Provides:	%mklibname SDL 1.2 -d

%description -n %{develname}
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
rm -rf %{buildroot}
%makeinstall_std

# remove unpackaged files
%if %{build_plugins}
rm -f %{buildroot}%{_libdir}/SDL/*.a
%endif

# --disable-rpath does not seem to work correctly
chrpath -d %{buildroot}%{_libdir}/libSDL.so

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/sdl-config

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README-SDL.txt CREDITS BUGS
%{_libdir}/libSDL-%{apiver}.so.%{major}*
%if %{build_plugins}
%dir %{_libdir}/SDL
%endif

%if %{build_plugins}

%if %{build_ggi}
%files -n %{libname}-video-ggi
%defattr(-,root,root)
%{_libdir}/SDL/video_ggi.*
%endif

%if %{build_directfb}
%files -n %{libname}-video-directfb
%defattr(-,root,root)
%{_libdir}/SDL/video_directfb.*
%endif
%endif

%files -n %{develname}
%defattr(-,root,root)
%doc README README-SDL.txt CREDITS BUGS WhatsNew docs.html
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
