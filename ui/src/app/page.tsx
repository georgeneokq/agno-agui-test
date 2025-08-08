
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat, CopilotKitCSSProperties } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit" 
      agent="investment_advisor_team"
    >
      <div style={
        {
          "--copilot-kit-primary-color": "#6366f1",
        } as CopilotKitCSSProperties
      }>
        <CopilotChat
          className="w-full h-[100vh]"
          labels={{
            title: "Multiagent",
            initial: "Hey there, feel free to state a company you would like me to research on. (e.g. Tesla)"
          }}
        />
      </div>
    </CopilotKit>
  )
}
