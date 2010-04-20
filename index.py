from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from gdata.youtube.service import YouTubeService

class VideoResource(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write('<?xml version="1.0" encoding="UTF-8"?>')
        
        video_id = self.request.get('video_id', default_value='')
        video = None
        try:
            yt = YouTubeService()
            video = yt.GetYouTubeVideoEntry(video_id=video_id)
        except Exception, e:
            pass #will return empty result :)
        
        if video:
            self.response.out.write('<result>')
            self.response.out.write('   <video>')
            self.response.out.write('       <id>%s</id>' % video_id)
            self.response.out.write('       <url><![CDATA[%s]]></url>' % video.media.player.url)
            self.response.out.write('       <title><![CDATA[%s]]></title>' % video.title.text)
            self.response.out.write('       <content><![CDATA[%s]]></content>' % video.content.text)
            self.response.out.write('       <author><![CDATA[%s]]></author>' % video.author[0].name.text)
            video.media.duration.seconds
            self.response.out.write('       <comment_count>%d</comment_count>' % video.comments.feed_link[0].count_hint)
            
            self.response.out.write('       <categories>')
            for category in [category.label for category in video.category if category.label]:
                self.response.out.write('           <category><![CDATA[%s]]></category>' % category)
            self.response.out.write('       </categories>')
            
            self.response.out.write('       <tags>')
            if video.media.keywords.text:
                for tag in video.media.keywords.text.split(','):
                    self.response.out.write('           <tag><![CDATA[%s]]></tag>' % tag)
            self.response.out.write('       </tags>')
            
            self.response.out.write('       <thumbnails>')
            for thumbnail in video.media.thumbnail:
                self.response.out.write('           <thumbnail width="%d" height="%d" time="">%s</thumbnail>' % (thumbnail.width, thumbnail.height, thumbnail.url, thumbnail.extension_attributes.get('time', '')))
            self.response.out.write('       </thumbnails>')
            
            self.response.out.write('       <files>')
            for video_file in video.media.content:
                self.response.out.write('           <file type="%s">%s</file>' % (video_file.type, video_file.url))
            self.response.out.write('       </files>')
            
            self.response.out.write('   </video>')
            self.response.out.write('</result>')
        else:
            self.response.out.write('<result />')

application = webapp.WSGIApplication(
                                     [('/video/.*', VideoResource)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()