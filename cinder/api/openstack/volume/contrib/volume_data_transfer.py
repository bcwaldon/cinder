# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import webob

from cinder.api.openstack import extensions
from cinder.openstack.common import log as logging
import cinder.volume

LOG = logging.getLogger(__name__)

class Controller(object):

    def show(self, req, id):
        context = req.environ['cinder.context']
        volume_api = cinder.volume.API()
        volume = volume_api.get(context, id)
        resp = webob.Response()
        resp.app_iter = volume_api.read_volume(context, volume)
        return resp

    def update(self, req, id):
        context = req.environ['cinder.context']
        volume_api = cinder.volume.API()
        volume = volume_api.get(context, id)
        volume_api.write_volume(context, volume, req.body_file)
        return webob.Response()


class Volume_data_transfer(extensions.ExtensionDescriptor):
    """Transfer raw data in and out of a volume"""

    name = "Volume_data_transfer"
    alias = "os-volume-data-transfer"
    namespace = ("http://docs.openstack.org/volume/ext/"
                 "volume-data-transfer/api/v1.1")
    updated = "2012-03-12T00:00:00+00:00"

    def get_resources(self):
        resources = []

        res = extensions.ResourceExtension('os-volume-data-transfer',
                                           Controller())
        resources.append(res)

        return resources
