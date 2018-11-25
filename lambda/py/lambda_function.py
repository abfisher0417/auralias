# -*- coding: utf-8 -*-

# This is an Alexa skill to improve aural skills in early stage musicians
import random
import logging
import json
import six

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response, ui
from ask_sdk_model.slu.entityresolution import StatusCode

from lessons import LESSONS

SKILL_NAME = 'Auralias'
CARD_FOLDER = 'https://s3.amazonaws.com/auralias-alexa-skill/cards/'
MP3_FOLDER = 'https://s3.amazonaws.com/auralias-alexa-skill/mp3s/'

sb = StandardSkillBuilder(table_name="Auralias", auto_create_table=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def calculate_assessment_questions(subject, level):
    major_scale_formula = [0, 2, 2, 1, 2, 2, 2, 1]
    major_interval_names = ['unison', 'major 2nd', 'major 3rd', 'perfect 4th', 'perfect 5th', 'major 6th',
                            'major 7th', 'octave']
    major_interval_cards = [1, 2, 3, 4, 5, 6, 7, 8]
    start_note_midi_key_map = {
        'c_major_asc': 60,
        'd_major_asc': 62,
        'd_major_desc': 74
    }
    scales_notes = {
        'd_major': ['d', 'e', 'f sharp', 'g', 'a', 'b', 'c sharp', 'd']
    }
    scales_numbers = {
        'd_major': ['1', '2', '3', '4', '5', '6', '7', '8']
    }
    choices = []

    # INTERVALS
    if subject == 'intervals':
        for key in level['keys']:
            for asc_desc in level['asc_desc']:
                start_note = start_note_midi_key_map['%s_%s' % (key, 'asc')]
                degree = start_note
                major_interval_midi_notes = []
                for interval in major_scale_formula:
                    degree += interval
                    major_interval_midi_notes.append(degree)
                for interval in level['intervals']:
                    idx = major_interval_names.index(interval)
                    choice = {}
                    choice['note1'] = start_note if asc_desc == 'asc' else major_interval_midi_notes[idx]
                    choice['note2'] = major_interval_midi_notes[idx] if asc_desc == 'asc' else start_note
                    choice['card'] = 'interval_%s_%s_%d' % (key, asc_desc, major_interval_cards[idx])
                    choice['answer'] = interval
                    choices.append(choice)

    # SCALES
    if subject == 'scales':
        for key in level['keys']:
            for asc_desc in level['asc_desc']:
                for number_or_note_name in level['number_or_note_name']:
                    for i in range(len(scales_notes[key])):
                        choice = {}
                        choice['note1'] = "scale_%s_%s_stop_at_%d" % (key, asc_desc, i)
                        choice['card'] = "scale_%s_%s" % (key, asc_desc)
                        if number_or_note_name == 'number':
                            choice['answer'] = scales_numbers[key][i]
                        else:
                            choice['answer'] = scales_notes[key][i]
                        choices.append(choice)

    # CHORDS
    if subject == 'chords':
        for chord in level['chords']:
            choice = {}
            choice['note1'] = "%s_chord" % (chord)
            choice['card'] = "chord_%s" % (chord)
            choice['answer'] = chord.replace("_", " ")
            choices.append(choice)

    random.seed()
    quiz = []
    while len(quiz) < 8:
        rand_sample = random.sample(choices, len(choices))
        quiz.extend(rand_sample)

    return quiz[:8]


def get_assessment_audio_tags(question):
    note1 = question['note1']
    tags = "<audio src=\"{}{}.mp3\" />".format(MP3_FOLDER, note1)
    if 'note2' in question:
        note2 = question['note2']
        tags += " <audio src=\"{}{}.mp3\" />".format(MP3_FOLDER, note2)
    return tags


def get_assessment_standard_card(subject, question):
    image = "{}{}.png".format(CARD_FOLDER, question['card'])
    card = ui.StandardCard(
        title=subject,
        text=" ",
        image=ui.Image(
            small_image_url=image,
            large_image_url=image
        )
    )
    return card


def get_lesson_card(slide):
    card = None
    card_image = slide['card_image']
    title = slide['title']
    content = slide['voice']
    if card_image == "":
        card = ui.SimpleCard(title=title, content=content)
    elif 'https' not in card_image:
        card = ui.SimpleCard(title=title, content=card_image)
    else:
        card = ui.StandardCard(title=title, text=" ", image=ui.Image(
            small_image_url=card_image, large_image_url=card_image))
    return card


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch.

    Get the persistence attributes, to figure out the state.
    """
    # type: (HandlerInput) -> Response
    attr = handler_input.attributes_manager.persistent_attributes
    if not attr:
        attr['last_visited_module'] = 'NA'  # To track what module one is working on
        attr['intervals_lesson_or_assessment_flag'] = 'lesson'  # To track if one is on the lesson or assessment
        attr['intervals_lesson_or_assessment_idx'] = -1  # To track the index into the lesson or level of assessment
        attr['intervals_assessment_question_counter'] = -1  # To track the number of questions asked by assessment level
        attr['intervals_assessment_correct_score_counter'] = -1  # To track the number of right questions by level
        attr['scales_lesson_or_assessment_flag'] = 'lesson'  # To track if one is on the lesson or assessment
        attr['scales_lesson_or_assessment_idx'] = -1  # To track the index into the lesson or level of assessment
        attr['scales_assessment_question_counter'] = -1  # To track the number of questions asked by assessment level
        attr['scales_assessment_correct_score_counter'] = -1  # To track the number of right questions by level
        attr['chords_lesson_or_assessment_flag'] = 'lesson'  # To track if one is on the lesson or assessment
        attr['chords_lesson_or_assessment_idx'] = -1  # To track the index into the lesson or level of assessment
        attr['chords_assessment_question_counter'] = -1  # To track the number of questions asked by assessment level
        attr['chords_assessment_correct_score_counter'] = -1  # To track the number of right questions by level

    handler_input.attributes_manager.session_attributes = attr

    speech_text = ("Welcome to Auralias Music. I will guide you through ear training exercises "
                   "to help you develop a good musical ear. For best results, practice a little "
                   "bit every day. What would you like to do? Say intervals, scales, or chords.")
    reprompt = "Say intervals, scales, or chords."

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
is_intent_name("ModuleIntent")(input))
def module_handler(handler_input):
    """Handler for processing integrated tutorial component."""
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    subject = str(handler_input.request_envelope.request.intent.slots["subject"].value)
    logger.info("Subject: {}".format(subject))

    if subject == "scales":
        speech_text = "You said scales. Is that right?"
        reprompt = "You said scales. Is that right?"
    elif subject == "chords":
        speech_text = "You said chords. Is that right?"
        reprompt = "You said chords. Is that right?"
    elif subject == "intervals":
        speech_text = "You said intervals. Is that right?"
        reprompt = "You said intervals. Is that right?"

    session_attr['last_visited_module'] = subject

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
is_intent_name("AMAZON.YesIntent")(input))
def yes_handler(handler_input):
    """Handler for Yes Intent, only if the player said yes.
    """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    subject = session_attr['last_visited_module']
    lesson_or_assessment_flag = session_attr['%s_lesson_or_assessment_flag' % subject]
    lesson_or_assessment_idx = session_attr['%s_lesson_or_assessment_idx' % subject]
    assessment_question_counter = session_attr['%s_assessment_question_counter' % subject]
    assessment_correct_score_counter = session_attr['%s_assessment_correct_score_counter' % subject]

    logger.info("Subject: {}\n" \
                "Flag: {}\n" \
                "Index: {}\n" \
                "Question Counter: {}\n" \
                "Correct Questions: {}" \
                .format(subject, lesson_or_assessment_flag, lesson_or_assessment_idx, assessment_question_counter,
                        assessment_correct_score_counter))

    if (lesson_or_assessment_flag == 'lesson' and lesson_or_assessment_idx < len(
            LESSONS['modules'][subject][lesson_or_assessment_flag]) - 1):
        logger.info("Increasing lesson index")
        lesson_or_assessment_idx += 1
    elif (lesson_or_assessment_flag == 'lesson'
          and lesson_or_assessment_idx == len(LESSONS['modules'][subject][lesson_or_assessment_flag]) - 1):
        logger.info("Moving onto the assessment")
        lesson_or_assessment_flag = 'assessment'
        lesson_or_assessment_idx = 0
        assessment_question_counter = 0
        assessment_correct_score_counter = 0
    elif (lesson_or_assessment_flag == 'assessment'
          and lesson_or_assessment_idx < len(LESSONS['modules'][subject][lesson_or_assessment_flag]['levels']) - 1):
        logger.info("Resuming the assessment")
        # If the user previously got through 8 questions with more than 80% correct, advance to next level
        if (assessment_question_counter == 8
                and float(assessment_correct_score_counter) / assessment_question_counter > 0.8):
            logger.info("Increasing assessment index. Score was {} of {}.".format(assessment_correct_score_counter,
                                                                              assessment_question_counter))
            lesson_or_assessment_idx += 1
        # Otherwise, keep on current level from beginning
        assessment_question_counter = 0
        assessment_correct_score_counter = 0
    else:
        logger.info("Resetting module since it is finished")
        lesson_or_assessment_flag = 'lesson'
        lesson_or_assessment_idx = 0
        assessment_question_counter = 0
        assessment_correct_score_counter = 0

    if lesson_or_assessment_flag == 'lesson':
        speech_text = LESSONS['modules'][subject][lesson_or_assessment_flag][lesson_or_assessment_idx]['voice'] \
                      + " " \
                      + LESSONS['modules'][subject][lesson_or_assessment_flag][lesson_or_assessment_idx]['prompt']
        reprompt = LESSONS['modules'][subject][lesson_or_assessment_flag][lesson_or_assessment_idx]['prompt']
        handler_input.response_builder.set_card(get_lesson_card(LESSONS['modules'][subject][lesson_or_assessment_flag][lesson_or_assessment_idx]))
    elif lesson_or_assessment_flag == 'assessment':
        # Calculate 8-question quiz for the current assessment level and persist in session
        session_attr['quiz'] = calculate_assessment_questions(subject,
                                                              LESSONS['modules'][subject][lesson_or_assessment_flag][
                                                                  'levels'][lesson_or_assessment_idx])
        # Explain assessment instructions
        # Ask first question. Response will be handled by assessment intents.
        instructions = LESSONS['modules'][subject][lesson_or_assessment_flag]['instructions']
        reprompt = LESSONS['modules'][subject][lesson_or_assessment_flag]['prompt']
        if 'instructions' in LESSONS['modules'][subject][lesson_or_assessment_flag]['levels'][lesson_or_assessment_idx]:
            instructions = LESSONS['modules'][subject][lesson_or_assessment_flag]['levels'][lesson_or_assessment_idx]['instructions']
            reprompt = LESSONS['modules'][subject][lesson_or_assessment_flag]['levels'][lesson_or_assessment_idx]['prompt']
        speech_text = instructions \
                      + " " \
                      + get_assessment_audio_tags(session_attr['quiz'][assessment_question_counter])
        reprompt = reprompt
        handler_input.response_builder.set_card(
            get_assessment_standard_card(LESSONS['modules'][subject][lesson_or_assessment_flag]['title'],
                                         session_attr['quiz'][assessment_question_counter]))

    session_attr['%s_lesson_or_assessment_idx' % subject] = lesson_or_assessment_idx
    session_attr['%s_lesson_or_assessment_flag' % subject] = lesson_or_assessment_flag
    session_attr['%s_assessment_question_counter' % subject] = assessment_question_counter
    session_attr['%s_assessment_correct_score_counter' % subject] = assessment_correct_score_counter

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
is_intent_name("AMAZON.NoIntent")(input))
def no_handler(handler_input):
    """Handler for No Intent, only if the player said no.
    """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes

    handler_input.attributes_manager.persistent_attributes = session_attr
    handler_input.attributes_manager.save_persistent_attributes()

    speech_text = "Ok. See you next time!!"

    handler_input.response_builder.speak(speech_text)
    return handler_input.response_builder.response


def currently_assessing(handler_input):
    """Function that acts as can handle for the assessment."""
    # type: (HandlerInput) -> str
    is_currently_assessing = ''
    session_attr = handler_input.attributes_manager.session_attributes
    if 'last_visited_module' in session_attr:
        subject = session_attr['last_visited_module']
        flag_name = '%s_lesson_or_assessment_flag' % subject
        if flag_name in session_attr and session_attr[flag_name] == 'assessment':
            is_currently_assessing = subject
    logger.info("Is Currently Assessing: {}".format(is_currently_assessing))
    return is_currently_assessing


@sb.request_handler(can_handle_func=lambda input:
(currently_assessing(input) != '') and
is_intent_name("QuizIntent")(input))
def quiz_handler(handler_input):
    """Handler for QuizIntent
    """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    subject = session_attr['last_visited_module']
    lesson_or_assessment_flag = session_attr['%s_lesson_or_assessment_flag' % subject]
    lesson_or_assessment_idx = session_attr['%s_lesson_or_assessment_idx' % subject]
    assessment_question_counter = session_attr['%s_assessment_question_counter' % subject]
    assessment_correct_score_counter = session_attr['%s_assessment_correct_score_counter' % subject]
    quiz = session_attr['quiz']
    answer = quiz[assessment_question_counter]['answer']
    user_answer = str(handler_input.request_envelope.request.intent.slots["interval"].value)

    # Parse slot values to obtain user answer
    slot_value_map = {}
    current_intent = handler_input.request_envelope.request.intent
    for slot_name, current_slot in six.iteritems(current_intent.slots):
        if current_slot.resolutions and current_slot.resolutions.resolutions_per_authority[0]:
            resolutions = current_slot.resolutions.resolutions_per_authority[0]
            if resolutions.status.code == StatusCode.ER_SUCCESS_MATCH:
                values = []
                for val in resolutions.values:
                    values.append(val.value.name)
                slot_value_map[slot_name] = values
        elif not current_slot.resolutions and current_slot.value:
            values = [current_slot.value]
            slot_value_map[slot_name] = values

    logger.info("Subject: {}\n" \
                "Flag: {}\n" \
                "Index: {}\n" \
                "Question Counter: {}\n" \
                "Correct Questions: {}" \
                "Answer: {}" \
                "Slot Value Map: {}" \
                .format(subject, lesson_or_assessment_flag, lesson_or_assessment_idx, assessment_question_counter,
                        assessment_correct_score_counter, answer, slot_value_map))

    correct_answer = False
    if subject == 'intervals':
        if 'interval' in slot_value_map and answer in slot_value_map['interval']:
            correct_answer = True
    elif subject == 'chords':
        if 'chord' in slot_value_map and answer in slot_value_map['chord']:
            correct_answer = True
    elif subject == 'scales':
        if 'note' in slot_value_map and answer in slot_value_map['note']:
            correct_answer = True
        elif 'number' in slot_value_map and answer in slot_value_map['number']:
            correct_answer = True

    assessment_question_counter += 1
    if correct_answer:
        speech_text = (
            "Yeah. {} is the correct answer.".format(answer))
        assessment_correct_score_counter += 1
    else:
        speech_text = (
            "That was incorrect. {} is the correct answer.".format(answer))

    session_attr['%s_assessment_question_counter' % subject] = assessment_question_counter
    session_attr['%s_assessment_correct_score_counter' % subject] = assessment_correct_score_counter

    if assessment_question_counter < 8:
        speech_text += " " \
                       + "Let's try another one. " \
                       + get_assessment_audio_tags(session_attr['quiz'][assessment_question_counter])
        reprompt = LESSONS['modules'][subject][lesson_or_assessment_flag]['prompt']
        if 'instructions' in LESSONS['modules'][subject][lesson_or_assessment_flag]['levels'][lesson_or_assessment_idx]:
            reprompt = LESSONS['modules'][subject][lesson_or_assessment_flag]['levels'][lesson_or_assessment_idx]['prompt']
        handler_input.response_builder.set_card(
            get_assessment_standard_card(LESSONS['modules'][subject][lesson_or_assessment_flag]['title'],
                                         session_attr['quiz'][assessment_question_counter]))
        handler_input.response_builder.speak(speech_text).ask(reprompt)
    else:
        speech_text += " " \
                       + "You answered {} of {} questions correctly. ".format(assessment_correct_score_counter, assessment_question_counter) \
                       + "Let's take a break for now. Good bye."
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()
        handler_input.response_builder.speak(
            speech_text).set_should_end_session(True)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = ("During the introductory section for each module, I will tell you a bit about intervals, scales, or chords. Say yes to move on or no to stop.")
    if currently_assessing(handler_input) == 'intervals':
        speech_text = ("Name the interval. For example, say unison, perfect fifth, or octave.")
    elif currently_assessing(handler_input) == 'scales':
        speech_text = ("Identify the note I stopped on.")
    elif currently_assessing(handler_input) == 'chords':
        speech_text = ("Identify the chord I played by name. For example, c major")

    handler_input.response_builder.speak(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda input:
    is_intent_name("AMAZON.CancelIntent")(input) or
    is_intent_name("AMAZON.StopIntent")(input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Ok. See you next time!!"

    handler_input.response_builder.speak(
        speech_text).set_should_end_session(True)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    logger.info(
        "Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input: True)
def unhandled_intent_handler(handler_input):
    """Handler for all other unhandled requests."""
    # type: (HandlerInput) -> Response
    speech = "I don't know what to do. Please say again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)
    speech = "Sorry, I can't understand that. Please say again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Response logger."""
    # type: (HandlerInput, Response) -> None
    logger.info("Response: {}".format(response))


lambda_handler = sb.lambda_handler()
