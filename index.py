from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from gdata.youtube.service import YouTubeService

class VideoResource(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write('<?xml version="1.0" encoding="UTF-8"?>')
        
        video_id = self.request.get('id', default_value='')
        video = None
        try:
            yt = YouTubeService()
            video = yt.GetYouTubeVideoEntry(video_id=video_id)
        except Exception, e:
            pass #will return empty result :)
        
        if video:
            self.response.out.write(u'<result>')
            self.response.out.write(u'   <video>')
            self.response.out.write(u'       <id>%s</id>' % video_id)
            self.response.out.write(u'       <url><![CDATA[%s]]></url>' % video.media.player.url)
            self.response.out.write(u'       <title><![CDATA[%s]]></title>' % unicode(video.title.text))
            self.response.out.write(u'       <content><![CDATA[%s]]></content>' % unicode(video.content.text))
            self.response.out.write(u'       <author><![CDATA[%s]]></author>' % video.author[0].name.text)
            self.response.out.write(u'       <duration>%d</duration>' % int(video.media.duration.seconds))
            self.response.out.write(u'       <comment_count>%d</comment_count>' % int(video.comments.feed_link[0].count_hint))
            
            self.response.out.write(u'       <categories>')
            for category in [category.label for category in video.category if category.label]:
                self.response.out.write(u'           <category><![CDATA[%s]]></category>' % category)
            self.response.out.write(u'       </categories>')
            
            self.response.out.write(u'       <tags>')
            if video.media.keywords.text:
                for tag in video.media.keywords.text.split(u','):
                    self.response.out.write(u'           <tag><![CDATA[%s]]></tag>' % tag.strip())
            self.response.out.write(u'       </tags>')
            
            self.response.out.write(u'       <thumbnails>')
            for thumbnail in video.media.thumbnail:
                self.response.out.write(u'           <thumbnail width="%d" height="%d" time="%s">%s</thumbnail>' % (int(thumbnail.width), int(thumbnail.height), thumbnail.extension_attributes.get('time', ''), thumbnail.url))
            self.response.out.write(u'       </thumbnails>')
            
            self.response.out.write(u'       <files>')
            for video_file in video.media.content:
                self.response.out.write(u'           <file type="%s"><![CDATA[%s]]></file>' % (video_file.type, video_file.url))
            self.response.out.write(u'       </files>')
            
            self.response.out.write(u'   </video>')
            self.response.out.write(u'</result>')
        else:
            self.response.out.write(u'<result />')

application = webapp.WSGIApplication(
                                     [('/video.*', VideoResource)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()