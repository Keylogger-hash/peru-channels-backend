# with open(settings.DATA_DIR / "categories.json", "r") as f:
#     category_objects = []
#     data = json.loads(f.read())
#     for item in data:
#         category_object = Category(
#             category_id=item["id"], category_name=item["name"]
#         )
#         category_objects.append(category_object)
#     Category.objects.bulk_create(category_objects)
# with open(settings.DATA_DIR / "streams.json", "w+") as f:
#     with open(
#         "/Users/pavelmorozov/Downloads/Rus18.m3u", "r"
#     ) as playlist_file:
#         streams_data = streams_request.json()
#         content = playlist_file.read()
#         russian_playlist = playlist.loads(content)
#         channels = russian_playlist.get_channels()
#         for channel in channels:
#             channel_name = channel.name
#             channel_id = (
#                 channel.attributes.get("tvg-id")
#                 if channel.attributes.get("tvg-id")
#                 else channel.name
#             )
#             channel_url = channel.url
#             channel = channel.attributes.get("tvg-logo")
#             rus_streams_data = {
#                 "channel": channel_id,
#                 "url": channel_url,
#                 "timeshift": None,
#                 "user_agent": None,
#                 "http_referrer": None,
#             }
#             streams_data.append(rus_streams_data)
#             rus_channels_data = {
#                 "id": channel_id,
#                 "name": channel_name,
#                 "alt_names": [],
#                 "network": None,
#                 "owners": [],
#                 "country": "DO",
#                 "subdivision": None,
#                 "city": "Santo Domingo",
#                 "broadcast_area": ["c/DO"],
#                 "languages": ["ru"],
#                 "categories": ["general"],
#                 "is_nsfw": False,
#                 "launched": None,
#                 "closed": None,
#                 "replaced_by": None,
#                 "website": "https://example.com",
#                 "logo": "https://i.imgur.com/7oNe8xj.png",
#             }
#         f.write(json.dumps(data))
#     with open(settings.DATA_DIR / "channels.json", "w+") as f:
#         data = json.dumps(channels_request.json())
#         f.write(data)
# xchannels_objects.append(channel_object)


# def write():
#     r = requests.get("https://iptv-org.github.io/api/channels.json")


#     with open("channels.json", "w+") as f:
#         data = json.dumps(r.json())
#         f.write(data)

# def read():
#     channels = Channel.objects.all()
#     print(channels)
# read()
