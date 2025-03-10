import { tool } from "@langchain/core/tools";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { z } from "zod";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { MemorySaver } from "@langchain/langgraph";
import { HumanMessage } from "@langchain/core/messages";

const agentCheckpointer = new MemorySaver();



// Define your tool
const fakeBrowserTool = tool(
  (_) => {
    return "The search result is xyz...";
  },
  {
    name: "browser_tool",
    description:
      "Useful for when you need to find something on the web or summarize a webpage.",
    schema: z.object({
      url: z.string().describe("The URL of the webpage to search."),
      query: z.string().optional().describe("An optional search query to use."),
    }),
  }
);

const agentTools = [];
const llm = new ChatGoogleGenerativeAI({
  model: "gemini-pro",
});

const agent = createReactAgent({
  llm: llm,
  tools: agentTools,
  checkpointSaver: agentCheckpointer,
});

async function testing(){

// Now it's time to use!
// const agentFinalState = await agent.invoke(
//   { messages: [new HumanMessage("what is the current weather in sf")] },
//   { configurable: { thread_id: "42" } },
// );

// console.log(
//   agentFinalState.messages[agentFinalState.messages.length - 1].content,
// );

// const agentNextState = await agent.invoke(
//   { messages: [new HumanMessage("what about ny")] },
//   { configurable: { thread_id: "42" } },
// );

// console.log(
//   agentNextState.messages[agentNextState.messages.length - 1].content,
// );
}

export default agent;
testing();
