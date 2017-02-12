# jklhoods
A livestream program, which streams jyväskylä-themed posts from Instagram and Twitter to to webpage at http://jklhoods.herokuapp.com/ . 
Program is currently not active. This project has 3 contributors in total and it was made as a university project.

To deploy a service like this on Heroku or local machine, you will need access tokens, client IDs and client secrets, which you can get through 
Twitter and Instagram accounts. To deploy it locally, you can use services like Localtunnel. For example, lt --port 8000 --subdomain nzmpqlpmhe
exposes localhost to web address https://nzmpqlpmhe.localtunnel.me/realtime . This can be used as a callback address to run the stream. In any case, 
the callback address must be an address, which Twitter and Instagram APIs can reach.
