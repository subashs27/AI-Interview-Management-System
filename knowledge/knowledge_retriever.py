from database.database import get_knowledge

def retrieve_knowledge(candidate):

    knowledge_list = []
    searched = set()

    search_terms = []

    # Target Role
    if candidate.get("target_role"):
        search_terms.append(candidate["target_role"])

    # Skills
    search_terms.extend(candidate.get("skills", []))

    # Project Titles
    for project in candidate.get("projects", []):
        if isinstance(project, dict):
            search_terms.append(project.get("title", ""))

            for tech in project.get("technologies", []):
                search_terms.append(tech)

    # Certifications
    search_terms.extend(candidate.get("certifications", []))

    # Search Database
    for term in search_terms:

        term = term.strip()

        if not term:
            continue

        if term.lower() in searched:
            continue

        searched.add(term.lower())

        knowledge = get_knowledge(term)

        if knowledge:
            knowledge_list.append(knowledge)
            print(f"✅ Found: {knowledge['topic']}")
        else:
            print(f"❌ Not Found: {term}")

    print("=" * 80)
    print(f"Knowledge Retrieved: {len(knowledge_list)}")
    print("=" * 80)

    return knowledge_list