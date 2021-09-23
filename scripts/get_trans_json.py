from google.cloud import speech_v1p1beta1 as speech
import google_storage
import glob
import os
import uuid
import proto
import json


# https://cloud.google.com/speech-to-text/docs/adaptation


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tsy/Desktop/google/quickstart.json"

# Creates the new bucket
bucket_name = "grid_bucket_1"
project_id = "hale-boulevard-318911"
location = "global"
audio_fpath = "/Users/tsy/Desktop/study/Dissertation/grid_audio/sample/*/*.wav"
output_dir = "/Users/tsy/Desktop/google/shilin/data/adaptation"

with open("phrase_set.json", "r") as z:
    phrases = json.load(z)

with open("verb_colour_prep.json", "r") as f:
    item = json.load(f)

with open("verb.json", "r") as a:
    item1 = json.load(a)

with open("colour.json", "r") as b:
    item2 = json.load(b)

with open("prep.json", "r") as c:
    item3 = json.load(c)

with open("adverb.json", "r") as d:
    item6 = json.load(d)


def run_asr(speech_file):
    # Upload audio to bucket
    google_storage.upload_blob(bucket_name, speech_file, "sample.wav")

    # Create the adaptation client
    adaptation_client = speech.AdaptationClient()

    # The parent resource where the custom class and phrase set will be created.
    parent = f"projects/{project_id}/locations/{location}"

    # Create the custom class resource
    class_vcp = adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": str(uuid.uuid4())[:8],
            "custom_class": {
                "items": item
            },
        }
    )
    vcp=class_vcp.name

    class_verb = adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": str(uuid.uuid4())[:8],
            "custom_class": {
                "items": item1
            },
        }
    )
    verb=class_verb.name

    class_colour = adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": str(uuid.uuid4())[:8],
            "custom_class": {
                "items": item2
            },
        }
    )
    colour=class_colour.name

    class_prep = adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": str(uuid.uuid4())[:8],
            "custom_class": {
                "items": item3
            },
        }
    )
    prep=class_prep.name

    # class_alpha = adaptation_client.create_custom_class(
    #     {
    #         "parent": parent,
    #         "custom_class_id": str(uuid.uuid4())[:8],
    #         "custom_class": {
    #             "items": [{"value": "$OOV_CLASS_ALPHA_SEQUENCE"}]
    #         },
    #     }
    # )
    # alpha=class_alpha.name
    #
    # class_digit = adaptation_client.create_custom_class(
    #     {
    #         "parent": parent,
    #         "custom_class_id": str(uuid.uuid4())[:8],
    #         "custom_class": {
    #             "items": [{"value": "$OOV_CLASS_ALPHA_SEQUENCE"}]
    #         },
    #     }
    # )
    # digit=class_digit.name

    class_adverb = adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": str(uuid.uuid4())[:8],
            "custom_class": {
                "items": item6
            },
        }
    )
    adverb=class_adverb.name

    # Create the phrase set resource
    # phrase_set_id = str(uuid.uuid4())[:8]
    # print(phrase_set_id)


    phrase_set = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": phrases
            }
        }
    )
    phrase = phrase_set.name

    phrase_set0 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": f"${vcp}"}]
            }
        }
    )
    phrase0 = phrase_set0.name

    phrase_set1 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": f"${verb}"}]
            }
        }
    )
    phrase1 = phrase_set1.name

    phrase_set2 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": f"${colour}"}]
            }
        }
    )
    phrase2 = phrase_set2.name

    phrase_set3 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": f"${prep}"}]
            }
        }
    )
    phrase3 = phrase_set3.name

    phrase_set4 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": "$OOV_CLASS_ALPHA_SEQUENCE"}]
            }
        }
    )
    phrase4 = phrase_set4.name

    phrase_set5 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": "$OOV_CLASS_DIGIT_SEQUENCE"}]
            }
        }
    )
    phrase5 = phrase_set5.name

    phrase_set6 = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": str(uuid.uuid4())[:8],
            "phrase_set": {
                "boost": 20,
                "phrases": [{"value": f"${adverb}"}]
            }
        }
    )
    phrase6 = phrase_set6.name

    # Speech adaptation configuration
    speech_adaptation = speech.SpeechAdaptation(
        phrase_set_references=[phrase]
    )

    speech_adaptation1 = speech.SpeechAdaptation(
        phrase_set_references=[phrase0, phrase4, phrase5, phrase6]
    )

    speech_adaptation2 = speech.SpeechAdaptation(
        phrase_set_references=[phrase1, phrase2, phrase3, phrase4, phrase5, phrase6]
    )

    # Speech context
    speech_context0 = speech.SpeechContext(phrases=[f"${vcp}"])
    speech_context1 = speech.SpeechContext(phrases=[f"${verb}"])
    speech_context2 = speech.SpeechContext(phrases=[f"${colour}"])
    speech_context3 = speech.SpeechContext(phrases=[f"${prep}"])
    speech_context4 = speech.SpeechContext(phrases=["$OOV_CLASS_ALPHA_SEQUENCE"])
    speech_context5 = speech.SpeechContext(phrases=["$OOV_CLASS_DIGIT_SEQUENCE"])
    speech_context6 = speech.SpeechContext(phrases=[f"${adverb}"])

    # speech configuration object
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=25000,
        language_code="en-GB",
        adaptation=speech_adaptation,
        # adaptation=speech_adaptation1,
        # adaptation=speech_adaptation2,  # not work well
        # speech_contexts=[speech_context0, speech_context4, speech_context5, speech_context6],
        # speech_contexts=[speech_context1, speech_context2, speech_context3, speech_context4, speech_context5,speech_context6],
        max_alternatives=3,
        enable_word_confidence=True,
        use_enhanced=True,
    )

    # print(config)
    # The name of the audio file to transcribe
    # storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    audio = speech.RecognitionAudio(uri=f"gs://{bucket_name}/sample.wav")

    # Create the speech client
    speech_client = speech.SpeechClient()

    response = speech_client.recognize(config=config, audio=audio)
    # response_message = self.speech_client.recognize(config=self.config, audio=self.audio)

    res = json.loads(proto.Message.to_json(response))

    return res



# Recursively loop through wav files in given paths
for speech_file in glob.iglob(audio_fpath, recursive=True):
    audio_name = speech_file.split("/")[-1][:-4]
    dir_name = f"{output_dir}/{speech_file.split('/')[-2]}"
    os.makedirs(dir_name, exist_ok=True)
    json_fname = f"{dir_name}/{audio_name}.json"
    if os.path.isfile(json_fname):
        print(f"{json_fname} exists, skipping ...")
    else:
        res = run_asr(speech_file)
        print(f"writing to {json_fname}")
        with open(json_fname, "w") as f:
            json.dump(res, f, indent=4)
        # exit()
