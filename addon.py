from xbmcswift2 import Plugin
import urllib2
import json

plugin = Plugin()

def api_call(url):
	url="http://rokutvchannel.churchlivenow.com/api/"+url
	return json.loads(urllib2.urlopen(url).read())


@plugin.route('/')
def index():
    categories=api_call('categories')
    items = [
        {'label': category['title'], 'path': plugin.url_for('show_subcategories', category_id=category['id']),'thumbnail':category['image'],'icon':category['image']}
    for category in categories]
    return items

@plugin.route('/categories/<category_id>')
def show_subcategories(category_id):
    '''Display subcategories'''
    subcategories=api_call('subcategories/'+category_id)
    items = [
	        {'label': subcategory['title'], 'path': plugin.url_for('show_videos', subcategory_id=subcategory['id'])}
	    for subcategory in subcategories]
	
    return items

@plugin.route('/videos/<subcategory_id>')
def show_videos(subcategory_id):
	videos=api_call('videos/'+subcategory_id)
	items=[
		{'label':video['title'],'info':{'title':video['title'],'plot':video['description']},'path':plugin.url_for('play_video',video_id=video['id']),'thumbnail':video['image'],'icon':video['image']}
	for video in videos]
	return items

@plugin.route('/play/<video_id>')
def play_video(video_id):
	video=api_call('details/'+video_id)
	items=[{'label':video['title'],'thumbnail':video['image'],'info':{'title':video['title'],'plot':video['description']},'path':video['video'],'is_playable':True,},]
	return plugin.finish(items)



if __name__ == '__main__':
    plugin.run()
