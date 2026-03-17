## MOving from Conversational Prompt to Structural Output Prompt (iteration 001)

## Iteration 002 --> ReACT Framework --> CoT (style) Observe and Act Framework 
   --> Dataset used: HotpotQA


## ReAct Paper: Synergizing Reasoning and Acting in Language Models 
   (Yao et al.)

   Dataset used: HOtPOtQA and ALFWorld (text-based) games datasets.


   The "Act" Prompt (Action-Only) --> 
   Structure the Prompt as follows: 
   Question: [The User Question]
   Action 1: [Search/Lookup]

   Observation 1: [Result from the environment/Wikipedia]
   Action 2: [Next Action].


   The ReACT Prompt (Reason + Act): 

   Question: Aside from the Apple Remote, what other devices can control the program Apple Remote was originally designed to interact with?

	Action 1: Search[Apple Remote]

	Observation 1: The Apple Remote is a remote control... designed to control the Front Row media center program...

	Action 2: Search[Front Row (software)]

	Observation 2: Front Row is a discontinued media center software...

	Action 3: Finish[...list of devices...]

	Structure: 

	Question: [The User Question]
	Thought 1: 
	Action 1: 

	Obersavtion 1: 

	Thought:


	Action....


	..............................................................


Current Challenges with existing Language Models: 
In Simpler terms, lets say an agent receives an observation ot element (O), there is an action at element (A) following some policy, pi (at given ct), where ct s a collection of all actions and observations which the agent has seen so far.





Ref: https://medium.com/@deejairesearcher/react-paper-explained-simply-how-language-models-can-think-and-act-f500395f88db 



