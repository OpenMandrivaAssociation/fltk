%define _disable_ld_no_undefined 1

%define major	%(echo %{version} |cut -d. -f1)
%define minor	%(echo %{version} |cut -d. -f2)
%define micro	%(echo %{version} |cut -d. -f3)

%define oldlibname %mklibname %{name} 1.3
%define libname %mklibname %{name}
%define devname	%mklibname %{name} -d

# enable/disable cairo support
%bcond_without	cairo
%bcond_without	cairoext

# enable/disable static libraries
%bcond_without	static_lib

Name:		fltk
Version:	1.4.3
Release:	1
Group:		System/Libraries
Summary:	Fast Light Tool Kit (FLTK)
License:	LGPLv2+
URL:		https://www.fltk.org
Source0:	https://github.com/fltk/fltk/releases/download/release-%{version}/fltk-%{version}-source.tar.bz2

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(libdecor-0)
BuildRequires:	jpeg-devel
BuildRequires:	man

BuildConflicts: fltk-devel

%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

#---------------------------------------------------------------------------

%package fluid
Summary:	Fast Light User-Interface Designer (FLUID)
Group:		System/Libraries
Requires:	%{devname} = %{version}

%description fluid
FLUID allows you to develop complex applications with %{name} quickly. You
can build complete applications within FLUID, drawing your user-interface and
creating functions, classes, and variables as needed.

FLUID creates C++ source and header files that can be compiled by themselves
or included as part of a larger project.-interface.

%files fluid
%{_bindir}/fluid
%{_datadir}/mime/packages/fluid.xml
%{_datadir}/applications/fluid.desktop
%{_iconsdir}/hicolor/*/apps/fluid.png
%{_mandir}/man1/fluid.1*
%doc COPYING

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Fast Light Tool Kit (FLTK) - main library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
%rename %{oldlibname}

%description -n	%{libname}
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

%files -n %{libname}
%{_libdir}/libfltk.so.%{major}.%{minor}*
%{_libdir}/libfltk_cairo.so.%{major}.%{minor}*
%{_libdir}/libfltk_forms.so.%{major}.%{minor}*
%{_libdir}/libfltk_gl.so.%{major}.%{minor}*
%{_libdir}/libfltk_images.so.%{major}.%{minor}*
%doc COPYING

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Fast Light Tool Kit (FLTK) - development environment
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	pkgconfig(xext)
Requires:	pkgconfig(xinerama)
Requires:	pkgconfig(xfixes)
Requires:	pkgconfig(xcursor)
Requires:	pkgconfig(xft)
Requires:	pkgconfig(xrender)
Requires:	pkgconfig(cairo)
Requires:	pkgconfig(pango)
Requires:	pkgconfig(pangocairo)
Requires:	pkgconfig(pangoxft)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(fontconfig)
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(x11)
Requires:	pkgconfig(libdecor-0)

%description -n	%{devname}
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

Install libfltk1-devel if you need to develop FLTK applications. You'll
need to install the libfltk1.1 package if you plan to run dynamically 
linked applications.

%files -n %{devname}
%doc ANNOUNCEMENT
%dir %{_includedir}/FL
%{_includedir}/FL/*
%{_bindir}/fltk-config
%{_bindir}/fltk-options
%{_datadir}/applications/fltk-options.desktop
%{_datadir}/icons/hicolor/*/apps/fltk-options.*
%{_datadir}/mime/packages/fltk-options.xml
%{_libdir}/libfltk.so
%{_libdir}/libfltk_cairo.so
%{_libdir}/libfltk_forms.so
%{_libdir}/libfltk_gl.so
%{_libdir}/libfltk_images.so
%if %{with static_lib}
%{_libdir}/libfltk.a
%{_libdir}/libfltk_cairo.a
%{_libdir}/libfltk_forms.a
%{_libdir}/libfltk_gl.a
%{_libdir}/libfltk_images.a
%endif
%{_mandir}/man1/fltk-config.1*
%{_mandir}/man1/fltk-options.1*
%{_mandir}/man3/fltk.3*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
%doc COPYING

#---------------------------------------------------------------------------
%package examples
Summary:	Example applications for the FLTK toolkit
Group:		Development/Tools

%description examples
Example applications for the FLTK toolkit

%files examples
%{_bindir}/blocks
%{_bindir}/checkers
%{_bindir}/glpuzzle
%{_bindir}/sudoku
%{_mandir}/man6/blocks.6*
%{_mandir}/man6/checkers.6*
%{_mandir}/man6/glpuzzle.6*
%{_mandir}/man6/sudoku.6*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# remove bundled libraries
rm -fr png jpeg zlib

# Fix check for a define that isn't set anywhere
sed -i -e 's,FLTK_USE_STDXX,FLTK_USE_STD,' src/Fl_Table.cxx

export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
%cmake -G Ninja \
	-DFLTK_BUILD_TEST:BOOL=ON \
	-DFLTK_BUILD_EXAMPLES:BOOL=ON \
	-DFLTK_BUILD_SHARED_LIBS:BOOL=ON \
%if %{with cairo}
	-DFLTK_OPTION_CAIRO_WINDOW:BOOL=ON \
%if %{with cairoext}
	-DFLTK_OPTION_CAIRO_EXT:BOOL=ON \
%endif
%endif
	-DFLTK_OPTION_STD:BOOL=ON \
	-DFLTK_USE_LIBDECOR_GTK:BOOL=OFF \
	-DFLTK_USE_GL:BOOL=ON \
	-DFLTK_USE_SVG:BOOL=ON \
	-DFLTK_USE_THREADS:BOOL=ON \
	-DFLTK_USE_XCURSOR:BOOL=ON \
	-DFLTK_USE_XDBE:BOOL=ON \
	-DFLTK_USE_XFIXES:BOOL=ON \
	-DFLTK_USE_XFT:BOOL=ON \
	-DFLTK_USE_XINERAMA:BOOL=ON \
	-DFLTK_USE_XRENDER:BOOL=ON \
	-DFLTK_USE_SYSTEM_LIBJPEG:BOOL=ON \
	-DFLTK_USE_SYSTEM_LIBPNG:BOOL=ON \
	-DFLTK_USE_SYSTEM_ZLIB:BOOL=ON \
	-DFLTK_USE_SYSTEM_LIBDECOR:BOOL=ON \
	%{nil}

%build

%ninja_build -C build

%install
%ninja_install -C build

# remove spurious includes
find %{buildroot}%{_includedir} -type f -not -iname \*h -delete

%if %{without static_lib}
# remove static lib
find %{buildroot}%{_libdir} -type f -name \*a -delete
%endif

# No need for the statically linked binaries
mv -f %{buildroot}%{_bindir}/fluid-shared %{buildroot}%{_bindir}/fluid
mv -f %{buildroot}%{_bindir}/fltk-options-shared %{buildroot}%{_bindir}/fltk-options

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/fluid.desktop
