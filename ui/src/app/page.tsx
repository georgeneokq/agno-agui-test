"use client"

import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat, CopilotKitCSSProperties } from "@copilotkit/react-ui";

export default function Home() {

  const { state } = useCoAgent({
    name: "investment_advisor_team",
    initialState: {}
  })
  console.log(state)

  return (
      <div style={
        {
          "--copilot-kit-primary-color": "#6366f1",
        } as CopilotKitCSSProperties
      }>
        <div className="flex flex-col gap-y-2 h-[100vh]">
          <div className="flex flex-col gap-y-2 p-8">
            <span>Watch the agent state being updated in real time!</span>
            <span>Agent's state:</span>
            <span>
              {JSON.stringify(state, null, 4)}
            </span>
          </div>
          <CopilotChat
            className="w-full h-full"
            labels={{
              title: "Multiagent",
              initial: "Hey there, feel free to state a company you would like me to research on. (e.g. Tesla)"
            }}
          />
        </div>
      </div>
  )
}
