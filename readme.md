<p align="center">
  <img src="disappeer/images/logo_icon_large.png">
</p>

# Disappeer

#### Disappeer is a pure Python GUI application that provides:

* an interface to basic GPG functionality 
* peer-to-peer, GPG-encrypted messaging over Tor  

![gpg_tab](https://user-images.githubusercontent.com/38816908/40272041-b3b580a2-5b74-11e8-9e69-f37401bf62eb.png)

## Goals
Disappeer is experimental software.

The overarching goal of this project was to practice test-driven development of a non-trivial, pure Python GUI application, utilizing as few external libraries as possible, with an object-oriented design and a discrete number of worthwhile use cases, namely: access to basic GPG functionality and encrypted peer-to-peer messaging over TOR. A sub-goal was to create a decent-looking GUI interface using only the Python standard library's tkinter module. 

## Requirements

Disappeer has been developed and tested for use on Debian. To access all of Disappeer's functionality, your system must have:

* Python >=3.4, installed by default on Debian
* GPG, installed by default on Debian
* a properly configured, running Tor service

Disappeer requires three external Python libraries:

* **python-gnupg**: to provide access to GPG
* **stem**: to provide access to the TOR controller to proxy network servers with .onion addresses
* **PySocks**: to proxy network clients through the Tor service. 

Depending on your system, you may also need to install Python's `tkinter` module, if it is not included in your base Python package by default. 

It goes without saying that you should use a virtual environment if you opt to install Disappeer on your system.  

## TOR Configuration
Your TOR service must be properly configured so that disappeer can proxy through it. In your `torrc` file, you must have these two lines uncommented:

	ControlPort 9051
	CookieAuthentication 1

Remember to restart your tor service after updating your `torrc` file!

To access tor networking functionality, the user that runs `disappeer` from the command line must also be added to the debian-tor user group. For example:

	sudo usermod -a -G debian-tor YourUserName

After adding this user to the debian-tor group, you may need to log out, and then log back in, for the change to take effect.

## Installation
If you wish to install Disappeer, download the project. Then `cd` into outermost directory and run: 
	
	pip install -r requirements.txt
	pip install . 

Add the `-e` flag to the final install command above, as you may need to edit basic settings or configs, ex. your node's default home directory.

Then run from the command line with:

	disappeer

## Unit Test Suite
As stated above, Disappeer was created using a test-driven development methodology. Disappeer's test suite contains over 2400 tests, utilizing Python's built-in `unittest` framework. To run the test suite, after installing both the requirements and the project itself, `cd` into `disappeer/disappeer` and run:

	TESTING=1 python -m unittest

## License
GPLv3

##  Demo

### THIS IS STILL TODO
A prepackaged, fully-functioning instance of Disappeer can be found in the provided Debian VirtualBox virtual machine. To check out the demo:

* Download and unpack the virtual machine file. 
* Import the appliance to VirtualBox or any other suitable virtualization application.
* Start it up. 
* Log in (disappeer:disappeer). 
* Click the Disappeer icon on the desktop to launch the app.

***

# Overview
## GPG Functionality

Disappeer provides a graphical interface to basic GPG functionality such as:

* key creation
* key deletion
* key inspection
* encryption
* decryption
* key import
* key export
* message signing
* signature verification

## Messaging Functionality

Disappeer provides for peer-to-peer, GPG-encrypted messaging over Tor.

Message encryption, decryption, signing and verification are performed on the fly, transparently to the user, using the node's current **Host Key** and the **Host Key's Passphrase** stored in memory. 

All sent and received messages are encrypted with the public keys of both the sender and the receiver and stored on disk in ciphertext.

### The Contact Protocol
Disappeer maintains user/node identities on the basis of GPG public/private key pairs.

Contacts between peer nodes are established by exchanging their respective GPG public Host Keys, and network addresses, over three separate network servers, each of which is proxied by a different Tor .onion address. 

Two-way peer contacts are established by completing a request/response/message protocol between two nodes that are both online. Assuming both Alice and Bob have created Host Keys for their respective nodes, and both have started their network services and Tor proxies:

1. Out of band, Alice publicizes the .onion address of her node's request server.
2.  Bob sends a contact request to Alice's request server .onion address.
3. Alice is notified of the request in her contact request list.

	3.5. Alice accepts the request. 
		
4. Bob is notified of Alice's response, and Alice is added to Bob's peer contacts list.
5. Bob sends Alice a message, and once that message is received, Bob is then added to Alice's peer contacts.
6. Alice can now send a message to Bob.

Disappeer allows for the creation of an arbitrary number of user identities via the creation of new GPG **Host Keys**, as well as an arbitrary number of Tor .onion address sets.

It also allows for the use of persistent Tor .onion address keys that can be associated with specific user identities. 

# The Interface
Some general info on the GUI interface.

![gpg_tab](https://user-images.githubusercontent.com/38816908/40272041-b3b580a2-5b74-11e8-9e69-f37401bf62eb.png)

## Main Console
The main console contains a toolbar and a text entry field. 

### The Toolbar

The first three **icon buttons** in the toolbar allow you to: 

* save the current text in the text area to a file;
* open a file and display its contents in the text area;
* clear all contents from the console text area. 

The next item in the console toolbar is a **Public Key** dropdown menu that lists the keys from the key ring in the current home directory. Following that is the **Function** dropdown menu that provides access to GPG functionality, namely: encrypt, decrypt, import, export, sign, and verify. 

To run the selected function, click the final icon in the toolbar, the **gear icon**. 

Here is a rundown of the basic functions:

* Encrypt: this function encrypts the current text in the console with the public key selected from the console key dropdown menu.

* Decrypt: this function decrypts the current ciphertext in the console, provided the current key ring contains the corresponding secret key for which the plaintext was encrypted; clicking decrypt launches a popup to provide the decryption passphrase.

* Import: if the console contains the text of a GPG public key, this function will import that key into the current key ring.

* Export: this function exports the GPG public key for the key selected from the dropdown menu, and displays it in the console.

* Sign: this function will prompt for a passphrase and sign the current console text with the primary secret key for the current key ring, provided of course that a secret key exists in the current key ring and the passphrase is correct.

* Verify: this function verifies whether the current console text contains a valid GPG signature, which it checks against the public keys in the current key ring.

## The Left Sidebar
The left sidebar contains a number of tab views that provide access basic functionality, such as:

* GPG: GPG key management
* Net: Start/Stop Networking Services
* Net: Start/Stop Tor Proxies
* Requests: Sent and Received Peer Requests
* Messages: Sent and Received Messages
* Messages: Peer Contacts

## GPG Tab
You can access basic GPG key management functionality under the GPG tab in the left sidebar.

![gpg_tab](https://user-images.githubusercontent.com/38816908/40272041-b3b580a2-5b74-11e8-9e69-f37401bf62eb.png)

### Home Directory

Under the GPG tab, select your desired home directory for your node's key ring by clicking the **Home Entry Field**, or simply use the default directory. If no key ring exists in this directory, an empty key ring will be created when it is selected. 

Create a new key by clicking the **New Key** button below and filling out the popup form with the necessary info. This key will become the default identity (i.e. the **Host Key**) for the node. If a directory is selected that already contains a key ring with a secret key, the first secret key in that ring will become the current **Host Key** for the node. 

When a new **Home Directory** with corresponding **Host Key** is selected, the application will prompt you to supply the passphrase for the **Host Key**. This passphrase is stored in memory to provide on-the-fly encryption, decryption, signing and verification for Disapeer's peer-to-peer messaging functionality. 

If you decline to provide the passphrase, you will not be able to run a network session. You can set the passphrase at any time by clicking the **Set Passphrase** button and entering the passphrase in the popup.

### Key Info

You can inspect the keys in the currently selected key ring by selecting a given key from the **Public Keys** dropdown list and then clicking **Key Info**.

### Manage Keys
Create a new key by clicking the **New Key** button, filling out the popup form and clicking the **Create** button. Some default values are supplied. Note that key creation may take some time, depending on your hardware. 

Delete a key from the current key ring by clicking the **Delete Key** button, checking the desired key for deletion in the popup check button list, and then clicking **Delete**. This action cannot be undone!

## Network Tab

The network tab provides and interface to networking functionality.

![network_tab](https://user-images.githubusercontent.com/38816908/40272056-e0acb882-5b74-11e8-956a-2da44664b0af.png)

### Network Services
A Disappeer node runs three different network servers for contact requests, contact responses and messages. You can start and stop the node's servers by clicking **Start** and **Stop** in the **Network Services** frame. Note, these servers only listen on the loopback interface. Traffic is routed to these servers by the Tor proxy. 

### Tor Proxies
Start and stop the Tor proxies for those servers by clicking **Start** and **Stop** in the **Tor Proxy** frame. 

To create a set of persistent Tor .onion addresses for the current Host Key, check the **Persistent** option before starting the proxies. 

If a set of persistent .onion addresses has already been created for the current **Host Key**, those addresses will be resumed if the **Persistent** option is checked when you click **Start**. 

If **Persistent** is not selected, a set of ephemeral Tor .onion addresses will be created for the current session. 

Once the hidden services have been establshed, the display will show the Tor .onion proxy address for all three network servers: request, response and message. 

For most use cases, end users really only need concern themselves with the address for a node's request server. To send a message to another node, you must first complete the entire request/response/message protocol, which begins by sending or receiving a **Contact Request**. 

To allow someone to send you a contact request, provide them with the .onion address of your **Request Server**. Both nodes must be online at the same time to successfully complete the request/response/message protocol. 

Both nodes must be online at the same time to successfully send/receive messages after a two-way contact is established.  

## Requests Tab
The requests tab provides functionality to contact network peers.

![requests_tab](https://user-images.githubusercontent.com/38816908/40272059-fc6de456-5b74-11e8-9142-92ee8ef02d71.png)

### Contact Requests

To send a contact request to a remote peer, click **New Contact Request** and enter the .onion address of the peer's **Request Server** in the popup menu. If the peer provides a port different from the default, enter that too. Click **Send**. 

If the request successfully reaches the remote peer, the request will appear in your **Sent Requests** list. If and when the remote peer accepts your request, this listing will disappear from your **Sent Requests** list, and the peer's **Host Key** user info will be added to the **Contacts** list under the **Message** tab.

If someone sends you a peer request, this request will appear under the **Received Requests** list. Click the Received Request item. This will launch a popup with the requester's key info. If you accept the request, and the peer is online, this listing will disappear, and the peer's key will be imported to your current **Key Ring**. The remote peer will now be able to send you a message. 

When you receive your first message from that peer, they will be added to your **Contacts** list, and you will be able to send a message to them. 

## Messages Tab

The messages tab provides access to sent and received messages and to your peer contacts list.

![messages_tab](https://user-images.githubusercontent.com/38816908/40272070-3ab71bba-5b75-11e8-9a64-ed6bd9e1875e.png)


### Sent and Received Messages
When someone sends you a message, that message will appear under the **Received** heading in the **Messages** frame. Click the item, and it will display the message in a popup. When a peer sends you a message for the first time, that peer will be added to the **Contacts** list below.

### Contacts

Once you have successfully established a contact with a remote peer, the peer will be listed in your **Contacts** list. Click on an individual contact to see info on the peer. 

To send a message to a peer, type your message into the console text area. Click the peer's contact listing in your **Contacts** list. In the popup, click **Send**, then confirm the **Send**. 

If the message is succeessfully sent, your sent message will be appended to your **Sent Messages** listing in the Messages frame. When you receive a message, it will appear in the Received messages listing in the Messages frame. 


