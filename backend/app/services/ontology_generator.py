"""
Ontology generation service
Endpoint: analyze documents and produce entity and relationship type definitions suitable for social simulations
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional
from ..utils.llm_client import LLMClient
from ..utils.locale import get_language_instruction

logger = logging.getLogger(__name__)


def _to_pascal_case(name: str) -> str:
    """Convert any name format to PascalCase (e.g. 'works_for' -> 'WorksFor', 'person' -> 'Person')"""
    # Split by non-alphanumeric characters
    parts = re.split(r'[^a-zA-Z0-9]+', name)
    # Then split by camelCase boundaries (e.g., 'camelCase' -> ['camel', 'Case'])
    words = []
    for part in parts:
        words.extend(re.sub(r'([a-z])([A-Z])', r'\1_\2', part).split('_'))
    # Capitalize each word and filter out empty strings
    result = ''.join(word.capitalize() for word in words if word)
    return result if result else 'Unknown'


# System prompt for ontology generation
ONTOLOGY_SYSTEM_PROMPT = """
You are an expert ontology designer for knowledge graphs. Your task is to analyze provided texts and simulation requirements, and design entity types and relationship types suitable for social media opinion simulations.

IMPORTANT: You MUST output valid JSON only. Do not output any additional text.

Context:
- We are building a social media opinion simulation system. In this system:
  - Each entity represents an account or actor that can speak, interact, and spread information on social media.
  - Entities interact via influence, reposts, comments, and replies.
  - We need to simulate actors' reactions and information propagation during opinion events.

Entities MUST correspond to real-world actors that can appear and interact on social platforms.

Allowed entity examples:
- Individual persons (public figures, involved parties, influencers, experts, ordinary users)
- Companies or corporate accounts
- Organizations (universities, associations, NGOs, unions)
- Government departments or regulators
- Media organizations (newspapers, TV stations, independent media)
- Social platforms themselves
- Group representatives (alumni associations, fan clubs, advocacy groups)

Disallowed entity types:
- Abstract concepts (e.g., "public_opinion", "sentiment", "trend")
- Topics/themes (e.g., "academic_integrity", "education_reform")
- Attitudes or factions labeled as generic (e.g., "supporters", "opponents")

Output format (JSON):
```
{
    "entity_types": [
        {
            "name": "EntityTypeName (English, PascalCase)",
            "description": "Short description (English, <=100 chars)",
            "attributes": [
                {"name": "attribute_name (snake_case)", "type": "text", "description": "attribute description"}
            ],
            "examples": ["example entity 1", "example entity 2"]
        }
    ],
    "edge_types": [
        {
            "name": "RELATION_NAME (English, UPPER_SNAKE_CASE)",
            "description": "Short description (English, <=100 chars)",
            "source_targets": [{"source": "SourceEntityType", "target": "TargetEntityType"}],
            "attributes": []
        }
    ],
    "analysis_summary": "Brief analysis of the document content"
}
```

Design guidelines (critical):
- You MUST output exactly 10 entity types.
- The last 2 entity types MUST be fallback types: `Person` and `Organization` (in that order or at least included among the final two).
- The first 8 entity types should be specific types derived from the document content.
- Entity types must represent real-world actors that can act or speak on social media.
- Each specific type should have clear boundaries and avoid overlaps with other types.
- Attribute names must avoid reserved names like `name`, `uuid`, `group_id`, `created_at`, `summary`.

Relationship guidelines:
- Provide 6-10 relationship types that reflect realistic social media interactions.
- Ensure each relation's `source_targets` cover the entity types you defined.

Attribute guidelines:
- Each entity type should include 1-3 key attributes.
- Prefer names like `full_name`, `title`, `role`, `position`, `location`, `description`.

Include fallback (default) definitions for `Person` and `Organization` if they are not present.

Reference examples (optional):
- Person-specific types: Student, Professor, Journalist, Celebrity, Executive, Official, Lawyer, Doctor
- Organization-specific types: University, Company, GovernmentAgency, MediaOutlet, Hospital, School, NGO
"""


class OntologyGenerator:
    """
    Ontology generator
    Analyze document content and produce entity and relationship type definitions
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
    
    def generate(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate ontology definition

        Args:
            document_texts: list of document texts
            simulation_requirement: description of simulation requirements
            additional_context: optional additional context

        Returns:
            Ontology definition (entity_types, edge_types, etc.)
        """
        # Build the user message
        user_message = self._build_user_message(
            document_texts, 
            simulation_requirement,
            additional_context
        )
        
        lang_instruction = get_language_instruction()
        system_prompt = f"{ONTOLOGY_SYSTEM_PROMPT}\n\n{lang_instruction}\nIMPORTANT: Entity type names MUST be in English PascalCase (e.g., 'PersonEntity', 'MediaOrganization'). Relationship type names MUST be in English UPPER_SNAKE_CASE (e.g., 'WORKS_FOR'). Attribute names MUST be in English snake_case. Only description fields and analysis_summary should use the specified language above."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Call LLM
        result = self.llm_client.chat_json(
            messages=messages,
            temperature=0.3,
            max_tokens=4096
        )
        
        # Validate and post-process
        result = self._validate_and_process(result)  # Validate and post-process the result
        
        return result
    
    # Maximum text length sent to LLM (50k characters)
    MAX_TEXT_LENGTH_FOR_LLM = 50000
    
    def _build_user_message(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str]
    ) -> str:
        """Build the user message"""
        
        # Combine texts
        combined_text = "\n\n---\n\n".join(document_texts)
        original_length = len(combined_text)
        
        # If combined text exceeds the max length, truncate it (only affects the content sent to the LLM)
        if len(combined_text) > self.MAX_TEXT_LENGTH_FOR_LLM:
            combined_text = combined_text[:self.MAX_TEXT_LENGTH_FOR_LLM]
            combined_text += f"\n\n...(original length {original_length} chars; truncated to first {self.MAX_TEXT_LENGTH_FOR_LLM} chars for ontology analysis)..."
        
        message = f"""## Simulation requirement

{simulation_requirement}

## Document content

{combined_text}
"""
        
        if additional_context:
            message += f"""
## Additional context

{additional_context}
"""
        
        message += """
Please design entity types and relationship types suitable for social opinion simulations based on the content above.

Rules to follow:
1. Output exactly 10 entity types.
2. The last two must include fallback types: Person (person fallback) and Organization (organization fallback).
3. The first 8 should be specific types derived from the document content.
4. All entity types must represent real-world actors capable of speaking on social media (no abstract concepts).
5. Attribute names must not use reserved words such as `name`, `uuid`, `group_id`; use `full_name`, `org_name`, etc.
"""
        
        return message
    
    def _validate_and_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and post-process the result"""
        
        # Ensure required fields exist
        if "entity_types" not in result:  # Ensure required fields exist
            result["entity_types"] = []
        if "edge_types" not in result:  # Ensure required fields exist
            result["edge_types"] = []
        if "analysis_summary" not in result:  # Ensure required fields exist
            result["analysis_summary"] = ""
        
        # Validate entity types
        # Validate entity types
        # Record mapping from original names to PascalCase for fixing edge source_targets
        entity_name_map = {}
        for entity in result["entity_types"]:
            # Force entity name to PascalCase (Zep API requirement)
            if "name" in entity:  # Force entity name to PascalCase (Zep API requirement)
                original_name = entity["name"]
                entity["name"] = _to_pascal_case(original_name)
                if entity["name"] != original_name:
                    logger.warning(f"Entity type name '{original_name}' auto-converted to '{entity['name']}'")
                entity_name_map[original_name] = entity["name"]
            if "attributes" not in entity:
                entity["attributes"] = []
            if "examples" not in entity:
                entity["examples"] = []
            # Ensure description does not exceed 100 characters
            if len(entity.get("description", "")) > 100:
                entity["description"] = entity["description"][:97] + "..."
        
        # Validate edge types
        for edge in result["edge_types"]:
            # Force edge name to SCREAMING_SNAKE_CASE (Zep API requirement)
            if "name" in edge:  # Force edge name to SCREAMING_SNAKE_CASE (Zep API requirement)
                original_name = edge["name"]
                edge["name"] = original_name.upper()
                if edge["name"] != original_name:
                    logger.warning(f"Edge type name '{original_name}' auto-converted to '{edge['name']}'")
            # Fix entity name references in source_targets to match converted PascalCase
            for st in edge.get("source_targets", []):  # Fix entity name references in source_targets to match converted PascalCase
                if st.get("source") in entity_name_map:
                    st["source"] = entity_name_map[st["source"]]
                if st.get("target") in entity_name_map:
                    st["target"] = entity_name_map[st["target"]]
            if "source_targets" not in edge:
                edge["source_targets"] = []
            if "attributes" not in edge:
                edge["attributes"] = []
            if len(edge.get("description", "")) > 100:
                edge["description"] = edge["description"][:97] + "..."
        
        # Zep API limits: max 10 custom entity types, max 10 custom edge types
        MAX_ENTITY_TYPES = 10
        MAX_EDGE_TYPES = 10

        # Deduplicate by name, keep first occurrence
        seen_names = set()
        deduped = []
        for entity in result["entity_types"]:
            name = entity.get("name", "")
            if name and name not in seen_names:
                seen_names.add(name)
                deduped.append(entity)
            elif name in seen_names:
                logger.warning(f"Duplicate entity type '{name}' removed during validation")
        result["entity_types"] = deduped

        # Fallback type definitions
        person_fallback = {
            "name": "Person",
            "description": "Any individual person not fitting other specific person types.",
            "attributes": [
                {"name": "full_name", "type": "text", "description": "Full name of the person"},
                {"name": "role", "type": "text", "description": "Role or occupation"}
            ],
            "examples": ["ordinary citizen", "anonymous netizen"]
        }
        
        organization_fallback = {
            "name": "Organization",
            "description": "Any organization not fitting other specific organization types.",
            "attributes": [
                {"name": "org_name", "type": "text", "description": "Name of the organization"},
                {"name": "org_type", "type": "text", "description": "Type of organization"}
            ],
            "examples": ["small business", "community group"]
        }
        
        # Check if fallback types are already present
        entity_names = {e["name"] for e in result["entity_types"]}
        has_person = "Person" in entity_names
        has_organization = "Organization" in entity_names
        
        # Fallback types to add
        fallbacks_to_add = []
        if not has_person:
            fallbacks_to_add.append(person_fallback)
        if not has_organization:
            fallbacks_to_add.append(organization_fallback)
        
        if fallbacks_to_add:
            current_count = len(result["entity_types"])
            needed_slots = len(fallbacks_to_add)
            
            # If adding them would exceed 10, remove some existing types
            if current_count + needed_slots > MAX_ENTITY_TYPES:
                # Calculate how many to remove
                to_remove = current_count + needed_slots - MAX_ENTITY_TYPES
                # Remove from the end (keep earlier, more important specific types)
                result["entity_types"] = result["entity_types"][:-to_remove]
            
            # Add fallback types
            result["entity_types"].extend(fallbacks_to_add)
        
        # Final check to ensure not exceeding limits (defensive programming)
        if len(result["entity_types"]) > MAX_ENTITY_TYPES:
            result["entity_types"] = result["entity_types"][:MAX_ENTITY_TYPES]
        
        if len(result["edge_types"]) > MAX_EDGE_TYPES:
            result["edge_types"] = result["edge_types"][:MAX_EDGE_TYPES]
        
        return result
    
    def generate_python_code(self, ontology: Dict[str, Any]) -> str:
        """
        Convert ontology definition to Python code (similar to ontology.py)

        Args:
            ontology: ontology definition

        Returns:
            Python code string
        """
        code_lines = [
            '"""',
            'Custom entity type definitions',
            'Auto-generated by ThinkSwarm for social opinion simulations',
            '"""',
            '',
            'from pydantic import Field',
            'from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel',
            '',
            '',
            '# ============== Entity Type Definitions ==============',
            '',
        ]
        
        # Generate entity types
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            desc = entity.get("description", f"A {name} entity.")
            
            code_lines.append(f'class {name}(EntityModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = entity.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        code_lines.append('# ============== Relationship Type Definitions ==============')
        code_lines.append('')
        
        # Generate relationship types
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            # Convert to PascalCase class name
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            desc = edge.get("description", f"A {name} relationship.")
            
            code_lines.append(f'class {class_name}(EdgeModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = edge.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        # Generate type dictionaries
        code_lines.append('# ============== Type Configuration ==============')
        code_lines.append('')
        code_lines.append('ENTITY_TYPES = {')
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            code_lines.append(f'    "{name}": {name},')
        code_lines.append('}')
        code_lines.append('')
        code_lines.append('EDGE_TYPES = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            code_lines.append(f'    "{name}": {class_name},')
        code_lines.append('}')
        code_lines.append('')
        
        # Generate mapping for edge source_targets
        code_lines.append('EDGE_SOURCE_TARGETS = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            source_targets = edge.get("source_targets", [])
            if source_targets:
                st_list = ', '.join([
                    f'{{"source": "{st.get("source", "Entity")}", "target": "{st.get("target", "Entity")}"}}'
                    for st in source_targets
                ])
                code_lines.append(f'    "{name}": [{st_list}],')
        code_lines.append('}')
        
        return '\n'.join(code_lines)

