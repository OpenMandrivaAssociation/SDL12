%define	fname	SDL

%define	build_plugins	0
%define	build_directfb	1
%define	build_ggi	1
%define	build_aalib	1

Summary:	Simple DirectMedia Layer
Name:		SDL12
Version:	1.2.15
Release:	4
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
# needs to be updated or dropped
Patch104:	221_check_SDL_NOKBD_environment_variable.diff
Patch107:	310_fixmouseclicks

# libGL is required to enable glx support
BuildRequires:	pkgconfig(glu)
BuildRequires:	nas-devel
BuildRequires:	chrpath
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	zlib-devel
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
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
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
##patch104 -p1
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
%{_libdir}/*.a
%{_libdir}/*.so
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_datadir}/aclocal/*
%{_mandir}/*/*


%changelog
* Mon May 14 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.15-3
+ Revision: 798687
- rebuild for new directfb-1.5.3

* Tue Apr 03 2012 Andrey Bondrov <abondrov@mandriva.org> 1.2.15-2
+ Revision: 788966
- Bump release, update BuildRequires to fix x86_64 build
- Disable patch 104 for now
- New version 1.2.15, drop no longer needed patches, update patch 104

* Mon Mar 12 2012 Andrey Bondrov <abondrov@mandriva.org> 1.2.14-12
+ Revision: 784396
- Use pkgconfig(alsa) instead of alsa-lib-devel (no longer provided by alsa devel package)
- Require alsa-lib-devel instead of libalsa-devel

* Wed Dec 28 2011 Andrey Bondrov <abondrov@mandriva.org> 1.2.14-11
+ Revision: 745920
- Rebuild for .la files issue

  + Zé <ze@mandriva.org>
    -clean virtual provides from lib package
    - fix provides to include versioning

* Wed Jul 13 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.2.14-9
+ Revision: 689925
- add -funroll-loops to compile flags
- fix crash when trying to exit because of an xio-error (rhbz#603984, sdlbz#1009)
- remove dead configure options
- Adapt to nasm-2.09 (rhbz#678818)
- Do not call memcpy() on overlapping areas (rhbz#669844)
- disable esound support as it's now deprecated

* Thu May 26 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.2.14-8
+ Revision: 679195
- removed non std unicode space characted

* Wed Apr 27 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.2.14-7
+ Revision: 659651
- bump

* Wed Apr 27 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.2.14-6
+ Revision: 659527
- compile with -ffast-math
- build with --enable-assembly
- build nas as shared
- enable assembly instructions on x86_64 as well
- cleanups
- sync in various patches from debian

* Tue Apr 19 2011 Antoine Ginies <aginies@mandriva.com> 1.2.14-4
+ Revision: 655991
- fix bug in wesnoth windowed mode

* Fri Dec 17 2010 Funda Wang <fwang@mandriva.org> 1.2.14-3mdv2011.0
+ Revision: 622441
- rebuild for new directfb

* Sat Dec 04 2010 Tomas Kindl <supp@mandriva.org> 1.2.14-2mdv2011.0
+ Revision: 609502
- rebuild
- fix encoding of 'CREDITS' file

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 1.2.14-1mdv2010.1
+ Revision: 462998
- New version 1.2.14
- New version 1.2.14

* Sat Apr 11 2009 Michael Scherer <misc@mandriva.org> 1.2.13-13mdv2009.1
+ Revision: 366227
- add a RH patch to fix mdv bug #45721, patch from rh 484362
  ( found from  https://bugzilla.redhat.com/show_bug.cgi?id=484121 )

* Mon Mar 02 2009 Anssi Hannula <anssi@mandriva.org> 1.2.13-12mdv2009.1
+ Revision: 347292
- buildrequires on libalsa-devel and libxrandr-devel
- use yasm instead of nasm as it is preferred by configure and no longer
  breaks build (drop disable_yasm.patch)

* Mon Feb 09 2009 Helio Chissini de Castro <helio@mandriva.com> 1.2.13-11mdv2009.1
+ Revision: 338954
- Adios arts...

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - ditch --enable-arts*
    - ditch arts-devel buildrequires

* Wed Aug 20 2008 Colin Guthrie <cguthrie@mandriva.org> 1.2.13-10mdv2009.0
+ Revision: 274289
- Update spec to not include package descriptions for packages that will not be built (rpmlint)
- Update pulseaudio buffering patch as recommended by Lennart Pottering
- Prefer pulseaudio output over ESD and ALSA

* Sun Aug 17 2008 Funda Wang <fwang@mandriva.org> 1.2.13-9mdv2009.0
+ Revision: 272979
- rebuild for new dfb

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 26 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2.13-8mdv2008.1
+ Revision: 190355
- Update patch51 to favor esd backend instead of pulse one, until it is fixed (Mdv bug #37235)

* Tue Mar 11 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2.13-7mdv2008.1
+ Revision: 186644
- Patch57: fix crash in pulseaudio backend when /proc is not mounted (Mdv bug #38220)

* Thu Mar 06 2008 Colin Guthrie <cguthrie@mandriva.org> 1.2.13-6mdv2008.1
+ Revision: 180259
- Second attempt to fix pulse buffering issues (mdv#37235)

* Tue Mar 04 2008 Colin Guthrie <cguthrie@mandriva.org> 1.2.13-5mdv2008.1
+ Revision: 179233
- Use default buffering for pulseaudio output (mdv#37235)

* Wed Feb 06 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2.13-4mdv2008.1
+ Revision: 163109
- Patch55 (Fedora): fix pulseaudio backend, no longer dynamic linked, use dlopen instead

* Tue Feb 05 2008 Anssi Hannula <anssi@mandriva.org> 1.2.13-3mdv2008.1
+ Revision: 162646
- devel package requires mesaglu-devel and mesagl-devel

* Mon Jan 14 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2.13-2mdv2008.1
+ Revision: 151334
- Update patch51 to favor PulseAudio (when running) over Alsa (Mdv bug #36768)

* Sat Jan 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.13-1mdv2008.1
+ Revision: 149210
- new license policy
- new devel policy
- correct libification, add apiver which on this case is 1.2, major is 0
- spec file clean
- do not package COPYING file
- drop disabled patches, as they are not needed
- also drop patches 2, 35 and 44
- regenerate patches 4 and 53
- do not hardcode buildrequires on automake1.9
- run autogen.sh
- new version
- enable PulseAudio support

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jul 26 2007 Funda Wang <fwang@mandriva.org> 1.2.12-1mdv2008.0
+ Revision: 55747
- Redif patch51, patch52
- New version

* Mon May 21 2007 Funda Wang <fwang@mandriva.org> 1.2.11-8mdv2008.0
+ Revision: 29100
- Rebuuild against directfb 1.0.0


* Sun Feb 18 2007 Anssi Hannula <anssi@mandriva.org> 1.2.11-7mdv2007.0
+ Revision: 122613
- ggi and directfb can now be enabled again

* Sun Feb 18 2007 Anssi Hannula <anssi@mandriva.org> 1.2.11-6mdv2007.1
+ Revision: 122548
- build without directfb and ggi until they will be rebuilt
- rebuild for new libgii
- buildrequire chrpath for rpath removal
- disable rpath
- add missing buildrequires

  + Olivier Blin <oblin@mandriva.com>
    - Import SDL12

* Tue Aug 22 2006 Guillaume Bedot <littletux@mandriva.org> 1.2.11-3mdv2007.0
- fix for #24005

* Wed Jul 26 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.2.11-2
- add BuildRequires: libmesaglu-devel

* Sat Jul 22 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.11-1mdv2007.0
- 1.2.11
- use nasm, not yasm as it will fail to build (P53 from debian)
- Do not propagate -lpthread to sdl-config --libs (P54 from debian)
- Removed ugly stuff from acinclude.m4 (P55 from debian)
- drop P37 (merged upstream)
- fix macro-in-%%changelog

* Sun Jun 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.10-1mdv2007.0
- New release 1.2.10
- enable aalib support
- regenerate P0, P1, P2, P21, P31,
- sync P35, P37, P39, P40 with debian	
- drop P4, P7, P10, P22, P30, P32, P34, P36 & P41 (fixed upstream)
- fix nas detection (P44 from debian)
- fix problem with little/big endian (P50 from fedora)
- prefer alsa, arts and esd too before oss (P51 from fedora)
- new pagesize patch (drop PAGE_SIZE, use sysconf(_SC_PAGESIZE) instead (P52 from fedora)

* Thu May 11 2006 Götz Waschk <waschk@mandriva.org> 1.2.9-5mdk
- update patch 4 for new SDL

* Thu Apr 20 2006 Stefan van der Eijk <stefan@eijk.nu> 1.2.9-4mdk
- BuildRequires:	automake1.8

* Wed Apr 19 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.9-3mdk
- remove redundant requires (fixes #22048)
- patches from our nice friends @ debian (with debian bugzilla references):
	o Patch courtesy of Jochen Voss to fix lookup of keys using eg. the
	  AltGr modifier (Closes: #299864) (P30)
	o Patch courtesy of Bas Wijnen to generate release events for lock keys
	  (Caps Lock and Num Lock) just like normal keys (Closes: #317010). (P31)
	o Arrow keys and the numeric keypad conflict in the aalib driver, make the
	  former take precedence (Closes: #170548). (P32)
	o Fix a crash when aa_getevent returns a scancode value bigger than 400. (P32)
	o When both are available, try the ALSA output driver before the OSS one. (P33)
	o New patch: "dst_w == last.src_w" should be "dst_w == last.dst_w" in
	  src/video/SDL_stretch.c. (P34)
	o SDL_stretch.c: use mprotect() on the pages storing dynamically generated
	  code so that we still work on systems that enforce W^X. (P35)
	o Add ".note.GNU-stack" sections to all NASM files so that gcc does not
	  think these files need an executable stack. (P36)
	o Add PIC support to the Hermes assembly files, one step closer to a fully
	  PIC compliant libSDL. (P37)
	o New patch: ConvertMMXpII32_24RGB888 was not used anywhere, yet it is
	  fully functional. This patch activates it. (P38)
	o Do not strip -DPIC from the NASM compilation flags. They are useful. (P39)
	o Improved cleaning up in autogen.sh and activated AM_MAINTAINER_MODE. (P40)
	o New patch: add -I$(srcdir)/ to the NASM flags so that we can include
	  common files. (P41)
	o Fixed PPC fullscreen vidmode problem (Closes: 285729). (P42)

* Wed Nov 09 2005 Götz Waschk <waschk@mandriva.org> 1.2.9-2mdk
- patch for new DirectFB

* Sun Oct 09 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.9-1mdk
- 1.2.9
- drop x86_64 patch (P3, merged upstream)
- fix build with gcc 4 (P22 from SDL CVS)
- clean out old junk from %%build
- %%mkrel

* Tue Aug 16 2005 Götz Waschk <waschk@mandriva.org> 1.2.8-5mdk
- Rebuild

* Mon Aug 01 2005 Guillaume Bedot <littletux@mandriva.org> 1.2.8-4mdk
- rebuild
- Patch20: allows build with gcc4 (from fedora)
- Patch21: should fix anonymous enum problem with armagetron. (from debian)

* Thu Feb 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.8-3mdk
- libtool fixes to nuke lib64 rpaths
- fix build on x86_64, drop rdtsc() part which is obsolete

* Tue Feb 01 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.8-2mdk
- multiarch
- compile with -O3

* Tue Dec 21 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.8-1mdk
- 1.2.8
- regenerate P2 & P3
- drop P8 & P9 (fixed upstream)

* Wed Sep 29 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.7-9mdk
- forgot to regenerate a fixed patch

* Wed Sep 29 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.7-8mdk
- build ggi and directfb support as a plugin on MDK >= 10.1

* Wed Sep 01 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.7-7mdk
- update patch 9 from SDL cvs

* Fri Jul 30 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.2.7-6mdk
- Merged Gwenole 64bit fixes from 1.2.7-2.1mdk: cputoolize.

* Sat Jun 12 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.7-5mdk
- patch to make it build with gcc 3.4

* Mon Apr 19 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.7-4mdk
- fix joystick bug (P8, fixes #9432)

* Fri Apr 16 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.7-3mdk
- enable directfb and ggi support

* Tue Mar 02 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.7-2mdk
- fix buildrequires

* Thu Feb 26 2004 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.7-1mdk
- new version (fix for #8371 at least) (debian and CVS stuff added by
  Per Oyvind merged upstream)

