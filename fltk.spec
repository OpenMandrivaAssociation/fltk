%define major	1.3
%define soname	0
%define libname 	%mklibname %{name} %{soname}
%define	libforms	%mklibname %{name}_forms %{soname}
%define	libgl		%mklibname %{name}_gl %{soname}
%define	libimages	%mklibname %{name}_images %{soname}
%define devname		%mklibname %{name} -d

Summary:	Fast Light Tool Kit (FLTK)
Name:		fltk
Version:	1.3.2
Release:	7
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.fltk.org
Source0:	ftp://ftp.easysw.com/pub/fltk/%{version}/%{name}-%{version}-source.tar.gz
Patch0:		fltk-1.3.0-link.patch

BuildRequires:	cmake
BuildRequires:	man
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)

%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

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

%package -n %{libforms}
Summary:	Fast Light Tool Kit (FLTK) - library
Group:		System/Libraries
Conflicts:	%{_lib}fltk0 < 1.3.2-1

%description -n	%{libforms}
This package contains a shared library for %{name}.

%package -n %{libgl}
Summary:	Fast Light Tool Kit (FLTK) - library
Group:		System/Libraries
Conflicts:	%{_lib}fltk0 < 1.3.2-1

%description -n	%{libgl}
This package contains a shared library for %{name}.

%package -n %{libimages}
Summary:	Fast Light Tool Kit (FLTK) - library
Group:		System/Libraries
Conflicts:	%{_lib}fltk0 < 1.3.2-1

%description -n	%{libimages}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Fast Light Tool Kit (FLTK) - development environment
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{libforms} = %{version}-%{release}
Requires:	%{libgl} = %{version}-%{release}
Requires:	%{libimages} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Install libfltk1-devel if you need to develop FLTK applications.  You'll
need to install the libfltk1.1 package if you plan to run dynamically 
linked applications.

%prep
%setup -q
%apply_patches

%build
%define Werror_cflags %{nil}
%cmake \
	-DOPTION_BUILD_SHARED_LIBS=ON \
	-DOPTION_CAIRO=ON \
	-DOPTION_CAIROEXT=ON \
	-DOPTION_PREFIX_MAN=%{_mandir} \
	-DOPTION_PREFIX_LIB=%{_libdir} \
	-DOPTION_BUILD_EXAMPLES=OFF \
	-DOPTION_PREFIX_CONFIG=%{_libdir}/FLTK-%{major} \
	-DFLTK_USE_SYSTEM_ZLIB=ON \
	-DFLTK_USE_SYSTEM_JPEG=ON \
	-DFLTK_USE_SYSTEM_PNG=ON \
	-DBUILD_EXAMPLES=OFF
%make

%install
%makeinstall_std -C build

%multiarch_binaries %{buildroot}%{_bindir}/fltk-config

%files -n %{libname}
%{_libdir}/libfltk.so.%{soname}
%{_libdir}/libfltk.so.%{major}

%files -n %{libforms}
%{_libdir}/libfltk_forms.so.%{soname}
%{_libdir}/libfltk_forms.so.%{major}

%files -n %{libgl}
%{_libdir}/libfltk_gl.so.%{soname}
%{_libdir}/libfltk_gl.so.%{major}

%files -n %{libimages}
%{_libdir}/libfltk_images.so.%{soname}
%{_libdir}/libfltk_images.so.%{major}

%files -n %{devname}
%doc README CHANGES
%{_includedir}/F?
%{_bindir}/fltk-config
%{_bindir}/fluid
%{multiarch_bindir}/fltk-config
%{_mandir}/man?/*
%{_libdir}/libfltk*.so
%{_libdir}/libfltk*.a
%dir %{_libdir}/FLTK-%{major}
%{_libdir}/FLTK-%{major}/*

