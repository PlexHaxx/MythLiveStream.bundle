TITLE = 'MythTV Livestream'
PREFIX = '/video/mythlivestream'
API_URL = '%s' % (Prefs['server'])
WEB_URL = '%s' % (Prefs['hlsserver'])
ICON = 'icon-default.png'
ART = 'art-default.jpg'

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)

    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


@handler(PREFIX, TITLE)
def MainMenu():
    oc = ObjectContainer()
    for video in XML.ElementFromURL(API_URL + '/Content/GetLiveStreamList').xpath('//LiveStreamInfo'):
       rurl = video.xpath('./RelativeURL')[0].text
       url = WEB_URL + rurl
       chanid = url.rsplit('/', 1)
       chanid = chanid[1]
       chanid = chanid.split('_', 1)
       chanid = chanid[0] 
       status = video.xpath('./StatusStr')[0].text
       created = video.xpath('./Created')[0].text
       channum = XML.ElementFromURL(
             API_URL + 
             '/Guide/GetProgramGuide?NumChannels=1&StartChanId=%s&StartTime=%s&EndTime=%s' % 
             (chanid, created, created)).xpath('//ProgramGuide/Channels/ChannelInfo/ChanNum')[0].text
       station = XML.ElementFromURL(
              API_URL + 
              '/Guide/GetProgramGuide?NumChannels=1&StartChanId=%s&StartTime=%s&EndTime=%s' % 
              (chanid, created, created)).xpath('//ProgramGuide/Channels/ChannelInfo/ChannelName')[0].text
       showname = XML.ElementFromURL(
              API_URL + 
              '/Guide/GetProgramGuide?NumChannels=1&StartChanId=%s&StartTime=%s&EndTime=%s' % 
               (chanid, created, created)).xpath('//ProgramGuide/Channels/ChannelInfo/Programs/Program/Title')[0].text
       title = "%s: (%s) -  %s (%s)" % (channum, station, showname, status)
       thumb = R(ICON)
       oc.add(CreateVideoClipObject(url, title, thumb ))

    return oc


@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, container = False):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, container = True),
        url = url,
        title = title,
        thumb = R(ICON),
        items = [ MediaObject( parts = [ PartObject( key = GetVideoURL(url = url)) ], optimized_for_streaming = True) ]
        )

    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco

def GetVideoURL(url, live = True):
        return HTTPLiveStreamURL(url = url)

