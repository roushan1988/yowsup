import urllib2
import urllib
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity

class ReadLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)
        
	if messageProtocolEntity.getType() == 'text':
	    messageObject = {"input": messageProtocolEntity.getBody()}
            url = "http://localhost:8080/restricted/offlineBooking?from="+messageProtocolEntity.getFrom()+"&"+urllib.urlencode(messageObject)
            messageProtocolEntity.setBody(urllib2.urlopen(url, timeout=60).read())
            messageProtocolEntityNew = messageProtocolEntity
        elif messageProtocolEntity.getType() == 'media' and messageProtocolEntity.getMediaType() == "location":
	    urlLocation = "http://localhost:8080/restricted/offlineBooking?lat="+messageProtocolEntity.getLatitude()+"&lng="+messageProtocolEntity.getLongitude()
	    print urlLocation
	    replyText = urllib2.urlopen(urlLocation, timeout=60).read()
	    messageProtocolEntityNew = TextMessageProtocolEntity(
                 replyText,
                 to = messageProtocolEntity.getFrom()
            )
	else:
            messageProtocolEntityNew = TextMessageProtocolEntity(
           	 "Please try again",
            	 to = messageProtocolEntity.getFrom()
            )
	self.toLower(messageProtocolEntityNew.forward(messageProtocolEntity.getFrom()))	
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image")

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
