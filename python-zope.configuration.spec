#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.configuration
Summary:	Zope Configuration Markup Language (ZCML)
Summary(pl.UTF-8):	Zope Configuration Markup Language (ZCML) - język opisu konfiguracji Zope
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.4.1
Release:	2
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.configuration/zope.configuration-%{version}.tar.gz
# Source0-md5:	02268ab7c1714813aa6532be017f0540
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-manuel
BuildRequires:	python-zope.i18nmessageid
BuildRequires:	python-zope.interface
BuildRequires:	python-zope.schema >= 4.9.0
BuildRequires:	python-zope.testing
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-manuel
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.schema >= 4.9.0
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zope configuration system provides an extensible system for
supporting various kinds of configurations.

%description -l pl.UTF-8
System konfiguracji Zope to rozszerzalny system obsługujący różne
rodzaje konfiguracji.

%package -n python3-%{module}
Summary:	Zope Configuration Markup Language (ZCML)
Summary(pl.UTF-8):	Zope Configuration Markup Language (ZCML) - język opisu konfiguracji Zope
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
The Zope configuration system provides an extensible system for
supporting various kinds of configurations.

%description -n python3-%{module} -l pl.UTF-8
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
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/zope/configuration/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/configuration/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/zope/configuration
%{py_sitescriptdir}/zope.configuration-%{version}-py*.egg-info
%{py_sitescriptdir}/zope.configuration-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/configuration
%{py3_sitescriptdir}/zope.configuration-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.configuration-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,*.html,*.js}
%endif
