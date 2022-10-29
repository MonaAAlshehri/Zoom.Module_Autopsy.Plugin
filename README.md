# Zoom.Module_Autopsy.Plugin
This ingest module used to decrypt Zoom database and process Zoom artifacts.
## Experimental Environment:
This study is based on Windows 10 operating system environments which use VMware virtual machine software on PCs. Each of the virtual machines is equipped with 64-bit Windows 10 industrial version, both in 64-bit and 32-bit versions. Later, Zoom version 5.7.4 was installed to enable zoom features directly in the application. Table 1 illustrates the software listed above.

| Devices/OS    | Specification/Versions |
| ------------- | ------------- |
| VMware® Workstation 16 Pro | Version 16.1.2 build-17966106  |
| Windows 10 | Windows 10 Pro, 64-bit (Build 19042.1165)|
| Zoom Application  | Version 5.7.4 (804)|

### the project has two scripts:
## 1. Zoom_key.py
•	The first tool for retrieving the keys called zoom_keys.py.
The remote key part was based by the following tool 
script used code written by” Alba Mendez” https://github.com/mildsunrise/protobuf-inspector.git . 
To run, with Python 3.7 is needed with the following Python modules installed: dpapick3, Crypto, pathlib, blackboxprotobuf, configparser, hashlib, os,requests, sys, urllib.
#### Local Key:

`local  <Microsoft/Protect/SID folder> <Zoom.us.ini> <optional windows password>`

zoom_keys.py is the first tool that retrieve the users' local keys using python 3.7. DPAPIck3 library, will be used to retrieve the local key, allowing offline decryption of DPAPI structures, regardless the type of the zoom account (e.g. SSO,Google or Basic). Investigators must pass `SID folder` from Active directory and `Zoom.us.ini` as the main inputs to fetch the local Key. 

#### Remote Key:

`remote [ basic/sso/google] <zoom login> <zoom password>` 

the code will re-login into zoom.us/login to get the HTTP response `resp`, then the HTTP response will be decoded using `blackboxprotobuf.decode\_`message(resp)  function, which allow us to get the specific part that related to the remote key and user information. 

		resp\_decoded = blackboxprotobuf.decode\_message(resp)[0] 

		remote\_key = resp\_decoded['5']['95'].decode("utf-8")

## 2.Add-On Module:  Zoom Module  
The second tool in the repository composes the add-on modules. Downloading and placing it in the appropriate directory is all that's needed (the ingest module that run on Autopsy Version 4.18.0).

The second tool programmed by Jython 2.7.2 as an ingest module that run on Autopsy. The Investigators will enter both the **local key** and **remote key** fetched by the previous tool zoom_key.py . the module can extract artifacts from multiple users that use the same zoom application on the same device, one the investigator has all their remote keys. 
### 2.1 Genreate the Master Key: 
the inputs basically will create the secondary key from the provided local key and remote key, then the module will decrypt the databases and execute SQL queries to get all the interested evidences. 


### 2.2 Database Decryption:
the decryption process is devied into two parts: 
1. Decryption the basic database(zoom.us.enc.db and zoommeeting.enc.db) by the **local key**  
	`key = self.try_zoom_db_decryption( zoom_file_local_path_enc, zoom_file_local_path_dec, self.Local_Keys)`
2. Decrypting the profile-specific databases that withen the user folder that end with the @xmpp.zoom.us by the **Mater Key** then only take the databases that ends with .enks.db.the generating the **Master key** by calling this function 
		`self.try_zoom_db_decryption( zoom_file_local_path_enc, zoom_file_local_path_dec, self.Master_Keys)`
3. Integrity Check: After each parts of the decryption process there is an integrity check applied by return the local and the master key if decryption succeed and add it zoom_log_key folder along with the name of decrypted database.

### 2.3  Reporting and Interpretation process:

This is the part of the code that process information about recent used zoom profile. The presented artifacts are divided into six types:
for each artifact type a SQL Query generated to fetch the interested attributes’ contents from relevant database.

#### 2.3.1 Artifacts:
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

  #### 2.3.2 Example:Zoom Meeting Chat Artifact:
we will take Zoom Meeting Chat artifact as an example to show the reporting process:

1. we give this artifact and ID to refers to it in fetching process.

 `artID = blackboard.getOrAddArtifactType("TSK_ZOOM_MEETING_MSG", "Zoom Meeting Chats")`

2. Create result statement, to get all important evidence form the database tha has information about chat feature during a meeting.

`resultSet = stmt.executeQuery("SELECT confID, time, content, read, sender, receiver, senderName, receiverName from zoom_conf_chat_gen2_enc;")`

3. Define the properties of the Zoom Meeting Chats artifact, such as Conference ID,Time,Content, Read, Sender Name.and then add the relevant evidence for each attribute.

`attID_1 = blackboard.getOrAddAttributeType("TSK_ZOOM_MEETING_MSG_ID", BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Conference ID")`

`attribute_1 = BlackboardAttribute(attID_1, ZoomIngestModuleFactory.moduleName, confID).`







