%define _disable_ld_no_undefined 1

%define major	1
%define minor	3
%define micro	4

%define libname %mklibname %{name} %{major}.%{minor}
%define devname	%mklibname %{name} -d

# enable/disable cairo support
%bcond_without	cairo
%bcond_without	cairoext

# enable/disable static libraries
%bcond_without	static_lib

Name:		fltk
Version:	%{major}.%{minor}.%{micro}
Release:	4
Group:		System/Libraries
Summary:	Fast Light Tool Kit (FLTK)
License:	LGPLv2+
URL:		http://www.fltk.org
Source0:	http://fltk.org/pub/fltk/%{version}/fltk-%{version}-source.tar.gz
Patch0:		%{name}-1.3.4-fix-cairo.patch
Patch1:		%{name}-1.3.4-fix-cmake-shared-libraries-suffix.patch
Patch2:		%{name}-1.3.4-fix-cmake-install-cmake-path.patch
Patch3:		%{name}-1.3.4-fix-cmake-install-example.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
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
%doc ANNOUNCEMENT CHANGES CREDITS KNOWN_BUGS.html README
%dir %{_includedir}/FL
%{_includedir}/FL/*
%{_bindir}/fltk-config
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
%{_mandir}/man3/fltk.3*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
%doc COPYING

#---------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

# remobe bundled libraries
rm -fr png jpeg zlib

%build
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
%cmake \
	-DOPTION_BUILD_SHARED_LIBS:BOOL=ON \
	-DOPTION_BUILD_EXAMPLES=OFF \
%if %{with cairo}
	-DOPTION_CAIRO:BOOL=ON \
%if %{with cairoext}
	-DOPTION_CAIROEXT:BOOL=ON \
%endif
%endif
	-DOPTION_USE_SYSTEM_LIBJPEG:BOOL=ON \
	-DOPTION_USE_SYSTEM_LIBPNG:BOOL=ON \
	-DOPTION_USE_SYSTEM_ZLIB:BOOL=ON \
	%{nil}
%make

%install
%makeinstall_std -C build

# remove spurious includes
find %{buildroot}%{_includedir} -type f -not -iname \*h -delete

%if %{without static_lib}
# remove static lib
find %{buildroot}%{_libdir} -type f -name \*a -delete
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/fluid.desktop

