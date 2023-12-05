from my_html_parser import qna_data
import yaml
import os
training_data = {"nlu": []}
responses_data = {}
stories_data = {"stories": []}
count = 0

for heading, examples in qna_data.items():
    # Add intent data to training_data
    intent = "intent_" + str(count)
    training_data["nlu"].append({"intent": intent, "examples": heading})

    # Prepare response data
    utter = "utter_" + str(count)
    examples = "".join(examples)
    responses_data[utter] = [{"- text": str(examples)}]

    # stories data
    story_name = f"AskQuestion_{intent}"
    story = {"story": story_name, "steps": [{"intent": intent}, {"action": utter}]}
    stories_data["stories"].append(story)
    count += 1







# Save training data to nlu.yml
nlu_file_path = "data/nlu.yml"
with open(nlu_file_path, "a") as file:
    for item in training_data["nlu"]:
        yaml.dump(item, file)
        file.write("\n")

# Update intents in domain.yml
domain_file_path = "domain.yml"
with open(domain_file_path, "r") as domain_file:
    domain_data = yaml.safe_load(domain_file)

# Extract the intents from the training data
intents_from_nlu = [item["intent"] for item in training_data["nlu"]]

# Update the intents in the domain data
domain_data["intents"] = intents_from_nlu

# Save the updated domain.yml file
with open(domain_file_path, "w") as updated_domain_file:
    yaml.dump(domain_data, updated_domain_file)

# Save response data to domain.yml
with open(domain_file_path, "a") as file:
    yaml.dump({"responses": responses_data}, file)

# Save stories data to stories.yml
stories_file_path = "data/stories.yml"
with open(stories_file_path, "a") as file:
    for story in stories_data["stories"]:
        yaml.dump(story, file)
        file.write("\n")
