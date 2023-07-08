def txt_to_mp3(_txt):
    _mp3 = speech_ms(_txt)
    if _mp3:
        return _mp3
    else:
        return None


def speech_ms(_txt):
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _mp3_path = _pwd.parent.parent.parent
    from module.util import timestamp_now
    _ts = timestamp_now()
    # print(f"_ts: {_ts}")
    import os
    _mp3 = os.path.join(_mp3_path, "tmp", "mp3", f"{_ts}.mp3")
    # print(f"_mp3: {_mp3}")
    if ms_txt2mp3(_txt, _mp3):
        return _mp3
    else:
        return None


def ms_txt2mp3(_txt, _mp3):
    _ssml_str = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
    <voice name="zh-CN-YunxiNeural">
        <mstts:express-as style="cheerful" styledegree="1">
            {}
        </mstts:express-as>
    </voice>
</speak>
'''.format(_txt)
    import azure.cognitiveservices.speech as speechsdk
    import os
    speech_key = os.getenv('MS_SPEECH_KEY')
    service_region = os.getenv('MS_SERVICE_REGION')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = 'zh-CN'
    speech_config.speech_synthesis_voice_name='zh-CN-YunzeNeural'
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(_ssml_str).get()
    from module.logger import logger
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        logger.info(f"'{_txt}' synthesized to {_mp3}")
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file(_mp3)
        return 1
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                logger.error(f"Error details: {cancellation_details.error_details}")
        logger.debug(f"Did you update the subscription info?")
        return 0


if __name__ == "__main__":
    speech_ms("你好，世界！")

