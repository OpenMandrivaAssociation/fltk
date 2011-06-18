Name: fltk
Version: 1.3.0
Release: %mkrel 1
Group: System/Libraries
Summary: Fast Light Tool Kit (FLTK)
License: LGPLv2+
Source: ftp://ftp.easysw.com/pub/fltk/%{version}/%{name}-%{version}-source.tar.gz
Patch0: fltk-1.3.0-link.patch
URL: http://www.fltk.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libx11-devel
BuildRequires: libxinerama-devel
BuildRequires: mesagl-devel
BuildRequires: jpeg-devel
BuildRequires: png-devel
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel
BuildRequires: libxft-devel
BuildRequires: man
BuildRequires: cmake

%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

#---------------------------------------------------------------------------

%define lib_major 1.3
%define libname %mklibname %{name} %lib_major

%package -n %{libname}
Summary: Fast Light Tool Kit (FLTK) - main library
Group: System/Libraries
Obsoletes: %{name} < %{version}-%{release}
Provides: %{name} = %{version}-%{release}

%description -n	%{libname}
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libfltk*.so.*

#---------------------------------------------------------------------------

%define develname	%mklibname %name -d

%package -n	%{develname}
Summary: Fast Light Tool Kit (FLTK) - development environment
Group: Development/C
Requires: %{libname} = %{version}
Obsoletes: %{name}-devel < %{version}-%{release}
Obsoletes: %{_lib}%{name}1.1-devel
Provides: %{name}-devel = %{version}-%{release}

%description -n	%{develname}
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

Install libfltk1-devel if you need to develop FLTK applications.  You'll
need to install the libfltk1.1 package if you plan to run dynamically 
linked applications.

%files -n %{develname}
%defattr(-,root,root)
%doc README CHANGES
%{_includedir}/F?
%{_bindir}/*
%{multiarch_bindir}/fltk-config
%{_mandir}/man?/*
%{_libdir}/libfltk*.so
%{_libdir}/libfltk*.a
%dir %{_libdir}/FLTK-%{lib_major}
%{_libdir}/FLTK-%{lib_major}/*

#---------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0

%build
%define Werror_cflags %{nil}
%cmake \
    -DOPTION_BUILD_SHARED_LIBS=ON \
    -DOPTION_CAIRO=ON \
    -DOPTION_CAIROEXT=ON \
    -DOPTION_PREFIX_MAN=%{_mandir} \
    -DOPTION_PREFIX_LIB=%{_libdir} \
    -DOPTION_BUILD_EXAMPLES=OFF \
    -DOPTION_PREFIX_CONFIG=%{_libdir}/FLTK-%{lib_major} \
    -DFLTK_USE_SYSTEM_ZLIB=ON \
    -DFLTK_USE_SYSTEM_JPEG=ON \
    -DFLTK_USE_SYSTEM_PNG=ON \
    -DBUILD_EXAMPLES=OFF
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std -C build

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/fltk-config

%clean
rm -rf $RPM_BUILD_ROOT

