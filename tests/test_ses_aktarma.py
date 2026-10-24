import base64
import io
import json
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer

import numpy as np
import soundfile as sf

from ses_tasarim.arayuz import make_handler
from ses_tasarim.oku import find_voice


class ImportHTTPTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.settings = {"sesler": root / "voices", "hazir_sesler": root / "bundled"}
        for path in self.settings.values():
            path.mkdir()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.settings, None))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, payload, headers=None):
        req = urllib.request.Request(self.url + "/api/aktar", json.dumps(payload).encode(),
                                     {"Content-Type": "application/json", **(headers or {})})
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response)

    def recording(self, seconds=9, silent=False):
        audio = np.zeros(16000 * seconds) if silent else .1 * np.sin(np.arange(16000 * seconds) * .1)
        stream = io.BytesIO()
        sf.write(stream, audio, 16000, format="WAV")
        return base64.b64encode(stream.getvalue()).decode()

    def test_import_list_playback_and_no_overwrite(self):
        payload = {"ad": "My voice", "metin": "Merhaba, bu bir deneme.", "kayit": self.recording()}
        code, result = self.request(payload)
        self.assertEqual(code, 201, result)
        self.assertEqual(result["kimlik"], "my_voice/1")
        folder = find_voice(self.settings, result["kimlik"])
        self.assertEqual(sf.info(folder / "referans.wav").duration, 9)
        with urllib.request.urlopen(self.url + "/api/sesler") as r:
            self.assertEqual(json.load(r)["tasarlanan"][0]["kimlik"], result["kimlik"])
        with urllib.request.urlopen(self.url + "/dosya/my_voice/1/referans.wav") as r:
            self.assertTrue(r.read().startswith(b"RIFF"))
        self.assertEqual(self.request(payload)[1]["kimlik"], "my_voice/2")

    def test_invalid_inputs_leave_no_voice(self):
        for recording in ("!bad", base64.b64encode(b"not audio").decode(), self.recording(1), self.recording(silent=True)):
            code, result = self.request({"ad": "Test", "metin": "Merhaba.", "kayit": recording})
            self.assertEqual(code, 400, result)
        self.assertFalse(list(self.settings["sesler"].iterdir()))

    def test_origin_and_field_types(self):
        self.assertEqual(self.request({}, {"Origin": "https://example.com"})[0], 403)
        self.assertEqual(self.request({"ad": [], "metin": 5, "kayit": None})[0], 400)


if __name__ == "__main__":
    unittest.main()
