

class OriginChannels():

    def __init__(self, fhdhr, origin):
        self.fhdhr = fhdhr
        self.origin = origin

        self.base_api = 'http://watchnewson.com/api/linear/channels'

    def get_channels(self):

        channel_list = []

        channels_json = self.fhdhr.web.session.get(self.base_api).json()
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
        channels_json = self.fhdhr.web.session.get(self.base_api).json()
        origin_chandict = self.get_channel_dict(channels_json, "identifier", chandict["origin_id"])
        streamdict = self.get_channel_dict(origin_chandict["streams"], "StreamType", 'website')
        streamurl = streamdict['Url']

        stream_info = {"url": streamurl}

        return stream_info

    def get_channel_dict(self, chanlist, keyfind, valfind):
        return next(item for item in chanlist if item[keyfind] == valfind)