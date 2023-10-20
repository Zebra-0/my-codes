from pytube.innertube import InnerTube
from pytube import YouTube
import json
def write_json_config(item):
    with open('ineertube.json', 'w') as arquivo:
        json.dump(item, arquivo)
        return item

link = "https://www.youtube.com/watch?v=wqnVzzJadTA"
data = YouTube("https://www.youtube.com/watch?v=wqnVzzJadTA", use_oauth=True, allow_oauth_cache=True)
innertube = InnerTube(
    client='ANDROID_EMBED',
    use_oauth=True,
    allow_cache=True
)
innertube_response = innertube.player(data.video_id)
age = innertube.verify_age(data.video_id)
print(age)
#write_json_config(innertube_response)

'''playability_status = innertube_response['playabilityStatus'].get('status', None)

# If we still can't access the video, raise an exception
# (tier 3 age restriction)
if playability_status == 'UNPLAYABLE':
    raise exceptions.AgeRestrictedError(self.video_id)

self._vid_info = innertube_response
'''
