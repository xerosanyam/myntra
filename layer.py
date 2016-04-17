from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
import requests
import extracteproduct
import hotinarea

class EchoLayer(YowInterfaceLayer):
    status = "continue"
    url = ""
    caption = ""
    problem = ""
    destination = ""
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        # send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(),
                                                    'read', messageProtocolEntity.getParticipant())
            mobnum =  messageProtocolEntity.getParticipant()
            x = messageProtocolEntity.isGroupMessage()
            print x
            if x is True:
                if messageProtocolEntity.getType() == "text":
                    message = "Invalid Request"
                    input = messageProtocolEntity.getBody()
                    inputList = input.split(' ')
                    print inputList, len(inputList)
                    inputMessage = inputList[0]

                    message = "Invalid Command. Please type #info"

                    if inputMessage == "#suggest" or inputMessage == "#s":
                        message=""
                        temp=extracteproduct.getUrl(mobnum)
                        for i in temp:
                            message+=i[1]+"\n\n"

                    elif inputMessage == "#trending" or inputMessage == "#t":
                      message="Please send your location"
                      self.status="trending_location"

                    elif inputMessage == "#find" or inputMessage == "#f":
                        message = "#color <color>: to change color\n#random: for random color\n#blink: to blink for few seconds"

                    elif inputMessage == "#complaint" or inputMessage == "#c":
                        message = "1. #s(uggest): suggests new products based on your social profile\n2. #t(rending) : shows a trending product in your nearby location\n3. #f(ind) :Give an image of product and find similar product on myntra\n4. #c(omplaint): lodge complaint of a product."

                    elif inputMessage == "#info" or inputMessage == "#i":
                        message = "1. #s(uggest): suggests new products based on your social profile\n2. #t(rending) : shows a trending product in your nearby location\n3. #f(ind) :Give an image of product and find similar product on myntra\n4. #c(omplaint): lodge complaint of a product."

                    elif inputMessage == "#complaint" and len(inputList) == 2:
                        self.problem = inputList[1]
                        self.status = "complaint_image"
                        message = "Please Upload the image"

                    
                    outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                        message,
                        to=messageProtocolEntity.getFrom())

                    self.toLower(receipt)
                    self.toLower(outgoingMessageProtocolEntity)
                elif messageProtocolEntity.getType() == "media":
                    message = ""
                    if messageProtocolEntity.getMediaType() == "location":

                        if self.status == "trending_location":
                            temp = hotinarea.getProducts(messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude())
                            for i in temp:
                              message+=i+"\n"

                        elif self.status == "hospital_origin":
                            ans = nearbyhospitals.waypoints([messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()])
                            print len(ans)
                            k = 1
                            for i in ans:
                                message += str(k) + ". " +i + "\n"
                                k += 1
                            self.status = "continue"
                            print messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()

                        elif self.status == "complaint_location":
                            complaint.complaintLodge(self.problem,messageProtocolEntity.getLatitude(),messageProtocolEntity.getLongitude(), self.url,self.caption)
                            self.status = "continue"
                            print messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()
                            message = "Complaint received. Thanks!\nSee all complaints at http://informed-complaints.github.io"

                        elif self.status == "bus_origins":
                            origin = ""
                            origin += str(messageProtocolEntity.getLatitude()) + ","
                            origin += str(messageProtocolEntity.getLongitude())
                            print messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()
                            message = route.waypoints(origin, self.destination)
                            print message

                    elif messageProtocolEntity.getMediaType() == "image":
                        if self.status == "complaint_image":
                            self.url = messageProtocolEntity.getMediaUrl()
                            self.caption = messageProtocolEntity.getCaption()
                            self.status = "complaint_location"
                            message = "Image received. Please send your location"

                    outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                            message,
                            to=messageProtocolEntity.getFrom())

                    self.toLower(receipt)
                    self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
