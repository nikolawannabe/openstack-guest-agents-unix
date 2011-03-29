# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#  Copyright (c) 2011 Openstack, LLC.
#  All Rights Reserved.
#
#     Licensed under the Apache License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may obtain
#     a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#     WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#     License for the specific language governing permissions and limitations
#     under the License.
#

"""
resetnetwork hostname tester
"""

import os
import unittest
from cStringIO import StringIO

import commands.redhat.network
import commands.debian.network
import commands.arch.network
import commands.gentoo.network
import commands.suse.network


class TestHostNameUpdates(unittest.TestCase):

    def _run_redhat(self, infile, hostname):
        outfile = commands.redhat.network._update_hostname(infile, hostname)
        outfile.seek(0)
        return outfile

    def _run_debian(self, hostname):
        outfile = commands.debian.network._update_hostname(hostname)
        outfile.seek(0)
        return outfile

    def _run_arch(self, infile, hostname):
        outfile = commands.arch.network._update_hostname(infile, hostname)
        outfile.seek(0)
        return outfile

    def _run_suse(self, hostname):
        outfile = commands.suse.network._update_hostname(hostname)
        outfile.seek(0)
        return outfile

    def test_redhat_add_entry(self):
        """Test adding hostname to /etc/sysconfig/network"""
        infile = StringIO('NETWORKING=yes\n' +
            'NETWORKING_IPV6=yes\n')
        outfile = self._run_redhat(infile, 'example')
        self.assertEqual(outfile.read(), 'NETWORKING=yes\n' +
            'NETWORKING_IPV6=yes\n' +
            'HOSTNAME=example\n')

    def test_redhat_update_entry(self):
        """Test updating hostname in /etc/sysconfig/network"""
        infile = StringIO('NETWORKING=yes\n' +
            'NETWORKING_IPV6=yes\n' +
            'HOSTNAME=other\n')
        outfile = self._run_redhat(infile, 'example')
        self.assertEqual(outfile.read(), 'NETWORKING=yes\n' +
            'NETWORKING_IPV6=yes\n' +
            'HOSTNAME=example\n')

    def test_debian(self):
        """Test updating hostname in /etc/hostname"""
        outfile = self._run_debian('example')
        self.assertEqual(outfile.read(), 'example\n')

    def test_arch_add_entry(self):
        """Test adding hostname to /etc/rc.conf"""
        infile = StringIO('eth0="eth0 192.0.2.42 netmask 255.255.255.0"\n' +
            'INTERFACES=(eth0)\n')
        outfile = self._run_arch(infile, 'example')
        self.assertEqual(outfile.read(),
            'eth0="eth0 192.0.2.42 netmask 255.255.255.0"\n' +
            'INTERFACES=(eth0)\n' +
            'HOSTNAME="example"\n')

    def test_arch_update_entry(self):
        """Test updating hostname in /etc/rc.conf"""
        infile = StringIO('eth0="eth0 192.0.2.42 netmask 255.255.255.0"\n' +
            'INTERFACES=(eth0)\n' +
            'HOSTNAME="other"\n')
        outfile = self._run_arch(infile, 'example')
        self.assertEqual(outfile.read(),
            'eth0="eth0 192.0.2.42 netmask 255.255.255.0"\n' +
            'INTERFACES=(eth0)\n' +
            'HOSTNAME="example"\n')

    def test_suse(self):
        """Test updating hostname in /etc/HOSTNAME"""
        outfile = self._run_suse('example')
        self.assertEqual(outfile.read(), 'example\n')


if __name__ == "__main__":
    agent_test.main()
