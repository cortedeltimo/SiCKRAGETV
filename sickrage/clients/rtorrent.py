# Author: jkaberg <joel.kaberg@gmail.com>, based on fuzemans work (https://github.com/RuudBurger/CouchPotatoServer/blob/develop/couchpotato/core/downloaders/rtorrent/main.py)
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import traceback

import sickrage
from rtorrent import RTorrent
from sickrage.clients import GenericClient


class rTorrentAPI(GenericClient):
    def __init__(self, host=None, username=None, password=None):
        super(rTorrentAPI, self).__init__('rTorrent', host, username, password)

    def _get_auth(self):
        self.auth = None

        if self.auth is not None:
            return self.auth

        if not self.host:
            return

        sp_kwargs = {}
        if sickrage.srCore.srConfig.TORRENT_AUTH_TYPE != 'None':
            sp_kwargs['authtype'] = sickrage.srCore.srConfig.TORRENT_AUTH_TYPE

        if not sickrage.srCore.srConfig.TORRENT_VERIFY_CERT:
            sp_kwargs['check_ssl_cert'] = False

        if self.username and self.password:
            url_parts = self.host.split('//')
            self.auth = RTorrent( url_parts[0] + "{0}:{1}@".format(self.username, self.password) + url_parts[1])
        else:
            self.auth = RTorrent(self.host)

        return self.auth

    def _add_torrent_uri(self, result):

        if not self.auth:
            return False

        if not result:
            return False

        try:
            # Send magnet to rTorrent
            torrent = self.auth.load_torrent(result.url)

            if not torrent:
                return False

            # Set label
            label = sickrage.srCore.srConfig.TORRENT_LABEL
            if result.show.is_anime:
                label = sickrage.srCore.srConfig.TORRENT_LABEL_ANIME
            if label:
                torrent.set_custom(1, label)

            if sickrage.srCore.srConfig.TORRENT_PATH:
                torrent.set_directory(sickrage.srCore.srConfig.TORRENT_PATH)

            # Start torrent
            torrent.start()

            return True

        except Exception:
            sickrage.srCore.srLogger.debug(traceback.format_exc())
            return False

    def _add_torrent_file(self, result):

        if not self.auth:
            return False

        if not result:
            return False

            # group_name = 'sb_test'.lower() ##### Use provider instead of _test
            # if not self._set_torrent_ratio(group_name):
            # return False

        # Send request to rTorrent
        try:
            # Send torrent to rTorrent
            torrent = self.auth.load_torrent(result.content)

            if not torrent:
                return False

            # Set label
            label = sickrage.srCore.srConfig.TORRENT_LABEL
            if result.show.is_anime:
                label = sickrage.srCore.srConfig.TORRENT_LABEL_ANIME
            if label:
                torrent.set_custom(1, label)

            if sickrage.srCore.srConfig.TORRENT_PATH:
                torrent.set_directory(sickrage.srCore.srConfig.TORRENT_PATH)

            # Set Ratio Group
            # torrent.set_visible(group_name)

            # Start torrent
            torrent.start()

            return True

        except Exception:
            sickrage.srCore.srLogger.debug(traceback.format_exc())
            return False

    def _set_torrent_ratio(self, name):

        # if not name:
        # return False
        #
        # if not self.auth:
        # return False
        #
        # views = self.auth.get_views()
        #
        # if name not in views:
        # self.auth.create_group(name)

        # group = self.auth.get_group(name)

        # ratio = int(float(sickrage.TORRENT_RATIO) * 100)
        #
        # try:
        # if ratio > 0:
        #
        # # Explicitly set all group options to ensure it is setup correctly
        # group.set_upload('1M')
        # group.set_min(ratio)
        # group.set_max(ratio)
        # group.set_command('d.stop')
        # group.enable()
        # else:
        # # Reset group action and disable it
        # group.set_command()
        # group.disable()
        #
        # except:
        # return False

        return True

    def testAuthentication(self):
        try:
            self._get_auth()

            if self.auth is not None:
                return True, 'Success: Connected and Authenticated'
            else:
                return False, 'Error: Unable to get ' + self.name + ' Authentication, check your config!'
        except Exception:
            return False, 'Error: Unable to connect to ' + self.name


api = rTorrentAPI()
