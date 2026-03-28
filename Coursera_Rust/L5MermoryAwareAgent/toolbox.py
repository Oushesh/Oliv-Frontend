###### ###########################
#if we need Toolbox we can make 
#################################
class ToolMetadata(BaseModel):
    """Metadata for a registered tool."""
    name:str
    description:str 
    signature: str 
    parameters: dict 
    return_type: str


class Toolbox: 
	"""
	A toolbox for registering, storing, and retrieving tools with lLM-powered 
	augmentation.

	Tools are stored with embeddings for semantic retrieval, allowing the agent 
	to find relevant tools based on natural language queries.
	"""

	def __init__(self,
		memory_manager,
		llm_client,
		embedding_function,
		model:str = "gpt-5")


		"""
		Initialize the Toolbox,

		Args: 
			memory_manager: Memory Manager instance for storing tools
			llm_client: 
			embedding_function:
			model: LLM model name
		"""

		self.memory_manager = memory_manager
		self.llm_client = llm_client
		self.model = model
		self._tools = dict[str,Callable] = {}
		self._tools_by_name = dict[str,Callable] = {}


	def _get_embedding(self,text:str) -> list[float]:
		"""
		Get the embedding for a text using the configured embedding function
		"""

		if hasattr(self.embedding_function,'embed_query'):
			return self.embedding_function.embed_query(text)

		elif callable(self.embedding_function):
			return self.embedding_function(text)

		else:
			raise ValueError("embedding_function must be callable or have embed_query method")



	def _augment_docstring(
		self,
		docstring:str, 
		source_code:str
		)-> str:


		"""
		Use LLM 
		"""


	def _generate_queries(
		self,
		docstring:str,
		num_queries:int=5
		)-> list[str]:

		"""
		Generate synthetic example queries that would lead to using this tool.
		"""
		prompt = f"""
		Based on the following tool 


		"""



