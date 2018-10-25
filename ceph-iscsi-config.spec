#
# spec file for package ceph-iscsi-config
#
# Copyright (C) 2017-2018 The Ceph iSCSI Config Project Developers. See
# COPYING file at the top-level directory of this distribution and at
# https://github.com/ceph-iscsi-config/ceph/blob/master/COPYING
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon.
#
# This file is under the GNU General Public License, version 3 or any
# later version.
#
# Please submit bugfixes or comments via http://tracker.ceph.com/
#

Name:           ceph-iscsi-config
Version:        2.7
Release:        1%{?dist}
Summary:        Python package providing modules for Ceph iSCSI gateway configuration management

License:        GPL-3.0-or-later
URL:            https://github.com/ceph/ceph-iscsi-config
%if 0%{?suse_version}
Group:		Development/Languages/Python
Source0:        %{name}.tar.gz
%else
Source0: https://github.com/ceph/ceph-iscsi-config/archive/%{version}/%{name}-%{version}.tar.gz
%endif

%if 0%{?suse_version}
Requires:  python3-rados >= 10.2.2
Requires:  python3-rbd >= 10.2.2
Requires:  python3-netaddr >= 0.7.5
Requires:  python3-netifaces >= 0.10.4
Requires:  python3-rtslib >= 2.1.fb67
Requires:  python3-rpm >= 4.11
Requires:  python3-crypto >= 2.6
Requires:  python3-flask >= 0.10.1
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
%else
Requires:  python-rados >= 10.2.2
Requires:  python-rbd >= 10.2.2
Requires:  python-netaddr >= 0.7.5
Requires:  python-netifaces >= 0.10.4
Requires:  python-rtslib >= 2.1.fb67
Requires:  rpm-python >= 4.11
Requires:  python-crypto >= 2.6
Requires:  python-flask >= 0.10.1
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%endif
BuildRequires:  systemd
BuildArch:  noarch
%if 0%{?suse_version}
%python_subpackages
%endif

%description
Python package providing the modules used to handle the configuration of an
iSCSI gateway, backed by ceph/RBD. The rpm installs configuration management
logic (ceph_iscsi_config modules) and an rbd-target-gw systemd service.

The configuration management modules may be are consumed by custom Ansible
playbooks, and API server available from a separate rpm.

The rbd-target-gw service is responsible for startup and shutdown actions,
replacing the 'target' service used in standalone LIO implementations. In addition,
rbd-target-gw also provides a prometheus exporter for gateway LIO performance
statistics, supporting monitoring and visualisation tools like Grafana.

%prep
%if 0%{?suse_version}
%setup -c -q
%else
%setup -q
%endif

%build
%if 0%{?suse_version}
%python3_build
%else
%{__python2} setup.py build
%endif

%install
%if 0%{?suse_version}
%python3_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}
%else
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}  --install-scripts %{_bindir}
%endif
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 .%{_unitdir}/rbd-target-gw.service %{buildroot}%{_unitdir}

%post
%if 0%{?suse_version}
%service_add_post rbd-target-gw.service
%else
/bin/systemctl --system daemon-reload &> /dev/null || :
/bin/systemctl --system enable rbd-target-gw &> /dev/null || :
%endif

%pre
%if 0%{?suse_version}
%service_add_pre rbd-target-gw.service
%endif

%postun
%if 0%{?suse_version}
%service_del_postun rbd-target-gw.service
%endif

%preun
%if 0%{?suse_version}
%service_del_preun rbd-target-gw.service
%endif

%files -n ceph-iscsi-config
%if 0%{?suse_version}
%license LICENSE
%license COPYING
%else
%doc LICENSE
%doc COPYING
%endif
%doc README
%doc iscsi-gateway.cfg_sample
%if 0%{?suse_version}
%{python3_sitelib}/*
%else
%{python2_sitelib}/*
%endif
%{_bindir}/rbd-target-gw
%{_unitdir}/rbd-target-gw.service

%changelog

