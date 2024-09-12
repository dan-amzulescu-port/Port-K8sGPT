## Supercharging Your Internal Developer Portal with K8s AI

Integrating AI-driven insights into your Kubernetes workflow can significantly streamline incident response, minimize manual tasks, and empower DevOps teams to tackle issues more efficiently—all from within a seamless developer portal experience.

In the high-pressure realm of DevOps and Site Reliability Engineering (SRE), rapidly identifying and resolving issues is a perennial challenge. Engineers often navigate a maze of commands, logs, and dashboards, each necessitating a unique approach. This fragmented methodology not only delays resolutions but also increases the probability of human error. As the DevOps landscape grows more complex, platform engineering has emerged as a critical discipline, with the Internal Developer Portal (IDP) increasingly seen as the holy grail of streamlined operations. For the uninitiated, an IDP offers a centralized, focused approach to managing infrastructure and deployments. (Learn more about IDPs here.)

However, there's room to make IDPs even more effective by incorporating AI, which can reduce the time engineers spend on processes that are both labor-intensive and prone to mistakes. In this blog entry, I'll walk you through a straightforward example of how leveraging AI can accelerate issue resolution, all displayed within the single pane of glass provided by the IDP. While this example focuses on a specific domain expert—Kubernetes (K8s)—it merely scratches the surface. In more advanced scenarios, AI can broaden its scope to assist across multiple domains such as cloud infrastructure and applications, where issues often span different layers of the stack. Our ultimate aim extends beyond equipping AI to manage multiple domains; we want to empower it to fully automate the remediation process, resolving issues independently.

With that visionary goal in mind, let's start with fundamental steps and explore how a single-domain workflow can enhance efficiency.

### Introducing K8sGPT

This is where K8sGPT comes into play. Designed specifically for Kubernetes environments, K8sGPT illuminates the often challenging process of troubleshooting within this domain. While Kubernetes is just one piece of a much larger puzzle, K8sGPT offers valuable insights that can significantly cut down the time spent on issue resolution. By integrating K8sGPT with your IDP, you can streamline your troubleshooting efforts while maintaining the overarching visibility needed for higher-level oversight.

### Diving into the Nuts and Bolts

Let’s explore the key components that make this integration possible:

#### Key Components

1. **Internal Developer Portal (IDP):** A centralized platform that streamlines access to developer tools, resources, and workflows, aiding in managing and scaling operations across your team.
   
2. **Kubernetes (K8s):** The backbone of container orchestration, managing the deployment, scaling, and operation of application containers across clusters of hosts.
   
3. **K8sGPT:** A command-line interface allowing DevOps engineers to interact with Kubernetes and trigger analyses directly from the terminal. It also serves REST and GRPC API access.
   
4. **AI Language Learning Model (LLM):** The core intelligence behind K8sGPT, leveraging natural language processing to interpret Kubernetes data and provide actionable recommendations.
   
5. **Communication Facilitator:** Crucial in bridging the gap between IDP and K8sGPT, ensuring that commands, queries, and insights flow seamlessly between these systems. Depending on your organization's security and compliance requirements, several secure and less secure methods can establish this communication.

### Connecting the Components

#### Prerequisites:
- A K8s cluster
- An IDP dynamically populated with K8s component health status

#### Step-by-Step Integration:

1. **Deploying K8sGPT:**
   - K8sGPT can be deployed both outside and in-cluster. To deploy the K8sGPT REST API server, follow the [Installation Guide].
   - To serve REST API: `k8sgpt serve --http`
   - Follow the guide for in-cluster deployment.

2. **Deploying/Configuring LLM:**
   - K8sGPT supports 11 different types of AI backends.
   - Tested with Ollama; follow the instructions to download a model.
   - Configure K8sGPT to use Ollama: `k8sgpt serve --http -b openai`

3. **Preparation of IDP:**
   - Ensure the IDP can both ingest K8sGPT insights and notify health status to a Kafka topic via an automated workflow.
   - JSON representation of a K8s workload blueprint (link to GitHub).
   - Automation triggered by health status change, sending a message to a Kafka topic with all relevant information (link to GitHub).

4. **Communication Facilitator:**
   - For this proof of concept (POC), a simple Python "Facilitator" was created to:
     - Listen continuously to the Kafka topic.
     - Poll K8sGPT for insights when a relevant message is received.
     - Populate K8sGPT insights for the relevant K8s workload.

Now that we have assembled all components, let's visualize the flow of events:

1. A K8s integration updates the IDP with the health status of a workload.
2. An automated workflow issues a message to a Kafka topic.
3. The Python script picks up the message data.
4. The Python script polls K8sGPT for insights.
5. K8sGPT communicates with the K8s cluster and AI.
6. K8sGPT replies to the script with insights.
7. The Python script leverages the IDP API to populate the workload entity with insights on how to fix the issue.

#### Example

Here’s an example of what K8s AI insights look like within the IDP.

### Points Worth Mentioning

1. The flow of events could be simplified in various ways—such as bypassing the entire process of triggering K8sGPT through an event, instead modifying the script to continually monitor the cluster's health and distribute insights autonomously.
2. The command-line outputs and overall refinements currently outperform the outputs provided via the REST API, necessitating some additional modifications to improve REST API-generated output.

### Summary

- Debugging and resolving issues often consume significant time and involve error-prone manual processes for engineers.
- Reducing time-to-resolution is crucial for enhancing service quality and allowing teams to focus on innovation.
- Internal Developer Portals (IDPs) significantly contribute to reducing time-to-resolution by offering refined, contextual information.
- IDPs can be further enhanced by leveraging AI insights across various domains.
- The ultimate goal is to achieve cross-domain insights and automated remediation, thereby streamlining problem-solving processes.

By following these steps, you can integrate powerful AI-driven insights into your developer portal, making your DevOps practice more efficient and reliable.