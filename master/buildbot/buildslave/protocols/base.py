# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from buildbot.util import service
from buildbot.util import subscription


class Listener(service.ReconfigurableServiceMixin, service.AsyncMultiService):

    def __init__(self, master):
        service.AsyncMultiService.__init__(self)
        self.master = master


class Connection(object):

    def __init__(self, master, buildslave):
        self.master = master
        self.buildslave = buildslave
        name = buildslave.slavename
        self._disconnectSubs = subscription.SubscriptionPoint(
            "disconnections from %s" % name)

    # disconnection handling

    def notifyOnDisconnect(self, cb):
        return self._disconnectSubs.subscribe(cb)

    def notifyDisconnected(self):
        self._disconnectSubs.deliver()

    def loseConnection(self):
        raise NotImplementedError

    # methods to send messages to the slave

    def remotePrint(self, message):
        raise NotImplementedError

    def remoteGetSlaveInfo(self):
        raise NotImplementedError

    def remoteSetBuilderList(self, builders):
        raise NotImplementedError

    def remoteStartCommand(self, remoteCommand, builderName, commandId, commandName, args):
        raise NotImplementedError

    def remoteShutdown(self):
        raise NotImplementedError

    def remoteStartBuild(self, builderName):
        raise NotImplementedError

    def remoteInterruptCommand(self, commandId, why):
        raise NotImplementedError


class RemoteCommandImpl(object):

    def remote_update(self, updates):
        raise NotImplementedError

    def remote_complete(self, failure=None):
        raise NotImplementedError


class RemoteCommandProxy(object):

    def __init__(self, impl):
        assert isinstance(impl, RemoteCommandImpl)
        self.impl = impl

    def remote_update(self, updates):
        return self.impl.remote_update(updates)

    def remote_complete(self, failure=None):
        return self.impl.remote_complete(failure)
