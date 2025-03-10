const express = require('express');
const { default: agent } = require('./agent');
var messages_1 = require("@langchain/core/messages");
// const agent = require('./agent.js');
const app = express();
const PORT = 3000;

// Middleware for parsing JSON and URL-encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route for handling all paths
app.all('*', async (req, res) => {

  response = await agent.invoke({ messages: [new messages_1.HumanMessage("My business creates websites for new businesses, every page should have an input field that sends a get request with the value entered in the field as a url parameter and redirect the page with that url. there should always be a navigation bar on top with appropriate links. Can you generate a html page for my business for path "+req.path+", use the query parameter to figure out what the client is looking for and create fake page for that, all the output should be a legally valid HTML string with js and css embedded in the page source as html, no text at all")] }, { configurable: { thread_id: "42" } });
  let content = response.messages[response.messages.length - 1].content;
  content = content.substr(content.indexOf("<!DOCTYPE html>"),content.lastIndexOf("```")-3);
  
  console.log(content);
  console.log(content.lastIndexOf("```"));
  console.log(content.length);
  res.end(content);
//   res.status(200).json({
//     message: 'This route handles all paths!',
//     method: req.method,
//     path: req.path,
//     query: req.query,
//     body: req.body,
//   });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
