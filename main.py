import json
import sys
from pathlib import Path

def group_footnotes_by_service(json_path: str = "files/MCMCv2.json") -> list:
    with open(json_path) as fp:
        entries = json.load(fp)
    
    result = []
    current_entry = None
    
    for entry in entries:
        service = entry.get("service")
        footnotes = entry.get("footnotes")
        
        if service is not None:
            if current_entry is not None:
                result.append(current_entry)
            current_entry = {
                "band": entry.get("band"),
                "service": service,
                "status": entry.get("status"),
                "footnotes": []
            }
        elif footnotes is not None:
            if current_entry is None:
                print(f"Warning: Footnote '{footnotes}' found before any service", file=sys.stderr)
            else:
                current_entry["footnotes"].append(footnotes)
    
    if current_entry is not None:
        result.append(current_entry)
    
    empty_footprints = [e for e in result if not e["footnotes"]]
    for e in empty_footprints:
        print(f"Warning: Service '{e['service']}' has no footnotes", file=sys.stderr)
    
    return result

if __name__ == "__main__":
    grouped = group_footnotes_by_service()
    output_path = Path("output/footnotes_by_service.json")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as fp:
        json.dump(grouped, fp, indent=2)
