# PRD: AI Triage & Auto-Resolve

**Status:** Draft  
**Owner:** Product Team  
**Last updated:** 24 August 2026  
**Product:** SmartDesk, an existing customer support platform

## 1. Background

SmartDesk is an established helpdesk platform already used by support teams to manage tickets from email and chat in a unified inbox. Agents currently triage and respond to every ticket manually. This PRD covers a new feature, an AI agent embedded into the existing ticket pipeline, rather than a new product. It builds on SmartDesk's current inbox, ticket data model, and agent permissions rather than replacing them.

## 2. Problem statement

Within the existing SmartDesk workflow, agents spend a disproportionate amount of time on repetitive, low-complexity tickets such as order status checks, password resets, and subscription cancellations that do not require human judgement. This slows first-response time on every ticket, including those that need a human. Customers have also asked, via existing CSAT surveys, for faster resolution on simple requests.

## 3. Goals and objectives

- Reduce average first-response time across the existing ticket queue by 50% within two quarters of launch.
- Have the new AI agent autonomously resolve at least 30% of incoming tickets, without requiring changes to how agents work on the remaining 70%.
- Ship as an opt-in feature toggle within existing SmartDesk workspace settings, so current customers can enable it without a migration.
- Maintain existing CSAT levels or better.

## 4. Target users

- **Existing SmartDesk support agents:** Keep their current inbox and workflow. The feature should reduce their queue, not add new tools they must learn to use for every ticket.
- **Existing SmartDesk admins and team leads:** Need a way to turn the feature on, configure which ticket types the AI agent may resolve, and monitor its impact.
- **End customers of SmartDesk's customers:** Continue using the same email and chat channels, with no new customer-facing surface.

## 5. Scope

### In scope

- A new AI Auto-Resolve toggle in the existing SmartDesk workspace admin settings.
- Ticket classification by intent and urgency, running on tickets already flowing through the current inbox.
- Autonomous resolution for a configurable allow-list of ticket types, starting with order status, password reset, and subscription cancellation confirmation, using SmartDesk's existing internal APIs for those lookups.
- AI-drafted reply suggestions surfaced inside the existing ticket view for tickets the agent does not resolve outright.
- A new panel in the existing manager dashboard showing AI-resolved versus human-resolved volume.

### Out of scope

- Any change to SmartDesk's core inbox UI, ticket data model, or existing integrations.
- New channels such as social or phone. The AI agent acts only on channels SmartDesk already supports.
- Billing disputes, account security, or any ticket type not explicitly allow-listed by the admin.
- Non-English tickets, matching current SmartDesk language support.

## 6. Functional requirements

### Integration with the existing pipeline

- The AI agent runs as an additional step in the existing ticket ingestion pipeline. Tickets are unaffected if the feature is toggled off.
- It uses SmartDesk's existing customer and ticket-history data already available to human agents. No new data sources are required for v1.

### AI agent behaviour

- Classifies each incoming ticket by intent, urgency, and confidence.
- For ticket types on the admin's allow-list with high confidence, resolves and replies directly using existing internal APIs for order lookup, account reset, and subscription management.
- For everything else, routes to the existing human queue as today and attaches a suggested draft reply in the ticket view.
- Records every autonomous resolution in the existing audit trail used for compliance today.
- Retains the existing “talk to a human” escalation path in SmartDesk's chat and email flows.

### Admin controls

- Toggle the feature on or off per workspace.
- Choose which ticket types are eligible for autonomous resolution from a predefined list.
- Set a confidence threshold below which tickets always go to a human.

### Agent-facing changes

- Tickets resolved autonomously appear in the existing inbox as closed, tagged “Resolved by AI”, and remain editable and reopenable like any other ticket.
- Draft reply suggestions appear as an optional accept, edit, or reject action on tickets already in an agent's queue, with no new screen.

### Reporting

- Add metrics to the current manager dashboard: percentage of tickets resolved by AI, first-response time before and after, and CSAT split by resolution source.

## 7. Non-functional requirements

- Must not increase load or latency on SmartDesk's existing ticket ingestion pipeline beyond an agreed threshold, for example under 500 ms added per ticket.
- AI-generated responses must arrive within five seconds.
- All autonomous actions must be logged through SmartDesk's existing audit and compliance system, with no new logging infrastructure.
- The feature must degrade gracefully. If the AI service is unavailable, tickets fall back to the current all-human routing with zero disruption.
- No changes to existing data retention or privacy commitments already made to SmartDesk customers.

## 8. Success metrics

- First-response time at workspace level, before versus after enabling the feature.
- Percentage of tickets autonomously resolved by the AI agent, with a target of at least 30%.
- CSAT split by AI-resolved versus human-resolved, compared with each workspace's existing baseline.
- Feature adoption: percentage of existing SmartDesk workspaces that enable the toggle within 90 days.
- Escalation and override rate: how often agents or customers reject an AI resolution or reopen an AI-closed ticket.

## 9. Risks and assumptions

- **Risk:** The feature erodes trust if AI mis-resolves a ticket the customer considers unresolved. **Mitigation:** Use a conservative default confidence threshold, easy reopening, and an admin-controlled allow-list that starts narrow.
- **Risk:** Existing agents distrust or ignore AI-drafted suggestions. **Mitigation:** Make the feature opt-in per workspace and share adoption data from early workspaces.
- **Assumption:** Existing internal APIs for order lookup, account reset, and subscription management expose enough structured data for the AI agent to act reliably without new integration work.
- **Dependency:** The feature ships as an addition to the current SmartDesk release train, not a separate product launch. No new onboarding flow is needed for existing customers.

## 10. Rollout plan

- **Phase 1:** Internal dogfooding on SmartDesk's own support workspace.
- **Phase 2:** Opt-in beta with three to five existing customer workspaces, with the allow-list limited to one ticket type: order status.
- **Phase 3:** General availability as a toggle for all existing workspaces, with the full allow-list.
- **Phase 4:** Expand the allow-list based on observed accuracy and admin demand.
