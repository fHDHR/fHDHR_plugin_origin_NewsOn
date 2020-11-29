import m3u8


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

    def get_channel_stream(self, chandict):
        channels_json = self.fhdhr.web.session.get(self.base_api).json()
        origin_chandict = self.get_channel_dict(channels_json, "identifier", chandict["origin_id"])
        streamdict = self.get_channel_dict(origin_chandict["streams"], "StreamType", 'website')
        streamurl = streamdict['Url']
        if self.fhdhr.config.dict["origin"]["force_best"]:
            streamurl = self.m3u8_beststream(streamurl)
        return streamurl

    def get_channel_dict(self, chanlist, keyfind, valfind):
        return next(item for item in chanlist if item[keyfind] == valfind)

    def m3u8_beststream(self, m3u8_url):
        bestStream = None
        videoUrlM3u = m3u8.load(m3u8_url)
        if not videoUrlM3u.is_variant:
            return m3u8_url

        for videoStream in videoUrlM3u.playlists:
            if not bestStream:
                bestStream = videoStream
            elif videoStream.stream_info.bandwidth > bestStream.stream_info.bandwidth:
                bestStream = videoStream

        if not bestStream:
            return bestStream.absolute_uri
        else:
            return m3u8_url
