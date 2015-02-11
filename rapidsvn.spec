%define	major 3
%define	libname %mklibname svncpp %{major}
%define	devname %mklibname svncpp -d

Summary:	A cross-platform GUI for the Subversion concurrent versioning system
Name:		rapidsvn
Version:	0.12.1
Release:	1
License:	GPLv2+
Group:		Development/Other
Url:		http://rapidsvn.tigris.org
Source0:	http://www.rapidsvn.org/download/release/%{version}/%{name}-%{version}.tar.gz
Source1:	rapidsvn_logo.png
# missing from build
Source2:	svncpp.dox
Patch1:		rapidsvn-0.12.0-linkage_fix.patch
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	db-devel
BuildRequires:	graphviz
BuildRequires:	imagemagick
BuildRequires:	libtool >= 1.4.2
BuildRequires:	subversion >= 1.2
BuildRequires:	xsltproc
BuildRequires:	apache-devel
BuildRequires:	subversion-devel >= 1.2
BuildRequires:	wxgtku-devel
BuildRequires:	pkgconfig(cppunit)
BuildRequires:	pkgconfig(neon)
Requires:	subversion

%description
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

%package -n %{libname}
Summary:	RapidSVN shared SvnCpp C++ API libraries
Group:		System/Libraries

%description -n %{libname}
This package contains shared SvnCpp C++ API libraries for
RapidSVN.

%package -n %{devname}
Summary:	RapidSVN SvnCpp C++ API development libraries
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libsvncpp-devel = %{version}-%{release}

%description -n %{devname}
As part of the RapidSVN effort it became clear that it would make
the code easier to update and manage if the Subversion client C
API were wrapped in C++. This is where SvnCpp comes from. Right
now it has the following aspects of the C API have been
abstracted: authentication, logging, status, notification, and
properties. SvnCpp should provide an object-oriented programming
interface to any project that uses C++ or a SWIG-compatible
language like Python or Java. 

%prep
%setup -qn %{name}-%{version}
%apply_patches
sed -i 's/python/python2/' src/locale/Makefile.*
autoreconf -fi

cp %{SOURCE1} rapidsvn_logo.png
cp -p %{SOURCE2} doc/svncpp/

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS=$CFLAGS

%configure2_5x \
	--enable-shared \
	--disable-static \
	--with-svn-include=%{_includedir} \
	--with-svn-lib=%{_libdir} \
	--with-xsltproc=%{_bindir}/xsltproc \
	--with-apr-config=%{_bindir}/apr-1-config \
	--with-apu-config=%{_bindir}/apu-1-config

%make

%install
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

mv doc/svncpp/html .

%find_lang %{name}

%files -f %{name}.lang
%doc html AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%{_libdir}/libsvncpp.so.%{major}*

%files -n %{devname}
%{_includedir}/svncpp
%{_libdir}/libsvncpp.so

