#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define module	zope.configuration
Summary:	Zope Configuration Markup Language (ZCML)
Summary(pl.UTF-8):	Zope Configuration Markup Language (ZCML) - język opisu konfiguracji Zope
Name:		python3-%{module}
Version:	6.0
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.configuration/zope_configuration-%{version}.tar.gz
# Source0-md5:	3e894fa3a615b79159acdaa1b25c14da
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-manuel
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.schema >= 4.9.0
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zope configuration system provides an extensible system for
supporting various kinds of configurations.

%description -l pl.UTF-8
System konfiguracji Zope to rozszerzalny system obsługujący różne
rodzaje konfiguracji.

%package apidocs
Summary:	API documentation for Python zope.configuration module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.configuration
Group:		Documentation

%description apidocs
API documentation for Python zope.configuration module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.configuration.

%prep
%setup -q -n zope_configuration-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/configuration/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/configuration
%{py3_sitescriptdir}/zope.configuration-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.configuration-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,*.html,*.js}
%endif
