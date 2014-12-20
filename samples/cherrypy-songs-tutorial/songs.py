# Example of dic based on the CherryPy songs tutorial
# See https://cherrypy.readthedocs.org/en/3.3.0/tutorial/REST.html#getting-started

import cherrypy
import dic

songs = {
    '1': {
        'title': 'Lumberjack Song',
        'artist': 'Canadian Guard Choir'
    },

    '2': {
        'title': 'Always Look On the Bright Side of Life',
        'artist': 'Eric Idle'
    },

    '3': {
        'title': 'Spam Spam Spam',
        'artist': 'Monty Python'
    }
}


class Song(object):
    def __init__(self, title, artist):
    pass


class SongDatabase(object):
    def __init__(self, song_factory: dic.Factory(Song)):
        self.song_factory = song_factory
        self.songs =

    def __getitem__(self, item):
        return self.songs[item]




class Songs:
    exposed = True

    def __init__(self, song_database: SongDatabase):
        self.songs = song_database

    def GET(self, id=None):

        if id is None:
            return('Here are all the songs we have: %s' % songs)
        elif id in songs:
            song = songs[id]

            return(
                'Song with the ID %s is called %s, and the artist is %s' % (
                    id, song['title'], song['artist']))
        else:
            return('No song with the ID %s :-(' % id)

    def POST(self, title, artist):

        id = str(max([int(_) for _ in songs.keys()]) + 1)

        songs[id] = {
            'title': title,
            'artist': artist
        }

        return ('Create a new song with the ID: %s' % id)

    def PUT(self, id, title=None, artist=None):
        if id in songs:
            song = songs[id]

            song['title'] = title or song['title']
            song['artist'] = artist or song['artist']

            return(
                'Song with the ID %s is now called %s, '
                'and the artist is now %s' % (
                    id, song['title'], song['artist'])
            )
        else:
            return('No song with the ID %s :-(' % id)

    def DELETE(self, id):
        if id in songs:
            songs.pop(id)

            return('Song with the ID %s has been deleted.' % id)
        else:
            return('No song with the ID %s :-(' % id)

if __name__ == '__main__':
    builder = dic.ContainerBuilder()
    builder.register_class(Songs)
    builder.register_class(SongDatabase)
    builder.register_class(Song)

    container = builder.build()

    cherrypy.tree.mount(
        container.resolve(Songs), '/api/songs',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
