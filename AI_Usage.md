AI Assistance
=============
This page will document all uses of AI assistance per the requirements. 

Note that I have an extension installed in my browser to block Google's incredibly annoying and incompitent AI Overview. For the purposes of this document, anything from research to ideas to code generated in whole or in part by ChatGPT, CoPilot, or any other AI assistance will be tracked. 

However, general research (Google, StackOverflow, Reddit, etc...) will not be tracked as it does not fall into the scope of AI despite how much overlap there is in their particular use cases in recent years.

Uses
----
* Used ChatGPT to diagnose an issue where the version of Python being used in my VS Code terminal worked just fine to execute the `CV2DisplayVideo.py` example, but the build in `Execute` button in VS Code did not. Turns out the issue was just which Python interpreter VS Code (rather than the terminal) was pointing to. Went ahead and just made a venv to keep things simple.

* Used ChatGPT to diagnose why the bounding boxes for the masked version of the video feed were showing up as black, instead of colored. Turns out it was because the entire video channel was actually set to grayscale. I just had to convert the channel back to a color friendly channel setting.