Name:           pathagar
Version:        0
Release:        1

Summary:        Book Server

Group:          Applications/Archiving
License:        GPLv2

URL:            http://wiki.laptop.org
%global         path1        git://github.com/johnsensible/django-sendfile.git

%global         path2        git://github.com/manuq/pathagar


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      yum
Requires:       python
Requires:       mod_python
Requires:       mod_wsgi
Requires:       python-setuptools
Requires:       sqlite
Requires:       Django
BuildRequires: git


%description
This package contains the XS repository configuration.

%prep
%setup -q  -c -T


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}
cd $RPM_BUILD_ROOT/%{python_sitelib}
git clone %{path1}
git clone %{path2}
rm -rf */.git*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*


%changelog
