
class custom_question:
    def __init__(self, id, type, text):
        self.id = id
        self.type = type
        self.text = text
        
    def __str__(self):
        self.text = self.text.replace("|", "/")
        return(f"{self.id};{self.type};{self.text}|")

def string2custom_questions(string):
    question_strings = string.split("|")
    custom_questions = []

    for question_string in question_strings:
        if question_string == "":
            continue
        id = int(question_string.split(";")[0])
        type = question_string.split(";")[1]
        text = question_string.replace(f"{id};{type};", "")
        custom_questions.append(custom_question(id, type, text))
    return custom_questions

def custom_questions2string(custom_questions):
    string = ""
    for custom_question in custom_questions:
        string = string + str(custom_question)
    return string

# Does generate id for custom question automatically
def add_custom_question_to_array(array, type, text):
    hightest_id = -1
    for e in array:
        if int(e.id) > hightest_id:
            hightest_id = int(e.id)
    hightest_id += 1
    array.append(custom_question(hightest_id, type, text))
    return array

def remove_custom_question_from_array(array, id):
    for e in array:
        if int(e.id) == id:
            array.remove(e)
            return array
    return array

def string2question_answer_pairs(string_custom_answers, string_custom_questions):
    custom_answer_strings = string_custom_answers.split("|")
    custom_answers = []

    for custom_answer in custom_answer_strings:
        if custom_answer == "":
            continue
        id = int(custom_answer.split(";")[0])
        value = custom_answer.replace(f"{id};", "")
        custom_answers.append({"id": id, "value": value})

    custom_questions = string2custom_questions(string_custom_questions)

    custom_question_answer_pairs = []
    for custom_question in custom_questions:
        custom_question_answer_pair = {"value": ""}
        for custom_answer in custom_answers:
            if int(custom_answer["id"]) == int(custom_question.id):
                custom_question_answer_pair = custom_answer
                custom_answers.remove(custom_answer)
                break
        custom_question_answer_pair["id"] = custom_question.id
        custom_question_answer_pair["text"] = custom_question.text
        custom_question_answer_pair["type"] = custom_question.type
        custom_question_answer_pairs.append(custom_question_answer_pair)

    return custom_question_answer_pairs

def post_answer2custom_answers_string(request, string_custom_questions):
    post = request.POST
    custom_questions = string2custom_questions(string_custom_questions)
    custom_answers_string = ""
    for custom_question in custom_questions:
        if f"custom_question_{custom_question.id}" in post.keys():
            value = post[f"custom_question_{custom_question.id}"]
            if custom_question.type == "c":
                # Browser sends only the field, if it was checked. So if we can find it in our post, then this was checked
                value = "1"
            value = value.replace("|", "/")
            custom_answers_string += f"{custom_question.id};{value}|"
    return custom_answers_string
