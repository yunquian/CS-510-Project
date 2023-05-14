# CDL Hashtag Subsystem (backend)

This project is an extension of the Community Digital Library []()

The backend is a server that interacts with the CDL Chrome extension.

The server consists of the following parts:
- request handler (unimplemented): receives and handles the requests, calls core functions of the hashtag subsystem
- core functionalities
  - concept extraction
    - for highlighted text
    - for document text
  - keyword search in db
- database