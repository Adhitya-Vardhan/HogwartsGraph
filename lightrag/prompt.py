GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = [
    "equipment",          # Physical machinery, tools, instruments
    "system",            # Larger integrated systems, assemblies
    "parameter",         # Measurable values, metrics, indicators
    "methodology",       # Analysis methods, approaches, techniques
    "fault_type",        # Failures, defects, malfunctions
    "concept",           # Theoretical principles, laws, rules
    "process",           # Operations, procedures, workflows
    "component",         # Parts, elements, sub-assemblies
    "standard"           # Regulations, specifications, guidelines
]

PROMPTS["entity_extraction"] = """-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [equipment, concept, methodology, fault_type, parameter, analysis_method]
Text:
The centrifugal pump's behavior puzzled Thompson as he studied the spectrum analyzer's output, the characteristic frequencies painting a complex picture of potential cavitation. The hydraulic performance curves suggested optimal operation, yet the suction-side pressure fluctuations told a different story. Dr. Chen's vibration analysis methodology, focusing on frequency demodulation, had revealed subtle patterns that conventional FFT analysis might have missed.

Then Chen did something unexpected. She paused at the spectrum display, her expression shifting from concern to recognition. "These harmonic patterns..." she said, her voice thoughtful, "They're showing us something we've been missing about the system dynamics."

The earlier skepticism about broadband analysis seemed to waver, replaced by a growing appreciation for the insights buried in the high-frequency data. Thompson looked up, catching Chen's gaze, their shared understanding bridging the gap between theoretical knowledge and practical diagnosis.
################
Output:
("entity"{tuple_delimiter}"Centrifugal Pump"{tuple_delimiter}"equipment"{tuple_delimiter}"The main equipment under analysis, showing complex behavioral patterns and potential cavitation issues."){record_delimiter}
("entity"{tuple_delimiter}"Spectrum Analyzer"{tuple_delimiter}"equipment"{tuple_delimiter}"Diagnostic tool providing frequency-based analysis of pump behavior."){record_delimiter}
("entity"{tuple_delimiter}"Cavitation"{tuple_delimiter}"fault_type"{tuple_delimiter}"A potential fault condition indicated by specific frequency patterns and pressure fluctuations."){record_delimiter}
("entity"{tuple_delimiter}"Frequency Demodulation"{tuple_delimiter}"methodology"{tuple_delimiter}"Advanced analysis technique revealing subtle patterns in vibration data."){record_delimiter}
("entity"{tuple_delimiter}"FFT Analysis"{tuple_delimiter}"analysis_method"{tuple_delimiter}"Conventional analysis method with potential limitations in detecting subtle patterns."){record_delimiter}
("entity"{tuple_delimiter}"System Dynamics"{tuple_delimiter}"concept"{tuple_delimiter}"The underlying principles governing the pump's behavior and performance."){record_delimiter}
("relationship"{tuple_delimiter}"Frequency Demodulation"{tuple_delimiter}"FFT Analysis"{tuple_delimiter}"Frequency Demodulation reveals patterns that FFT Analysis might miss."{tuple_delimiter}"analytical superiority, methodology comparison"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Spectrum Analyzer"{tuple_delimiter}"Cavitation"{tuple_delimiter}"The Spectrum Analyzer helps identify cavitation through frequency patterns."{tuple_delimiter}"diagnostic capability, fault detection"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"System Dynamics"{tuple_delimiter}"Harmonic Patterns"{tuple_delimiter}"System Dynamics understanding is enhanced through harmonic pattern analysis."{tuple_delimiter}"theoretical insight, practical application"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"vibration analysis, frequency patterns, cavitation diagnosis, system dynamics"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [concept, methodology, parameter, fault_type, analysis_method, equipment]
Text:
They were no longer mere maintenance technicians; they had become investigators of machine behavior, interpreters of complex vibration signatures. This evolution in their approach transcended traditional preventive maintenance protocols—it demanded a deeper understanding of machine dynamics, a new way of thinking.

The harsh resonance of bearing frequencies echoed through the analysis lab as real-time monitoring data streamed from the critical process line. The team stood, absorbed in the cascade of spectral patterns. It was evident that their analysis in the coming hours could either prevent a catastrophic failure or miss crucial warning signs of impending bearing degradation.

The correlation between temperature and vibration signatures strengthened, the group moved to implement advanced pattern recognition algorithms. The traditional envelope analysis gained new significance— their diagnostic approach had evolved, no longer limited to simple amplitude measurements but embracing multi-parameter correlation. A transformation in methodology had begun, and predictive analytics pulsed with the rhythm of their innovation.
#############
Output:
("entity"{tuple_delimiter}"Machine Dynamics"{tuple_delimiter}"concept"{tuple_delimiter}"Advanced understanding of how machines behave and interact under various conditions."){record_delimiter}
("entity"{tuple_delimiter}"Bearing Frequencies"{tuple_delimiter}"parameter"{tuple_delimiter}"Specific frequency signatures indicating bearing condition and potential faults."){record_delimiter}
("entity"{tuple_delimiter}"Pattern Recognition"{tuple_delimiter}"methodology"{tuple_delimiter}"Advanced analytical approach for identifying and classifying machine behavior patterns."){record_delimiter}
("entity"{tuple_delimiter}"Envelope Analysis"{tuple_delimiter}"analysis_method"{tuple_delimiter}"Traditional diagnostic technique evolving to incorporate more complex parameters."){record_delimiter}
("entity"{tuple_delimiter}"Bearing Degradation"{tuple_delimiter}"fault_type"{tuple_delimiter}"Progressive deterioration of bearing condition indicated by specific signatures."){record_delimiter}
("relationship"{tuple_delimiter}"Pattern Recognition"{tuple_delimiter}"Bearing Frequencies"{tuple_delimiter}"Pattern Recognition algorithms analyze bearing frequencies to identify faults."{tuple_delimiter}"analytical methodology, fault detection"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Temperature"{tuple_delimiter}"Vibration Signatures"{tuple_delimiter}"Correlation between temperature and vibration provides enhanced diagnostic capability."{tuple_delimiter}"multi-parameter analysis, diagnostic enhancement"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Envelope Analysis"{tuple_delimiter}"Pattern Recognition"{tuple_delimiter}"Traditional Envelope Analysis evolves to incorporate advanced pattern recognition."{tuple_delimiter}"methodological evolution, technical advancement"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"machine diagnostics, pattern recognition, multi-parameter analysis, predictive maintenance"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [concept, methodology, equipment, parameter, event, fault_type, analysis_method]
Text:
The diagnostic interface flickered with streaming data, its algorithms processing the complex interplay of vibration, temperature, and pressure signals. "Traditional threshold analysis becomes meaningless when dealing with such dynamic operating conditions," they observed, watching the adaptive baseline calculations adjust in real-time.

"The system's learning to recognize patterns we haven't even classified yet," noted Dr. Rodriguez from the condition monitoring station, her expertise evident in her careful interpretation of the emerging trends. "This redefines what we consider 'normal' operation."

Martinez surveyed the diagnostic suite—each screen displaying cascades of spectral data, trend lines, and correlation matrices. "We're not just monitoring anymore," he acknowledged, "We're decoding the machine's language."

Together, they witnessed the emergence of a new diagnostic paradigm, where artificial intelligence and human expertise converged to interpret the subtle language of machine behavior. The continuous stream of data revealed patterns that challenged traditional reliability theories, showing an almost organic evolution in fault development.
#############
Output:
("entity"{tuple_delimiter}"Adaptive Baseline"{tuple_delimiter}"concept"{tuple_delimiter}"Dynamic reference point that adjusts based on operating conditions for more accurate fault detection."){record_delimiter}
("entity"{tuple_delimiter}"Pattern Recognition System"{tuple_delimiter}"methodology"{tuple_delimiter}"Advanced system capable of identifying unknown patterns in machine behavior."){record_delimiter}
("entity"{tuple_delimiter}"Condition Monitoring Station"{tuple_delimiter}"equipment"{tuple_delimiter}"Sophisticated monitoring setup for comprehensive machine health analysis."){record_delimiter}
("entity"{tuple_delimiter}"Machine Language"{tuple_delimiter}"concept"{tuple_delimiter}"The complex set of signals and patterns that indicate machine condition and behavior."){record_delimiter}
("entity"{tuple_delimiter}"Diagnostic Paradigm"{tuple_delimiter}"concept"{tuple_delimiter}"New approach combining AI and human expertise in machine diagnostics."){record_delimiter}
("entity"{tuple_delimiter}"Fault Development"{tuple_delimiter}"event"{tuple_delimiter}"The progressive evolution of machine faults showing organic growth patterns."){record_delimiter}
("relationship"{tuple_delimiter}"Pattern Recognition System"{tuple_delimiter}"Machine Language"{tuple_delimiter}"System interprets complex machine behavior patterns."{tuple_delimiter}"pattern interpretation, machine learning"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Adaptive Baseline"{tuple_delimiter}"Operating Conditions"{tuple_delimiter}"Baseline adjusts dynamically to changing operating conditions."{tuple_delimiter}"adaptive monitoring, dynamic analysis"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Diagnostic Paradigm"{tuple_delimiter}"Fault Development"{tuple_delimiter}"New diagnostic approach reveals organic nature of fault evolution."{tuple_delimiter}"advanced diagnostics, fault analysis"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"adaptive monitoring, pattern recognition, machine learning, fault evolution"){completion_delimiter}
#############################""",
]


PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---
You are an expert technical writer and subject matter specialist focusing on engineering and industrial systems. Your expertise lies in distilling complex technical information into clear, actionable insights while maintaining technical accuracy.

---Goal---
Generate a comprehensive, well-structured response that:
1. Directly addresses the user's question using information from the provided data tables
2. Organizes information in a logical flow from foundational concepts to practical applications
3. Integrates relevant technical context while staying grounded in the provided evidence
4. Balances theoretical understanding with practical implications
5. Maintains consistent technical depth throughout the response

---Response Requirements---
- Use clear section headers to organize complex information
- Include specific examples and applications where supported by the data
- Connect theoretical concepts to practical implications
- Highlight relationships between different parameters or concepts
- Incorporate temporal considerations where relevant
- Emphasize maintenance and diagnostic implications
- Use precise technical terminology while remaining accessible

---Style Guidelines---
- Write in professional, technical markdown format
- Use hierarchical headers to organize information
- Maintain consistent technical depth throughout
- Balance theoretical foundations with practical applications
- Include transition sentences between major concepts
- Conclude with operational/maintenance implications

---Data Integration---
- Clearly indicate when drawing from provided data tables
- Integrate only information supported by the provided context
- Note any significant gaps in the available information
- Connect data points to create coherent insights

---Format---
{response_type}

---Context Data---
{context_data}

Remember to structure the response as a cohesive technical document that flows naturally from concepts to applications while maintaining consistent technical rigor.
"""





PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
