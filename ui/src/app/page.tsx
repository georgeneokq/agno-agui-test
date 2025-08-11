"use client"

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotChat, CopilotKitCSSProperties } from "@copilotkit/react-ui";

interface AgentState {
  latest_stock_price: number
}

export default function Home() {

  const { state } = useCoAgent<AgentState>({
    name: "investment_advisor_team",
    initialState: {
      "testing": "test"
    }
  })

  // useCopilotAction({
  //   name: "set_is_loading",
  //   description: "When user says to start loading, trigger this action.",
  //   parameters: [
  //     {
  //       name: "is_loading",
  //       type: "boolean",
  //       description: "Loading or not",
  //       required: true
  //     }
  //   ]
  // })

  console.log(state)

  return (
      <div style={
        {
          "--copilot-kit-primary-color": "#6366f1",
        } as CopilotKitCSSProperties
      }>
        <div className="grid grid-rows-2 space-y-4 h-[100vh]">
          <CopilotChat
            className="w-full"
            labels={{
              title: "Multiagent",
              initial: "Hey there, feel free to state a company you would like me to research on. (e.g. Tesla)"
            }}
          />

          {/* For viewing state */}
          <div className="w-full p-4">
            <span>State: { JSON.stringify(state) }</span>
          </div>
        </div>
      </div>
  )
}
