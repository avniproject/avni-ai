# Avni AI Assistant Test Cases

| Tests | Issue | Conversation ID for Reference | Status |
|-------|-------|------------------------------|--------|
| Basic questions | RAG does not work for:<br>• what are catchments?<br>• what are user groups?<br>• what is an identifier source?<br>• what is phone verification<br>• what is documentation<br>• what is the use of the broadcast dabba in this screen? | | Fixed |
| User Experience | App should personally greet the user | | |
| User Experience | App should keep history based on username | | |
| Configuration Management | Deleting config should be manual - currently it is triggered whenever something goes wrong | | |
| Subject Type Recognition | If a subject type already exists, then it is not recognized | | |
| Group Creation | Creating a group for an existing subject type fails | e939491c-0905-4523-8dbe-040508977f34 | |
| Subject Type Attributes | Every time, the chat asks for attributes in the subject type while we know they are not useful since they are not getting created | | |
| Configuration Error | Creating the config failed - grouprole error | 625051f7-4111-4ebd-932c-f56b866bb102 | |	