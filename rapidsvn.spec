%define	major 1
%define libname	%mklibname svncpp %{major}
%define oldlibname %mklibname rapidsvn 0
%define develname %mklibname svncpp -d

Summary:	A cross-platform GUI for the Subversion concurrent versioning system
Name:		rapidsvn
Version:	0.10.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Development/Other
URL:		http://rapidsvn.tigris.org
Source0:	http://www.rapidsvn.org/download/%{name}-%{version}.tar.gz
Source1:	rapidsvn_logo.png
Patch1:		rapidsvn-linkage_fix.diff
Patch2:		rapidsvn-0.9.6-format_not_a_string_literal_and_no_format_arguments.patch
BuildRequires:	apache-devel >= 2.0.54
BuildRequires:	doxygen
BuildRequires:	subversion-devel >= 1.2
BuildRequires:	subversion >= 1.2
BuildRequires:	libtool >= 1.4.2
BuildRequires:	wxGTK2.8-devel
BuildRequires:	libxslt-proc
BuildRequires:	db4.7-devel
BuildRequires:	docbook-style-xsl
#BuildRequires:	neon0.26-devel >= 0.26.4
BuildRequires:	imagemagick
BuildRequires:	libcppunit-devel
Requires(post):	%{libname} = %{version}-%{release}
Requires(preun): %{libname} = %{version}-%{release}
Requires:	subversion
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

%package -n %{libname}
Summary:	RapidSVN shared SvnCpp C++ API libraries
Group:		System/Libraries
Obsoletes:	%mklibname svncpp 0

%description -n %{libname}
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

This package contains shared SvnCpp C++ API libraries for
RapidSVN.

%package -n %{develname}
Summary:	RapidSVN SvnCpp C++ API development libraries
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libsvncpp-devel = %{version}-%{release}
Provides:	%{oldlibname}-devel = %{version}-%{release}
Obsoletes:	%{oldlibname}-devel
Obsoletes:	%{mklibname svncpp -d 0}

%description -n %{develname}
As part of the RapidSVN effort it became clear that it would make
the code easier to update and manage if the Subversion client C
API were wrapped in C++. This is where SvnCpp comes from. Right
now it has the following aspects of the C API have been
abstracted: authentication, logging, status, notification, and
properties. SvnCpp should provide an object-oriented programming
interface to any project that uses C++ or a SWIG-compatible
language like Python or Java. 

%prep

%setup -q
%patch1 -p1
%patch2 -p1

cp %{SOURCE1} rapidsvn_logo.png

%build
autoreconf -fis
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS=$CFLAGS

%configure2_5x \
    --enable-shared \
    --disable-static \
    --with-svn-include=%{_includedir} \
    --with-svn-lib=%{_libdir} \
    --with-xsltproc=%{_bindir}/xsltproc \
    --with-apr-config=%{_bindir}/apr-1-config \
    --with-apu-config=%{_bindir}/apu-1-config \
    --with-neon-config=/bin/true

%make

%install
%{__rm} -rf %{buildroot}

%makeinstall_std


# Mandriva Icons
install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

convert rapidsvn_logo.png -resize 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert rapidsvn_logo.png -resize 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert rapidsvn_logo.png -resize 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=RapidSVN
Comment=%{summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Development;RevisionControl;
EOF

%{__mv} doc/svncpp/html .

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc html AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/svncpp
%{_libdir}/*.so
%{_libdir}/*.la
