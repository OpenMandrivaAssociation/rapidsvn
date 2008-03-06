%define	major 0
%define libname	%mklibname svncpp %{major}
%define oldlibname %mklibname rapidsvn 0
%define develname %mklibname svncpp -d

Summary:	A cross-platform GUI for the Subversion concurrent versioning system
Name:		rapidsvn
Version:	0.9.6
Release:	%mkrel 1
License:	GPLv2+
Group:		Development/Other
URL:		http://rapidsvn.tigris.org
Source0:	http://www.rapidsvn.org/download/%{name}-%{version}.tar.bz2
Source1:	rapidsvn_logo.png
Patch0:		wx28.diff
BuildRequires:	apache-devel >= 2.0.54
BuildRequires:	doxygen
BuildRequires:	subversion-devel >= 1.2
BuildRequires:	subversion >= 1.2
BuildRequires:	libtool >= 1.4.2
BuildRequires:	wxGTK2.8-devel
BuildRequires:	libxslt-proc
BuildRequires:	db4-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	neon0.26-devel >= 0.26.4
BuildRequires:	autoconf2.5 >= 2.53
BuildRequires:	imagemagick
Requires(post): %{libname} = %{version}
Requires(preun): %{libname} = %{version}
Requires:	subversion
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

%package -n	%{libname}
Summary:	RapidSVN shared SvnCpp C++ API libraries
Group:          System/Libraries

%description -n	%{libname}
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

This package contains shared SvnCpp C++ API libraries for
RapidSVN.

%package -n	%{develname}
Summary:	RapidSVN SvnCpp C++ API development libraries
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libsvncpp-devel = %{version}-%{release}
Provides:	%{oldlibname}-devel = %{version}-%{release}
Obsoletes:	%{oldlibname}-devel
Obsoletes:	%{mklibname svncpp -d 0}

%description -n	%{develname}
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
%patch0

cp %{SOURCE1} rapidsvn_logo.png

%build
#export WANT_AUTOCONF_2_5="1"
#libtoolize --copy --force && aclocal-1.7 && automake-1.7 --add-missing --foreign && autoconf

if [ -x %{_bindir}/apr-config ]; then APR=%{_bindir}/apr-config; fi
if [ -x %{_bindir}/apu-config ]; then APU=%{_bindir}/apu-config; fi

if [ -x %{_bindir}/apr-1-config ]; then APR=%{_bindir}/apr-1-config; fi
if [ -x %{_bindir}/apu-1-config ]; then APU=%{_bindir}/apu-1-config; fi

%configure \
    --enable-shared \
    --with-svn-include=%{_includedir} \
    --with-svn-lib=%{_libdir} \
    --with-xsltproc=%{_bindir}/xsltproc \
    --disable-no-exceptions \
    --with-apr-config=$APR \
    --with-apu-config=$APU

%make

%install
%{__rm} -rf %{buildroot}

%makeinstall_std


# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

convert rapidsvn_logo.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert rapidsvn_logo.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert rapidsvn_logo.png -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png


mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

%post
%update_menus

%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc html AUTHORS ChangeLog INSTALL NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/svncpp
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
