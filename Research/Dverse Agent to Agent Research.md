# Dverse Agent to Agent Research
In the sixth semester at Fontys, we are creating a group project called [Dverse](https://fuas-dverse.github.io/). The main goal of this project is to create a system where different agents can work together. Our individual is creating one or more of those agents that can complete tasks in the group project's system. To get a better understanding of how we want to create this platform, it is crucial to research certain aspects of this project as best as possible. This research will be written for one of these research questions.

## Research
What technology should the system use to enable dynamic interaction between agent to agent?

### Context
While starting this research, So far we already have had two sprint delivery's and also two functioning prototypes. The first sprint delivery was a very hard coded approach. It worked by having a set route between the endpoints of agents. The second prototype was already a little more dynamic, it includes a message bus where messages will be sent to that can be consumed by agents.

Our next step is to figure out how to achieve a good architecture where agents can communicate with agents, as this is not yet the case. With the current prototype it is only possible to send a request or prompt to the system and the system then handles the agents.

For our final prototype, this is not an ideal solution, as the ideal solution could have a conversation going on that last for an infinite amount of time. Only then have we set up the project as intended. Of course, this is not the right way, but once we have this, we could look at when the conversation will stop.

### Library

#### Literature Study
For this question, I first want to look into some ways applications can communicate with each other. Not necessarily meaning how to do this dynamically but in general.

##### Interaction between applications
[The Power of APIs](https://medium.com/@tonydain9_78432/the-power-of-apis-simplifying-interactions-between-applications-4696f6448c7)
- Communication
	- An API is a set of rules and protocols that allows different software applications to talk to each other and share information. It abstracts the underlying complexity, making it easier for developers to integrate functionalities from other systems seamlessly.

##### Communication between decoupled software applications”
[Decoupled Architecture & Microservices](https://medium.com/@saurabh.engg.it/decoupled-architecture-microservices-29f7b201bd87)
- Architectures
	- **Microservices Architecture**: Within this approach, the system is made of small, independent services that communicate over a network.
	- **Event-Driven Architecture**: Withing this architecture, components communicate through asynchronous events. When a change/event is triggered in a component, other components can listen and respond accordingly.
	- **Service-Oriented Architecture**: This involves designing software as a collection of services that communicate through standardized interfaces.
	- **Plugin-Based Architecture**: Software applications with plugin-based architectures allow third-party modules or plugins to be added or removed without affecting the core functionality of the application. 

[Micorservices: Intra-service communication](https://medium.com/@saurabh.engg.it/micorservices-intra-service-communication-de6265c7e820)
- Communication
	- **Synchronous & Asynchronous**
		- Synchronous communication involves real-time exchange of information between two or more services, typically facilitated by REST APIs. However, it necessitates all involved microservices to be operational continuously, which can be a significant limitation.
		- Asynchronous communication involves the transfer of data or messages between services without the need for immediate responses from all parties involved. This is typically accomplished through messaging queues or database polling.
	- **Database Polling**
		- This approach involves utilizing a database table to manage request details, with one service responsible for adding rows to the table, including request state statuses such as INITIAL or START. Another service periodically checks the same table for new data or for request states like INITIAL or START. This setup facilitates indirect communication between services through a shared database table or model.
	- **Distributed Messaging System**
		- A distributed messaging system is a promising solution for asynchronous inter-service communication. It overcomes the shortcomings of Database polling and provides more cohesion.
		- Apache Kafka is a well known and robust solution for Asynchronous inter-service communication. There are other solutions as well like Solace, Active MQ, etc.

After having done some research about the possible ways of communicating, a couple of methods can already be excluded as they won't fit the project. Ultimately, I think it will become one of the 'Distributed Messaging System' methods.

#### Best good and bad practices
In the Literature Study section of this research, I used an article [Micorservices: Intra-service communication](https://medium.com/@saurabh.engg.it/micorservices-intra-service-communication-de6265c7e820) that explains how to use Kafka as a Distributed Messaging System. So, in this section I will look at some good and bad practices regarding Apache Kafka as this is properly the software that we also will be using.

[Kafka Best Practices (High Level)](https://medium.com/@byteblog/kafka-best-practices-high-level-9afcfb92645a)
- Decide how you want to partition your data and how you want to structure your messages. Avoid changing the schema frequently, as this can cause compatibility issues and downtime.
- Kafka topics are the primary means of organizing data in Kafka.
	- Use descriptive topic names that reflect the data being stored
	- Create a sufficient number of partitions for each topic
	- Use the same number of partitions across all topics
	- Ensure that partition keys are evenly distributed
	- Set appropriate retention policies based on your use case
- Kafka consumers are the applications that consume data from Kafka topics.
	- Use a consumer group to manage multiple consumers
	- Use the latest Kafka client libraries to ensure compatibility and performance
	- Use a consumer load balancer to distribute work evenly across consumers
	- Tune consumer settings to optimize performance and prevent data loss

[Apache Kafka Common Mistakes and Bad Practices](https://oso.sh/blog/apache-kafka-common-mistakes/)
- Trying to delay messages in real-time streaming. This is not recommended because it can lead to issues and impact the overall performance of your Kafka cluster.
- Kafka is not designed to be a key-value store, and using it as one can lead to unexpected behavior. It is important to understand that compaction happens eventually, not immediately. This means that you may experience duplicates and should ensure that your consumer is able to handle them appropriately.

### Field

#### Problem Analysis
The aim of this problem analysis is to identify the technology or strategy that our system should use to achieve dynamic communication between agents. In our current set up, we have made it so that there is a bot orchestrator present that manages the conversation for the user. In the end, we want to be able to remove this piece of software and let the agents manage their own conversation.

##### Problem
The challenge is to determine the most effective technology or method to make it possible for agents to communicate with each other inside the Dverse platform. 

###### Why?
Before proceeding with the development of the Dverse application, it's good to know the core of the issue at hand and ensure alignment with project objectives. Moreover, understanding the details of the issue will help in avoiding misdirected efforts towards solving an irrelevant issue.

1. **Purpose Clarification:** Dynamic communication between agents is essential to adaptively respond to user queries and achieve natural conversations within the system.
2. **Functionality Evaluation:** The current reliance on a centralized bot orchestrator is due to the initial design choice to simplify conversation management and ensure consistency in user interactions.
3. **User Experience Enhancement:** Autonomous conversation among agents will improve the user experience by fostering more natural and seamless interactions, mimicking human-like conversation flow.
###### How?
1. **Purpose Clarification:** Achieving dynamic communication between agents by implementing an agent communication protocol that allows them to communicate and collaborate in real-time.
2. **Functionality Evaluation:** Evaluate alternative approaches to conversation management, such as decentralized decision-making algorithms or distributed messaging systems, to gradually reduce reliance on the bot orchestrator.
3. **User Experience Enhancement:** Enhance user experience by designing conversational agents with natural language processing capabilities, context-awareness, and personalized interaction strategies to simulate human-like conversations effectively.

#### Domain Modelling
In this new domain model I used the already existing part but changed a small piece. First, each topic had a so-called bot orchestrator. This orchestrator was used to manage what agents to use and manage the results of these agents. The new part just checks itself if there is any unfinished business and send it to a new topic for a new agent to pick it up.

![Architecture diagram 8](https://github.com/fuas-dverse/DVerse/assets/43666923/5b5bee4c-0cf3-4156-977f-17b538ad8458)


### Workshop
#### Prototyping
For the prototype, I will try to create two agents that get chained together. With this I mean that first I ask a question to the first agent. The second agent will then give feedback to the result of the first one. After this, the first agent gets the context of the feedback and will try to fix its own mistakes. This will simulate the communication between bots on how this will improve efficiency of an agent.

First we set up a simple LangChain prompt where we take an input and puts it in a prompt a prints the output of the completed prompt.

For example:
```python
from langchain.prompts import PromptTemplate  
  
prompt = PromptTemplate(  
    input_variables=["product"],  
    template="What is a good name for a company that makes {product}?",  
)  
  
print(prompt.format(product="smartphones"))

# OUTPUT: What is a good name for a company that makes smartphones 
```

Now the next step is to chain some LLM into the code to create a chain that asks for feedback and rewrites itself.

To do this we first need to create a function that generates a bad paragraph about a certain context, for this example I will use the following context: `A dog that hurt its knee by stepping on a bee.`

First, we create the bad function:

```python
def get_bad_llm_output(context):  
    prompt = ChatPromptTemplate.from_template(  
        """Write a bad paragraph about the following: {context}"""  
    )  
  
    model = ChatOpenAI()  
  
    chain = (  
            RunnableParallel({  
                "context": RunnablePassthrough(),  
            })  
            | prompt  
            | model  
            | StrOutputParser()  
    )  
  
    return chain.invoke({  
        "context": context,  
    })
```

Then we write a function that asks for feedback on the output of the first function:

```python
def get_llm_feedback(context):  
    prompt = ChatPromptTemplate.from_template(  
        """  
            Give feedback on the following written paragraph, include grammar and spelling: {context}            Do not include the new paragraph, only the feedback.        """    )  
  
    model = ChatOpenAI()  
  
    chain = (  
            RunnableParallel({  
                "context": RunnablePassthrough(),  
            })  
            | prompt  
            | model  
            | StrOutputParser()  
    )  
  
    return chain.invoke({  
        "context": context,  
    })
```

And then we create a function that updates the written takes with the new feedback it received:

```python
def get_updated_llm_output(context, feedback):  
    prompt = ChatPromptTemplate.from_template(  
        """  
            Rewrite the following text: {context}            Based on this feedback: {feedback}        """    )  
  
    model = ChatOpenAI()  
  
    chain = (  
            RunnableParallel({  
                "context": RunnablePassthrough(),  
                "feedback": RunnablePassthrough(),  
            })  
            | prompt  
            | model  
            | StrOutputParser()  
    )  
  
    return chain.invoke({  
        "context": context,  
        "feedback": feedback  
    })
```

As last step, we give the context to all the functions when the script runs and keep track of the message for the output:

```python
if __name__ == "__main__":  
    history = []  
  
    # Start with a prompt that sets the context  
    context = "A dog that hurt its knee by stepping on a bee."  
    history.append(context)  
  
    # Get a badly written paragraph based on the prompt  
    output = get_bad_llm_output(context)  
    history.append(output)  
  
    # Ask for feedback on the bad paragraph to correct it  
    feedback = get_llm_feedback(output)  
    history.append(feedback)  
  
    # Update the bad paragraph based on the feedback  
    updated_output = get_updated_llm_output(output, feedback)  
    history.append(updated_output)  
  
    # Print the history of the conversation  
    for i, item in enumerate(history):  
        print(f"{i}: {item}")
```

The output of this will look something like:

```cmd
0: A dog that hurt its knee by stepping on a bee.
1: This dog is so dumb, it hurt its knee by stepping on a bee. Who even does that? It must be the most clumsy and foolish canine around. Just imagine the embarrassment of having to explain to other dogs how it got injured. Pathetic.
2: The paragraph contains several grammar and spelling errors. Here are the corrections:

- "dumb" should be replaced with a more appropriate term, such as "unintelligent" or "clumsy."
- "it hurt its knee" should be "it hurt its knee" or "it injured its knee."
- "clumsy" is misspelled as "clumsey."
- "canine" should be followed by a comma, like this: "foolish canine," or replaced with a more common term like "dog."
- "Just imagine the embarrassment of having to explain" should be "Just imagine the embarrassment of having to explain."
- "Pathetic" is an inappropriate word choice and should be replaced with a more respectful term.
3: Rewritten text: 

This dog is so unwise, it injured its knee by stepping on a bee. Who even does that? It must be the most clumsy and foolish dog around. Just imagine the embarrassment of having to explain to other dogs how it got injured. Inappropriate.

```

#### Decomposition
To decomposition, I will create a very small diagram of how we want to event drive architecture to function. This will not be worked out completely as there are still a lot of uncertainties in our application. This will be improved in time.


![Untitled Diagram drawio](https://github.com/fuas-dverse/DVerse/assets/43666923/39812900-f601-41eb-843c-d6ef0f0c39b7)

This diagram is small but says a lot about the architecture and how we want to create it. First, the user sends a prompt via the UI, which will get handled by some smaller agents. Once this is completed, it will be sent back to the UI.

### Lab
#### Component test
For this component test I will not write any tests as this is very hard to do for the solution to our problem. Instead, I will be testing the throughput of the Apache Kafka message bus.

To do this I will use our prototype instance of Kafka and add a for loop that fires, 100000 times.


![Pasted image 20240506113201](https://github.com/fuas-dverse/DVerse/assets/43666923/75958d91-b79a-4b22-9e0e-735518ec5391)


In this screenshot, we can see that I modified the script to just print instead of doing some heavy lifting like classifying and to send a lot of requests. While running both these scripts, we can see that it has no issue keeping up with the load of Apache Kafka. Of course, this is not a real world example and the classifier has some heavy lifting to do. This could be resolved by having it run in a Kubernetes cluster.

### Reflection
In doing this research, my primary objective was to identify effective techniques for communication between agents in our Dverse application.

We have looked at different technology options like APIs and microservices, settling on Apache Kafka for its scalability and asynchronous communication.

After having settled on Apache Kafka, we did some research about the best and bad practices for Apache Kafka, like managing topics and consumer groups etc.

Identifying a centralized orchestrator as a bottleneck, we propose a shift to a decentralized communication model. This is visualized through domain modeling, showing how agents would interact within the platform.

The prototyping demonstrates how agents could generate, evaluate, and update outputs based on feedback that they received by another LLM as this can improve reliability in our system.

By completing this research, we can look deeper into the specific technique and implement it in the Dverse application.

This research has contributed to our group project, providing valuable insights into new technologies and their practical uses. Moving forward, we aim to integrate the chosen technique into our application, enhancing its capabilities and user experience.
