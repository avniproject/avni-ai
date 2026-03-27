### As is:
<img width="279" height="339" alt="Image" src="https://github.com/user-attachments/assets/bf30f3d9-501f-4502-a728-11fca9124915" />

### AC:
- When someone interacts for setting up a program, answer something like below:
You can go about setting up program by uploading Field workflow specification. Here is a [sample field workflow specification document](https://docs.google.com/spreadsheets/d/1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8/edit?gid=262841117#gid=262841117). I can clarify any questions you have for filling this document.

- User should be able to download the linked document.
- When users asks clarifying questions, Avni AI assistant should be able to respond from knowledge base uploaded.
- User should be able to upload file from local filesystem by clicking + icon and send arrow should become enabled once the file is ready to be sent. On clicking send, file to be sent to AI assistant.

**Reference image with plus icon:**
<img width="360" height="674" alt="Image" src="https://github.com/user-attachments/assets/58d3b027-f086-43ab-81af-9fd2cb930a01" />

- From the  Field workflow specification, create location hierarchy, subject type, encounter types, and program. The format will not always be exact or same like in the above sheet. 
- On second time upload, should be able to update the entities.
- Should not recreate on second time upload, when already created
- For most of the things, AI assistant should be itself able to determine and create the needed entities. If not possible, can clarify with the user by asking questions.
- When processing is happening, we can show different progress messages like it appears in mobile app sync or in windsurf or v0 app or when you tell claude to create presentation when it is processing. And it needs to be blocking for users from sending next message.
- Confirming with the user before creating can lead to more flooding of data esp., for forms. So clarify with user only when uncertain.

### Out of scope:
Updating knowledge base to answer clarifying questions from user mentioned in 2nd AC point 