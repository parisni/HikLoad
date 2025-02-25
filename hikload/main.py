from xml.etree import ElementTree
import requests
from hikload.util import chdir, getList, getXmlString, downloadRTSP, getConfig
import datetime


def main():
    # This is needed because Hikvision only uses XML
    search = ElementTree.fromstring("""<?xml version="1.0" encoding="utf-8"?>
    <CMSearchDescription>
        <searchID>C85AB0C7-F380-0001-E33B-A030EEB671F0</searchID>
        <trackList>
            <trackID></trackID>
        </trackList>
        <timeSpanList>
            <timeSpan>
                <startTime></startTime>
                <endTime></endTime>
            </timeSpan>
        </timeSpanList>
        <maxResults>40</maxResults>
        <searchResultPostion>0</searchResultPostion>
        <metadataList>
            <metadataDescriptor>//recordType.meta.std-cgi.com</metadataDescriptor>
        </metadataList>
    </CMSearchDescription>""")

    headers = {'Content-Type': 'application/xml'}

    serverpath = "http://" + getConfig('user') + ":" + getConfig(
        "password") + "@" + getConfig("server") + "/ISAPI/ContentMgmt/search"

    chdir(getConfig("downloadPath"))
    # TODO: Specify time in config file
    starttime = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    endtime = datetime.datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=0).isoformat() + "Z"

    # This downloads the files from every camera
    for i in getConfig("cameras"):
        print("Trying to download from camera " + i)
        search[1][0].text = i
        search[2][0][0].text = starttime
        search[2][0][1].text = endtime
        data = getXmlString(search)
        responseXML = requests.post(serverpath, data, headers).text
        response = ElementTree.fromstring(responseXML)
        for stream in getList(response):
            downloadRTSP(stream)


if __name__ == "__main__":
    main()
