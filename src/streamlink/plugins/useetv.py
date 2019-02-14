import re

from streamlink.plugin import Plugin
from streamlink.stream import HLSStream

class UseeTV(Plugin):
    url_re = re.compile(r"https://www.useetv.com/(?:(?:livetv/(?P<channel_id>\w+))|(?:play/\w+/(?P<video_id>\d+)/))")
    _source_url_re = re.compile(r"source\s+src=\"(.*?)\" type=\"application/x-mpegURL\"")

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url)

    def _get_streams(self):
        res = self.session.http.get(self.url)
        match = self._source_url_re.search(res.text)
        if match is None:
            return

        return HLSStream.parse_variant_playlist(self.session, match.group(1))

__plugin__ = UseeTV
