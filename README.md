# Zoom.Module_Autopsy.Plugin
This ingest module used to decrypt Zoom database and process Zoom artifacts.

## the project has two scripts:
•	The first tool for retrieving the keys called zoom_keys.py.
The remote key part was based by the following tool 
script used code written by” Alba Mendez” https://github.com/mildsunrise/protobuf-inspector.git . 
To run, with Python 3.7 is needed with the following Python modules installed: dpapick3, Crypto, pathlib, blackboxprotobuf, configparser, hashlib, os,requests, sys, urllib.

•	The second tool in the repository composes the add-on modules. Downloading and placing it in the appropriate directory is all that's needed (the ingest module that run on Autopsy Version 4.18.0).

## Experimental Environment:
This study is based on Windows 10 operating system environments which use VMware virtual machine software on PCs. Each of the virtual machines is equipped with 64-bit Windows 10 industrial version, both in 64-bit and 32-bit versions. Later, Zoom version 5.7.4 was installed to enable zoom features directly in the application. Table 1 illustrates the software listed above.

| Devices/OS    | Specification/Versions |
| ------------- | ------------- |
| VMware® Workstation 16 Pro | Version 16.1.2 build-17966106  |
| Windows 10 | Windows 10 Pro, 64-bit (Build 19042.1165)|
| Zoom Application  | Version 5.7.4 (804)|

## Artifacts:
for each artifact type a SQL Query generated to fetch the interested attributes’ contents from relevant database. 
The artifacts are divided into six types:
|#|Artifact Type    |
|---| ------------- |
| 1 |Zoom Meeting Chat| |
| 2 |Zoom Chat |
| 3 |File Transfer |
| 4 |Zoom Contacts |
| 5 |Zoom Keys|
| 6 |Zoom Transcript|
  ### Example:Zoom Meeting Chat Artifact:
  
we will take Zoom Meeting Chat artifact as an example to show the reporting process:
1. we give this artifact and ID to refers to it in fetching process.
 artID = blackboard.getOrAddArtifactType("TSK_ZOOM_MEETING_MSG", "Zoom Meeting Chats")
2. Create result statement, to get all important evidence form the database tha has information about chat feature during a meeting. 
resultSet = stmt.executeQuery("SELECT confID, time, content, read, sender, receiver, senderName, receiverName from zoom_conf_chat_gen2_enc;")
3. Define the properties of the Zoom Meeting Chats artifact, such as Conference ID,Time,Content, Read, Sender Name.and then add the relevant evidence for each attribute. 
attID_1 = blackboard.getOrAddAttributeType("TSK_ZOOM_MEETING_MSG_ID", BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Conference ID")
attribute_1 = BlackboardAttribute(attID_1, ZoomIngestModuleFactory.moduleName, confID).

