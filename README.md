# CDL Hashtag Subsystem

This project is an extension of the Community Digital Library. It implements the following features/components of a hashtag subsystem:
- Hashtag database
- Automatic hashtag extraction from unstructured text
- Hashtag disambiguation/recommendation

The backend is located in the root directory, and the `webapp` dir contains a webapp for demo.

## Usage

In the root dir run
```
flask --app server run
```
to start the backend server.

In the `webapp` dir setup the React webapp with Next.js and run `npm run dev`