from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json
import uuid


def uid(prefix: str) -> str:
    """Generate a unique ID with a prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


# -------------------------
# Base Model Element
# -------------------------

@dataclass
class SysMLProperties:
    text: Optional[str] = None
    risk: Optional[str] = None
    priority: Optional[str] = None
    phase: Optional[str] = None
    level: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class SysMLElement:
    id: str
    type: str
    name: str
    shortName: Optional[str] = None
    documentation: Optional[str] = None
    properties: Optional[SysMLProperties] = None
    ownedRelationships: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON‑serializable dict."""
        data = asdict(self)
        # Remove None fields for clean JSON
        return {k: v for k, v in data.items() if v not in (None, [], {})}


# -------------------------
# RequirementUsage
# -------------------------

@dataclass
class RequirementUsage(SysMLElement):
    def __init__(
        self,
        name: str,
        text: str,
        shortName: Optional[str] = None,
        documentation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            id=uid("req"),
            type="RequirementUsage",
            name=name,
            shortName=shortName,
            documentation=documentation,
            properties=SysMLProperties(text=text, **kwargs)
        )


# -------------------------
# ConcernUsage (Rationale / Concern)
# -------------------------

@dataclass
class ConcernUsage(SysMLElement):
    def __init__(
        self,
        name: str,
        text: str,
        shortName: Optional[str] = None,
        documentation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            id=uid("concern"),
            type="ConcernUsage",
            name=name,
            shortName=shortName,
            documentation=documentation,
            properties=SysMLProperties(text=text, **kwargs)
        )


# -------------------------
# Trace Relationship
# -------------------------

@dataclass
class Trace(SysMLElement):
    source: str = ""
    target: str = ""

    def __init__(
        self,
        source: str,
        target: str,
        name: Optional[str] = None,
        documentation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            id=uid("trace"),
            type="Trace",
            name=name or "Trace",
            documentation=documentation,
            properties=SysMLProperties(**kwargs)
        )
        self.source = source
        self.target = target

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["source"] = self.source
        base["target"] = self.target
        return base


# -------------------------
# Model Container
# -------------------------

@dataclass
class SysMLModel:
    elements: List[SysMLElement] = field(default_factory=list)

    def add(self, element: SysMLElement):
        self.elements.append(element)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(
            {"elements": [el.to_dict() for el in self.elements]},
            indent=indent
        )



def main() -> None:
    model = SysMLModel()

    req = RequirementUsage(
        name="SystemShallDoX",
        text="The system shall perform function X under condition Y.",
        shortName="REQ-001",
        priority="High",
        phase="Concept",
        level="System",
        tags=["safety", "core"]
    )
    
    rat = ConcernUsage(
        name="RationaleForREQ001",
        text="Ensures compliance with safety regulation ABC‑123.",
        shortName="RAT-001",
        phase="Concept",
        tags=["regulatory"]
    )
    
    trace = Trace(
        source=rat.id,
        target=req.id,
        name="RationaleTrace",
        documentation="Rationale traces to requirement."
    )
    
    # Link rationale to requirement
    req.ownedRelationships.append({
        "id": uid("rel"),
        "type": "ConcernUsageMembership",
        "memberElement": rat.id,
        "kind": "rationale"
    })
    
    model.add(req)
    model.add(rat)
    model.add(trace)
    
    print(model.to_json())

    



if __name__ == "__main__":
    main()
    