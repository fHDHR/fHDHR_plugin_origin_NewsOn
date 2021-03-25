import json
from simplejson import errors as simplejsonerrors


class Plugin_OBJ():

    def __init__(self, plugin_utils):
        self.plugin_utils = plugin_utils

        self.base_api = 'http://watchnewson.com/api/linear/channels'

    @property
    def tuners(self):
        return self.plugin_utils.config.dict["newson"]["tuners"]

    @property
    def stream_method(self):
        return self.plugin_utils.config.dict["newson"]["stream_method"]

    def get_channels(self):

        channel_list = []

        try:
            channels_json = self.plugin_utils.web.session.get(self.base_api).json()
        except json.JSONDecodeError as err:
            self.plugin_utils.logger.error('Collecting Channels Failed: %s' % err)
            return []
        except simplejsonerrors.JSONDecodeError as err:
            self.plugin_utils.logger.error('Collecting Channels Failed: %s' % err)
            return []

        for channel_dict in channels_json:
            if not channel_dict["disabled"]:

                clean_station_item = {
                                     "name": channel_dict["config"]["affiliation"] or channel_dict["config"]["callsign"],
                                     "callsign": channel_dict["config"]["callsign"],
                                     "id": channel_dict["identifier"],
                                     "thumbnail": channel_dict["icon"],
                                     }
                channel_list.append(clean_station_item)

        return channel_list

    def get_channel_stream(self, chandict, stream_args):
        channels_json = self.plugin_utils.web.session.get(self.base_api).json()
        origin_chandict = self.get_channel_dict(channels_json, "identifier", chandict["origin_id"])
        streamdict = self.get_channel_dict(origin_chandict["streams"], "StreamType", 'website')
        streamurl = streamdict['Url']

        stream_info = {"url": streamurl}

        return stream_info

    def get_channel_dict(self, chanlist, keyfind, valfind):
        return next(item for item in chanlist if item[keyfind] == valfind)
