import unittest
from unittest.mock import patch

from app.tools.resolver import resolve_tool
from app.tools.tools import (
    extract_google_query,
    extract_youtube_query,
    open_facebook,
    open_instagram,
    play_youtube_song,
    search_google,
)


class WebToolResolverTests(unittest.TestCase):
    def test_resolves_new_web_tools(self) -> None:
        cases = {
            "เปิดเพลง Numb Linkin Park": "play_youtube_song",
            "เปิด facebook": "open_facebook",
            "เปิดไอจี": "open_instagram",
            "ค้นหาในกูเกิลเรื่อง AI Agent": "search_google",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(expected, resolve_tool(None, text))


class WebToolTests(unittest.TestCase):
    def test_extracts_queries(self) -> None:
        self.assertEqual("Numb Linkin Park", extract_youtube_query("เปิดเพลง Numb Linkin Park"))
        self.assertEqual("เรื่อง AI Agent", extract_google_query("ค้นหาในกูเกิลเรื่อง AI Agent"))

    @patch("app.tools.tools.webbrowser.open")
    def test_opens_social_sites(self, browser_open) -> None:
        open_facebook()
        browser_open.assert_called_with("https://www.facebook.com")
        open_instagram()
        browser_open.assert_called_with("https://www.instagram.com")

    @patch("app.tools.tools.webbrowser.open")
    def test_google_search_encodes_query(self, browser_open) -> None:
        search_google("ค้นหาในกูเกิล AI Agent")
        browser_open.assert_called_once_with("https://www.google.com/search?q=AI+Agent")

    @patch("app.tools.tools.webbrowser.open")
    @patch("app.tools.tools._find_first_youtube_url")
    def test_song_opens_first_result(self, find_url, browser_open) -> None:
        find_url.return_value = "https://www.youtube.com/watch?v=test"
        result = play_youtube_song("เปิดเพลง Numb Linkin Park")
        find_url.assert_called_once_with("Numb Linkin Park")
        browser_open.assert_called_once_with("https://www.youtube.com/watch?v=test")
        self.assertIn("Numb Linkin Park", result)


if __name__ == "__main__":
    unittest.main()
