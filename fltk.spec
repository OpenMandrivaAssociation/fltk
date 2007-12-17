%define	name		fltk
%define	lib_name	lib%{name}
%define	version		1.1.8
%define pre		5940
%if %pre
%define	release		%mkrel 0.%pre.1
%else
%define release		%mkrel 1
%endif
%define	lib_major	1.1
%define	libname		%mklibname %{name} %lib_major
%define develname	%mklibname %name -d

%define debug_package          %{nil}

Summary:	Fast Light Tool Kit (FLTK)
Name:		fltk
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	LGPLv2+
%if %pre
Source:		ftp://ftp.easysw.com/pub/fltk/snapshots/%{name}-1.1.x-r%{pre}.tar.bz2
%else
Source:		ftp://ftp.easysw.com/pub/fltk/%{version}/%{name}-%{version}-source.tar.bz2
%endif
Patch1:		fltk-1.1.7-cmake-libdir.patch
URL:		http://www.fltk.org
BuildRequires:	X11-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	man
BuildRequires:	cmake

%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

%package -n	%{libname}
Summary:	Fast Light Tool Kit (FLTK) - main library
Group:		System/Libraries
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

%package -n	%{develname}
Summary:	Fast Light Tool Kit (FLTK) - development environment
Group:		Development/C
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	%{_lib}%{name}1.1-devel
Provides:	%{name}-devel = %{version}-%{release}, %{lib_name}-devel = %{version}-%{release}

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

%prep
%if %pre
%setup -q -n %{name}-1.1.x-r%{pre}
%else
%setup -q
%endif
%patch1

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_OPT_FLAGS" ./configure \
       --prefix=%{_prefix} --libdir=%{_libdir} --enable-shared --enable-threads
# need to pass CXX=... here else it is always gcc instead of g++ (fpons)
%make
#CXX="g++"

# only run cmake, don't use it to build and install: the result is less conplete than the
# configure version
mkdir cmake
pushd cmake
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_CXX_COMPILER:PATH=%{_bindir}/c++ \
      -DCMAKE_C_COMPILER:PATH=%{_bindir}/gcc \
      -DBUILD_SHARED_LIBS:BOOL=ON \
      -DCMAKE_BUILD_TYPE:STRING=Release \
      -DFLTK_USE_SYSTEM_JPEG:BOOL=ON \
      -DFLTK_USE_SYSTEM_PNG:BOOL=ON \
      -DFLTK_USE_SYSTEM_ZLIB:BOOL=ON \
      -DUSE_OPENGL:BOOL=ON \
      -DCMAKE_SKIP_RPATH:BOOL=ON \
      -DLIB_DIR:STRING=%{_lib} \
..
popd


%install
rm -rf $RPM_BUILD_ROOT

# Makefile hack for 64bitness - from Fedora
%if "%{_lib}" != "lib"
mkdir -p $RPM_BUILD_ROOT%{_libdir}
pushd $RPM_BUILD_ROOT%{_libdir}/..
ln -s %{_lib} lib
popd
%endif

%makeinstall
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/doc/%{libname}-devel
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/cat*

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/fltk-config

# install cmake files by hand - fltk is not configured with cmake
mkdir -p $RPM_BUILD_ROOT%{_libdir}/FLTK-%{lib_major}
cp CMake/FLTKUse.cmake $RPM_BUILD_ROOT%{_libdir}/FLTK-%{lib_major}
cp cmake/FLTKBuildSettings.cmake $RPM_BUILD_ROOT%{_libdir}/FLTK-%{lib_major}
cp cmake/FLTKLibraryDepends.cmake $RPM_BUILD_ROOT%{_libdir}/FLTK-%{lib_major}
cp cmake/CMake/FLTKConfig.cmake $RPM_BUILD_ROOT%{_libdir}/FLTK-%{lib_major}

# clean up after hack
%if "%{_lib}" != "lib"
rm -f $RPM_BUILD_ROOT/%{_libdir}/../lib
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libfltk*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc README CHANGES
%docdir %{_datadir}/doc/%{libname}-devel
%{_datadir}/doc/%{libname}-devel
%{_includedir}/F?
%{_bindir}/*
%{_libdir}/libfltk*.so
%{_libdir}/libfltk*.a
%dir %{_libdir}/FLTK-%{lib_major}
%{_libdir}/FLTK-%{lib_major}/*.cmake
%doc %{_mandir}/man1/* 
%doc %{_mandir}/man3/* 

