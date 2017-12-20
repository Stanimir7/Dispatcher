# Johan Burke

## Clover Android App
In the beginning, the project was implemented as an android app for Clover.  I worked with Jake to develop the frontend functionality for the android app itself.  My contribution for this part was the "logic" portion of the app, creating all connections from the clover app to the server.

## Design Document Contributions
I authored summaries for the behaviors of each portion of the android app.

## OAuth/Clover interfacing
During both the android app and web app phases of our project, interfacing with Clover, especially for authentication, was necessary.  I implemented the endpoints and functionality necessary for our web app to comply with the specifications for authentication with Clover.  These include redirecting to the Clover sign-in page when insufficient authentication information is provided, ensuring each endpoint checks for the necessary information, and obtaining an auth token from Clover when the authentication information is provided.

## Smooth Redirects
As part of the polish phase, I implemented redirects so that there are no "dead ends" in navigating between individual web pages of the project.  These include replacing all error messages with pages that redirect back to the field pages the error originated from, etc.

## Logout Function/Cookies
As a second part of the polish phase, I implemented two pieces of functionality:
* Logout Button that clears the current session authentication information and returns the user to the home page
* Cookies that allow a smooth user experience without having to log in too often or see the Clover redirect page in between each page navigation.

## Git branch management
As our project required multiple features, we adopted the workflow of using a branch for each new feature.  This resulted in a complex network of branches on our Github repository, and I was reponsible for ensuring they were merged and for resolving any conflicts that occurred when attempting to merge.
