# coding: utf-8

from json import dumps, loads

from facegraph import Graph
from urllib2 import HTTPError

class FriendListException(Exception):
    pass

class FriendList(set):
    def __init__(self, g, id=None, name=None, members=None, type=None):
        self.g = g
        self.id = id
        self.name = name
        set.__init__(self, [str(x) for x in members])

#    def __new__(cls, *args):
#        return set.__new__(cls, *args)

    def __str__(self):
        return set.__str__(self)

    def save(self):
        # List might already on FB
        if self.id:
            fblist = None
            try:
                fblist = g[self.id].members()
            except HTTPError, e:
                if e.code not in [400, 404]: # Not found or no permission.
                    raise e
            if fblist is None: # invalid id
                self.id = None # Fallthrough.
            else: # Overwrite
                # TODO: is there a way to overwrite the name?
                fbusers = set([str(x['id']) for x in fblist['data']])
                return self.updateusers(self - fbusers, fbusers - self)

        if self.name == None:
            raise FriendListException("No name was given.") 
        if len(self.name) > 25:
            raise FriendListException("The name must not be longer than 25 characters.")

        # Create list.
        try:
            fblist = g.me.friendlists.post(name=self.name)
            self.id = fblist['id']
        except Exception, e:
            raise e # TODO

        # Add members
        self.updateusers(self.members)

    def updateusers(self, toadd=None, todel=None):
        if toadd is None:
            toadd = set()
        if todel is None:
            todel = set()

        # Maximum 50 requests per batch.
        # TODO: better space usage here
        requests = [{'method': 'POST', 'relative_url': '%s/members/%s' % (self.id, member)} for member in toadd] + \
            [{'method': 'DELETE', 'relative_url': '%s/members/%s' % (self.id, member)} for member in todel]

        REQS_PER_POST = 50
        for i in range((len(requests) // REQS_PER_POST)+1):
            try:
                print requests[i*REQS_PER_POST:(i+1)*REQS_PER_POST]
                result = self.g.post(batch=dumps(requests[i*REQS_PER_POST:(i+1)*REQS_PER_POST]))
                print result
            except Exception, e:
                raise e # TODO


if __name__ == "__main__":
    g = Graph("...") # Replace with OAuth token.
#    print "Friends"
#    print g.me.friends() # Friends
#    fl = FriendList(g, name='New test list', members=set(['1', '2', '3'])) # Replace these with actual friend IDs.
#    fl.save()

    # Get all of the friendlists with their members.
    lists = g.me.friendlists()['data']
    lids = [fl['id'] for fl in lists]
    members = g.ids(lids).members()
#    print members
