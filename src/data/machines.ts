export type Machine = {
  slug: string;
  name: string;
  goal: string;
  description: string;
  kpi: string;
  signal: string;
  decision: string;
  detail?: {
    context: string;
    inputs: string[];
    signals: string[];
    decisions: string[];
    measurement: string;
    owner: string;
    guardrail: string;
    ifRejected: string;
  };
};

export const machines: Machine[] = [
  {
    slug: "revenue-recovery",
    name: "Revenue Recovery",
    goal: "Recover sales lost to operational gaps.",
    description: "Finds stockouts, supplier delays, and allocation gaps while there is still time to act.",
    kpi: "Recovered revenue",
    signal: "Inventory cover falls as demand rises",
    decision: "Reallocate stock or accelerate replenishment",
    detail: {
      context: "A retailer can have inventory in the network and still lose sales where demand is strongest. This machine connects store, SKU, inventory, supplier, and sales context so an operator can act on the gap.",
      inputs: ["Store and SKU sales", "Inventory and replenishment", "Supplier fill rates", "Demand and promotion plans"],
      signals: ["Fast-moving SKU below cover threshold", "Supplier fill rate deteriorating", "Demand spike in a constrained region"],
      decisions: ["Move inventory from lower-velocity stores", "Accelerate replenishment or escalate a supplier", "Pause a promotion where stock cannot support demand"],
      measurement: "Compare recovered sales and stockout rate with a pre-action baseline over an agreed window, accounting for demand and seasonality.",
      owner: "A merchandising or supply-chain owner reviews inventory and supplier actions before execution.",
      guardrail: "A transfer cannot take the sending store below its agreed inventory-cover floor; supplier escalations follow the approved sourcing policy.",
      ifRejected: "The proposed transfer stops. The owner records why, then requests another option or changes the threshold for review.",
    },
  },
  {
    slug: "collections",
    name: "Collections",
    goal: "Improve recovery from overdue accounts.",
    description: "Prioritizes accounts and field actions using repayment, risk, and intervention history.",
    kpi: "Collection rate",
    signal: "Broken promises to pay increase",
    decision: "Change contact strategy or assign a visit",
    detail: {
      context: "Collections teams need to decide which account needs attention, why, and which intervention is likely to help. This machine works from customer, loan, repayment, field visit, and branch context.",
      inputs: ["Loan and repayment history", "Promise-to-pay records", "Field visit completion", "Branch and risk segments"],
      signals: ["Roll-forward rate rises", "Promise to pay is broken", "High-value overdue accounts have no completed visit"],
      decisions: ["Prioritize an account for contact", "Assign a field officer or escalate to a branch manager", "Review a change in contact or settlement strategy"],
      measurement: "Track collection rate, promise-to-pay kept rate, and recovery per intervention against a baseline for the same account segment.",
      owner: "A collections or branch operations owner approves account reassignment and customer-facing interventions.",
      guardrail: "Account contact and reassignment follow approved customer-treatment rules, role permissions, and capacity limits.",
      ifRejected: "No customer-facing workflow starts. The owner records the reason and can request a different intervention.",
    },
  },
  {
    slug: "customer-retention",
    name: "Customer Retention",
    goal: "Keep customers at risk of leaving.",
    description: "Connects service, engagement, and renewal signals to a timely retention decision.",
    kpi: "Retention rate",
    signal: "Renewal risk rises in a customer segment",
    decision: "Prioritize a service or renewal intervention",
  },
  {
    slug: "sales-productivity",
    name: "Sales Productivity",
    goal: "Improve conversion across the sales team.",
    description: "Separates lead quality, follow-up, coaching, and territory effects before recommending a change.",
    kpi: "Lead-to-sale conversion",
    signal: "Conversion falls despite steady activity",
    decision: "Adjust coaching or lead allocation",
    detail: {
      context: "A leaderboard shows who is behind. This machine investigates whether the gap comes from lead quality, follow-up, coaching, or territory conditions before suggesting an intervention.",
      inputs: ["Leads and opportunities", "Activity and follow-up timing", "Manager coaching records", "Territory and account context"],
      signals: ["Conversion falls while activity remains steady", "Follow-up time exceeds the agreed SLA", "Performance diverges across comparable lead segments"],
      decisions: ["Create a targeted coaching plan", "Reassign high-fit leads", "Review territory or manager support"],
      measurement: "Measure conversion and pipeline velocity before and after the intervention for comparable reps and lead segments.",
      owner: "A sales manager approves lead, territory, or coaching changes and owns follow-through.",
      guardrail: "Lead changes respect territory rules, account ownership, and agreed limits on rep capacity.",
      ifRejected: "The current assignment remains in place. The manager records the objection and can request a revised recommendation.",
    },
  },
  {
    slug: "branch-performance",
    name: "Branch Performance",
    goal: "Improve performance across locations.",
    description: "Finds where branch outcomes diverge and which operating practices may explain the gap.",
    kpi: "Outcome per branch",
    signal: "Comparable branches begin to diverge",
    decision: "Investigate staffing or operating practice",
  },
  {
    slug: "procurement",
    name: "Procurement",
    goal: "Reduce avoidable supply and spend loss.",
    description: "Connects demand, price, supplier reliability, and inventory to sourcing decisions.",
    kpi: "Cost per supplied unit",
    signal: "Supplier fill rate deteriorates",
    decision: "Escalate or shift supply allocation",
  },
];
